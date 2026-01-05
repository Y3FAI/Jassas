#!/usr/bin/env python3
"""
Preload Models Script - Downloads embedding models using HuggingFace mirror.
Run this on the server before starting the API.

Usage:
    python scripts/preload_models.py

Environment:
    HF_ENDPOINT - HuggingFace mirror URL (default: https://hf-mirror.com)
"""
import os
import sys

# Set HuggingFace mirror before any imports
MIRROR_URL = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com")
os.environ["HF_ENDPOINT"] = MIRROR_URL

print(f"Using HuggingFace mirror: {MIRROR_URL}")
print("-" * 50)

# Now import the libraries
from fastembed import TextEmbedding

# Model used by Jassas
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def main():
    print(f"Downloading model: {MODEL_NAME}")
    print("This may take a few minutes on first run...\n")

    try:
        # Load model (downloads if not cached)
        model = TextEmbedding(MODEL_NAME)
        print("Model loaded successfully!")

        # Test embedding
        print("\nTesting embedding generation...")
        test_text = ["اختبار البحث"]
        embedding = list(model.embed(test_text))[0]
        print(f"Embedding shape: {embedding.shape}")
        print(f"Embedding dtype: {embedding.dtype}")

        # Show cache location
        cache_dir = os.path.expanduser("~/.cache/fastembed")
        if os.path.exists(cache_dir):
            print(f"\nCache location: {cache_dir}")
            for item in os.listdir(cache_dir):
                print(f"  - {item}")

        print("\n" + "=" * 50)
        print("SUCCESS: Model is ready. You can now start the API.")
        print("=" * 50)

    except Exception as e:
        print(f"\nERROR: Failed to load model: {e}")
        print("\nTroubleshooting:")
        print("1. Check internet connectivity")
        print("2. Try a different mirror: HF_ENDPOINT=https://huggingface.co python scripts/preload_models.py")
        print("3. Manually download and copy cache from local machine")
        sys.exit(1)


if __name__ == "__main__":
    main()
