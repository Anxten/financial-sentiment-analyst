---
title: Financial Sentiment Analyst
emoji: 📈
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: src/app.py
pinned: false
license: mit
---

# 🤖 The Intelligent Financial Sentiment Analyst

[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces/Anxten/financial-sentiment-analyst)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AI](https://img.shields.io/badge/AI-Transformers-orange.svg)
![Status](https://img.shields.io/badge/Status-Live_Dashboard-green.svg)

A robust, end-to-end financial sentiment analysis system that bridges the gap between raw financial news and investment intelligence. Developed with a focus on robustness and real-time data accuracy.

## 🔗 Live Demo
You can try the live version of this AI Analyst without any installation here:  
👉 **[Launch App on Hugging Face Spaces](https://huggingface.co/spaces/Anxten/financial-sentiment-analyst)**

## 🚀 Key Features
* **Hybrid News Scraper:** Dual-layer scraping using Yahoo Finance API with an automatic failover to Google News RSS for regional tickers (e.g., IDX).
* **FinBERT Intelligence:** Utilizes the `ProsusAI/finbert` transformer model, specialized for financial context.
* **Market Context Integration:** Real-time price tracking and daily price change percentage.
* **Professional Dashboard:** Built with Streamlit for a clean, interactive user experience.
* **Historical Logging:** Automated data persistence in CSV format for trend analysis.

## 🧠 The Math Behind the Sentiment
The overall sentiment score is calculated using the following logic:

$$\text{Sentiment Score} = \frac{\text{Positive} - \text{Negative}}{\text{Total}}$$

* **Score > 0.2**: Bullish (Optimistic)
* **Score < -0.2**: Bearish (Pessimistic)
* **Otherwise**: Neutral (Wait and See)

## 🛠️ Tech Stack
- **Model:** FinBERT (ProsusAI/finbert)
- **Architecture:** Transformer (Encoder-only)
- **Frameworks:** PyTorch, Transformers, Streamlit
- **Data Sources:** Yahoo Finance API, Google News RSS
- **Environment:** Fedora Linux | VS Code

## 📦 Installation & Setup

Follow these steps to get the analyst running on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Anxten/financial-sentiment-analyst.git
cd financial-sentiment-analyst
```

### 2. Set Up Virtual Environment

It's highly recommended to use a virtual environment to keep dependencies isolated.

**For Linux (Fedora/Ubuntu) & MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application

**CLI Version (Terminal):**
```bash
python src/main.py
```

**Web Dashboard (Browser):**
```bash
streamlit run src/app.py
```

## 📊 Project Structure
```
financial-sentiment-analyst/
├── src/
│   ├── main.py           # CLI version with Rich terminal UI
│   ├── app.py            # Streamlit web dashboard
│   └── news_scraper.py   # Hybrid news scraping module
├── data/
│   └── sentiment_history.csv  # Historical analysis logs
├── requirements.txt
└── README.md
```

## 🎯 Use Cases
- **Retail Investors:** Quick sentiment check before making trading decisions
- **Financial Analysts:** Automated news monitoring for multiple tickers
- **Research:** Historical sentiment data collection for backtesting strategies

## 🔮 Future Enhancements
- [ ] Multi-language sentiment support (Bahasa Indonesia)
- [ ] Integration with technical indicators (RSI, MACD)
- [ ] Real-time alert system via Telegram/Discord
- [ ] Sentiment-price correlation visualization

## 📝 License
This project is open-source and available under the MIT License.

---

**Developed by Allan Bendatu**  
*Informatics Student & Calculus Teaching Assistant*  
*Bridging Mathematics, AI, and Financial Markets*
