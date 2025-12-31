from peak_trough import find_peaks, find_trough_after_peak


def analyze_stock(df,
                  window=5,
                  min_drop=0.03,
                  max_buy_drop=0.10):

    peaks = find_peaks(df, window)
    if not peaks:
        return {"status": "无阶段性高点"}

    latest_peak = peaks[-1]
    peak_price = df.iloc[latest_peak]["close"]

    trough_idx, trough_drop = find_trough_after_peak(
        df, latest_peak, window, min_drop
    )

    current_price = df.iloc[-1]["close"]
    current_drop = (current_price - peak_price) / peak_price

    result = {
        "peak_index": latest_peak,
        "peak_price": peak_price,
        "current_price": current_price,
        "current_drop_pct": round(current_drop * 100, 2)
    }

    if trough_idx:
        result["confirmed_trough_index"] = trough_idx
        result["confirmed_drop_pct"] = round(trough_drop * 100, 2)

    if current_drop >= -min_drop:
        result["stage"] = "尚未形成有效下跌"
    elif current_drop <= -max_buy_drop:
        result["stage"] = "下跌过深，超出买入阈值"
    else:
        result["stage"] = "处于可关注买入区间"

    return result
