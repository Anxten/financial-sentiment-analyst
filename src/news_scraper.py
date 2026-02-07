import yfinance as yf

def fetch_stock_news(ticker_symbol):
    print(f"🕵️‍♂️ Sedang mencari berita terbaru untuk: {ticker_symbol}...")
    stock = yf.Ticker(ticker_symbol)
    
    try:
        news_list = stock.news
    except Exception as e:
        print(f"❌ Error saat mengambil data: {e}")
        return []
    
    if not news_list:
        print("⚠️ Tidak ada berita ditemukan.")
        return []

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
                "publisher": publisher,
                "link": link
            })
    
    return processed_news

if __name__ == "__main__":
    symbol = "TSLA" 
    berita = fetch_stock_news(symbol)
    
    print(f"\n✅ Berhasil menangkap {len(berita)} berita:")
    for i, n in enumerate(berita[:5], 1): 
        # Pakai default value jika publisher atau title None
        t = n['title'] or "No Title"
        p = n['publisher'] or "Unknown Publisher"
        print(f"{i}. {t} | [{p}]")