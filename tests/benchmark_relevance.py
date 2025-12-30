"""
Jassas Relevance Benchmark - LLM-as-a-Judge
Uses OpenRouter free model to evaluate search quality.
"""
import os
import sys
import json
import math
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
MODEL = "mistralai/devstral-2512:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Test queries - 90% Arabic, 10% English
QUERIES = [
    # Arabic queries (18 = 90%)
    "تجديد جواز السفر",
    "رخصة القيادة",
    "المخالفات المرورية",
    "الأمن السيبراني",
    "وزارة الصحة",
    "تجديد الهوية الوطنية",
    "العنوان الوطني",
    "التأشيرات",
    "الضمان الاجتماعي",
    "حساب المواطن",
    "التأمينات الاجتماعية",
    "نظام نور",
    "أبشر",
    "توكلنا",
    "الزكاة والضريبة",
    "السجل التجاري",
    "التوظيف الحكومي",
    "الخدمات الإلكترونية",
    # English queries (2 = 10%)
    "government services",
    "visa application",
]


def format_results_for_llm(results: List[dict]) -> str:
    """Format search results for LLM evaluation."""
    formatted = []
    for i, r in enumerate(results[:10], 1):
        title = r.get('title', 'No Title')[:100]
        snippet = r.get('clean_text', '')[:200]
        formatted.append(f"{i}. Title: {title}\n   Snippet: {snippet}")
    return "\n\n".join(formatted)


def call_llm_judge(query: str, results: List[dict]) -> List[int]:
    """
    Send results to LLM for relevance scoring.
    Returns list of scores 0-3 for each result.
    """
    if not OPENROUTER_API_KEY:
        console.print("[red]Error: OPENROUTER_API_KEY not set[/red]")
        return [0] * len(results)

    prompt = f"""You are a Search Relevance Evaluator for Saudi government services.

Query: "{query}"

Rate each document's relevance to the query on a scale of 0-3:
- 0: Irrelevant (wrong topic entirely)
- 1: Tangentially related (mentions topic but not useful)
- 2: Relevant (answers the query partially)
- 3: Perfect (exact match, official service page)

Documents:
{format_results_for_llm(results)}

Return ONLY a JSON array of {min(len(results), 10)} integers (scores), nothing else.
Example: [3, 2, 1, 0, 2, 1, 0, 0, 1, 2]"""

    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 100,
            },
            timeout=30
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Parse JSON array from response
        # Handle markdown code blocks if present
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        scores = json.loads(content)
        return scores[:10]
    except Exception as e:
        console.print(f"[red]LLM error: {e}[/red]")
        return [0] * min(len(results), 10)


def calculate_mrr(scores: List[int]) -> float:
    """
    Mean Reciprocal Rank - position of first relevant result.
    Relevant = score >= 2
    """
    for i, score in enumerate(scores):
        if score >= 2:
            return 1.0 / (i + 1)
    return 0.0


def calculate_ndcg(scores: List[int], k: int = 10) -> float:
    """
    Normalized Discounted Cumulative Gain.
    Measures ranking quality - are best results at the top?
    """
    scores = scores[:k]
    if not scores or max(scores) == 0:
        return 0.0

    # DCG
    dcg = scores[0]
    for i in range(1, len(scores)):
        dcg += scores[i] / math.log2(i + 2)

    # Ideal DCG (perfect ranking)
    ideal = sorted(scores, reverse=True)
    idcg = ideal[0]
    for i in range(1, len(ideal)):
        idcg += ideal[i] / math.log2(i + 2)

    if idcg == 0:
        return 0.0
    return dcg / idcg


def calculate_precision_at_k(scores: List[int], k: int = 10) -> float:
    """Precision@K - fraction of top-k results that are relevant."""
    scores = scores[:k]
    if not scores:
        return 0.0
    relevant = sum(1 for s in scores if s >= 2)
    return relevant / len(scores)


