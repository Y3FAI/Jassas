"""
Jassas QA Benchmark - Task Completion Metric
Measures: Can the user's question be answered using search results?

Unlike P@10/NDCG which assume many relevant docs, this measures
whether the search helps users complete their task.
"""
import os
import sys
import json
import requests
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich import box

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from ranker.engine import Ranker

console = Console()

# OpenRouter config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Dual judges
JUDGES = [
    "mistralai/devstral-2512:free",
    "qwen/qwen3-235b-a22b:free",
]

# Test questions - specific queries matching actual DB content
QUESTIONS = [
    "اصدار رخصه بناء",
    "دفع ضريبه قيمه مضافه",
    "حجز مواعيد طبيه",
    "تجديد اقامه",
    "اصدار تاشيرات عمل",
    "حجز اسم تجاري",
    "تسجيل تصرف عقاري",
    "اصدار هويه وطنيه",
    "اصدار تاشيره خروج والعوده",
    "اصدار رخصه سير",
    "تجديد رخص عمل",
    "اصدار شهاده اشتراك",
    "تسجيل في جامعات",
    "اصدار رخصه حرفيه",
    "طلب ابتعاث خارجي",
]


def format_results(results: List[dict], k: int) -> str:
    """Format top-k results for judge."""
    formatted = []
    for i, r in enumerate(results[:k], 1):
        title = r.get('title', 'No Title')[:100]
        snippet = r.get('clean_text', '')[:300]
        formatted.append(f"[{i}] {title}\n{snippet}")
    return "\n\n".join(formatted)


def judge_answerable(model: str, question: str, results: List[dict], k: int) -> bool:
    """
    Ask judge: Can this question be answered using top-k results?
    Returns True/False
    """
    if not results:
        return False

    prompt = f"""You are evaluating a search engine for Saudi government services.

User Question: "{question}"

Search Results (Top {k}):
{format_results(results, k)}

Do the search results help the user find what they're looking for?
- YES if: Results contain the relevant service page or direct link to answer
- YES if: User would click on a result and find their answer
- NO if: Results are completely unrelated to the question
- NO if: No result points to the right service/information

This is a SERVICE DIRECTORY - results point to services, not full answers.

Reply with ONLY: YES or NO"""

    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 10,
            },
            timeout=60
        )
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"].strip().upper()
        return "YES" in answer
    except Exception as e:
        return None


def evaluate_question(question: str, results: List[dict]) -> Dict[str, bool]:
    """
    Evaluate if question is answerable at different K values.
    Uses multiple judges and takes majority vote.
    """
    k_values = [1, 3, 5, 10]
    scores = {}

    for k in k_values:
        votes = []
        for model in JUDGES:
            result = judge_answerable(model, question, results, k)
            if result is not None:
                votes.append(result)

        # Majority vote (or True if tie with at least one True)
        if votes:
            scores[f"top_{k}"] = sum(votes) >= len(votes) / 2
        else:
            scores[f"top_{k}"] = False

    return scores


def run_qa_benchmark():
    console.print("\n[bold cyan]📋 Jassas QA Benchmark (Task Completion)[/bold cyan]\n")

    if not OPENROUTER_API_KEY:
        console.print("[red]❌ Set OPENROUTER_API_KEY environment variable[/red]")
        return

    console.print(f"[dim]Judges: {', '.join(j.split('/')[1].split(':')[0] for j in JUDGES)}[/dim]")
    console.print(f"[dim]Questions: {len(QUESTIONS)}[/dim]")
    console.print("[dim]Metric: Can user answer their question with Top-K results?[/dim]\n")

    # Load ranker
    console.print("[yellow]Loading search engine...[/yellow]")
    ranker = Ranker(verbose=False)
    ranker._load_vector_engine()
    console.print("[green]✓ Engine ready[/green]\n")

    # Results table
    table = Table(title="Question Answerability", box=box.ROUNDED)
    table.add_column("Question", style="cyan", max_width=35)
    table.add_column("Top 1", justify="center")
    table.add_column("Top 3", justify="center")
    table.add_column("Top 5", justify="center")
    table.add_column("Top 10", justify="center")

    # Aggregate scores
    totals = {"top_1": 0, "top_3": 0, "top_5": 0, "top_10": 0}

    for question in QUESTIONS:
        console.print(f"[dim]Evaluating: {question[:40]}...[/dim]")

        # Search
        results = ranker.search(question, k=10)

        # Evaluate at each K
        scores = evaluate_question(question, results)

        # Update totals
        for key in totals:
            if scores.get(key, False):
                totals[key] += 1

        # Format row
        def fmt(k):
            return "[green]✓[/green]" if scores.get(k, False) else "[red]✗[/red]"

        table.add_row(
            question[:35],
            fmt("top_1"),
            fmt("top_3"),
            fmt("top_5"),
            fmt("top_10")
        )

    console.print(table)

    # Summary
    n = len(QUESTIONS)
    console.print("\n[bold yellow]Success Rate (% of questions answerable):[/bold yellow]")

    summary = Table(box=box.SIMPLE)
    summary.add_column("Metric", style="cyan")
    summary.add_column("Score", justify="right", style="bold")
    summary.add_column("Interpretation", style="dim")

    s1 = totals["top_1"] / n * 100
    s3 = totals["top_3"] / n * 100
    s5 = totals["top_5"] / n * 100
    s10 = totals["top_10"] / n * 100

    summary.add_row("Success@1", f"{s1:.0f}%", "Answer in first result")
    summary.add_row("Success@3", f"{s3:.0f}%", "Answer in top 3")
    summary.add_row("Success@5", f"{s5:.0f}%", "Answer in top 5")
    summary.add_row("Success@10", f"{s10:.0f}%", "Answer in top 10")

    console.print(summary)

    # Overall grade
    avg_success = (s1 + s3 + s5 + s10) / 4

    if avg_success >= 70:
        grade = "[bold green]A - Excellent[/bold green]"
    elif avg_success >= 50:
        grade = "[bold yellow]B - Good[/bold yellow]"
    elif avg_success >= 30:
        grade = "[bold orange3]C - Needs Work[/bold orange3]"
    else:
        grade = "[bold red]D - Poor[/bold red]"

    console.print(f"\n[bold]Overall Score: {avg_success:.0f}% - {grade}[/bold]")

    # Insight
    console.print("\n[dim]Insight: Success@1 is the 'I'm feeling lucky' metric.[/dim]")
    console.print("[dim]Success@10 shows if the answer exists in your corpus at all.[/dim]")


if __name__ == "__main__":
    run_qa_benchmark()
