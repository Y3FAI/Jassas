"""
Jassas Web Performance Benchmark - Live Server
Tests against running server at localhost:8000
"""
import time
import statistics
import urllib.request
import urllib.parse

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

BASE_URL = "http://localhost:8000"

TEST_QUERIES = [
    "خدمات",
    "تسجيل",
    "الهوية الوطنية",
    "رخصة قيادة",
    "جواز سفر",
]


def benchmark_endpoint(name: str, url: str, runs: int = 5):
    """Benchmark a single endpoint."""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                resp.read()
            times.append((time.perf_counter() - start) * 1000)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return None
    return times


def main():
    console.print("\n[bold cyan]Jassas Live Server Benchmark[/bold cyan]")
    console.print(f"Target: {BASE_URL}\n")

    # Test health endpoint first
    try:
        with urllib.request.urlopen(f"{BASE_URL}/health", timeout=5) as resp:
            resp.read()
        console.print("[green]Server is up[/green]\n")
    except:
        console.print("[red]Server not responding. Run: ./jassas serve[/red]")
        return

    results = []

    # Benchmark home page
    times = benchmark_endpoint("Home /", f"{BASE_URL}/")
    if times:
        results.append(("Home /", times))

    # Benchmark each search query
    for query in TEST_QUERIES:
        encoded = urllib.parse.quote(query)
        url = f"{BASE_URL}/search?q={encoded}"
        times = benchmark_endpoint(f"Search: {query}", url)
        if times:
            results.append((f"Search: {query}", times))

    # Benchmark API endpoint
    for query in TEST_QUERIES[:2]:
        encoded = urllib.parse.quote(query)
        url = f"{BASE_URL}/api/v1/search?q={encoded}"
        times = benchmark_endpoint(f"API: {query}", url)
        if times:
            results.append((f"API: {query}", times))

    # Print results
    table = Table(title="Response Times (ms)", box=box.ROUNDED)
    table.add_column("Endpoint", style="cyan")
    table.add_column("Min", justify="right")
    table.add_column("Avg", justify="right")
    table.add_column("Max", justify="right")

    for name, times in results:
        avg = statistics.mean(times)
        color = "red" if avg > 1000 else "yellow" if avg > 200 else "green"
        table.add_row(
            name,
            f"{min(times):.0f}",
            f"[{color}]{avg:.0f}[/{color}]",
            f"{max(times):.0f}",
        )

    console.print(table)

    # Summary
    all_search_times = [t for name, times in results if "Search" in name for t in times]
    if all_search_times:
        avg = statistics.mean(all_search_times)
        console.print(f"\n[bold]Average search: {avg:.0f}ms[/bold]")
        if avg > 1000:
            console.print("[red]SLOW - Target is <50ms[/red]")
        elif avg > 200:
            console.print("[yellow]OK but can improve[/yellow]")
        else:
            console.print("[green]Good performance[/green]")


if __name__ == "__main__":
    main()
