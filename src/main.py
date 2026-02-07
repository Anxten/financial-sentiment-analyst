from transformers import pipeline
from news_scraper import fetch_stock_news

def run_sentiment_analysis(ticker):
    print(f"\n--- 📊 Memulai Analisis Sentimen untuk: {ticker} ---")
    
    # 1. Ambil Berita
    headlines = fetch_stock_news(ticker)
    if not headlines:
        print(f"⚠️ Tidak dapat melanjutkan analisis untuk {ticker} karena data berita kosong.")
        return

    # 2. Muat Model FinBERT dengan Error Handling
    try:
        print("🤖 Memuat AI FinBERT...")
        sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    except Exception as e:
        print(f"❌ Error memuat model AI: {e}")
        return
    
    # 3. Analisis per Judul
    results = []
    print(f"📖 Menganalisis {len(headlines)} berita...\n")
    
    for h in headlines:
        try:
            prediction = sentiment_pipeline(h['title'])[0]
            results.append(prediction)
            print(f"[{prediction['label'].upper()}] - {h['title'][:70]}...")
        except Exception as e:
            print(f"⚠️ Gagal menganalisis judul: {h['title'][:30]}... | Error: {e}")

    # 4. Kalkulasi Skor Akhir
    pos_count = sum(1 for r in results if r['label'] == 'positive')
    neg_count = sum(1 for r in results if r['label'] == 'negative')
    
    total = len(results)
    sentiment_score = (pos_count - neg_count) / total if total > 0 else 0
    
    print(f"\n--- 🏁 KESIMPULAN ANALISIS ---")
    print(f"Positif: {pos_count} | Negatif: {neg_count} | Netral: {total - (pos_count + neg_count)}")
    print(f"Overall Sentiment Score: {sentiment_score:.2f} (-1 sangat Bearish, +1 sangat Bullish)")
    
    if sentiment_score > 0.2:
        print("🚀 Verdict: SENTIMEN POSITIF. Pasar terlihat optimis.")
    elif sentiment_score < -0.2:
        print("📉 Verdict: SENTIMEN NEGATIF. Hati-hati, pasar sedang pesimis.")
    else:
        print("😐 Verdict: SENTIMEN NETRAL. Pasar sedang menunggu kepastian.")

if __name__ == "__main__":
    saham = input("Masukkan kode saham (contoh: TSLA atau BBCA.JK): ").strip().upper()
    if not saham:
        saham = "TSLA"
        print(f"⚠️ Input kosong. Menggunakan default: {saham}")
    
    run_sentiment_analysis(saham)