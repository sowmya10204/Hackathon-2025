# services/llm_rewriter.py
from transformers import pipeline

# Load once
generator = pipeline("text-generation", model="gpt2")

def rewrite_text(original_text: str, tone: str) -> str:
    prompt = f"Rewrite the following text in a {tone} tone while keeping the meaning the same:\n\n{original_text}\n\nRewritten:"
    result = generator(prompt, max_length=300, num_return_sequences=1, temperature=0.7)
    rewritten = result[0]["generated_text"]

    # Clean extra prompt artifacts
    if "Rewritten:" in rewritten:
        rewritten = rewritten.split("Rewritten:")[-1].strip()

    return rewritten
