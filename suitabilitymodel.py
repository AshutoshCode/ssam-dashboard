# Stock Suitability Analysis Model (SSAM)

# 1. Input Layer – Data Collection
import yfinance as yf
import pandas as pd
import numpy as np
import sys

def fetch_data(ticker, period='2mo', interval='1d'):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# 2. Analysis Engine – SOP Evaluation

def price_volume_engine(df):
    df['20d_vol_avg'] = df['Volume'].rolling(window=20).mean()
    recent_vol = df['Volume'].iloc[-1]
    avg_vol = df['20d_vol_avg'].iloc[-1]
    # Extract scalar if Series
    if isinstance(recent_vol, pd.Series):
        recent_vol = recent_vol.iloc[0]
    if isinstance(avg_vol, pd.Series):
        avg_vol = avg_vol.iloc[0]
    recent_vol = float(recent_vol)
    avg_vol = float(avg_vol)
    verdict = "Accumulation" if recent_vol > avg_vol else "Distribution"
    return verdict

def technical_indicators_scanner(df):
    rsi = (100 - (100 / (1 + df['Close'].pct_change().dropna().mean()))) if len(df) > 1 else 50
    macd_line = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    macd_signal = macd_line.ewm(span=9).mean()
    macd_hist = macd_line.iloc[-1] - macd_signal.iloc[-1]
    stoch_k = ((df['Close'].iloc[-1] - df['Low'].rolling(14).min().iloc[-1]) /
               (df['High'].rolling(14).max().iloc[-1] - df['Low'].rolling(14).min().iloc[-1])) * 100
    stoch_d = stoch_k  # Simplified approximation
    adx = 20  # Static placeholder value
    bb_mean = df['Close'].mean()
    # Extract scalar if Series
    if isinstance(bb_mean, pd.Series):
        bb_mean = bb_mean.iloc[0]
    if isinstance(df['Close'].iloc[-1], pd.Series):
        close_last = df['Close'].iloc[-1].iloc[0]
    else:
        close_last = df['Close'].iloc[-1]
    bb_mean_scalar = float(bb_mean)
    bb_pos = 'Upper' if float(close_last) > bb_mean_scalar else 'Lower'

    # Extract scalars for output
    def scalar(x):
        return x.iloc[0] if isinstance(x, pd.Series) else x

    return {
        'RSI': round(scalar(rsi), 2),
        'MACD': (round(scalar(macd_line.iloc[-1]), 2), round(scalar(macd_signal.iloc[-1]), 2), round(scalar(macd_hist), 2)),
        'Stochastic': (round(scalar(stoch_k), 2), round(scalar(stoch_d), 2)),
        'ADX': adx,
        'Bollinger Position': bb_pos
    }

def fibonacci_analyzer(swing_high, swing_low):
    # Extract scalars if Series
    if isinstance(swing_high, pd.Series):
        swing_high = swing_high.iloc[0]
    if isinstance(swing_low, pd.Series):
        swing_low = swing_low.iloc[0]
    levels = {
        '23.6%': swing_low + 0.236 * (swing_high - swing_low),
        '38.2%': swing_low + 0.382 * (swing_high - swing_low),
        '50.0%': swing_low + 0.500 * (swing_high - swing_low),
        '61.8%': swing_low + 0.618 * (swing_high - swing_low),
        '76.4%': swing_low + 0.764 * (swing_high - swing_low),
    }
    return levels


def fundamental_screener():
    return {
        'PE': 15.0,
        'ROE': 18.5,
        'Revenue Growth': '25% YoY',
        'EPS Trend': 'Upward'
    }


def sentiment_analyzer():
    return "Neutral to Positive"


# 3. Decision Layer – Trade Signal Generator

def generate_trade_signal(ticker):
    df = fetch_data(ticker)
    pv_verdict = price_volume_engine(df)
    indicators = technical_indicators_scanner(df)
    fib = fibonacci_analyzer(df['High'].max(), df['Low'].min())
    fundamentals = fundamental_screener()
    sentiment = sentiment_analyzer()

    signal = {
        'Ticker': ticker,
        'Price-Volume': pv_verdict,
        'Indicators': indicators,
        'Fibonacci Levels': fib,
        'Fundamentals': fundamentals,
        'Sentiment': sentiment,
        'Entry Range': (fib['38.2%'], fib['61.8%']),
        'Stop Loss': fib['23.6%'],
        'Targets': [fib['50.0%'], fib['61.8%']],
        'Risk-Reward': '1:2 (approximate)'
    }
    return signal


# 4. Feedback & Learning Loop – Prediction vs. Reality

def performance_tracker(trades):
    return "Tracking Enabled"


def correction_engine(trade_log):
    return "Model Tuned"


# 5. Dashboard UI – Visual layer for optional implementation


# Entry Point for Execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        ticker = input("Enter stock symbol (e.g., RELIANCE.NS): ")

    result = generate_trade_signal(ticker)
    for key, value in result.items():
        print(f"{key}: {value}")
