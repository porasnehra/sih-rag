import os
from dotenv import load_dotenv
import pandas as pd
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from vector_store import search_vectors
from generation import generate_response

load_dotenv()

def run_evaluation():
    print("Preparing Evaluation Dataset...")
    
    # 5 Sample Test Questions
    eval_questions = [
        "What is the standard for pressure cookers?",
        "Do I need an ISI mark for electric kettles?",
        "What is the standard for alumino-ferric?",
        "Tell me about hallmarking of gold jewellery.",
        "What are the testing requirements for safety footwear?"
    ]
    
    # Ground truth answers (optional for faithfulness/relevancy, but good for context)
    ground_truths = [
        "IS 2347:2017",
        "Yes, electric kettles (IS 302-2-15) require an ISI mark under Scheme I.",
        "IS 299:2012 is the standard for alumino-ferric.",
        "IS 14625:2015 provides guidelines for hallmarking gold.",
        "Testing includes impact resistance of toe cap and slip resistance (IS 15298-2:2016)."
    ]
    
    answers = []
    contexts = []
    
    # Run our RAG pipeline for each question to gather answers and context
    for q in eval_questions:
        print(f"Evaluating query: {q}")
        results = search_vectors(q, k=2)
        
        # Extract text context
        ctx = []
        for r in results:
            meta = r['metadata']
            ctx.append(f"{meta['title']} ({meta['is_number']}): {meta['scope']}")
        contexts.append(ctx)
        
        # Generate response
        response = generate_response(q, results)
        answers.append(response.get('answer', str(response)))

    # Create dataset for Ragas
    data = {
        "question": eval_questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    print("\nRunning Ragas Evaluation...")
    
    # Setup Langchain models for Ragas
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=os.environ.get("GEMINI_API_KEY"))
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2", google_api_key=os.environ.get("GEMINI_API_KEY"))
    
    # Ragas evaluate
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy
        ],
        llm=llm,
        embeddings=embeddings
    )
    
    print("\n--- Evaluation Results ---")
    print(result)
    
    # Save to CSV
    df = result.to_pandas()
    df.to_csv("evaluation_results.csv", index=False)
    print("Detailed results saved to evaluation_results.csv")

if __name__ == "__main__":
    run_evaluation()
