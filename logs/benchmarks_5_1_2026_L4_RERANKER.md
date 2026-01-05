Requirement already satisfied: jinja2 in ./venv/lib/python3.12/site-packages (from torch>=1.11.0->sentence-transformers>=3.0.0) (3.1.6)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./venv/lib/python3.12/site-packages (from sympy>=1.13.3->torch>=1.11.0->sentence-transformers>=3.0.0) (1.3.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./venv/lib/python3.12/site-packages (from jinja2->torch>=1.11.0->sentence-transformers>=3.0.0) (3.0.3)
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib/python3.12/site-packages (from requests->transformers<6.0.0,>=4.41.0->sentence-transformers>=3.0.0) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.12/site-packages (from requests->transformers<6.0.0,>=4.41.0->sentence-transformers>=3.0.0) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.12/site-packages (from requests->transformers<6.0.0,>=4.41.0->sentence-transformers>=3.0.0) (2.6.2)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.12/site-packages (from requests->transformers<6.0.0,>=4.41.0->sentence-transformers>=3.0.0) (2026.1.4)
Requirement already satisfied: joblib>=1.3.0 in ./venv/lib/python3.12/site-packages (from scikit-learn->sentence-transformers>=3.0.0) (1.5.3)
Collecting threadpoolctl>=3.2.0 (from scikit-learn->sentence-transformers>=3.0.0)
Using cached threadpoolctl-3.6.0-py3-none-any.whl.metadata (13 kB)
Using cached sentence_transformers-5.2.0-py3-none-any.whl (493 kB)
Using cached transformers-4.57.3-py3-none-any.whl (12.0 MB)
Using cached huggingface_hub-0.36.0-py3-none-any.whl (566 kB)
Using cached safetensors-0.7.0-cp38-abi3-macosx_11_0_arm64.whl (447 kB)
Using cached torch-2.9.1-cp312-none-macosx_11_0_arm64.whl (74.5 MB)
Using cached networkx-3.6.1-py3-none-any.whl (2.1 MB)
Using cached scikit_learn-1.8.0-cp312-cp312-macosx_12_0_arm64.whl (8.1 MB)
Using cached threadpoolctl-3.6.0-py3-none-any.whl (18 kB)
Using cached setuptools-80.9.0-py3-none-any.whl (1.2 MB)
Installing collected packages: threadpoolctl, setuptools, safetensors, networkx, torch, scikit-learn, huggingface-hub, transformers, sentence-transformers
Attempting uninstall: huggingface-hub
Found existing installation: huggingface_hub 1.2.3
Uninstalling huggingface_hub-1.2.3:
Successfully uninstalled huggingface_hub-1.2.3
Successfully installed huggingface-hub-0.36.0 networkx-3.6.1 safetensors-0.7.0 scikit-learn-1.8.0 sentence-transformers-5.2.0 setuptools-80.9.0 threadpoolctl-3.6.0 torch-2.9.1 transformers-4.57.3
yousef@Yousefs-MacBook-Air jassas % clear

yousef@Yousefs-MacBook-Air jassas % ./jassas --help

Usage: jassas.py [OPTIONS] COMMAND [ARGS]...

Jassas Search Engine - Manager CLI

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help Show this message and exit. │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ init Initialize the database. │
│ seed Add a seed URL to the frontier with high priority. │
│ stats Show database statistics. │
│ frontier Show pending URLs in the frontier. │
│ crawl Run the crawler (optionally parse sitemap first). │
│ clean Run the cleaner to process raw pages. │
│ build Build search indexes from scratch (resets tokenization, rebuilds BM25 + vectors). │
│ search Search using hybrid RRF (NumPy BM25 + Vector Embeddings). │
│ benchmark Run benchmarks: accuracy (requires OPENROUTER_API_KEY) or latency. │
│ serve Start the web server. │
│ deduplicate Remove duplicate URLs from database (www vs non-www, http vs https). │
│ reset Reset the database (delete all data). │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

yousef@Yousefs-MacBook-Air jassas % ./jassas search "اصدار جواز سفر"

Searching: اصدار جواز سفر

Loading vector model...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector*model = TextEmbedding(VectorEngine.MODEL_NAME)
Loading vector index...
[Vector] load=1767.0ms, encode=12.7ms, search=19.6ms
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either: - Avoid using `tokenizers` before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
config.json: 100%|███████████████████████████████████████████████████████████████████████████████| 765/765 [00:00<00:00, 1.62MB/s]
╭────────────────────────────────────────────── Traceback (most recent call last) ───────────────────────────────────────────────╮
│ /Users/yousef/dev/jassas/src/manager/cli.py:317 in search │
│ │
│ 314 │ # Initialize ranker and search │
│ 315 │ from ranker import Ranker │
│ 316 │ ranker = Ranker(verbose=True) │
│ ❱ 317 │ results = ranker.search(query, k=limit) │
│ 318 │ │
│ 319 │ if not results: │
│ 320 │ │ console.print("[yellow]No results found.[/yellow]") │
│ │
│ ╭───────────────────────────── locals ──────────────────────────────╮ │
│ │ bm25_index_path = '/Users/yousef/dev/jassas/data/bm25_matrix.pkl' │ │
│ │ doc_count = 9785 │ │
│ │ limit = 10 │ │
│ │ os = <module 'os' (frozen)> │ │
│ │ query = 'اصدار جواز سفر' │ │
│ │ Ranker = <class 'ranker.engine.Ranker'> │ │
│ │ ranker = <ranker.engine.Ranker object at 0x1051d1790> │ │
│ ╰───────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/src/ranker/engine.py:142 in search │
│ │
│ 139 │ │ │
│ 140 │ │ # 5. Cross-encoder rerank │
│ 141 │ │ start = time.perf_counter() │
│ ❱ 142 │ │ results = self.reranker.rerank(query, candidates, top_k=k) │
│ 143 │ │ timings['rerank'] = (time.perf_counter() - start) * 1000 │
│ 144 │ │ │
│ 145 │ │ if debug or self.verbose: │
│ │
│ ╭────────────────────────────────────────────────────────── locals ──────────────────────────────────────────────────────────╮ │
│ │ bm25_results = [2853, 469, 2852, 3628, 4383, 2890, 2908, 4085, 325, 327, ... +40] │ │
│ │ candidates = [ │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 2853, │ │
│ │ │ │ 'score': 0.01639344262295082, │ │
│ │ │ │ 'title': 'اصدار جواز سفر سعودي | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/112093', │ │
│ │ │ │ 'clean_text': 'اصدار جواز سفر سعودي | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي │ │
│ │ تاب'+3420 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 269, │ │
│ │ │ │ 'score': 0.01639344262295082, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/agencies', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم │ │
│ │ ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 469, │ │
│ │ │ │ 'score': 0.016129032258064516, │ │
│ │ │ │ 'title': 'اصدار جواز بدل مفقود | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/343104', │ │
│ │ │ │ 'clean_text': 'اصدار جواز بدل مفقود | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي │ │
│ │ تاب'+3212 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 271, │ │
│ │ │ │ 'score': 0.016129032258064516, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/services', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم │ │
│ │ ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 2852, │ │
│ │ │ │ 'score': 0.015873015873015872, │ │
│ │ │ │ 'title': 'تجديد جواز سفر سعودي | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/112090', │ │
│ │ │ │ 'clean_text': 'تجديد جواز سفر سعودي | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي │ │
│ │ تاب'+3375 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 272, │ │
│ │ │ │ 'score': 0.015873015873015872, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/emergency-contact', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم │ │
│ │ ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 3628, │ │
│ │ │ │ 'score': 0.015625, │ │
│ │ │ │ 'title': 'جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/319232', │ │
│ │ │ │ 'clean_text': 'جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه جاري تحميل، يرجي انتظار... موقع │ │
│ │ حكوم'+3098 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 226, │ │
│ │ │ │ 'score': 0.015625, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/contact', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم │ │
│ │ ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 4383, │ │
│ │ │ │ 'score': 0.015384615384615385, │ │
│ │ │ │ 'title': 'تحـــــديث معلومـــــات جواز سفر | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/532976', │ │
│ │ │ │ 'clean_text': 'تحـــــديث معلومـــــات جواز سفر | منصه وطنيه جاري تحميل، يرجي انتظار... موقع │ │
│ │ حك'+3193 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 462, │ │
│ │ │ │ 'score': 0.015384615384615385, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/artities-performance-index', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم │ │
│ │ ت'+148 │ │
│ │ │ } │ │
│ │ ] │ │
│ │ debug = False │ │
│ │ doc_id = 6657 │ │
│ │ executor = <concurrent.futures.thread.ThreadPoolExecutor object at 0x11b7426f0> │ │
│ │ future_bm25 = <Future at 0x149e1c9b0 state=finished returned list> │ │
│ │ future_vector = <Future at 0x149e6b7d0 state=finished returned list> │ │
│ │ k = 10 │ │
│ │ merged_scores = { │ │
│ │ │ 2853: 0.01639344262295082, │ │
│ │ │ 469: 0.016129032258064516, │ │
│ │ │ 2852: 0.015873015873015872, │ │
│ │ │ 3628: 0.015625, │ │
│ │ │ 4383: 0.015384615384615385, │ │
│ │ │ 2890: 0.015151515151515152, │ │
│ │ │ 2908: 0.014925373134328358, │ │
│ │ │ 4085: 0.014705882352941176, │ │
│ │ │ 325: 0.014492753623188406, │ │
│ │ │ 327: 0.014285714285714285, │ │
│ │ │ ... +90 │ │
│ │ } │ │
│ │ normalized_query = 'اصدار جواز سفر' │ │
│ │ query = 'اصدار جواز سفر' │ │
│ │ rank = 49 │ │
│ │ rerank_pool = 10 │ │
│ │ self = <ranker.engine.Ranker object at 0x1051d1790> │ │
│ │ start = 381602.092960041 │ │
│ │ time = <module 'time' (built-in)> │ │
│ │ timings = { │ │
│ │ │ 'normalize': 0.3530000103637576, │ │
│ │ │ 'search_parallel': 1799.8295000288635, │ │
│ │ │ 'sort': 0.006999995093792677, │ │
│ │ │ 'fetch': 5.927458987571299 │ │
│ │ } │ │
│ │ top_doc_ids = [2853, 269, 469, 271, 2852, 272, 3628, 226, 4383, 462] │ │
│ │ vector_results = [269, 271, 272, 226, 462, 227, 5470, 4126, 3122, 3109, ... +40] │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/src/ranker/reranker.py:36 in rerank │
│ │
│ 33 │ │ if not candidates: │
│ 34 │ │ │ return [] │
│ 35 │ │ │
│ ❱ 36 │ │ self.\_load_model() │
│ 37 │ │ │
│ 38 │ │ # Build (query, title) pairs │
│ 39 │ │ pairs = [(query, doc['title']) for doc in candidates] │
│ │
│ ╭────────────────────────────────────────────────────────── locals ──────────────────────────────────────────────────────────╮ │
│ │ candidates = [ │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 2853, │ │
│ │ │ │ 'score': 0.01639344262295082, │ │
│ │ │ │ 'title': 'اصدار جواز سفر سعودي | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/112093', │ │
│ │ │ │ 'clean_text': 'اصدار جواز سفر سعودي | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي تاب'+3420 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 269, │ │
│ │ │ │ 'score': 0.01639344262295082, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/agencies', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 469, │ │
│ │ │ │ 'score': 0.016129032258064516, │ │
│ │ │ │ 'title': 'اصدار جواز بدل مفقود | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/343104', │ │
│ │ │ │ 'clean_text': 'اصدار جواز بدل مفقود | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي تاب'+3212 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 271, │ │
│ │ │ │ 'score': 0.016129032258064516, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/services', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 2852, │ │
│ │ │ │ 'score': 0.015873015873015872, │ │
│ │ │ │ 'title': 'تجديد جواز سفر سعودي | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/112090', │ │
│ │ │ │ 'clean_text': 'تجديد جواز سفر سعودي | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكومي رسمي تاب'+3375 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 272, │ │
│ │ │ │ 'score': 0.015873015873015872, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/emergency-contact', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 3628, │ │
│ │ │ │ 'score': 0.015625, │ │
│ │ │ │ 'title': 'جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/319232', │ │
│ │ │ │ 'clean_text': 'جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حكوم'+3098 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 226, │ │
│ │ │ │ 'score': 0.015625, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://www.my.gov.sa/ar/ar/contact', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم ت'+148 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 4383, │ │
│ │ │ │ 'score': 0.015384615384615385, │ │
│ │ │ │ 'title': 'تحـــــديث معلومـــــات جواز سفر | منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/services/532976', │ │
│ │ │ │ 'clean_text': 'تحـــــديث معلومـــــات جواز سفر | منصه وطنيه جاري تحميل، يرجي انتظار... موقع حك'+3193 │ │
│ │ │ }, │ │
│ │ │ { │ │
│ │ │ │ 'doc_id': 462, │ │
│ │ │ │ 'score': 0.015384615384615385, │ │
│ │ │ │ 'title': 'منصه وطنيه', │ │
│ │ │ │ 'url': 'https://my.gov.sa/ar/artities-performance-index', │ │
│ │ │ │ 'clean_text': 'منصه وطنيه en لم يتم عثور علي صفحه نظرا لاطلاق منصه وطنيه بحلتها جديده، فقد تم ت'+148 │ │
│ │ │ } │ │
│ │ ] │ │
│ │ query = 'اصدار جواز سفر' │ │
│ │ self = <ranker.reranker.Reranker object at 0x1076d6e40> │ │
│ │ top_k = 10 │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/src/ranker/reranker.py:19 in \_load_model │
│ │
│ 16 │ def \_load_model(self): │
│ 17 │ │ """Lazy load the cross-encoder.""" │
│ 18 │ │ if self.model is None: │
│ ❱ 19 │ │ │ self.model = CrossEncoder(self.MODEL_NAME) │
│ 20 │ │
│ 21 │ def rerank(self, query: str, candidates: List[dict], top_k: int = 10) -> List[dict]: │
│ 22 │ │ """ │
│ │
│ ╭──────────────────────── locals ─────────────────────────╮ │
│ │ self = <ranker.reranker.Reranker object at 0x1076d6e40> │ │
│ ╰─────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/sentence_transformers/cross_encoder/util.py:39 in wrapper │
│ │
│ 36 │ │ │ else: │
│ 37 │ │ │ │ kwargs["config_kwargs"]["classifier_dropout"] = classifier_dropout │
│ 38 │ │ │
│ ❱ 39 │ │ return func(self, *args, **kwargs) │
│ 40 │ │
│ 41 │ return wrapper │
│ 42 │
│ │
│ ╭────────────────────────────────── locals ───────────────────────────────────╮ │
│ │ args = ('y3fai/jassas-minilm-l4-int8',) │ │
│ │ func = <function CrossEncoder.**init** at 0x149c87560> │ │
│ │ kwargs = {} │ │
│ │ kwargs_renamed_mapping = { │ │
│ │ │ 'model_name': 'model_name_or_path', │ │
│ │ │ 'automodel_args': 'model_kwargs', │ │
│ │ │ 'tokenizer_args': 'tokenizer_kwargs', │ │
│ │ │ 'config_args': 'config_kwargs', │ │
│ │ │ 'cache_dir': 'cache_folder', │ │
│ │ │ 'default_activation_function': 'activation_fn' │ │
│ │ } │ │
│ │ new_name = 'activation_fn' │ │
│ │ old_name = 'default_activation_function' │ │
│ │ self = CrossEncoder() │ │
│ ╰─────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/sentence_transformers/cross_encoder/CrossEncoder.py:182 in **init** │
│ │
│ 179 │ │ │
│ 180 │ │ if num_labels is not None: │
│ 181 │ │ │ config.num_labels = num_labels │
│ ❱ 182 │ │ self.\_load_model( │
│ 183 │ │ │ model_name_or_path, │
│ 184 │ │ │ config=config, │
│ 185 │ │ │ backend=backend, │
│ │
│ ╭────────────────────────────────────────────── locals ──────────────────────────────────────────────╮ │
│ │ activation_fn = None │ │
│ │ backend = 'torch' │ │
│ │ cache_folder = None │ │
│ │ classifier_trained = True │ │
│ │ config = BertConfig { │ │
│ │ "architectures": [ │ │
│ │ │ "BertForSequenceClassification" │ │
│ │ ], │ │
│ │ "attention_probs_dropout_prob": 0.1, │ │
│ │ "classifier_dropout": null, │ │
│ │ "gradient_checkpointing": false, │ │
│ │ "hidden_act": "gelu", │ │
│ │ "hidden_dropout_prob": 0.1, │ │
│ │ "hidden_size": 384, │ │
│ │ "id2label": { │ │
│ │ │ "0": "LABEL_0" │ │
│ │ }, │ │
│ │ "initializer_range": 0.02, │ │
│ │ "intermediate_size": 1536, │ │
│ │ "label2id": { │ │
│ │ │ "LABEL_0": 0 │ │
│ │ }, │ │
│ │ "layer_norm_eps": 1e-12, │ │
│ │ "max_position_embeddings": 512, │ │
│ │ "model_type": "bert", │ │
│ │ "num_attention_heads": 12, │ │
│ │ "num_hidden_layers": 4, │ │
│ │ "pad_token_id": 0, │ │
│ │ "position_embedding_type": "absolute", │ │
│ │ "sbert_ce_default_activation_function": "torch.nn.modules.linear.Identity", │ │
│ │ "transformers_version": "4.57.3", │ │
│ │ "type_vocab_size": 2, │ │
│ │ "use_cache": true, │ │
│ │ "vocab_size": 30522 │ │
│ │ } │ │
│ │ config_kwargs = {} │ │
│ │ device = None │ │
│ │ local_files_only = False │ │
│ │ max_length = None │ │
│ │ model_card_data = None │ │
│ │ model_kwargs = {} │ │
│ │ model_name_or_path = 'y3fai/jassas-minilm-l4-int8' │ │
│ │ num_labels = None │ │
│ │ revision = None │ │
│ │ self = CrossEncoder() │ │
│ │ token = None │ │
│ │ tokenizer_kwargs = {} │ │
│ │ trust_remote_code = False │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/sentence_transformers/cross_encoder/CrossEncoder.py:243 in │
│ \_load_model │
│ │
│ 240 │ │ **model_kwargs, │
│ 241 │ ) -> None: │
│ 242 │ │ if backend == "torch": │
│ ❱ 243 │ │ │ self.model: PreTrainedModel = AutoModelForSequenceClassification.from_pretra │
│ 244 │ │ │ │ model_name_or_path, │
│ 245 │ │ │ │ config=config, │
│ 246 │ │ │ │ **model_kwargs, │
│ │
│ ╭────────────────────────────────────────────── locals ──────────────────────────────────────────────╮ │
│ │ backend = 'torch' │ │
│ │ config = BertConfig { │ │
│ │ "architectures": [ │ │
│ │ │ "BertForSequenceClassification" │ │
│ │ ], │ │
│ │ "attention_probs_dropout_prob": 0.1, │ │
│ │ "classifier_dropout": null, │ │
│ │ "gradient_checkpointing": false, │ │
│ │ "hidden_act": "gelu", │ │
│ │ "hidden_dropout_prob": 0.1, │ │
│ │ "hidden_size": 384, │ │
│ │ "id2label": { │ │
│ │ │ "0": "LABEL_0" │ │
│ │ }, │ │
│ │ "initializer_range": 0.02, │ │
│ │ "intermediate_size": 1536, │ │
│ │ "label2id": { │ │
│ │ │ "LABEL_0": 0 │ │
│ │ }, │ │
│ │ "layer_norm_eps": 1e-12, │ │
│ │ "max_position_embeddings": 512, │ │
│ │ "model_type": "bert", │ │
│ │ "num_attention_heads": 12, │ │
│ │ "num_hidden_layers": 4, │ │
│ │ "pad_token_id": 0, │ │
│ │ "position_embedding_type": "absolute", │ │
│ │ "sbert_ce_default_activation_function": "torch.nn.modules.linear.Identity", │ │
│ │ "transformers_version": "4.57.3", │ │
│ │ "type_vocab_size": 2, │ │
│ │ "use_cache": true, │ │
│ │ "vocab_size": 30522 │ │
│ │ } │ │
│ │ model_kwargs = { │ │
│ │ │ 'cache_dir': None, │ │
│ │ │ 'trust_remote_code': False, │ │
│ │ │ 'revision': None, │ │
│ │ │ 'local_files_only': False, │ │
│ │ │ 'token': None │ │
│ │ } │ │
│ │ model_name_or_path = 'y3fai/jassas-minilm-l4-int8' │ │
│ │ self = CrossEncoder() │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/transformers/models/auto/auto_factory.py:604 in from_pretrained │
│ │
│ 601 │ │ │ model_class = \_get_model_class(config, cls.\_model_mapping) │
│ 602 │ │ │ if model_class.config_class == config.sub_configs.get("text_config", None): │
│ 603 │ │ │ │ config = config.get_text_config() │
│ ❱ 604 │ │ │ return model_class.from_pretrained( │
│ 605 │ │ │ │ pretrained_model_name_or_path, \*model_args, config=config, **hub_kwargs, │
│ 606 │ │ │ ) │
│ 607 │ │ raise ValueError( │
│ │
│ ╭────────────────────────────────────────────────────── locals ───────────────────────────────────────────────────────╮ │
│ │ adapter_kwargs = None │ │
│ │ cls = <class 'transformers.models.auto.modeling_auto.AutoModelForSequenceClassification'> │ │
│ │ code_revision = None │ │
│ │ commit_hash = 'e7203729af5c6dbc5689b633cad2068c04b33e2c' │ │
│ │ config = BertConfig { │ │
│ │ "architectures": [ │ │
│ │ │ "BertForSequenceClassification" │ │
│ │ ], │ │
│ │ "attention_probs_dropout_prob": 0.1, │ │
│ │ "classifier_dropout": null, │ │
│ │ "gradient_checkpointing": false, │ │
│ │ "hidden_act": "gelu", │ │
│ │ "hidden_dropout_prob": 0.1, │ │
│ │ "hidden_size": 384, │ │
│ │ "id2label": { │ │
│ │ │ "0": "LABEL_0" │ │
│ │ }, │ │
│ │ "initializer_range": 0.02, │ │
│ │ "intermediate_size": 1536, │ │
│ │ "label2id": { │ │
│ │ │ "LABEL_0": 0 │ │
│ │ }, │ │
│ │ "layer_norm_eps": 1e-12, │ │
│ │ "max_position_embeddings": 512, │ │
│ │ "model_type": "bert", │ │
│ │ "num_attention_heads": 12, │ │
│ │ "num_hidden_layers": 4, │ │
│ │ "pad_token_id": 0, │ │
│ │ "position_embedding_type": "absolute", │ │
│ │ "sbert_ce_default_activation_function": "torch.nn.modules.linear.Identity", │ │
│ │ "transformers_version": "4.57.3", │ │
│ │ "type_vocab_size": 2, │ │
│ │ "use_cache": true, │ │
│ │ "vocab_size": 30522 │ │
│ │ } │ │
│ │ has_local_code = True │ │
│ │ has_remote_code = False │ │
│ │ hub_kwargs = {'cache_dir': None, 'local_files_only': False, 'revision': None} │ │
│ │ hub_kwargs_names = [ │ │
│ │ │ 'cache_dir', │ │
│ │ │ 'force_download', │ │
│ │ │ 'local_files_only', │ │
│ │ │ 'proxies', │ │
│ │ │ 'resume_download', │ │
│ │ │ 'revision', │ │
│ │ │ 'subfolder', │ │
│ │ │ 'use_auth_token', │ │
│ │ │ 'token' │ │
│ │ ] │ │
│ │ kwargs = {'trust_remote_code': False, '\_from_auto': True, 'adapter_kwargs': None} │ │
│ │ model_args = () │ │
│ │ model_class = <class 'transformers.models.bert.modeling_bert.BertForSequenceClassification'> │ │
│ │ pretrained_model_name_or_path = 'y3fai/jassas-minilm-l4-int8' │ │
│ │ token = None │ │
│ │ trust_remote_code = False │ │
│ │ upstream_repo = None │ │
│ │ use_auth_token = None │ │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/transformers/modeling_utils.py:277 in \_wrapper │
│ │
│ 274 │ def \_wrapper(*args, \*\*kwargs): │
│ 275 │ │ old_dtype = torch.get_default_dtype() │
│ 276 │ │ try: │
│ ❱ 277 │ │ │ return func(*args, \*\*kwargs) │
│ 278 │ │ finally: │
│ 279 │ │ │ torch.set_default_dtype(old_dtype) │
│ 280 │
│ │
│ ╭──────────────────────────────────────────── locals ─────────────────────────────────────────────╮ │
│ │ args = ( │ │
│ │ │ <class 'transformers.models.bert.modeling_bert.BertForSequenceClassification'>, │ │
│ │ │ 'y3fai/jassas-minilm-l4-int8' │ │
│ │ ) │ │
│ │ func = <function PreTrainedModel.from_pretrained at 0x1499f2020> │ │
│ │ kwargs = { │ │
│ │ │ 'config': BertConfig { │ │
│ │ "architectures": [ │ │
│ │ │ "BertForSequenceClassification" │ │
│ │ ], │ │
│ │ "attention_probs_dropout_prob": 0.1, │ │
│ │ "classifier_dropout": null, │ │
│ │ "gradient_checkpointing": false, │ │
│ │ "hidden_act": "gelu", │ │
│ │ "hidden_dropout_prob": 0.1, │ │
│ │ "hidden_size": 384, │ │
│ │ "id2label": { │ │
│ │ │ "0": "LABEL_0" │ │
│ │ }, │ │
│ │ "initializer_range": 0.02, │ │
│ │ "intermediate_size": 1536, │ │
│ │ "label2id": { │ │
│ │ │ "LABEL_0": 0 │ │
│ │ }, │ │
│ │ "layer_norm_eps": 1e-12, │ │
│ │ "max_position_embeddings": 512, │ │
│ │ "model_type": "bert", │ │
│ │ "num_attention_heads": 12, │ │
│ │ "num_hidden_layers": 4, │ │
│ │ "pad_token_id": 0, │ │
│ │ "position_embedding_type": "absolute", │ │
│ │ "sbert_ce_default_activation_function": "torch.nn.modules.linear.Identity", │ │
│ │ "transformers_version": "4.57.3", │ │
│ │ "type_vocab_size": 2, │ │
│ │ "use_cache": true, │ │
│ │ "vocab_size": 30522 │ │
│ │ } │ │
│ │ , │ │
│ │ │ 'cache_dir': None, │ │
│ │ │ 'local_files_only': False, │ │
│ │ │ 'revision': None, │ │
│ │ │ 'trust_remote_code': False, │ │
│ │ │ '\_from_auto': True, │ │
│ │ │ 'adapter_kwargs': None │ │
│ │ } │ │
│ │ old_dtype = torch.float32 │ │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/transformers/modeling_utils.py:4900 in from_pretrained │
│ │
│ 4897 │ │ │ │ "loaded from GGUF files." │
│ 4898 │ │ │ ) │
│ 4899 │ │ │
│ ❱ 4900 │ │ checkpoint_files, sharded_metadata = \_get_resolved_checkpoint_files( │
│ 4901 │ │ │ pretrained_model_name_or_path=pretrained_model_name_or_path, │
│ 4902 │ │ │ subfolder=subfolder, │
│ 4903 │ │ │ variant=variant, │
│ │
│ ╭──────────────────────────────────────────────────── locals ─────────────────────────────────────────────────────╮ │
│ │ * = None │ │
│ │ \_adapter_model_path = None │ │
│ │ adapter_kwargs = None │ │
│ │ adapter_name = 'default' │ │
│ │ cache_dir = None │ │
│ │ cls = <class 'transformers.models.bert.modeling_bert.BertForSequenceClassification'> │ │
│ │ commit_hash = 'e7203729af5c6dbc5689b633cad2068c04b33e2c' │ │
│ │ config = BertConfig { │ │
│ │ "architectures": [ │ │
│ │ │ "BertForSequenceClassification" │ │
│ │ ], │ │
│ │ "attention_probs_dropout_prob": 0.1, │ │
│ │ "classifier_dropout": null, │ │
│ │ "gradient_checkpointing": false, │ │
│ │ "hidden_act": "gelu", │ │
│ │ "hidden_dropout_prob": 0.1, │ │
│ │ "hidden_size": 384, │ │
│ │ "id2label": { │ │
│ │ │ "0": "LABEL_0" │ │
│ │ }, │ │
│ │ "initializer_range": 0.02, │ │
│ │ "intermediate_size": 1536, │ │
│ │ "label2id": { │ │
│ │ │ "LABEL_0": 0 │ │
│ │ }, │ │
│ │ "layer_norm_eps": 1e-12, │ │
│ │ "max_position_embeddings": 512, │ │
│ │ "model_type": "bert", │ │
│ │ "num_attention_heads": 12, │ │
│ │ "num_hidden_layers": 4, │ │
│ │ "pad_token_id": 0, │ │
│ │ "position_embedding_type": "absolute", │ │
│ │ "sbert_ce_default_activation_function": "torch.nn.modules.linear.Identity", │ │
│ │ "transformers_version": "4.57.3", │ │
│ │ "type_vocab_size": 2, │ │
│ │ "use_cache": true, │ │
│ │ "vocab_size": 30522 │ │
│ │ } │ │
│ │ device_in_context = None │ │
│ │ device_map = None │ │
│ │ device_mesh = None │ │
│ │ distributed_config = None │ │
│ │ dtype = None │ │
│ │ force_download = False │ │
│ │ from_auto_class = True │ │
│ │ from_flax = False │ │
│ │ from_pipeline = None │ │
│ │ from_pt = True │ │
│ │ from_tf = False │ │
│ │ generation_config = None │ │
│ │ gguf_file = None │ │
│ │ hf_quantizer = None │ │
│ │ ignore_mismatched_sizes = False │ │
│ │ key_mapping = None │ │
│ │ kwargs = {} │ │
│ │ load_in_4bit = False │ │
│ │ load_in_8bit = False │ │
│ │ local_files_only = False │ │
│ │ max_memory = None │ │
│ │ model_args = () │ │
│ │ model_kwargs = {} │ │
│ │ offload_buffers = False │ │
│ │ offload_folder = None │ │
│ │ output_loading_info = False │ │
│ │ pretrained_model_name_or_path = 'y3fai/jassas-minilm-l4-int8' │ │
│ │ proxies = None │ │
│ │ quantization_config = None │ │
│ │ revision = None │ │
│ │ state_dict = None │ │
│ │ subfolder = '' │ │
│ │ token = None │ │
│ │ torch_dtype = None │ │
│ │ tp_plan = None │ │
│ │ tp_size = None │ │
│ │ transformers_explicit_filename = None │ │
│ │ trust_remote_code = False │ │
│ │ use_auth_token = None │ │
│ │ use_kernels = False │ │
│ │ use_safetensors = None │ │
│ │ user_agent = {'file_type': 'model', 'framework': 'pytorch', 'from_auto_class': True} │ │
│ │ variant = None │ │
│ │ weights_only = True │ │
│ ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
│ │
│ /Users/yousef/dev/jassas/venv/lib/python3.12/site-packages/transformers/modeling_utils.py:1148 in │
│ \_get_resolved_checkpoint_files │
│ │
│ 1145 │ │ │ │ │ │ │ │ f" {variant}. Use `variant=None` to load this model from │
│ 1146 │ │ │ │ │ │ │ ) │
│ 1147 │ │ │ │ │ │ else: │
│ ❱ 1148 │ │ │ │ │ │ │ raise OSError( │
│ 1149 │ │ │ │ │ │ │ │ f"{pretrained_model_name_or_path} does not appear to hav │
│ 1150 │ │ │ │ │ │ │ │ f" {\_add_variant(WEIGHTS_NAME, variant)}, {\_add_variant( │
│ 1151 │ │ │ │ │ │ │ │ f" {TF2_WEIGHTS_NAME}, {TF_WEIGHTS_NAME} or {FLAX_WEIGHT │
│ │
│ ╭────────────────────────────────────────────────────────── locals ──────────────────────────────────────────────────────────╮ │
│ │ cache_dir = None │ │
│ │ cached_file_kwargs = { │ │
│ │ │ 'cache_dir': None, │ │
│ │ │ 'force_download': False, │ │
│ │ │ 'proxies': None, │ │
│ │ │ 'local_files_only': False, │ │
│ │ │ 'token': None, │ │
│ │ │ 'user_agent': { │ │
│ │ │ │ 'file_type': 'model', │ │
│ │ │ │ 'framework': 'pytorch', │ │
│ │ │ │ 'from_auto_class': True │ │
│ │ │ }, │ │
│ │ │ 'revision': None, │ │
│ │ │ 'subfolder': '', │ │
│ │ │ '\_raise_exceptions_for_gated_repo': False, │ │
│ │ │ '\_raise_exceptions_for_missing_entries': False, │ │
│ │ │ ... +1 │ │
│ │ } │ │
│ │ commit_hash = 'e7203729af5c6dbc5689b633cad2068c04b33e2c' │ │
│ │ filename = 'pytorch_model.bin' │ │
│ │ force_download = False │ │
│ │ from_flax = False │ │
│ │ from_tf = False │ │
│ │ gguf_file = None │ │
│ │ has_file_kwargs = { │ │
│ │ │ 'revision': None, │ │
│ │ │ 'proxies': None, │ │
│ │ │ 'token': None, │ │
│ │ │ 'cache_dir': None, │ │
│ │ │ 'local_files_only': False │ │
│ │ } │ │
│ │ is_local = False │ │
│ │ is_remote_code = False │ │
│ │ is_sharded = False │ │
│ │ local_files_only = False │ │
│ │ pretrained_model_name_or_path = 'y3fai/jassas-minilm-l4-int8' │ │
│ │ proxies = None │ │
│ │ resolved_archive_file = None │ │
│ │ revision = None │ │
│ │ subfolder = '' │ │
│ │ token = None │ │
│ │ transformers_explicit_filename = None │ │
│ │ use_safetensors = None │ │
│ │ user_agent = {'file_type': 'model', 'framework': 'pytorch', 'from_auto_class': True} │ │
│ │ variant = None │ │
│ ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯ │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
OSError: y3fai/jassas-minilm-l4-int8 does not appear to have a file named pytorch_model.bin, model.safetensors, tf_model.h5,
model.ckpt or flax_model.msgpack.
yousef@Yousefs-MacBook-Air jassas % ./venv/bin/pip install --no-user "optimum[onnxruntime]>=1.17.0"
Collecting optimum>=1.17.0 (from optimum[onnxruntime]>=1.17.0)
Downloading optimum-2.1.0-py3-none-any.whl.metadata (14 kB)
Requirement already satisfied: transformers>=4.29 in ./venv/lib/python3.12/site-packages (from optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (4.57.3)
Requirement already satisfied: torch>=1.11 in ./venv/lib/python3.12/site-packages (from optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2.9.1)
Requirement already satisfied: packaging in ./venv/lib/python3.12/site-packages (from optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (25.0)
Requirement already satisfied: numpy in ./venv/lib/python3.12/site-packages (from optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (1.26.4)
Requirement already satisfied: huggingface_hub>=0.8.0 in ./venv/lib/python3.12/site-packages (from optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (0.36.0)
Requirement already satisfied: filelock in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.20.2)
Requirement already satisfied: fsspec>=2023.5.0 in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2025.12.0)
Requirement already satisfied: pyyaml>=5.1 in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (6.0.3)
Requirement already satisfied: requests in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2.31.0)
Requirement already satisfied: tqdm>=4.42.1 in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (4.67.1)
Requirement already satisfied: typing-extensions>=3.7.4.3 in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (4.15.0)
Requirement already satisfied: hf-xet<2.0.0,>=1.1.3 in ./venv/lib/python3.12/site-packages (from huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (1.2.0)
Collecting optimum-onnx[onnxruntime] (from optimum[onnxruntime]>=1.17.0)
Downloading optimum_onnx-0.1.0-py3-none-any.whl.metadata (4.8 kB)
Requirement already satisfied: setuptools in ./venv/lib/python3.12/site-packages (from torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (80.9.0)
Requirement already satisfied: sympy>=1.13.3 in ./venv/lib/python3.12/site-packages (from torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (1.14.0)
Requirement already satisfied: networkx>=2.5.1 in ./venv/lib/python3.12/site-packages (from torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.6.1)
Requirement already satisfied: jinja2 in ./venv/lib/python3.12/site-packages (from torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.1.6)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./venv/lib/python3.12/site-packages (from sympy>=1.13.3->torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (1.3.0)
Requirement already satisfied: regex!=2019.12.17 in ./venv/lib/python3.12/site-packages (from transformers>=4.29->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2025.11.3)
Requirement already satisfied: tokenizers<=0.23.0,>=0.22.0 in ./venv/lib/python3.12/site-packages (from transformers>=4.29->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (0.22.1)
Requirement already satisfied: safetensors>=0.4.3 in ./venv/lib/python3.12/site-packages (from transformers>=4.29->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (0.7.0)
Requirement already satisfied: MarkupSafe>=2.0 in ./venv/lib/python3.12/site-packages (from jinja2->torch>=1.11->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.0.3)
Collecting onnx (from optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0)
Using cached onnx-1.20.0-cp312-abi3-macosx_12_0_universal2.whl.metadata (8.4 kB)
Requirement already satisfied: onnxruntime>=1.18.0 in ./venv/lib/python3.12/site-packages (from optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0) (1.23.2)
Requirement already satisfied: coloredlogs in ./venv/lib/python3.12/site-packages (from onnxruntime>=1.18.0->optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0) (15.0.1)
Requirement already satisfied: flatbuffers in ./venv/lib/python3.12/site-packages (from onnxruntime>=1.18.0->optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0) (25.12.19)
Requirement already satisfied: protobuf in ./venv/lib/python3.12/site-packages (from onnxruntime>=1.18.0->optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0) (6.33.2)
Requirement already satisfied: humanfriendly>=9.1 in ./venv/lib/python3.12/site-packages (from coloredlogs->onnxruntime>=1.18.0->optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0) (10.0)
Collecting ml_dtypes>=0.5.0 (from onnx->optimum-onnx[onnxruntime]; extra == "onnxruntime"->optimum[onnxruntime]>=1.17.0)
Downloading ml_dtypes-0.5.4-cp312-cp312-macosx_10_13_universal2.whl.metadata (8.9 kB)
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib/python3.12/site-packages (from requests->huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.4.4)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.12/site-packages (from requests->huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.12/site-packages (from requests->huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2.6.2)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.12/site-packages (from requests->huggingface_hub>=0.8.0->optimum>=1.17.0->optimum[onnxruntime]>=1.17.0) (2026.1.4)
Downloading optimum-2.1.0-py3-none-any.whl (161 kB)
Downloading optimum_onnx-0.1.0-py3-none-any.whl (194 kB)
Downloading onnx-1.20.0-cp312-abi3-macosx_12_0_universal2.whl (18.3 MB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 18.3/18.3 MB 6.2 MB/s 0:00:02
Downloading ml_dtypes-0.5.4-cp312-cp312-macosx_10_13_universal2.whl (676 kB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 676.9/676.9 kB 9.1 MB/s 0:00:00
Installing collected packages: ml_dtypes, onnx, optimum, optimum-onnx
Successfully installed ml_dtypes-0.5.4 onnx-1.20.0 optimum-2.1.0 optimum-onnx-0.1.0
yousef@Yousefs-MacBook-Air jassas % ./jassas search "اصدار جواز سفر"

Searching: اصدار جواز سفر

Loading vector model...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
Loading vector index...
[Vector] load=1765.2ms, encode=20.3ms, search=27.1ms
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either: - Avoid using `tokenizers` before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
tokenizer_config.json: 1.27kB [00:00, 223kB/s]
vocab.txt: 232kB [00:00, 1.24MB/s]
tokenizer.json: 711kB [00:00, 5.03MB/s]
special_tokens_map.json: 100%|███████████████████████████████████████████████████████████████████| 695/695 [00:00<00:00, 4.46MB/s]
./model_quantized.onnx: 100%|████████████████████████████████████████████████████████████████| 19.5M/19.5M [00:05<00:00, 3.65MB/s]
[Ranker] normalize=0.7ms, search=1813.1ms, sort=0.0ms, fetch=6.1ms, rerank=14589.4ms, total=16409.2ms
Results (10)  
╭─────┬──────────┬───────────────────────────────────────────────┬─────────────────────────────────────────────────╮
│ # │ Score │ Title │ URL │
├─────┼──────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ 1 │ 8.0859 │ اصدار جواز سفر سعودي | منصه وطنيه │ https://my.gov.sa/ar/services/112093 │
│ 2 │ 7.9263 │ جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه │ https://my.gov.sa/ar/services/319232 │
│ 3 │ 7.7564 │ تجديد جواز سفر سعودي | منصه وطنيه │ https://my.gov.sa/ar/services/112090 │
│ 4 │ 7.5388 │ اصدار جواز بدل مفقود | منصه وطنيه │ https://my.gov.sa/ar/services/343104 │
│ 5 │ 7.2103 │ تحـــــديث معلومـــــات جواز سفر | منصه وطنيه │ https://my.gov.sa/ar/services/532976 │
│ 6 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/agencies │
│ 7 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/services │
│ 8 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/emergency-contact │
│ 9 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/contact │
│ 10 │ 4.6795 │ منصه وطنيه │ https://my.gov.sa/ar/artities-performance-index │
╰─────┴──────────┴───────────────────────────────────────────────┴─────────────────────────────────────────────────╯
yousef@Yousefs-MacBook-Air jassas % ./jassas search "اصدار جواز سفر"

Searching: اصدار جواز سفر

Loading vector model...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
Loading vector index...
[Vector] load=1545.1ms, encode=16.8ms, search=20.1ms
[Ranker] normalize=0.2ms, search=1582.7ms, sort=0.0ms, fetch=6.6ms, rerank=3866.4ms, total=5455.9ms
Results (10)  
╭─────┬──────────┬───────────────────────────────────────────────┬─────────────────────────────────────────────────╮
│ # │ Score │ Title │ URL │
├─────┼──────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ 1 │ 8.0859 │ اصدار جواز سفر سعودي | منصه وطنيه │ https://my.gov.sa/ar/services/112093 │
│ 2 │ 7.9263 │ جواز سفر خيل (جديد / بدل فاقد) | منصه وطنيه │ https://my.gov.sa/ar/services/319232 │
│ 3 │ 7.7564 │ تجديد جواز سفر سعودي | منصه وطنيه │ https://my.gov.sa/ar/services/112090 │
│ 4 │ 7.5388 │ اصدار جواز بدل مفقود | منصه وطنيه │ https://my.gov.sa/ar/services/343104 │
│ 5 │ 7.2103 │ تحـــــديث معلومـــــات جواز سفر | منصه وطنيه │ https://my.gov.sa/ar/services/532976 │
│ 6 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/agencies │
│ 7 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/services │
│ 8 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/emergency-contact │
│ 9 │ 4.6795 │ منصه وطنيه │ https://www.my.gov.sa/ar/ar/contact │
│ 10 │ 4.6795 │ منصه وطنيه │ https://my.gov.sa/ar/artities-performance-index │
╰─────┴──────────┴───────────────────────────────────────────────┴─────────────────────────────────────────────────╯
yousef@Yousefs-MacBook-Air jassas % ./jassas search "تجديد رخصة سير"

Searching: تجديد رخصة سير

Loading vector model...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
Loading vector index...
[Vector] load=1541.9ms, encode=13.1ms, search=20.1ms
[Ranker] normalize=0.2ms, search=1575.5ms, sort=0.0ms, fetch=7.6ms, rerank=3879.8ms, total=5463.1ms
Results (10)  
╭─────┬──────────┬────────────────────────────────────────────────────┬───────────────────────────────────────╮
│ # │ Score │ Title │ URL │
├─────┼──────────┼────────────────────────────────────────────────────┼───────────────────────────────────────┤
│ 1 │ 8.6779 │ تخصيص عنوان فريد مكون من 24 بت للطائرات سعوديه ... │ https://my.gov.sa/ar/services/492542 │
│ 2 │ 8.3200 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء ... │ https://my.gov.sa/ar/events/16837 │
│ 3 │ 8.2568 │ تجديد رخصه سير | منصه وطنيه │ https://my.gov.sa/ar/services/112111 │
│ 4 │ 8.2374 │ تجديد رخصه عربه متنقله | منصه وطنيه │ https://my.gov.sa/ar/services/1052434 │
│ 5 │ 8.0212 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوا... │ https://my.gov.sa/ar/services/468819 │
│ 6 │ 7.8667 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ https://my.gov.sa/ar/services/349315 │
│ 7 │ 7.8593 │ استعراض رخصه سير رقميه | منصه وطنيه │ https://my.gov.sa/ar/services/538669 │
│ 8 │ 7.5547 │ طباعه رخصه سير | منصه وطنيه │ https://my.gov.sa/ar/services/538630 │
│ 9 │ 6.6662 │ مواعيد مرور | منصه وطنيه │ https://my.gov.sa/ar/services/538565 │
│ 10 │ 6.1314 │ وزاره داخليه | منصه وطنيه │ https://my.gov.sa/ar/agencies/17624 │
╰─────┴──────────┴────────────────────────────────────────────────────┴───────────────────────────────────────╯
yousef@Yousefs-MacBook-Air jassas % ./jassas benchmarks all  
Usage: jassas.py [OPTIONS] COMMAND [ARGS]...
Try 'jassas.py --help' for help.
╭─ Error ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ No such command 'benchmarks'. Did you mean 'benchmark'? │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
yousef@Yousefs-MacBook-Air jassas % ./jassas benchmark all

Running relevance benchmark...

Jassas Relevance Benchmark (LLM-as-a-Judge)

Judges: devstral-2512, mimo-v2-flash
Queries: 15

Loading search engine...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
OK Engine ready

Evaluating: اصدار رخصه بناء...

Query: اصدار رخصه بناء
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ اصدار رخصه بناء بالتزامن | منصه وطنيه │ 3 │ 3 │ 3 │
│ 2 │ اصدار رخصه بناء زراعي | منصه وطنيه │ 2 │ 2 │ 3 │
│ 3 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 4 │ اصدار رخصه بناء استثماري | منصه وطنيه │ 2 │ 2 │ 3 │
│ 5 │ اصدار رخصه بناء | منصه وطنيه │ 3 │ 3 │ 3 │
│ 6 │ اصدار رخصه بناء | منصه وطنيه │ 3 │ 3 │ 3 │
│ 7 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 8 │ تنفيذ واداره شبكات سيسكو (ccna) | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.92 | P@10=50% | Avg=1.3/3

Evaluating: دفع ضريبه قيمه مضافه...

Query: دفع ضريبه قيمه مضافه
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ مشاركه بالراي في مقترح حالات اضافيه للسماح باسترداد ضريبه │ 1 │ 1 │ 1 │
│ │ قيمه مضافه للمطورين عق │ │ │ │
│ 2 │ طلب خطه دفع ضريبه قيمه مضافه بالتقسيط | منصه وطنيه │ 3 │ 3 │ 3 │
│ 3 │ تسجيل في ضريبه قيمه مضافه (منشات) | منصه وطنيه │ 2 │ 2 │ 3 │
│ 4 │ تسجيل مجموعه في ضريبه قيمه مضافه | منصه وطنيه │ 2 │ 2 │ 3 │
│ 5 │ تسجيل افراد في ضريبه قيمه مضافه | منصه وطنيه │ 2 │ 2 │ 3 │
│ 6 │ غاء تسجيل في ضريبه قيمه مضافه | منصه وطنيه │ 2 │ 2 │ 3 │
│ 7 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 8 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.50 | NDCG@10=0.86 | P@10=50% | Avg=1.2/3

Evaluating: حجز مواعيد طبيه...

Query: حجز مواعيد طبيه
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تخصيص عنوان فريد مكون من 24 بت للطائرات سعوديه مجهزه بجهاز │ 0 │ 0 │ 0 │
│ │ ارسال واستقبال نمط اس │ │ │ │
│ 2 │ احوال مدنيه تطلق سبت مقبل حجز مواعيد سجل مدني كترونيا | منصه │ 1 │ 1 │ 1 │
│ │ وطنيه │ │ │ │
│ 3 │ تعديل طلب حجز مخيمات من قبل وزاره | منصه وطنيه │ 0 │ 0 │ 0 │
│ 4 │ خدمه حجز مواعيد طبيه | منصه وطنيه │ 3 │ 3 │ 3 │
│ 5 │ حجز مواعيد اسنان | منصه وطنيه │ 2 │ 2 │ 2 │
│ 6 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ فحص طبي قبل زواج | منصه وطنيه │ 1 │ 1 │ 1 │
│ 8 │ تعديلات مواصفات عمليات | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ رعايه صحيه منزليه | منصه وطنيه │ 1 │ 1 │ 1 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.25 | NDCG@10=0.60 | P@10=20% | Avg=0.8/3

Evaluating: تجديد اقامه...

Query: تجديد اقامه
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تجديد رخصه مكتب حجز اقامه سياحيه | منصه وطنيه │ 2 │ 1 │ 3 │
│ 2 │ رخصه مرافق اقامه سياحيه للضيافه - تجديد ترخيص | منصه وطنيه │ 2 │ 1 │ 2 │
│ 3 │ تجديد اقامه | منصه وطنيه │ 3 │ 3 │ 3 │
│ 4 │ تجديد اقامه | منصه وطنيه │ 3 │ 3 │ 3 │
│ 5 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 6 │ اصدار و تجديد رخص عمل | منصه وطنيه │ 1 │ 0 │ 2 │
│ 7 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ ø§ùùùø§ø° ø§ùùø·ùù ø§ùù ùø­ø ̄ │ 0 │ 0 │ 0 │
╰─────┴────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.90 | P@10=40% | Avg=1.1/3

Evaluating: اصدار تاشيرات عمل...

Query: اصدار تاشيرات عمل
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ خدمه زيارات عائليه للمهن عليا علي منصه تاشيرات الكترونيه | │ 2 │ 1 │ 3 │
│ │ منصه وطنيه │ │ │ │
│ 2 │ اصدار تاشيرات عمل فوريه | منصه وطنيه │ 3 │ 3 │ 3 │
│ 3 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 4 │ تمكين مواطنين من استصدار تاشيرات عماله منزليه كترونيا | منصه │ 2 │ 2 │ 3 │
│ │ وطنيه │ │ │ │
│ 5 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 6 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ تاشيرات والسياحه | منصه وطنيه │ 1 │ 1 │ 1 │
│ 9 │ تاشيرات مهنيه فوريه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.87 | P@10=40% | Avg=1.0/3

Evaluating: حجز اسم تجاري...

Query: حجز اسم تجاري
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 2 │ حجز تذاكر سفر | منصه وطنيه │ 0 │ 0 │ 0 │
│ 3 │ تعديل طلب حجز مخيمات من قبل وزاره | منصه وطنيه │ 0 │ 0 │ 0 │
│ 4 │ تمديد حجز اسم تجاري | منصه وطنيه │ 2 │ 2 │ 2 │
│ 5 │ حجز اسم تجاري | منصه وطنيه │ 3 │ 3 │ 3 │
│ 6 │ احوال مدنيه تطلق سبت مقبل حجز مواعيد سجل مدني كترونيا | منصه │ 0 │ 0 │ 0 │
│ │ وطنيه │ │ │ │
│ 7 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 8 │ حجز مرافق | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.25 | NDCG@10=0.47 | P@10=20% | Avg=0.5/3

Evaluating: تسجيل تصرف عقاري...

Query: تسجيل تصرف عقاري
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 2 │ مشاركه بالراي في مشروع ضوابط تطوير اراضي مخططه وفقا للماده │ 2 │ 2 │ 1 │
│ │ ثالثه عشره من لائحه ت │ │ │ │
│ 3 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 4 │ مشاركه بالراي في قواعد منظمه لتقديم خدمات تقييم عقاري للجهات │ 1 │ 1 │ 1 │
│ │ تمويليه | منصه وطني │ │ │ │
│ 5 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 6 │ طلب تسجيل تصرف عقاري | منصه وطنيه │ 3 │ 3 │ 3 │
│ 7 │ دليل خدمات في مملكه عربيه سعوديه علي منصه وطنيه | منصه وطنيه │ 0 │ 1 │ 0 │
│ 8 │ دليل خدمات في مملكه عربيه سعوديه علي منصه وطنيه | منصه وطنيه │ 0 │ 1 │ 0 │
│ 9 │ شهاده فرز | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.50 | NDCG@10=0.58 | P@10=20% | Avg=0.6/3

Evaluating: اصدار هويه وطنيه...

Query: اصدار هويه وطنيه
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ اصدار هويه وطنيه لفرد اسره | منصه وطنيه │ 3 │ 3 │ 3 │
│ 2 │ اصدار هويه بدل تالف | منصه وطنيه │ 2 │ 2 │ 2 │
│ 3 │ مشاركه بالراي في مشروع لائحه تنفيذيه لتنظيم فحص دوري | منصه │ 0 │ 0 │ 0 │
│ │ وطنيه │ │ │ │
│ 4 │ اصدار هويه بدل مفقود | منصه وطنيه │ 2 │ 2 │ 2 │
│ 5 │ اصدار هويه مقيم | منصه وطنيه │ 2 │ 2 │ 1 │
│ 6 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ تعديلات مواصفات عمليات | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ استعلام عن مسارات عربات متجوله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ طلب هويه بدل تالف | منصه وطنيه │ 2 │ 2 │ 2 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.94 | P@10=50% | Avg=1.1/3

Evaluating: اصدار تاشيره خروج والعوده...

Query: اصدار تاشيره خروج والعوده
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ مصدر مسؤول بوزاره خارجيه: مملكه تهنئ جمهوريه عراق باستعاده │ 0 │ 0 │ 0 │
│ │ قضاء رواه بالكامل من │ │ │ │
│ 2 │ اصدار تاشيره خروج والعوده او خروج نهائي | منصه وطنيه │ 3 │ 3 │ 3 │
│ 3 │ تمديد تاشيره خروج وعوده لمن هم خارج مملكه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 4 │ مشاركه بالراي في تعديل فقره (2) من ماده (3 مكرر) من لائحه │ 0 │ 0 │ 0 │
│ │ تنفيذيه لنظام تامين ضد │ │ │ │
│ 5 │ جبير: مملكه ستتخذ خطوات اضافيه في حال استمرار انتهاكات │ 0 │ 0 │ 0 │
│ │ ايرانيه ضد مملكه | منصه و │ │ │ │
│ 6 │ مشاركه بالراي في تعديل فقره (2) من بند (خامسا) من قرار وزاري │ 0 │ 0 │ 0 │
│ │ رقم (1/74) بتاريخ 1 │ │ │ │
│ 7 │ استعلام عن حاله تاشيره خروج وعوده | منصه وطنيه │ 2 │ 2 │ 2 │
│ 8 │ غاء تاشيره خروج والعوده | منصه وطنيه │ 2 │ 2 │ 2 │
│ 9 │ ترخيص مكاتب دعايه والاعلان، مكاتب تسويق، وكالات دعايه | منصه │ 0 │ 0 │ 0 │
│ │ وطنيه │ │ │ │
│ 10 │ دليل خدمات في مملكه عربيه سعوديه علي منصه وطنيه | منصه وطنيه │ 1 │ 1 │ 1 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.50 | NDCG@10=0.69 | P@10=40% | Avg=1.0/3

Evaluating: اصدار رخصه سير...

Query: اصدار رخصه سير
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تخصيص عنوان فريد مكون من 24 بت للطائرات سعوديه مجهزه بجهاز │ 0 │ 0 │ 0 │
│ │ ارسال واستقبال نمط اس │ │ │ │
│ 2 │ استعراض رخصه سير رقميه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 3 │ اصدار رخصه قياده | منصه وطنيه │ 2 │ 1 │ 2 │
│ 4 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 1 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 5 │ اصدار رخصه سير | منصه وطنيه │ 3 │ 3 │ 3 │
│ 6 │ تجديد رخصه سير | منصه وطنيه │ 2 │ 2 │ 2 │
│ 7 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 1 │
│ 8 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ مواعيد مرور | منصه وطنيه │ 0 │ 1 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.50 | NDCG@10=0.68 | P@10=40% | Avg=0.9/3

Evaluating: تجديد رخص عمل...

Query: تجديد رخص عمل
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تجديد رخص (للفرد) | منصه وطنيه │ 2 │ 2 │ 3 │
│ 2 │ تجديد رخص (للمنشاه) | منصه وطنيه │ 2 │ 1 │ 3 │
│ 3 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 4 │ خدمه تجديد رخص سكن جماعي | منصه وطنيه │ 0 │ 0 │ 0 │
│ 5 │ طلب تجديد رخصه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 6 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 0 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 7 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 8 │ اصدار و تجديد رخص عمل | منصه وطنيه │ 3 │ 3 │ 3 │
│ 9 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.81 | P@10=40% | Avg=0.9/3

Evaluating: اصدار شهاده اشتراك...

Query: اصدار شهاده اشتراك
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ اصدار شهاده اشتراك | منصه وطنيه │ 3 │ 3 │ 3 │
│ 2 │ مشاركه بالراي في مشروع لائحه تنفيذيه لتنظيم فحص دوري | منصه │ 0 │ 0 │ 0 │
│ │ وطنيه │ │ │ │
│ 3 │ اداره اشتراكات | منصه وطنيه │ 2 │ 2 │ 2 │
│ 4 │ تجديد اشتراك | منصه وطنيه │ 2 │ 1 │ 2 │
│ 5 │ اصدار شهاده اجور | منصه وطنيه │ 1 │ 1 │ 1 │
│ 6 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ استعلام عن مسارات عربات متجوله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ تعديلات مواصفات عمليات | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ قنوات تقديم خدمه | منصه وطنيه │ 0 │ 1 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.92 | P@10=30% | Avg=0.8/3

Evaluating: تسجيل في جامعات...

Query: تسجيل في جامعات
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ تسجيل في جلسه ارشاد مهني في جامعات | منصه وطنيه │ 2 │ 2 │ 2 │
│ 2 │ برنامج ابتعاث خارجي مستمر لسنوات قادمه واعلان لوائح تعليم │ 1 │ 1 │ 1 │
│ │ الكتروني قريبا | منصه │ │ │ │
│ 3 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 4 │ مشاركه بالراي في تعديل نظام جامعات | منصه وطنيه │ 2 │ 1 │ 2 │
│ 5 │ اختبار مقياس ميول مهني في (منصه سبل) | منصه وطنيه │ 1 │ 1 │ 1 │
│ 6 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ تنفيذ واداره شبكات سيسكو (ccna) | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ ورش عمل ارشاد مهني في جامعات | منصه وطنيه │ 2 │ 2 │ 2 │
│ 9 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ اعداد لنخبه جامعات | منصه وطنيه │ 1 │ 1 │ 1 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.88 | P@10=30% | Avg=0.9/3

Evaluating: اصدار رخصه حرفيه...

Query: اصدار رخصه حرفيه
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين │ 0 │ 0 │ 0 │
│ │ بتقديم خدمات محاسبه │ │ │ │
│ 2 │ اصدار رخصه حرفيه جديده | منصه وطنيه │ 3 │ 3 │ 3 │
│ 3 │ تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه │ 0 │ 0 │ 1 │
│ │ اخري | منصه وطنيه │ │ │ │
│ 4 │ اصدار رخصه حرفيه | منصه وطنيه │ 3 │ 3 │ 3 │
│ 5 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 6 │ غاء رخصه حرفيه | منصه وطنيه │ 1 │ 1 │ 1 │
│ 7 │ تعديل رخصه حرفيه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 8 │ تعديل رخصه حرفيه | منصه وطنيه │ 2 │ 2 │ 2 │
│ 9 │ ترخيص تشغيلي تربيه ابقار | منصه وطنيه │ 0 │ 0 │ 0 │
│ 10 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=0.50 | NDCG@10=0.68 | P@10=40% | Avg=1.1/3

Evaluating: طلب ابتعاث خارجي...

Query: طلب ابتعاث خارجي
Judges: 2 (devstral-2512, mimo-v2-flash)
Scored Documents  
╭─────┬──────────────────────────────────────────────────────────────┬─────┬──────────┬──────────╮
│ # │ Title │ Avg │ devstral │ mimo-v2- │
├─────┼──────────────────────────────────────────────────────────────┼─────┼──────────┼──────────┤
│ 1 │ طلب تقديم علي بعثه في برنامج خادم حرمين شريفين للابتعاث │ 3 │ 3 │ 3 │
│ │ خارجي | منصه وطنيه │ │ │ │
│ 2 │ برنامج ابتعاث خارجي مستمر لسنوات قادمه واعلان لوائح تعليم │ 2 │ 2 │ 2 │
│ │ الكتروني قريبا | منصه │ │ │ │
│ 3 │ ابتعاث خارجي والتعليم ذاتي لمواكبه تحول رقمي | منصه وطنيه │ 2 │ 1 │ 2 │
│ 4 │ "الطيران مدني" تبدا في تلقي طلبات ابتعاث | منصه وطنيه │ 2 │ 2 │ 2 │
│ 5 │ تعليم عالي يعلن مواعيد انطلاق ملتقيات مرحله سادسه للابتعاث │ 2 │ 2 │ 2 │
│ │ خارجي | منصه وطنيه │ │ │ │
│ 6 │ طلب نظام جديد | منصه وطنيه │ 0 │ 0 │ 0 │
│ 7 │ استعلام عن مسارات عربات متجوله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 8 │ تجديد رخصه عربه متنقله | منصه وطنيه │ 0 │ 0 │ 0 │
│ 9 │ لقاء بصمه مبتعث | منصه وطنيه │ 1 │ 1 │ 1 │
│ 10 │ ø§ùùùø§ø° ø§ùùø·ùù ø§ùù ùø­ø ̄ │ 0 │ 0 │ 0 │
╰─────┴──────────────────────────────────────────────────────────────┴─────┴──────────┴──────────╯
Metrics: MRR=1.00 | NDCG@10=0.99 | P@10=50% | Avg=1.2/3

                                    Relevance Scores by Query

╭───────────────────────────┬──────┬─────────┬──────┬───────────┬────────────────────────────────╮
│ Query │ MRR │ NDCG@10 │ P@10 │ Avg Score │ Scores │
├───────────────────────────┼──────┼─────────┼──────┼───────────┼────────────────────────────────┤
│ اصدار رخصه بناء │ 1.00 │ 0.92 │ 50% │ 1.3/3 │ [3, 2, 0, 2, 3, 3, 0, 0, 0, 0] │
│ دفع ضريبه قيمه مضافه │ 0.50 │ 0.86 │ 50% │ 1.2/3 │ [1, 3, 2, 2, 2, 2, 0, 0, 0, 0] │
│ حجز مواعيد طبيه │ 0.25 │ 0.60 │ 20% │ 0.8/3 │ [0, 1, 0, 3, 2, 0, 1, 0, 1, 0] │
│ تجديد اقامه │ 1.00 │ 0.90 │ 40% │ 1.1/3 │ [2, 2, 3, 3, 0, 1, 0, 0, 0, 0] │
│ اصدار تاشيرات عمل │ 1.00 │ 0.87 │ 40% │ 1.0/3 │ [2, 3, 0, 2, 0, 0, 0, 1, 2, 0] │
│ حجز اسم تجاري │ 0.25 │ 0.47 │ 20% │ 0.5/3 │ [0, 0, 0, 2, 3, 0, 0, 0, 0, 0] │
│ تسجيل تصرف عقاري │ 0.50 │ 0.58 │ 20% │ 0.6/3 │ [0, 2, 0, 1, 0, 3, 0, 0, 0, 0] │
│ اصدار هويه وطنيه │ 1.00 │ 0.94 │ 50% │ 1.1/3 │ [3, 2, 0, 2, 2, 0, 0, 0, 2, 0] │
│ اصدار تاشيره خروج والعوده │ 0.50 │ 0.69 │ 40% │ 1.0/3 │ [0, 3, 2, 0, 0, 0, 2, 2, 0, 1] │
│ اصدار رخصه سير │ 0.50 │ 0.68 │ 40% │ 0.9/3 │ [0, 2, 2, 0, 3, 2, 0, 0, 0, 0] │
│ تجديد رخص عمل │ 1.00 │ 0.81 │ 40% │ 0.9/3 │ [2, 2, 0, 0, 2, 0, 0, 3, 0, 0] │
│ اصدار شهاده اشتراك │ 1.00 │ 0.92 │ 30% │ 0.8/3 │ [3, 0, 2, 2, 1, 0, 0, 0, 0, 0] │
│ تسجيل في جامعات │ 1.00 │ 0.88 │ 30% │ 0.9/3 │ [2, 1, 0, 2, 1, 0, 0, 2, 0, 1] │
│ اصدار رخصه حرفيه │ 0.50 │ 0.68 │ 40% │ 1.1/3 │ [0, 3, 0, 3, 0, 1, 2, 2, 0, 0] │
│ طلب ابتعاث خارجي │ 1.00 │ 0.99 │ 50% │ 1.2/3 │ [3, 2, 2, 2, 2, 0, 0, 0, 1, 0] │
╰───────────────────────────┴──────┴─────────┴──────┴───────────┴────────────────────────────────╯

Summary Metrics:

Metric Score Interpretation  
 ─────────────────────────────────────────────────────────────
Mean MRR 0.733 1.0 = first result always relevant  
 Mean NDCG@10 0.786 1.0 = perfect ranking  
 Mean P@10 37.3% % of top 10 that are relevant  
 Avg Relevance 0.96/3 0=bad, 3=perfect

Overall Quality Score: 63% - B - Good

Running qa benchmark...

Jassas QA Benchmark (Task Completion)

Judges: devstral-2512, mimo-v2-flash
Questions: 15
Metric: Can user answer their question with Top-K results?

Loading search engine...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
OK Engine ready

Evaluating: اصدار رخصه بناء...

Question: اصدار رخصه بناء
Top results found:

1. اصدار رخصه بناء بالتزامن | منصه وطنيه
2. اصدار رخصه بناء زراعي | منصه وطنيه
3. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
4. اصدار رخصه بناء استثماري | منصه وطنيه
5. اصدار رخصه بناء | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ Y │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: دفع ضريبه قيمه مضافه...

Question: دفع ضريبه قيمه مضافه
Top results found:

1. مشاركه بالراي في مقترح حالات اضافيه للسماح باسترداد ضريبه قيمه مضافه للمطورين عق
2. طلب خطه دفع ضريبه قيمه مضافه بالتقسيط | منصه وطنيه
3. تسجيل في ضريبه قيمه مضافه (منشات) | منصه وطنيه
4. تسجيل مجموعه في ضريبه قيمه مضافه | منصه وطنيه
5. تسجيل افراد في ضريبه قيمه مضافه | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: حجز مواعيد طبيه...

Question: حجز مواعيد طبيه
Top results found:

1. تخصيص عنوان فريد مكون من 24 بت للطائرات سعوديه مجهزه بجهاز ارسال واستقبال نمط اس
2. احوال مدنيه تطلق سبت مقبل حجز مواعيد سجل مدني كترونيا | منصه وطنيه
3. تعديل طلب حجز مخيمات من قبل وزاره | منصه وطنيه
4. خدمه حجز مواعيد طبيه | منصه وطنيه
5. حجز مواعيد اسنان | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ OK │ Y │ N │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: تجديد اقامه...

Question: تجديد اقامه
Top results found:

1. تجديد رخصه مكتب حجز اقامه سياحيه | منصه وطنيه
2. رخصه مرافق اقامه سياحيه للضيافه - تجديد ترخيص | منصه وطنيه
3. تجديد اقامه | منصه وطنيه
4. تجديد اقامه | منصه وطنيه
5. تجديد رخصه عربه متنقله | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار تاشيرات عمل...

Question: اصدار تاشيرات عمل
Top results found:

1. خدمه زيارات عائليه للمهن عليا علي منصه تاشيرات الكترونيه | منصه وطنيه
2. اصدار تاشيرات عمل فوريه | منصه وطنيه
3. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
4. تمكين مواطنين من استصدار تاشيرات عماله منزليه كترونيا | منصه وطنيه
5. تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه اخري | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: حجز اسم تجاري...

Question: حجز اسم تجاري
Top results found:

1. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
2. حجز تذاكر سفر | منصه وطنيه
3. تعديل طلب حجز مخيمات من قبل وزاره | منصه وطنيه
4. تمديد حجز اسم تجاري | منصه وطنيه
5. حجز اسم تجاري | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ FAIL │ N │ N │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: تسجيل تصرف عقاري...

Question: تسجيل تصرف عقاري
Top results found:

1. تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه اخري | منصه وطنيه
2. مشاركه بالراي في مشروع ضوابط تطوير اراضي مخططه وفقا للماده ثالثه عشره من لائحه ت
3. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
4. مشاركه بالراي في قواعد منظمه لتقديم خدمات تقييم عقاري للجهات تمويليه | منصه وطني
5. ترخيص تشغيلي تربيه ابقار | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ FAIL │ N │ N │
   │ 5 │ FAIL │ N │ N │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار هويه وطنيه...

Question: اصدار هويه وطنيه
Top results found:

1. اصدار هويه وطنيه لفرد اسره | منصه وطنيه
2. اصدار هويه بدل تالف | منصه وطنيه
3. مشاركه بالراي في مشروع لائحه تنفيذيه لتنظيم فحص دوري | منصه وطنيه
4. اصدار هويه بدل مفقود | منصه وطنيه
5. اصدار هويه مقيم | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ Y │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار تاشيره خروج والعوده...

Question: اصدار تاشيره خروج والعوده
Top results found:

1. مصدر مسؤول بوزاره خارجيه: مملكه تهنئ جمهوريه عراق باستعاده قضاء رواه بالكامل من
2. اصدار تاشيره خروج والعوده او خروج نهائي | منصه وطنيه
3. تمديد تاشيره خروج وعوده لمن هم خارج مملكه | منصه وطنيه
4. مشاركه بالراي في تعديل فقره (2) من ماده (3 مكرر) من لائحه تنفيذيه لنظام تامين ضد
5. جبير: مملكه ستتخذ خطوات اضافيه في حال استمرار انتهاكات ايرانيه ضد مملكه | منصه و
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار رخصه سير...

Question: اصدار رخصه سير
Top results found:

1. تخصيص عنوان فريد مكون من 24 بت للطائرات سعوديه مجهزه بجهاز ارسال واستقبال نمط اس
2. استعراض رخصه سير رقميه | منصه وطنيه
3. اصدار رخصه قياده | منصه وطنيه
4. تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه اخري | منصه وطنيه
5. اصدار رخصه سير | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: تجديد رخص عمل...

Question: تجديد رخص عمل
Top results found:

1. تجديد رخص (للفرد) | منصه وطنيه
2. تجديد رخص (للمنشاه) | منصه وطنيه
3. تجديد رخصه عربه متنقله | منصه وطنيه
4. خدمه تجديد رخص سكن جماعي | منصه وطنيه
5. طلب تجديد رخصه | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ Y │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار شهاده اشتراك...

Question: اصدار شهاده اشتراك
Top results found:

1. اصدار شهاده اشتراك | منصه وطنيه
2. مشاركه بالراي في مشروع لائحه تنفيذيه لتنظيم فحص دوري | منصه وطنيه
3. اداره اشتراكات | منصه وطنيه
4. تجديد اشتراك | منصه وطنيه
5. اصدار شهاده اجور | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ Y │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: تسجيل في جامعات...

Question: تسجيل في جامعات
Top results found:

1. تسجيل في جلسه ارشاد مهني في جامعات | منصه وطنيه
2. برنامج ابتعاث خارجي مستمر لسنوات قادمه واعلان لوائح تعليم الكتروني قريبا | منصه
3. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
4. مشاركه بالراي في تعديل نظام جامعات | منصه وطنيه
5. اختبار مقياس ميول مهني في (منصه سبل) | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ OK │ Y │ N │
   │ 3 │ FAIL │ N │ N │
   │ 5 │ OK │ Y │ N │
   │ 10 │ OK │ Y │ N │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: اصدار رخصه حرفيه...

Question: اصدار رخصه حرفيه
Top results found:

1. مشاركه بالراي في تطوير برنامج مراقبه جوده اداء مهني للمرخصين بتقديم خدمات محاسبه
2. اصدار رخصه حرفيه جديده | منصه وطنيه
3. تحويل رخصه ورقيه الي كترونيه تربيه خيول والحيوانات خيليه اخري | منصه وطنيه
4. اصدار رخصه حرفيه | منصه وطنيه
5. تجديد رخصه عربه متنقله | منصه وطنيه
   Judge Votes by K  
   ╭────┬──────────┬──────────┬──────────╮
   │ K │ Decision │ devstral │ mimo-v2- │
   ├────┼──────────┼──────────┼──────────┤
   │ 1 │ FAIL │ N │ N │
   │ 3 │ OK │ Y │ Y │
   │ 5 │ OK │ Y │ Y │
   │ 10 │ OK │ Y │ Y │
   ╰────┴──────────┴──────────┴──────────╯

Evaluating: طلب ابتعاث خارجي...

Question: طلب ابتعاث خارجي
Top results found:

1.  طلب تقديم علي بعثه في برنامج خادم حرمين شريفين للابتعاث خارجي | منصه وطنيه
2.  برنامج ابتعاث خارجي مستمر لسنوات قادمه واعلان لوائح تعليم الكتروني قريبا | منصه
3.  ابتعاث خارجي والتعليم ذاتي لمواكبه تحول رقمي | منصه وطنيه
4.  "الطيران مدني" تبدا في تلقي طلبات ابتعاث | منصه وطنيه
5.  تعليم عالي يعلن مواعيد انطلاق ملتقيات مرحله سادسه للابتعاث خارجي | منصه وطنيه
    Judge Votes by K  
    ╭────┬──────────┬──────────┬──────────╮
    │ K │ Decision │ devstral │ mimo-v2- │
    ├────┼──────────┼──────────┼──────────┤
    │ 1 │ OK │ Y │ Y │
    │ 3 │ OK │ Y │ Y │
    │ 5 │ OK │ Y │ Y │
    │ 10 │ OK │ Y │ Y │
    ╰────┴──────────┴──────────┴──────────╯

                        Question Answerability

    ╭───────────────────────────┬───────┬───────┬───────┬────────╮
    │ Question │ Top 1 │ Top 3 │ Top 5 │ Top 10 │
    ├───────────────────────────┼───────┼───────┼───────┼────────┤
    │ اصدار رخصه بناء │ OK │ OK │ OK │ OK │
    │ دفع ضريبه قيمه مضافه │ FAIL │ OK │ OK │ OK │
    │ حجز مواعيد طبيه │ FAIL │ OK │ OK │ OK │
    │ تجديد اقامه │ OK │ OK │ OK │ OK │
    │ اصدار تاشيرات عمل │ OK │ OK │ OK │ OK │
    │ حجز اسم تجاري │ FAIL │ FAIL │ OK │ OK │
    │ تسجيل تصرف عقاري │ FAIL │ FAIL │ FAIL │ OK │
    │ اصدار هويه وطنيه │ OK │ OK │ OK │ OK │
    │ اصدار تاشيره خروج والعوده │ FAIL │ OK │ OK │ OK │
    │ اصدار رخصه سير │ FAIL │ OK │ OK │ OK │
    │ تجديد رخص عمل │ OK │ OK │ OK │ OK │
    │ اصدار شهاده اشتراك │ OK │ OK │ OK │ OK │
    │ تسجيل في جامعات │ OK │ FAIL │ OK │ OK │
    │ اصدار رخصه حرفيه │ FAIL │ OK │ OK │ OK │
    │ طلب ابتعاث خارجي │ OK │ OK │ OK │ OK │
    ╰───────────────────────────┴───────┴───────┴───────┴────────╯

Success Rate (% of questions answerable):

Metric Score Interpretation  
 ─────────────────────────────────────────────
Success@1 53% Answer in first result  
 Success@3 80% Answer in top 3  
 Success@5 93% Answer in top 5  
 Success@10 100% Answer in top 10

Overall Score: 82% - A - Excellent

Insight: Success@1 is the 'I'm feeling lucky' metric.
Success@10 shows if the answer exists in your corpus at all.

Running human benchmark...

============================================================
JASSAS HUMAN EVALUATION BENCHMARK
============================================================

Loading search engine...
/Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
OK Ready

---

Options:
[1] Start/Continue Evaluation
[2] View Summary
[3] Reset All Results
[q] Quit

Choice: q
Goodbye!

OK All benchmarks completed
yousef@Yousefs-MacBook-Air jassas % ./jassas benchmark latecny  
Invalid test type: latecny
Choose: relevance, qa, human, latency, all
yousef@Yousefs-MacBook-Air jassas % ./jassas benchmark latency

Running latency benchmark...

Jassas Benchmarking Suite

1. Measuring Cold Start...
   /Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
   self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
   Model & Index Load Time: 2.14s

2. Profiling Search Latency (5 queries)...
   Latency Breakdown (ms)  
   ╭────────────────────┬──────┬──────┬────────┬──────┬───────┬───────╮
   │ Query │ Norm │ BM25 │ Vector │ RRF │ Fetch │ Total │
   ├────────────────────┼──────┼──────┼────────┼──────┼───────┼───────┤
   │ تجديد جواز السفر │ 0.68 │ 6.12 │ 34.13 │ 0.03 │ 5.99 │ 46.95 │
   │ رخصة القيادة │ 0.02 │ 1.75 │ 9.06 │ 0.03 │ 6.28 │ 17.15 │
   │ المخالفات المرورية │ 0.02 │ 1.66 │ 9.43 │ 0.03 │ 7.96 │ 19.10 │
   │ الأمن السيبراني │ 0.02 │ 1.70 │ 8.20 │ 0.03 │ 5.67 │ 15.61 │
   │ وزارة الصحة │ 0.02 │ 1.40 │ 8.69 │ 0.03 │ 6.29 │ 16.42 │
   ╰────────────────────┴──────┴──────┴────────┴──────┴───────┴───────╯

Component Averages:

Component Avg (ms) % of Total  
 ───────────────────────────────────────
normalization 0.15 0.7%  
 bm25_search 2.53 11.0%  
 vector_search 13.90 60.3%  
 rrf_merge 0.03 0.1%  
 result_fetch 6.44 27.9%

3. Measuring Throughput (50 iterations)...
   Total Time: 8.78s
   Throughput: 5.69 QPS
   Avg Latency: 175.59ms
   Min Latency: 29.04ms
   Max Latency: 7147.90ms
   P95 Latency: 38.50ms
   yousef@Yousefs-MacBook-Air jassas % ./jassas benchmark latency

Running latency benchmark...

Jassas Benchmarking Suite

1. Measuring Cold Start...
   /Users/yousef/dev/jassas/src/ranker/engine.py:76: UserWarning: The model sentence-transformers/paraphrase-multilingual-mpnet-base-v2 now uses mean pooling instead of CLS embedding. In order to preserve the previous behaviour, consider either pinning fastembed version to 0.5.1 or using `add_custom_model` functionality.
   self.vector_model = TextEmbedding(VectorEngine.MODEL_NAME)
   Model & Index Load Time: 1.78s

2. Profiling Search Latency (5 queries)...
   Latency Breakdown (ms)  
   ╭────────────────────┬──────┬──────┬────────┬──────┬───────┬───────╮
   │ Query │ Norm │ BM25 │ Vector │ RRF │ Fetch │ Total │
   ├────────────────────┼──────┼──────┼────────┼──────┼───────┼───────┤
   │ تجديد جواز السفر │ 0.32 │ 4.20 │ 28.35 │ 0.04 │ 8.92 │ 41.83 │
   │ رخصة القيادة │ 0.02 │ 1.81 │ 9.15 │ 0.03 │ 7.95 │ 18.96 │
   │ المخالفات المرورية │ 0.02 │ 1.72 │ 10.05 │ 0.03 │ 8.01 │ 19.82 │
   │ الأمن السيبراني │ 0.02 │ 1.82 │ 8.55 │ 0.03 │ 7.94 │ 18.36 │
   │ وزارة الصحة │ 0.02 │ 1.66 │ 7.61 │ 0.03 │ 7.75 │ 17.07 │
   ╰────────────────────┴──────┴──────┴────────┴──────┴───────┴───────╯

Component Averages:

Component Avg (ms) % of Total  
 ───────────────────────────────────────
normalization 0.08 0.3%  
 bm25_search 2.24 9.7%  
 vector_search 12.74 54.9%  
 rrf_merge 0.03 0.1%  
 result_fetch 8.11 35.0%

3. Measuring Throughput (50 iterations)...
   Total Time: 7.14s
   Throughput: 7.00 QPS
   Avg Latency: 142.76ms
   Min Latency: 28.42ms
   Max Latency: 5506.30ms
   P95 Latency: 37.87ms
   yousef@Yousefs-MacBook-Air jassas %
