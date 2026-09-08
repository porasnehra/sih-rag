import os
from dotenv import load_dotenv
from query_understanding import analyze_query
from vector_store import search_vectors
from generation import detect_and_translate, generate_response

# Load environment variables
load_dotenv()

def bis_rag_pipeline(user_query):
    print(f"\n--- Processing Query: '{user_query}' ---")
    
    # Step 1: Multilingual Check (Translate Hindi to English if needed)
    english_query, is_hindi = detect_and_translate(user_query)
    if is_hindi:
        print(f"[Phase 5] Translated Query: {english_query}")

    # Step 2: Query Understanding (Intent & Entity Extraction)
    print("[Phase 3] Analyzing intent and extracting entities...")
    analysis = analyze_query(english_query)
    intent = analysis.get("intent", "general")
    product = analysis.get("product_entity")
    print(f"  -> Intent: {intent}")
    print(f"  -> Extracted Entity: {product}")
    
    # Uncertainty Guardrail: If intent is completely unrecognised or irrelevant
    # For a real system we could have a strict check here, but we will rely on retrieval score
    
    # Note: We pass the english_query for better semantic matching
    results = search_vectors(english_query, k=3)
    
    print(f"  -> Retrieved {len(results)} chunks.")
    for res in results:
        print(f"     - Score: {res['score']:.4f} | IS: {res['metadata']['is_number']}")
        
    # Guardrail: Check retrieval score. FAISS L2 distance: lower is better.
    # Set a threshold for L2 distance (needs tuning based on actual embeddings)
    THRESHOLD = 1.0 # This threshold is arbitrary and should be tuned.
    valid_results = [r for r in results if r['score'] < THRESHOLD]
    
    if not valid_results and results:
        print("[Phase 4 Guardrail] Retrieval scores too high (low similarity). Falling back.")
        valid_results = [] # Force fallback
    
    # Step 4: Generation with Grounding
    print("[Phase 4] Generating grounded response...")
    final_output = generate_response(english_query, valid_results, is_hindi=is_hindi)
    
    print("\n--- FINAL RESPONSE ---")
    if isinstance(final_output, dict):
        print(final_output.get("answer", final_output))
        if final_output.get("sources"):
            print("\nSources Cited:")
            for s in final_output.get("sources"):
                print(f"- {s}")
    else:
        print(final_output)
            
    return final_output

if __name__ == "__main__":
    print("Welcome to the BIS Standards AI Assistant.")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            q = input("\nEnter your query: ")
            if q.lower() in ['exit', 'quit']:
                break
            if not q.strip():
                continue
            bis_rag_pipeline(q)
        except EOFError:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
