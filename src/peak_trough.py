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


def find_min_trough_between(df, peak_idx, end_idx):
    """
    在 [peak_idx, end_idx) 区间内
    找最低收盘价
    """
    sub_df = df.iloc[peak_idx + 1 : end_idx]

    if sub_df.empty:
        return None, None

    trough_idx = sub_df["close"].idxmin()
    trough_price = df.loc[trough_idx]["close"]

    peak_price = df.iloc[peak_idx]["close"]
    drop_pct = (trough_price - peak_price) / peak_price

    return trough_idx, drop_pct
