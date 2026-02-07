from transformers import pipeline

def test_finbert():
    print("Memuat model FinBERT... (Mungkin agak lama di awal)")
    # Memilih model ProsusAI/finbert yang sudah spesifik untuk keuangan
    nlp = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    
    result = nlp("Bank Central Asia reports 15% profit growth in Q4.")
    print(f"\nHasil Test: {result}")

if __name__ == "__main__":
    test_finbert()