import yfinance as yf
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def fetch_stock_news(ticker_symbol):
    print(f"🕵️♂️ Sedang mencari berita terbaru untuk: {ticker_symbol}...")
    stock = yf.Ticker(ticker_symbol)
    
    try:
        news_list = stock.news
    except Exception as e:
        print(f"❌ Error saat mengambil data: {e}")
        return []
    
    # Jika Yahoo kosong, kita beralih ke Google News RSS (Fallback)
    if not news_list:
        print(f"⚠️ Yahoo News kosong untuk {ticker_symbol}. Mencoba Google News...")
        return fetch_google_news(ticker_symbol)

    processed_news = []
    for item in news_list:
        # Masuk ke dalam key 'content'
        content = item.get('content', {})
        if not content: continue
        
        title = content.get('title')
        publisher = content.get('publisher')
        
        # Cara aman ambil link yang bersarang (nested)
        link_data = content.get('clickThroughUrl')
        link = link_data.get('url') if link_data else None
        
        if title:
            processed_news.append({
                "title": title,
                "publisher": publisher or "Yahoo Finance",
                "link": link
            })
    
    return processed_news

def fetch_google_news(ticker_symbol):
    """Fallback scraper menggunakan Google News RSS dengan auto-translation."""
    # Bersihkan simbol .JK untuk pencarian yang lebih baik
    query = ticker_symbol.replace(".JK", "")
    url = f"https://news.google.com/rss/search?q={query}+stock&hl=id&gl=ID&ceid=ID:id"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')  # Pakai parser XML
        items = soup.find_all('item')
        
        translator = GoogleTranslator(source='auto', target='en')
        google_news = []
        
        print(f"🌍 Auto-translating {min(len(items), 10)} news for better AI accuracy...")
        
        for item in items[:10]:  # Ambil 10 berita teratas
            original_title = item.title.text if item.title else None
            if not original_title:
                continue
                
            try:
                # Terjemahkan judul agar FinBERT memberikan skor yang akurat
                translated_title = translator.translate(original_title)
            except:
                translated_title = original_title
            
            source = item.source.text if item.source else "Google News"
            link = item.link.text if item.link else None
            
            google_news.append({
                "title": translated_title,
                "original_title": original_title,
                "publisher": source,
                "link": link
            })
        
        if google_news:
            print(f"✅ Berhasil mengambil {len(google_news)} berita dari Google News.")
        return google_news
    except Exception as e:
        print(f"❌ Gagal mengambil berita dari Google: {e}")
        return []

if __name__ == "__main__":
    symbol = "TSLA" 
    berita = fetch_stock_news(symbol)
    
    print(f"\n✅ Berhasil menangkap {len(berita)} berita:")
    for i, n in enumerate(berita[:5], 1): 
        # Pakai default value jika publisher atau title None
        t = n['title'] or "No Title"
        p = n['publisher'] or "Unknown Publisher"
        print(f"{i}. {t} | [{p}]")
