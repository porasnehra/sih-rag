import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

model_id = 'gemini-3.5-flash'

def analyze_query(query):
    prompt = f"""
You are an intent classification and entity extraction assistant for a Bureau of Indian Standards (BIS) search system.

Classify the user query into one of the following intents:
- 'product_to_standard': Asking for the IS standard for a specific product.
- 'certification': Asking about certification schemes, ISI mark, or compulsory registration.
- 'lab_query': Asking about testing requirements or laboratory information.
- 'hallmarking': Asking about gold/silver hallmarking.
- 'general': Any other question about BIS.

Also, extract the 'product_category' or 'product_name' if mentioned in the query.

User Query: "{query}"

Return the result as a valid JSON object with the keys 'intent' and 'product_entity'. If no product is found, set 'product_entity' to null.
Do not wrap the JSON in markdown blocks (like ```json), just output the raw JSON string.
"""
    response = client.models.generate_content(
        model=model_id,
        contents=prompt
    )
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        result = json.loads(text)
        return result
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {"intent": "general", "product_entity": None}

if __name__ == "__main__":
    test_queries = [
        "What is the IS standard for pressure cookers?",
        "Where can I test my electric kettle?",
        "What are the rules for gold hallmarking?"
    ]
    for q in test_queries:
        print(f"Query: {q}")
        print(analyze_query(q))
        print("-" * 20)
