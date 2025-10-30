import streamlit as st
import os
from os import environ
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
import tempfile
from typing import List, Dict
import uuid

# Initialize the LLM
llm = ChatOpenAI(
    model="openai.gpt-4o",
    temperature=0.2,
    api_key=os.environ["API_KEY"],
    base_url="https://api.ai.it.cornell.edu"
)

# Initialize embeddings
embeddings = OpenAIEmbeddings(
    model="openai.text-embedding-3-large",
    api_key=os.environ["API_KEY"],
    base_url="https://api.ai.it.cornell.edu"
)

st.title("File Q&A with OpenAI")

# Initialize session state for storing documents
if "documents" not in st.session_state:
    st.session_state["documents"] = {}

# Add file uploader that accepts multiple files
uploaded_files = st.file_uploader(
    "Upload articles (PDF or TXT)",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

# Process uploaded files
for uploaded_file in uploaded_files:
    # Check if file is already processed
    if uploaded_file.name not in st.session_state["documents"]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()
            
            # Load document based on file type
            try:
                if uploaded_file.name.endswith('.pdf'):
                    loader = PyPDFLoader(tmp_file.name)
                else:
                    loader = TextLoader(tmp_file.name)
                    
                docs = loader.load()
                
                # Store document info
                st.session_state["documents"][uploaded_file.name] = {
                    "path": tmp_file.name,
                    "docs": docs
                }
                st.success(f"Successfully processed: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
# Display list of uploaded documents
if st.session_state["documents"]:
    st.write("Uploaded Documents:")
    for doc_name in st.session_state["documents"]:
        st.write(f"- {doc_name}")

question = st.chat_input(
    "Ask something about the documents",
    disabled=not st.session_state["documents"],
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the documents"}]

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and st.session_state["documents"]:
    # Initialize or get vectorstore
    if not st.session_state["vectorstore"]:
        # Collect all documents
        all_docs = []
        for doc_info in st.session_state["documents"].values():
            all_docs.extend(doc_info["docs"])
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Increased for better context
            chunk_overlap=50  # Added overlap for better coherence
        )
        chunks = text_splitter.split_documents(all_docs)
        
        # Create vector store
        st.session_state["vectorstore"] = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )
    
    # Set up retriever
    retriever = st.session_state["vectorstore"].as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    
    # Create prompt template
    template = """
    You are a helpful assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    
    Question: {question}
    
    Context: {context}
    
    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Retrieve relevant context
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Generate response
    with st.chat_message("assistant"):
        messages = prompt.invoke({
            "question": question,
            "context": context
        })
        response = llm.invoke(messages)
        
        st.write(response.content)
        
        # Show sources if any
        if retrieved_docs:
            st.write("\n\nSources:")
            seen_sources = set()
            for i, doc in enumerate(retrieved_docs, 1):
                source = doc.metadata.get('source', '').split('/')[-1]
                if source and source not in seen_sources:
                    st.write(f"[{i}] {source}")
                    seen_sources.add(source)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response.content})