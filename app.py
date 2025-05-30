import streamlit as st
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
import os

# Set your Hugging Face token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Title
st.title("📊 CSV-based RAG Q&A System")

# File uploader
uploaded_file = st.file_uploader("television_products", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Convert all rows into a string
    all_text = df.astype(str).apply(lambda row: ', '.join(row), axis=1).str.cat(sep="\n")

    # Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(all_text)

    # Create vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Load LLM from Hugging Face
    llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1", 
    model_kwargs={"temperature": 0.5, "max_new_tokens": 200}
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Ask question
    st.subheader("🔎 Ask a question")
    user_question = st.text_input("Ask something about the CSV data")

    if user_question:
        with st.spinner("Thinking..."):
            docs = retriever.get_relevant_documents(user_question)
            st.info(f"Retrieved Context:\n\n{docs[0].page_content if docs else 'No docs found'}")
            
            try:
                response = qa_chain.run(user_question)
                st.success(response)
            except Exception as e:
                st.error(f"Error: {e}")

