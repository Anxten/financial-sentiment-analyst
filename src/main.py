from transformers import pipeline
from news_scraper import fetch_stock_news
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

def run_sentiment_analysis(ticker):
    console.rule(f"[bold blue]📊 Financial Sentiment Dashboard: {ticker}[/bold blue]")
    
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

if __name__ == "__main__":
    saham = console.input("[bold yellow]Masukkan kode saham (e.g. TSLA, BBCA.JK): [/bold yellow]").strip().upper()
    if not saham:
        saham = "TSLA"
    run_sentiment_analysis(saham)