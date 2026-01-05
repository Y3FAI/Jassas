"""
Fair Embedding Model Comparison: jassas-embedding vs E5-large

Tests both models on:
1. Accuracy - Can it find the correct document?
2. Trap Resistance - Does it fall for lexically similar but wrong docs?
3. Latency - How fast is inference?

Usage:
    python tests/benchmark_embeddings.py
"""
import os
import sys
import time
import json
import random
import numpy as np
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

console = Console()

# ============================================================================
# TEST DATA - Tricky Arabic Government Scenarios
# ============================================================================

# These are designed to test semantic understanding, not just keyword matching
TEST_SCENARIOS = [
    {
        "topic": "جواز السفر",
        "query": "كم غرامة تأخير تجديد الجواز؟",
        "correct": "غرامة تأخير تجديد جواز السفر تبلغ 500 ريال عن كل سنة تأخير",
        "trap": "رسوم إصدار جواز السفر الجديد 300 ريال سعودي",  # Fee vs Fine trap
        "fillers": [
            "يمكن تجديد الجواز عبر منصة أبشر الإلكترونية",
            "الجواز السعودي يتيح الدخول لأكثر من 70 دولة بدون تأشيرة",
        ]
    },
    {
        "topic": "رخصة القيادة",
        "query": "ما هو السن القانوني للحصول على رخصة القيادة؟",
        "correct": "السن القانوني للحصول على رخصة قيادة خاصة هو 18 سنة",
        "trap": "يجب أن يكون عمر السائق 21 سنة للمركبات الثقيلة",  # Different license type
        "fillers": [
            "يمكن تجديد رخصة القيادة إلكترونياً عبر أبشر",
            "رسوم استخراج رخصة القيادة 40 ريال لمدة 5 سنوات",
        ]
    },
    {
        "topic": "تأشيرة الخروج والعودة",
        "query": "كم مدة صلاحية تأشيرة الخروج والعودة؟",
        "correct": "تأشيرة الخروج والعودة صالحة لمدة 6 أشهر من تاريخ الإصدار",
        "trap": "تأشيرة الخروج والعودة للمقيمين في دول الخليج صالحة لمدة سنة",
        "fillers": [
            "يمكن إصدار تأشيرة الخروج والعودة عبر منصة أبشر",
            "رسوم تأشيرة الخروج والعودة المفردة 200 ريال",
        ]
    },
    {
        "topic": "نقل الكفالة",
        "query": "هل يشترط موافقة الكفيل لنقل الكفالة؟",
        "correct": "نعم، يشترط موافقة الكفيل الحالي إلكترونياً لإتمام نقل الكفالة",
        "trap": "لا يشترط موافقة الكفيل في حال انتهاء عقد العمل",  # Exception case
        "fillers": [
            "يمكن تقديم طلب نقل الكفالة عبر منصة قوى",
            "رسوم نقل الكفالة 2000 ريال للمرة الأولى",
        ]
    },
    {
        "topic": "الإقامة",
        "query": "ما هي غرامة تأخير تجديد الإقامة؟",
        "correct": "غرامة تأخير تجديد الإقامة 500 ريال عن كل فترة تأخير",
        "trap": "رسوم تجديد الإقامة 650 ريال سنوياً",  # Fee vs Fine
        "fillers": [
            "يجب تجديد الإقامة قبل انتهائها بثلاثة أيام على الأقل",
            "يمكن تجديد الإقامة عبر منصة أبشر أو مقيم",
        ]
    },
    {
        "topic": "التأمين الصحي",
        "query": "هل التأمين الصحي إلزامي للمقيمين؟",
        "correct": "نعم، التأمين الصحي إلزامي لجميع المقيمين وأسرهم في المملكة",
        "trap": "التأمين الصحي اختياري للزيارات القصيرة أقل من شهر",
        "fillers": [
            "يمكن الاستعلام عن التأمين الصحي عبر موقع مجلس الضمان",
            "أسعار التأمين الصحي تختلف حسب الفئة العمرية",
        ]
    },
    {
        "topic": "المرور",
        "query": "كم غرامة قطع الإشارة الحمراء؟",
        "correct": "غرامة قطع الإشارة الحمراء 3000 ريال مع تصوير المخالفة",
        "trap": "غرامة تجاوز السرعة 300 ريال للمخالفة الأولى",  # Different violation
        "fillers": [
            "يمكن الاستعلام عن المخالفات المرورية عبر أبشر",
            "يتم خصم نقاط من رخصة القيادة عند ارتكاب المخالفات",
        ]
    },
    {
        "topic": "الزكاة والضريبة",
        "query": "ما هي نسبة ضريبة القيمة المضافة؟",
        "correct": "نسبة ضريبة القيمة المضافة في المملكة 15% على معظم السلع والخدمات",
        "trap": "نسبة الزكاة على الشركات 2.5% من الوعاء الزكوي",  # Different tax
        "fillers": [
            "يمكن تقديم الإقرار الضريبي عبر موقع هيئة الزكاة والضريبة",
            "بعض السلع الأساسية معفاة من ضريبة القيمة المضافة",
        ]
    },
    {
        "topic": "العمل",
        "query": "كم عدد ساعات العمل القانونية في الأسبوع؟",
        "correct": "عدد ساعات العمل القانونية 48 ساعة أسبوعياً أو 8 ساعات يومياً",
        "trap": "في شهر رمضان تكون ساعات العمل 6 ساعات يومياً للمسلمين",
        "fillers": [
            "يحق للعامل إجازة سنوية لا تقل عن 21 يوماً",
            "يجب دفع أجر إضافي عن ساعات العمل الإضافية",
        ]
    },
    {
        "topic": "السجل التجاري",
        "query": "كم رسوم إصدار السجل التجاري؟",
        "correct": "رسوم إصدار السجل التجاري الرئيسي 200 ريال سنوياً",
        "trap": "رسوم تجديد السجل التجاري الفرعي 100 ريال سنوياً",  # Main vs Branch
        "fillers": [
            "يمكن إصدار السجل التجاري عبر موقع وزارة التجارة",
            "يتطلب إصدار السجل التجاري وجود عنوان وطني",
        ]
    },
]


