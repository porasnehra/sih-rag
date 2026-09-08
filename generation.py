import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

model_id = 'gemini-3.5-flash'
translate_model_id = 'gemini-3.5-flash'

def detect_and_translate(query):
    # Very simple check: if non-ascii, assume it might be Hindi or other and translate.
    # In a real app, use langdetect.
    if any(ord(c) > 127 for c in query):
        prompt = f"Translate the following text to English. Output ONLY the English translation.\n\nText: {query}"
        response = client.models.generate_content(model=translate_model_id, contents=prompt)
        return response.text.strip(), True
    return query, False

def translate_to_hindi(text):
    prompt = f"Translate the following English response to Hindi. Maintain the structure, JSON formatting, and IS numbers exactly.\n\nText: {text}"
    response = client.models.generate_content(model=translate_model_id, contents=prompt)
    return response.text.strip()

def generate_response(query, context_results, is_hindi=False):
    if not context_results:
        msg = "I'm sorry, I couldn't find any specific information regarding your query in the available BIS standards. Please visit the official BIS website or contact their support channels."
        if is_hindi:
            return translate_to_hindi(msg)
        return msg

    # Format context
    context_str = ""
    for idx, res in enumerate(context_results):
        meta = res['metadata']
        context_str += f"--- Source {idx+1} (IS Number: {meta['is_number']}) ---\n"
        context_str += f"Title: {meta['title']}\n"
        context_str += f"Scope: {meta['scope']}\n"
        context_str += f"Testing: {meta['testing_requirements']}\n"
        context_str += f"Certification: {meta['certification_scheme']}\n"
        context_str += f"URL: {meta['url']}\n\n"

    prompt = f"""
You are a helpful assistant for the Bureau of Indian Standards (BIS).
Answer the user's query ONLY using the provided context. 

If the context does not contain enough information to answer the query, state: "I'm sorry, the provided context is insufficient to answer your question. Please check the official BIS channels." Do NOT use your own parametric knowledge.

Your response MUST be in JSON format with two keys:
- "answer": Your detailed response to the query based on the context.
- "sources": A list of source URLs or IS Numbers that you used to form the answer.

Context:
{context_str}

User Query: "{query}"
"""
    
    response = client.models.generate_content(model=model_id, contents=prompt)
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        result = json.loads(text)
        
        # If the query was originally in Hindi, translate the answer part back
        if is_hindi:
            result['answer'] = translate_to_hindi(result['answer'])
            
        return result
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return {"answer": response.text, "sources": []}

if __name__ == "__main__":
    # Mock test
    mock_context = [{
        "score": 0.1,
        "metadata": {
            "is_number": "IS 2347:2017",
            "title": "Domestic Pressure Cookers",
            "scope": "Pressure cookers scope",
            "testing_requirements": "Bursting pressure",
            "certification_scheme": "ISI Mark",
            "url": "https://bis.gov.in"
        }
    }]
    print(generate_response("What is the standard for pressure cookers?", mock_context))
