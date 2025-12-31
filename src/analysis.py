from peak_trough import find_peaks, find_trough_after_peak


def analyze_stock(df,
                  window=5,
                  min_drop=0.03,
                  max_buy_drop=0.10):

    peaks = find_peaks(df, window)
    if not peaks:
        return {"status": "无阶段性高点"}

    latest_peak = peaks[-1]
    peak_row = df.iloc[latest_peak]
    peak_price = peak_row["close"]
    peak_date = peak_row["date"]

    trough_idx, trough_drop = find_trough_after_peak(
        df, latest_peak, window, min_drop
    )

    current_row = df.iloc[-1]
    current_price = current_row["close"]
    current_date = current_row["date"]
    current_drop = (current_price - peak_price) / peak_price

    result = {
        "peak_date": peak_date.strftime("%Y-%m-%d"),
        "peak_price": round(peak_price, 2),
        "current_date": current_date.strftime("%Y-%m-%d"),
        "current_price": round(current_price, 2),
        "current_drop_pct": round(current_drop * 100, 2)
    }

    if trough_idx is not None:
        trough_row = df.iloc[trough_idx]
        result.update({
            "trough_date": trough_row["date"].strftime("%Y-%m-%d"),
            "trough_price": round(trough_row["close"], 2),
            "trough_drop_pct": round(trough_drop * 100, 2)
        })

    if current_drop >= -min_drop:
        result["stage"] = "尚未形成有效下跌"
    elif current_drop <= -max_buy_drop:
        result["stage"] = "下跌过深，超出买入阈值"
    else:
        result["stage"] = "处于可关注买入区间"

    return result