def create_test_cases(n_cases: int = 50) -> list:
    """Generate test cases from scenarios."""
    test_cases = []

    for i in range(n_cases):
        scenario = TEST_SCENARIOS[i % len(TEST_SCENARIOS)]

        # Build document set
        all_docs = [
            scenario["correct"],
            scenario["trap"],
        ] + scenario["fillers"]

        # Shuffle to avoid position bias
        random.shuffle(all_docs)

        test_cases.append({
            "id": i + 1,
            "topic": scenario["topic"],
            "query": scenario["query"],
            "docs": all_docs,
            "correct": scenario["correct"],
            "trap": scenario["trap"],
        })

    return test_cases


# ============================================================================
# MODEL LOADERS
# ============================================================================

class JassasEmbedding:
    """Load jassas-embedding (ONNX INT8)."""

    def __init__(self, model_path: str = "y3fai/jassas-embedding"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None

    def load(self):
        """Load model."""
        os.environ["OMP_NUM_THREADS"] = "1"

        from transformers import AutoTokenizer
        from optimum.onnxruntime import ORTModelForFeatureExtraction

        console.print(f"[cyan]Loading jassas-embedding from {self.model_path}...[/cyan]")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            clean_up_tokenization_spaces=True,
        )

        self.model = ORTModelForFeatureExtraction.from_pretrained(
            self.model_path,
            file_name="model_quantized.onnx"
        )

        console.print("[green]✓ jassas-embedding loaded[/green]")

    def encode(self, texts: list) -> np.ndarray:
        """Encode texts to embeddings."""
        # Tokenize
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        # Inference
        outputs = self.model(**inputs)

        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)

        # Normalize
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)

        return embeddings.detach().numpy()


class E5Embedding:
    """Load E5-large via FastEmbed."""

    def __init__(self):
        self.model = None

    def load(self):
        """Load model."""
        from fastembed import TextEmbedding

        console.print("[cyan]Loading intfloat/multilingual-e5-large...[/cyan]")
        self.model = TextEmbedding("intfloat/multilingual-e5-large")
        console.print("[green]✓ E5-large loaded[/green]")

    def encode(self, texts: list, is_query: bool = False) -> np.ndarray:
        """Encode texts with proper E5 prefixes."""
        # E5 requires prefixes
        if is_query:
            prefixed = [f"query: {t}" for t in texts]
        else:
            prefixed = [f"passage: {t}" for t in texts]

        embeddings = list(self.model.embed(prefixed))
        return np.array(embeddings)


# ============================================================================
# BENCHMARK
# ============================================================================

def benchmark_model(model, test_cases: list, model_name: str, use_prefixes: bool = False) -> dict:
    """Run benchmark on a model."""

    results = {
        "model": model_name,
        "total": len(test_cases),
        "correct": 0,
        "trap_selected": 0,
        "latencies": [],
    }

    console.print(f"\n[bold cyan]Testing {model_name}...[/bold cyan]")

    for case in test_cases:
        query = case["query"]
        docs = case["docs"]
        correct_doc = case["correct"]
        trap_doc = case["trap"]

        # Time the search
        start = time.perf_counter()

        if use_prefixes:
            # E5 style with prefixes
            q_vec = model.encode([query], is_query=True)
            d_vecs = model.encode(docs, is_query=False)
        else:
            # jassas-embedding style (no prefixes)
            q_vec = model.encode([query])
            d_vecs = model.encode(docs)

        # Cosine similarity (vectors are normalized)
        scores = np.dot(q_vec, d_vecs.T).flatten()
        best_idx = np.argmax(scores)
        selected_doc = docs[best_idx]

        latency = (time.perf_counter() - start) * 1000
        results["latencies"].append(latency)

        # Check results
        if selected_doc == correct_doc:
            results["correct"] += 1
        elif selected_doc == trap_doc:
            results["trap_selected"] += 1

    # Calculate stats
    results["accuracy"] = results["correct"] / results["total"] * 100
    results["trap_rate"] = results["trap_selected"] / results["total"] * 100
    results["avg_latency"] = np.mean(results["latencies"])
    results["p95_latency"] = np.percentile(results["latencies"], 95)

    return results


