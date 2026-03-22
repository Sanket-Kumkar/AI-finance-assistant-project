def clean_transactions(transactions):
    cleaned = []

    for t in transactions:
        desc = t["description"]

        if not desc or desc.strip() == "":
            continue

        desc = desc.lower().strip()

        t["description"] = desc

        cleaned.append(t)

    return cleaned