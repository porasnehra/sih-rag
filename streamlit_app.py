import streamlit as st
import os
from dotenv import load_dotenv
from query_understanding import analyze_query
from vector_store import search_vectors
from generation import detect_and_translate, generate_response

load_dotenv()

st.set_page_config(page_title="BIS Standards Assistant", page_icon="📜")

st.title("BIS Standards AI Assistant")
st.write("Ask questions about Bureau of Indian Standards (BIS) products, certifications, and testing.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is the standard for pressure cookers?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing and retrieving context..."):
            # 1. Detect & Translate
            english_query, is_hindi = detect_and_translate(prompt)
            
            # 2. Retrieve context
            results = search_vectors(english_query, k=3)
            THRESHOLD = 1.0
            valid_results = [r for r in results if r['score'] < THRESHOLD]
            if not valid_results and results:
                valid_results = []
                
            # 3. Generate response
            final_output = generate_response(english_query, valid_results, is_hindi=is_hindi)
            
            # Format output
            if isinstance(final_output, dict):
                response_text = final_output.get("answer", str(final_output))
                sources = final_output.get("sources", [])
                
                st.markdown(response_text)
                if sources:
                    st.markdown("**Sources Cited:**")
                    for s in sources:
                        st.markdown(f"- {s}")
                        
                # Add to history
                full_response = response_text
                if sources:
                    full_response += "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in sources])
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.markdown(final_output)
                st.session_state.messages.append({"role": "assistant", "content": final_output})
