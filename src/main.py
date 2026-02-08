from transformers import pipeline
from news_scraper import fetch_stock_news
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import yfinance as yf
import os
from datetime import datetime
import pandas as pd

console = Console()

def save_to_history(ticker, score, verdict):
    """Menyimpan hasil analisis ke CSV untuk tracking historis."""
    os.makedirs("data", exist_ok=True)
    file_path = "data/sentiment_history.csv"
    new_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "ticker": [ticker],
        "score": [score],
        "verdict": [verdict]
    }
    df_new = pd.DataFrame(new_data)
    
    # Simpan ke CSV (Append jika file sudah ada)
    if not os.path.isfile(file_path):
        df_new.to_csv(file_path, index=False)
    else:
        df_new.to_csv(file_path, mode='a', header=False, index=False)
    
    rprint(f"[dim]📁 Analysis saved to {file_path}[/dim]")

def get_stock_price_info(ticker):
    """Mengambil harga saham terbaru dan perubahan harganya."""
    try:
        stock = yf.Ticker(ticker)
        # Ambil data 2 hari terakhir untuk hitung perubahan
        hist = stock.history(period="2d")
        if len(hist) < 2:
            return None
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        return {
            "price": current_price,
            "change": change,
            "change_pct": change_pct,
            "currency": stock.info.get('currency', 'USD')
        }
    except:
        return None

def run_sentiment_analysis(ticker):
    console.rule(f"[bold blue]📊 Financial Sentiment Dashboard: {ticker}[/bold blue]")
    
    # 0. Ambil Info Harga (Market Context)
    price_info = get_stock_price_info(ticker)
    if price_info:
        color = "green" if price_info['change'] >= 0 else "red"
        sign = "+" if price_info['change'] >= 0 else ""
        price_text = (
            f"Current Price: [bold]{price_info['price']:.2f} {price_info['currency']}[/bold] "
            f"([{color}]{sign}{price_info['change']:.2f} | {sign}{price_info['change_pct']:.2f}%[/{color}])"
        )
        console.print(Panel(price_text, title="📈 Market Context", border_style="white"))
    
    # 1. Ambil Berita
    with console.status("[bold green]🕵️♂️ Scrapping news data...") as status:
        headlines = fetch_stock_news(ticker)
    
    if not headlines:
        rprint(Panel(f"[bold red]⚠️ Data berita untuk {ticker} tidak ditemukan atau kosong.[/bold red]"))
        return

    # 2. Muat Model
    try:
        with console.status("[bold cyan]🤖 Initializing FinBERT Transformer...") as status:
            sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    except Exception as e:
        rprint(Panel(f"[bold red]❌ Error memuat model AI: {e}[/bold red]"))
        return
    
    # 3. Analisis & Tabel
    table = Table(title=f"Sentiment Results for {ticker}", show_header=True, header_style="bold magenta")
    table.add_column("Sentiment", justify="center", style="dim")
    table.add_column("Headline", style="white")
    table.add_column("Score", justify="right")

    results = []
    with console.status("[bold yellow]📖 Analyzing sentiment context...") as status:
        for h in headlines:
            try:
                pred = sentiment_pipeline(h['title'])[0]
                results.append(pred)
                
                # Warna berdasarkan label
                color = "green" if pred['label'] == 'positive' else "red" if pred['label'] == 'negative' else "yellow"
                table.add_row(
                    f"[{color}]{pred['label'].upper()}[/{color}]",
                    h['title'][:80] + "...",
                    f"{pred['score']:.2f}"
                )
            except Exception:
                continue

    console.print(table)

    # 4. Kalkulasi & Ringkasan
    pos = sum(1 for r in results if r['label'] == 'positive')
    neg = sum(1 for r in results if r['label'] == 'negative')
    total = len(results)
    score = (pos - neg) / total if total > 0 else 0
    
    # Verdict Styling
    if score > 0.2:
        verdict = "[bold green]🚀 BULLISH / POSITIVE[/bold green]"
    elif score < -0.2:
        verdict = "[bold red]📉 BEARISH / NEGATIVE[/bold red]"
    else:
        verdict = "[bold yellow]😐 NEUTRAL / SIDEWAYS[/bold yellow]"

    summary_panel = Panel(
        f"Positif: {pos} | Negatif: {neg} | Netral: {total - (pos + neg)}\n"
        f"Overall Sentiment Score: [bold cyan]{score:.2f}[/bold cyan]\n\n"
        f"Market Verdict: {verdict}",
        title="[bold]🏁 Analysis Summary[/bold]",
        border_style="bright_blue"
    )
    console.print(summary_panel)
    
    # 5. Simpan ke History
    verdict_clean = verdict.replace("[bold green]", "").replace("[/bold green]", "").replace("[bold red]", "").replace("[/bold red]", "").replace("[bold yellow]", "").replace("[/bold yellow]", "")
    save_to_history(ticker, score, verdict_clean)

if __name__ == "__main__":
    saham = console.input("[bold yellow]Masukkan kode saham (e.g. TSLA, BBCA.JK): [/bold yellow]").strip().upper()
    if not saham:
        saham = "TSLA"
    run_sentiment_analysis(saham)