def run_relevance_benchmark():
    console.print("\n[bold cyan]⚖️  Jassas Relevance Benchmark (LLM-as-a-Judge)[/bold cyan]\n")

    if not OPENROUTER_API_KEY:
        console.print("[red]❌ Set OPENROUTER_API_KEY environment variable[/red]")
        console.print("[dim]export OPENROUTER_API_KEY='your-key-here'[/dim]")
        return

    console.print(f"[dim]Model: {MODEL}[/dim]")
    console.print(f"[dim]Queries: {len(QUERIES)}[/dim]\n")

    # Load ranker
    console.print("[yellow]Loading search engine...[/yellow]")
    ranker = Ranker(verbose=False)
    ranker._load_vector_engine()
    console.print("[green]✓ Engine ready[/green]\n")

    # Results table
    table = Table(title="Relevance Scores by Query", box=box.ROUNDED)
    table.add_column("Query", style="cyan", max_width=30)
    table.add_column("MRR", justify="right")
    table.add_column("NDCG@10", justify="right")
    table.add_column("P@10", justify="right")
    table.add_column("Avg Score", justify="right")
    table.add_column("Scores", style="dim", max_width=30)

    all_mrr = []
    all_ndcg = []
    all_precision = []
    all_avg_scores = []

    for query in QUERIES:
        console.print(f"[dim]Evaluating: {query[:40]}...[/dim]")

        # Search
        results = ranker.search(query, k=10)

        if not results:
            table.add_row(query[:30], "-", "-", "-", "-", "No results")
            continue

        # Get LLM scores
        scores = call_llm_judge(query, results)

        # Calculate metrics
        mrr = calculate_mrr(scores)
        ndcg = calculate_ndcg(scores)
        precision = calculate_precision_at_k(scores)
        avg_score = sum(scores) / len(scores) if scores else 0

        all_mrr.append(mrr)
        all_ndcg.append(ndcg)
        all_precision.append(precision)
        all_avg_scores.append(avg_score)

        # Color code scores
        score_str = str(scores)

        table.add_row(
            query[:30],
            f"{mrr:.2f}",
            f"{ndcg:.2f}",
            f"{precision:.0%}",
            f"{avg_score:.1f}/3",
            score_str[:30]
        )

    console.print(table)

    # Summary
    if all_mrr:
        console.print("\n[bold yellow]Summary Metrics:[/bold yellow]")

        summary = Table(box=box.SIMPLE)
        summary.add_column("Metric", style="cyan")
        summary.add_column("Score", justify="right", style="bold green")
        summary.add_column("Interpretation", style="dim")

        avg_mrr = sum(all_mrr) / len(all_mrr)
        avg_ndcg = sum(all_ndcg) / len(all_ndcg)
        avg_precision = sum(all_precision) / len(all_precision)
        avg_score = sum(all_avg_scores) / len(all_avg_scores)

        summary.add_row("Mean MRR", f"{avg_mrr:.3f}", "1.0 = first result always relevant")
        summary.add_row("Mean NDCG@10", f"{avg_ndcg:.3f}", "1.0 = perfect ranking")
        summary.add_row("Mean P@10", f"{avg_precision:.1%}", "% of top 10 that are relevant")
        summary.add_row("Avg Relevance", f"{avg_score:.2f}/3", "0=bad, 3=perfect")

        console.print(summary)

        # Overall grade
        overall = (avg_mrr + avg_ndcg + avg_precision) / 3 * 100

        if overall >= 80:
            grade = "[bold green]A - Excellent[/bold green]"
        elif overall >= 60:
            grade = "[bold yellow]B - Good[/bold yellow]"
        elif overall >= 40:
            grade = "[bold orange]C - Needs Work[/bold orange]"
        else:
            grade = "[bold red]D - Poor[/bold red]"

        console.print(f"\n[bold]Overall Quality Score: {overall:.0f}% - {grade}[/bold]")


if __name__ == "__main__":
    run_relevance_benchmark()
