import pandas as pd


COLUMN_MAPPING = {
    "时间": "raw_date",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "涨幅": "change_pct",
    "振幅": "amplitude",
    "总手": "volume",
    "金额": "amount",
    "换手%": "turnover",
    "成交次数": "trade_count"
}


def read_stock_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # 重命名字段
    df = df.rename(columns=COLUMN_MAPPING)

    # —— 1️⃣ 拆分日期列 ——
    date_split = df["raw_date"].astype(str).str.split(",", expand=True)
    df["date"] = pd.to_datetime(date_split[0])
    df["weekday"] = date_split[1]  # '一' '二' '三'

    # 清洗：确保数值类型
    for col in [
        "open", "high", "low", "close",
        "change_pct", "amplitude",
        "volume", "amount", "turnover", "trade_count"
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # —— 4️⃣ 按时间排序（非常重要） ——
    df = df.sort_values("date").reset_index(drop=True)

    return df
