import streamlit as st
import pandas as pd
from news_scraper import fetch_stock_news
import yfinance as yf
import os
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="AI Financial Analyst", page_icon="📈", layout="wide")

# 2. Cache Model (Agar tidak download/load ulang setiap klik)
@st.cache_resource
def load_model():
    # Model baru di-load saat dibutuhkan saja (Lazy Loading)
    from transformers import pipeline
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

# 3. Fungsi Helper Harga
def get_price_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if len(hist) < 2: return None
        curr = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        return curr, curr - prev, (curr - prev) / prev * 100
    except:
        return None

# 4. Fungsi Save Log
def save_log(ticker, score, verdict):
    """Menyimpan hasil analisis ke CSV untuk tracking historis."""
    log_path = "data/sentiment_history.csv"
    os.makedirs("data", exist_ok=True)
    
    new_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "ticker": [ticker],
        "score": [round(score, 2)],
        "verdict": [verdict]
    }
    df_new = pd.DataFrame(new_data)
    
    # Simpan ke CSV (Append jika file sudah ada)
    if not os.path.isfile(log_path):
        df_new.to_csv(log_path, index=False)
    else:
        df_new.to_csv(log_path, mode='a', header=False, index=False)
    
    return log_path

# --- INITIALIZE SESSION STATE ---
if 'last_analysis' not in st.session_state:
    st.session_state['last_analysis'] = None

# --- UI SIDEBAR ---
st.sidebar.title("🚀 AI Analyst Settings")
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="TSLA").upper()
analyze_btn = st.sidebar.button("Analyze Sentiment")

# --- UI MAIN CONTENT ---
st.title("🤖 The Intelligent Financial Sentiment Analyst")
st.markdown(f"Current Target: **{ticker}**")

if analyze_btn:
    # Row 1: Market Metrics
    price_data = get_price_data(ticker)
    if price_data:
        curr, diff, pct = price_data
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"{curr:.2f}", f"{diff:.2f}")
        col2.metric("Change (%)", f"{pct:.2f}%", f"{diff:.2f}")
        col3.write("")  # Spacer

    # Row 2: Analysis Process
    with st.spinner(f"Fetching news and analyzing {ticker}..."):
        # Load AI
        model = load_model()
        # Fetch News
        headlines = fetch_stock_news(ticker)
        
        if headlines:
            results = []
            for h in headlines:
                try:
                    pred = model(h['title'])[0]
                    results.append({
                        "Sentiment": pred['label'].upper(),
                        "Score": round(pred['score'], 2),
                        "Headline": h['title'],
                        "Source": h['publisher']
                    })
                except:
                    continue
            
            if results:
                df = pd.DataFrame(results)

                # Dashboard Summary
                pos = len(df[df['Sentiment'] == 'POSITIVE'])
                neg = len(df[df['Sentiment'] == 'NEGATIVE'])
                score = (pos - neg) / len(df) if len(df) > 0 else 0
                
                # Generate verdict text
                if score > 0.2:
                    verdict = "🚀 BULLISH / POSITIVE"
                elif score < -0.2:
                    verdict = "📉 BEARISH / NEGATIVE"
                else:
                    verdict = "😐 NEUTRAL / SIDEWAYS"

                # SIMPAN KE SESSION STATE (Agar tidak hilang saat rerun)
                st.session_state['last_analysis'] = {
                    "ticker": ticker,
                    "score": score,
                    "df": df,
                    "pos": pos,
                    "neg": neg,
                    "verdict": verdict
                }
                
                # Simpan ke CSV HANYA SEKALI saat tombol diklik
                save_log(ticker, score, verdict)
                st.success("✅ Analysis saved to history!")
            else:
                st.error("Failed to analyze news headlines.")
        else:
            st.error("No news found for this ticker.")

# TAMPILKAN HASIL DARI SESSION STATE
if 'last_analysis' in st.session_state:
    data = st.session_state['last_analysis']
    st.write(f"### Results for {data['ticker']}")
    
    # Display Verdict
    if data['score'] > 0.2: 
        st.success(f"Market Verdict: **BULLISH** (Score: {data['score']:.2f})")
    elif data['score'] < -0.2: 
        st.error(f"Market Verdict: **BEARISH** (Score: {data['score']:.2f})")
    else: 
        st.warning(f"Market Verdict: **NEUTRAL** (Score: {data['score']:.2f})")

    # Show Table
    st.dataframe(data['df'], use_container_width=True)

# TOMBOL DOWNLOAD (Selalu ada di sidebar jika data tersedia)
if os.path.exists("data/sentiment_history.csv"):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Export Data")
    with open("data/sentiment_history.csv", "rb") as f:
        st.sidebar.download_button(
            label="📥 Download History CSV",
            data=f,
            file_name="sentiment_history.csv",
            mime="text/csv"
        )
