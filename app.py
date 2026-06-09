import streamlit as st
from utils.retriever import get_retriever
from transformers import pipeline


# ====================================
# PAGE CONFIGURATION
# ====================================

st.set_page_config(
    page_title="AI Education Chatbot",
    page_icon="🎓",
    layout="wide"
)


# ====================================
# CUSTOM CSS
# ====================================

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #f8fafc;
}

/* Main Title */
.title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    color: #2563eb;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #475569;
    margin-bottom: 30px;
}

/* Input Box */
.stTextInput input {
    background-color: white !important;
    color: black !important;
    border: 2px solid #2563eb !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 16px !important;
}

/* Context Box */
.content-box {
    background-color: white;
    color: black;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #2563eb;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.1);
    margin-top: 15px;
}

/* Answer Box */
.answer-box {
    background-color: #ecfdf5;
    color: black;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #22c55e;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.1);
    margin-top: 15px;
    font-size: 17px;
    line-height: 1.7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Hide Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ====================================
# HEADER
# ====================================

st.markdown(
    '<p class="title">🎓 AI Education Chatbot</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Ask Questions from PDF Notes using RAG + TinyLlama</p>',
    unsafe_allow_html=True
)


# ====================================
# SIDEBAR
# ====================================

with st.sidebar:

    st.title("📚 About Project")

    st.markdown("""
    ### Features

    ✅ PDF Question Answering

    ✅ RAG Retrieval

    ✅ Chroma Vector Database

    ✅ HuggingFace Embeddings

    ✅ TinyLlama Language Model

    ---

    Built using Streamlit + LangChain + HuggingFace
    """)


# ====================================
# LOAD RETRIEVER
# ====================================

retriever = get_retriever()


# ====================================
# LOAD LLM
# ====================================

@st.cache_resource
def load_llm():

    llm = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        max_new_tokens=200
    )

    return llm


llm = load_llm()


# ====================================
# USER INPUT
# ====================================

question = st.text_input(
    "🔍 Enter your question:"
)


# ====================================
# PROCESS QUESTION
# ====================================

if question:

    with st.spinner("Searching documents..."):

        docs = retriever.invoke(question)

        context = ""

        for doc in docs:
            context += doc.page_content + "\n\n"

    st.markdown(
        f"""
        <div class="content-box">
        <h3>📄 Retrieved Context</h3>
        <p>{context}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    with st.spinner("Generating answer..."):

        response = llm(prompt)

        answer = response[0]["generated_text"]

    st.markdown(
        f"""
        <div class="answer-box">
        <h3>🤖 AI Answer</h3>
        <p>{answer}</p>
        </div>
        """,
        unsafe_allow_html=True
    )