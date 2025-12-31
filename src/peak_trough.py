def find_peaks(df, window=5):
    prices = df["close"].values
    peaks = []

    for i in range(window, len(prices) - window):
        if prices[i] == max(prices[i-window:i+window+1]):
            peaks.append(i)

    return peaks


def find_trough_after_peak(df, peak_idx, window=5, min_drop=0.03):
    prices = df["close"].values
    peak_price = prices[peak_idx]

    for i in range(peak_idx + window, len(prices) - window):
        price = prices[i]

        if price >= peak_price:
            continue

        if price == min(prices[i-window:i+window+1]):
            drop_pct = (price - peak_price) / peak_price
            if drop_pct <= -min_drop:
                return i, drop_pct

    return None, None
