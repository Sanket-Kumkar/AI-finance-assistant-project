import pandas as pd


def parse_csv(file):
    try:
        df = pd.read_excel(file)
    except:
        df = pd.read_csv(file)

    # Clean column names
    df.columns = [col.strip().lower().replace(".", "") for col in df.columns]

    # Standard column mapping
    column_map = {
        "date": "date",
        "narration": "description",
        "withdrawal amt": "debit",
        "deposit amt": "credit",
        "closing balance": "balance"
    }

    df = df.rename(columns=column_map)

    transactions = []

    for _, row in df.iterrows():

        debit = row.get("debit")
        credit = row.get("credit")

        if pd.notna(debit) and debit != 0:
            amount = -float(debit)
            t_type = "debit"
        elif pd.notna(credit) and credit != 0:
            amount = float(credit)
            t_type = "credit"
        else:
            continue

        transactions.append({
            "date": row.get("date"),
            "description": str(row.get("description", "")).strip(),
            "amount": amount,
            "type": t_type,
            "balance": float(row.get("balance", 0)) if pd.notna(row.get("balance")) else 0,
            "category": None
        })

    return transactions