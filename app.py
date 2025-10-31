import streamlit as st
import os

# --- (الخطوة 1: ظبط الـ API Key في البيئة "Environment") ---
# ده "لازم" يكون أول حاجة خالص، قبل أي import تاني
# عشان "vector.py" يلاقيه لما يشتغل
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("GOOGLE_API_KEY not found in Streamlit Secrets!", icon="🚨")
    st.stop()

# --- (الخطوة 2: باقي الـ Imports) ---
# (دلوقتي لما نستدعي vector، هو هيلاقي الـ Key جاهز)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever 

# --- (الخطوة 3: ظبط الصفحة) ---
st.set_page_config(page_title="Signavio Sage", page_icon="🤖")

# --- (الخطوة 4: تحميل الموديل والـ Chain) ---
@st.cache_resource
def load_model_chain():
    """
    Loads the LLM model and the prompt chain.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.7) 

    template = """
    You are 'Signavio Sage', a helpful AI assistant for the SAP Signavio Product Excellence team.
    Your job is to answer questions about internal processes, practices, and onboarding.
    You must answer *ONLY* based on the provided context documents.

    Here is the relevant context: {context}

    Here is the question to answer: {question}

    Follow these rules:
    1. If the answer is not in the context, clearly state: 'I am sorry, I do not have information on that topic in my knowledge base.'
    2. If the answer is in the context, be concise and helpful.
    3. At the end of your answer, *always* cite the filename found in the **'source' metadata** (e.g., 'Source: onboarding.md').
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

try:
    chain = load_model_chain()
    st.success("Google Gemini model loaded successfully!") 
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- (الخطوة 5: باقي الـ GUI بتاعك - زي ما هو بالظبط) ---
st.title("🤖 Signavio Sage Assistant")
st.info("Ask me anything... (Powered by Google Gemini & RAG)")

st.subheader("Demo: User Permission Simulation")
user_role = st.selectbox(
    "Select your role to test permissions:",
    ("Sales (Public Access)", "Product Team (Internal Access)")
)

with st.expander("Show Retrieved Context (For Demo Purposes)"):
    show_context = st.toggle("Toggle to see the context", value=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("What is our roadmapping process?"):

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Sage is thinking..."):

            context = retriever.invoke(question)

            if show_context:
                st.write("---")
                st.subheader("Retrieved Context:")
                st.json([doc.to_json() for doc in context])
                st.write("---")

            is_sensitive = False
            for doc in context:
                if 'project_phoenix.md' in doc.metadata.get('source', ''):
                    is_sensitive = True
                    break

            if is_sensitive and user_role == "Sales (Public Access)":
                result = "I'm sorry, I cannot answer this question as it contains information restricted to the Product Team only."
            else:
                result_obj = chain.invoke({"context": context, "question": question})
                result = result_obj.content 

            st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})