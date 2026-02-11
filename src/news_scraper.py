import yfinance as yf
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def fetch_stock_news(ticker_symbol):
    """Entry point utama untuk scraping berita."""
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
    """Smarter RSS Scraper for Global (TSLA) and Local (BBCA.JK) stocks."""
    clean_ticker = ticker_symbol.replace(".JK", "")
    
    # Penentuan keyword berdasarkan market
    is_idx = ".JK" in ticker_symbol
    query = f"{clean_ticker}+saham" if is_idx else f"{clean_ticker}+stock"
    
    # Gunakan hl=en untuk saham US agar berita yang didapat lebih relevan
    hl = "id" if is_idx else "en"
    gl = "ID" if is_idx else "US"
    ceid = "ID:id" if is_idx else "US:en"
    
    url = f"https://news.google.com/rss/search?q={query}&hl={hl}&gl={gl}&ceid={ceid}"
    
    # WAJIB: Identitas agar tidak diblokir Google
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')  # Pakai parser XML
        items = soup.find_all('item')
        
        if not items:
            print(f"⚠️ Tidak ada berita ditemukan untuk {ticker_symbol}")
            return []

        translator = GoogleTranslator(source='auto', target='en')
        google_news = []
        
        print(f"🌍 Auto-translating {min(len(items), 10)} news for better AI accuracy...")
        
        for item in items[:10]:  # Ambil 10 berita teratas
            original_title = item.title.text if item.title else None
            if not original_title:
                continue
                
            try:
                # TSLA (en) tidak akan diterjemahkan ulang, BBCA (id) akan diterjemahkan
                translated_title = translator.translate(original_title) if is_idx else original_title
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