def run_benchmark():
    """Run full benchmark comparison."""

    console.print("\n" + "=" * 60)
    console.print("[bold yellow]EMBEDDING MODEL COMPARISON BENCHMARK[/bold yellow]")
    console.print("=" * 60)

    # Generate test cases
    console.print("\n[cyan]Generating test cases...[/cyan]")
    test_cases = create_test_cases(n_cases=50)
    console.print(f"[green]✓ Created {len(test_cases)} test cases[/green]")

    # Preview a test case
    console.print("\n[dim]Example test case:[/dim]")
    example = test_cases[0]
    console.print(f"  Query: {example['query']}")
    console.print(f"  Correct: {example['correct'][:50]}...")
    console.print(f"  Trap: {example['trap'][:50]}...")

    all_results = []

    # Test jassas-embedding
    try:
        jassas = JassasEmbedding()
        jassas.load()

        # Warmup
        jassas.encode(["warmup"])

        results = benchmark_model(jassas, test_cases, "jassas-embedding", use_prefixes=False)
        all_results.append(results)

    except Exception as e:
        console.print(f"[red]Error loading jassas-embedding: {e}[/red]")
        console.print("[yellow]Skipping jassas-embedding benchmark[/yellow]")

    # Test E5-large
    try:
        e5 = E5Embedding()
        e5.load()

        # Warmup
        e5.encode(["warmup"], is_query=True)

        results = benchmark_model(e5, test_cases, "E5-large", use_prefixes=True)
        all_results.append(results)

    except Exception as e:
        console.print(f"[red]Error loading E5-large: {e}[/red]")
        console.print("[yellow]Skipping E5-large benchmark[/yellow]")

    # Display results
    if all_results:
        display_results(all_results)

    return all_results


def display_results(all_results: list):
    """Display benchmark results in a nice table."""

    console.print("\n" + "=" * 60)
    console.print("[bold green]RESULTS[/bold green]")
    console.print("=" * 60)

    # Main comparison table
    table = Table(title="Model Comparison", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")

    for r in all_results:
        table.add_column(r["model"], style="white")

    # Accuracy row
    row = ["Accuracy"]
    for r in all_results:
        acc = r["accuracy"]
        style = "green" if acc >= 80 else "yellow" if acc >= 60 else "red"
        row.append(f"[{style}]{acc:.1f}%[/{style}]")
    table.add_row(*row)

    # Trap rate row
    row = ["Trap Rate (lower=better)"]
    for r in all_results:
        trap = r["trap_rate"]
        style = "green" if trap <= 10 else "yellow" if trap <= 20 else "red"
        row.append(f"[{style}]{trap:.1f}%[/{style}]")
    table.add_row(*row)

    # Latency rows
    row = ["Avg Latency"]
    for r in all_results:
        lat = r["avg_latency"]
        style = "green" if lat <= 50 else "yellow" if lat <= 100 else "red"
        row.append(f"[{style}]{lat:.1f}ms[/{style}]")
    table.add_row(*row)

    row = ["P95 Latency"]
    for r in all_results:
        lat = r["p95_latency"]
        row.append(f"{lat:.1f}ms")
    table.add_row(*row)

    console.print(table)

    # Winner announcement
    if len(all_results) >= 2:
        console.print("\n[bold]Analysis:[/bold]")

        # Compare accuracy
        best_acc = max(all_results, key=lambda x: x["accuracy"])
        worst_acc = min(all_results, key=lambda x: x["accuracy"])
        acc_diff = best_acc["accuracy"] - worst_acc["accuracy"]

        if acc_diff > 5:
            console.print(f"  • [green]{best_acc['model']}[/green] is more accurate by {acc_diff:.1f}%")
        else:
            console.print(f"  • Accuracy is similar (within {acc_diff:.1f}%)")

        # Compare latency
        fastest = min(all_results, key=lambda x: x["avg_latency"])
        slowest = max(all_results, key=lambda x: x["avg_latency"])
        speed_ratio = slowest["avg_latency"] / fastest["avg_latency"]

        console.print(f"  • [green]{fastest['model']}[/green] is {speed_ratio:.1f}x faster")

        # Compare trap resistance
        best_trap = min(all_results, key=lambda x: x["trap_rate"])
        if best_trap["trap_rate"] < 15:
            console.print(f"  • [green]{best_trap['model']}[/green] is better at avoiding traps")


if __name__ == "__main__":
    run_benchmark()
