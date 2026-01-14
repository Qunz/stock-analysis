from peak_trough import find_peaks, find_trough_after_peak, find_min_trough_between
import pandas as pd


def analyze_all_peaks(df):
    results = []

    peaks = find_peaks(df)

    for i, peak_idx in enumerate(peaks):
        peak_row = df.iloc[peak_idx]
        peak_price = peak_row["close"]
        peak_date = peak_row["date"]

        if i < len(peaks) - 1:
            end_idx = peaks[i + 1]

            next_peak_idx = peaks[i + 1]
            next_peak_row = df.iloc[next_peak_idx]
            next_peak_price = next_peak_row["close"]
            next_peak_date = next_peak_row["date"]
        else:
            end_idx = len(df)

            next_peak_idx = None
            next_peak_price = None
            next_peak_date = None

        trough_idx, drop_pct = find_min_trough_between(
            df, peak_idx, end_idx
        )

        # ===> 这一段会代码会导致部分峰值没有对应的谷值
        # if trough_idx is None:
        #     continue

        # trough_row = df.loc[trough_idx]
        # <===

        if trough_idx is None:
            # 没有谷值
            results.append({
                "峰值日期": peak_date,
                "峰值价格": round(peak_price, 2),
                "谷值日期": None,
                "谷值价格": None,
                "最大跌幅%": None,
                "跌幅>=3%": False,
                "下一个峰值日期": next_peak_date,
                "谷值到下个峰值涨幅%": None,
                "状态": f"无有效谷值"
            })
        else:
            trough_row = df.loc[trough_idx]
            trough_price = trough_row["close"]

            # 计算 谷值 → 下一个峰值 的涨幅
            if next_peak_price is not None:
                rise_pct = (next_peak_price - trough_price) / trough_price
                rise_pct = round(rise_pct * 100, 2)
            else:
                rise_pct = None

            results.append({
                "峰值日期": peak_date,
                "峰值价格": round(peak_price, 2),
                "谷值日期": trough_row["date"],
                "谷值价格": round(trough_row["close"], 2),
                "最大跌幅%": round(drop_pct * 100, 2),
                "跌幅>=3%": drop_pct <= -0.03,
                "下一个峰值日期": next_peak_date,
                "谷值到下个峰值涨幅%": rise_pct,
                "状态": "有效回撤"
            })

    return pd.DataFrame(results)


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
