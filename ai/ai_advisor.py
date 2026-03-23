from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("groq_llama-3.1-8b-instant"))


def generate_advice(metrics, category_summary, health_score):

    prompt = f"""
You are a personal finance advisor.

IMPORTANT RULES:
- Use ONLY the provided numbers
- Savings = Income - Expenses
- If savings > 0 → user is saving (NOT overspending)
- If savings < 0 → user is overspending
- Always format currency like ₹40,000
- Do NOT break numbers into characters

User financial data:

Income: ₹{int(metrics['income']):,}
Expenses: ₹{int(metrics['expense']):,}
Savings: ₹{int(metrics['savings']):,}
Cash Withdrawn: ₹{int(metrics['cash']):,}

Category Spending:
{category_summary}

Financial Health Score: {health_score}/100

Instructions:
- Talk like you are interacting with user directly not in third person perspective
- Clearly state if user is saving or overspending
- Mention strongest financial behavior (like savings rate or low expenses)
- Mention one area to improve
- Do NOT assume cash withdrawals are unnecessary, instead suggest better tracking
- Give 1–2 actionable suggestions
- Keep response short (4–5 lines max)
- No bullet points
- No symbols like *, -, etc.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        advice = response.choices[0].message.content.strip()

        # Clean formatting issues
        advice = advice.replace("\n", " ").replace("  ", " ")

    except Exception as e:
        print("AI ADVICE ERROR:", e)
        advice = "Unable to generate advice at the moment."

    return advice