import os

import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def build_prompt(context_text, input_text):
    schema = """
You have access to the following tables:

1. distribution_centers.csv
- id, name, latitude, longitude

2. inventory_items.csv
- id, product_id, created_at, sold_at, cost, product_category, product_name, product_brand, product_retail_price, product_department, product_sku, product_distribution_center_id

3. order_items.csv
- id, order_id, user_id, product_id, inventory_item_id, status, created_at, shipped_at, delivered_at, returned_at

4. orders.csv
- order_id, user_id, status, gender, created_at, returned_at, shipped_at, delivered_at, num_of_item

5. products.csv
- id, cost, category, name, brand, retail_price, department, sku, distribution_center_id

6. users.csv
- id, first_name, last_name, email, age, gender, state, street_address, postal_code, city, country, latitude, longitude, traffic_source, created_at
"""

    instructions = """
As a helpful assistant, your task is to:
1. Understand the user’s query and determine which table(s) it relates to.
2. If the query is ambiguous (e.g., "Where is my order?" or "Show me electronics"), ask follow-up questions to get more context such as:
   - Date range
   - Specific product/category/brand
   - User identification
   - Order status or location
3. Once you have enough context, return a clear natural language summary of what will be queried.
4. Output should always be concise, structured, and ask for missing details if needed.
"""

    prompt = f"""{schema}
{instructions}

Conversation history:
{context_text}

User: {input_text}
Assistant:"""

    return prompt


def get_llm_response(user_input, context=None, model="llama3-70b-8192"):
    """
    Sends a prompt to the Groq LLM API and returns the response.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if context:
        messages.append({"role": "system", "content": context})
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error contacting LLM API: {str(e)}"
