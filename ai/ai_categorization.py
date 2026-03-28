from groq import Groq
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):
    """
    Extract JSON array safely from AI response
    """
    match = re.search(r"\[.*?\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None


def categorize_transactions(transactions):

    descriptions = [t["description"] for t in transactions]

    prompt = f"""
Return ONLY a JSON array.

Each transaction must be classified into ONE of:
Food, Transport, Shopping, Utilities, Entertainment, Subscription, Transfer, Cash Withdrawal, Income, Other

Transactions:
{chr(10).join(descriptions)}

STRICT RULES:
- Output must be JSON array
- No explanation
- No code
- No markdown
- No text

Example:
["Food", "Transport", "Income"]
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        print("RAW RESPONSE:", text)

        categories = extract_json(text)

        if not categories or len(categories) != len(transactions):
            raise ValueError("Invalid AI output")

    except Exception as e:
        print("AI ERROR:", e)
        categories = ["Other"] * len(transactions)

    # 🔥 FINAL RULE-BASED CONTROL (CRITICAL)
    for i in range(len(transactions)):

        desc = transactions[i]["description"]
        amount = transactions[i]["amount"]
        ai_category = categories[i].lower()

        # Normalize description
        desc_lower = desc.lower()

        # 1. Income
        if amount > 0:
            transactions[i]["category"] = "Income"
            continue

        # 2. Cash withdrawal
        if "atm" in desc_lower:
            transactions[i]["category"] = "Cash Withdrawal"
            continue

        # 🔥 3. EMI / Loan detection
        if "emi" in desc_lower or "loan" in desc_lower:
            transactions[i]["category"] = "Loan Repayment"
            continue

        # 🔥 4. Food detection
        if "swiggy" in desc_lower or "zomato" in desc_lower:
            transactions[i]["category"] = "Food"
            continue

        # 🔥 5. Shopping
        if "amazon" in desc_lower or "flipkart" in desc_lower:
            transactions[i]["category"] = "Shopping"
            continue

        # 🔥 6. Transport
        if "petrol" in desc_lower or "fuel" in desc_lower:
            transactions[i]["category"] = "Transport"
            continue

        # 7. Prevent wrong AI classification
        if ai_category == "income":
            transactions[i]["category"] = "Other"
            continue

        # 8. AI fallback
        transactions[i]["category"] = categories[i]

    return transactions
