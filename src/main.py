from reader import read_stock_excel
from analysis import analyze_stock
from pathlib import Path

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    df = read_stock_excel(BASE_DIR / "data/兴业银锡-000426.xlsx")

    result = analyze_stock(
        df,
        window=5,
        min_drop=0.03,
        max_buy_drop=0.10
    )

    print("分析结果：")
    for k, v in result.items():
        print(f"{k}: {v}")
