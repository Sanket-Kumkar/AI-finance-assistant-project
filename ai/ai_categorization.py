from groq import Groq
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("groq_llama-3.1-8b-instant"))


def extract_json(text):
    # extract JSON array safely
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

    for i in range(len(transactions)):
        transactions[i]["category"] = categories[i]

    return transactions