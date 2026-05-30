import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

# ----------------------------
# Stock Selection
# ----------------------------

ticker = "RELIANCE.NS"

print(f"\nDownloading data for {ticker}...\n")

# ----------------------------
# Download Data
# ----------------------------

df = yf.download(
    ticker,
    start="2024-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# ----------------------------
# Fix MultiIndex Columns
# ----------------------------

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Keep required columns only
df = df[['Close', 'Volume']].copy()

# ----------------------------
# Volume Trend Analysis
# ----------------------------

df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()

# ----------------------------
# Z-Score Analysis
# ----------------------------

df['Volume_Zscore'] = zscore(df['Volume'])

# Detect spikes
df['Volume_Spike'] = df['Volume_Zscore'] > 2

# ----------------------------
# Percentage Change Analysis
# ----------------------------

df['Volume_Change_%'] = (
    (df['Volume'] - df['Volume_MA20'])
    / df['Volume_MA20']
) * 100

# ----------------------------
# Extract Spike Records
# ----------------------------

spikes = df[df['Volume_Spike']]

print("========== UNUSUAL VOLUME ACTIVITY ==========\n")

if len(spikes) > 0:
    print(
        spikes[
            ['Close',
             'Volume',
             'Volume_Zscore',
             'Volume_Change_%']
        ]
    )
else:
    print("No unusual volume spikes detected.")

print("\nTotal Spikes Detected:", len(spikes))

# ----------------------------
# Save Report
# ----------------------------

spikes.to_csv("volume_spikes_report.csv")

# ----------------------------
# Visualization
# ----------------------------

plt.figure(figsize=(14, 7))

plt.plot(
    df.index,
    df['Volume'],
    label='Daily Volume'
)

plt.plot(
    df.index,
    df['Volume_MA20'],
    label='20-Day Average Volume'
)

plt.scatter(
    spikes.index,
    spikes['Volume'],
    s=80,
    label='Volume Spike'
)

plt.title(f"{ticker} Volume Spike Detection")
plt.xlabel("Date")
plt.ylabel("Trading Volume")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig("volume_spike_chart.png")

plt.show()

print("\nFiles Generated Successfully")
print("1. volume_spikes_report.csv")
print("2. volume_spike_chart.png")
