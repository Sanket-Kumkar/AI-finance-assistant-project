import pdfplumber


def parse_hdfc(file):

    transactions = []

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                # Skip small/invalid tables
                if len(table) < 2:
                    continue

                headers = table[0]

                # Check if this is transaction table
                if "Date" not in headers:
                    continue

                for row in table[1:]:

                    try:
                        date = row[0]
                        narration = row[1]
                        withdrawal = row[4]
                        deposit = row[5]

                        # Clean values
                        narration = narration.replace("\n", " ").lower() if narration else ""

                        amount = 0

                        if deposit and deposit.strip():
                            amount = float(deposit.replace(",", ""))
                        elif withdrawal and withdrawal.strip():
                            amount = -float(withdrawal.replace(",", ""))

                        transactions.append({
                            "date": date,
                            "description": narration,
                            "amount": amount
                        })

                    except:
                        continue

    return transactions