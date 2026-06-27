import json
from datetime import datetime, timedelta
from pykrx import stock

def date_str(d):
    return d.strftime('%Y/%m/%d')

def main():
    today = datetime.now()
    from_dt = today - timedelta(days=366)

    fromdate = from_dt.strftime('%Y%m%d')
    todate = today.strftime('%Y%m%d')

    print(f"Fetching KODEX 200 (069500): {fromdate} ~ {todate}")
    df = stock.get_market_ohlcv_by_date(fromdate, todate, "069500")

    if df.empty:
        print("No data received!")
        return

    df = df.reset_index()

    records = []
    prev_close = None

    for _, row in df.iterrows():
        c = int(row['종가'])
        chg = (c - prev_close) if prev_close is not None else 0
        records.append({
            'd': row['날짜'].strftime('%Y/%m/%d'),
            'o': int(row['시가']),
            'h': int(row['고가']),
            'l': int(row['저가']),
            'c': c,
            'chg': chg,
            'rt': round(float(row['등락률']), 2),
            'vol': int(row['거래량'])
        })
        prev_close = c

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Saved {len(records)} records | {records[0]['d']} ~ {records[-1]['d']}")

if __name__ == '__main__':
    main()
