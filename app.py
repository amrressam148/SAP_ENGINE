import streamlit as st
# امسح OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI # (ده الجديد)
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever # (ده هيستدعي الـ retriever الجديد)
import os # (ضيف ده)

# --- (الجديد: إزاي تحط الـ Key بأمان) ---
# Streamlit Cloud هيديك مكان تحط فيه الـ Key ده
# للتجربة المحلية، اعمل كده:
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = st.secrets.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE_FOR_LOCAL_TEST")
# ---

@st.cache_resource
def load_model_chain():
    """
    Loads the LLM model and the prompt chain.
    """
    # (استخدمنا الموديل بتاع جوجل)
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.7) 

    # (نفس الـ Prompt بتاعك بالظبط، مفيش تغيير)
    template = """
    You are 'Signavio Sage', ...
    ... (كل الـ template بتاعك) ...
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

# --- (باقي الكود بتاع الـ GUI زي ما هو بالظبط) ---
# (مفيش أي تغيير في الـ GUI أو الـ logic بتاع الـ permissions)
try:
    chain = load_model_chain()
    st.success("Google Gemini model loaded successfully!") # (غيرنا الرسالة)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.set_page_config(page_title="Signavio Sage", page_icon="🤖")
st.title("🤖 Signavio Sage Assistant")
st.info("Ask me anything... (Powered by Google Gemini & RAG)") # (غيرنا الرسالة)

# ... (كل كود الـ GUI بتاعك زي ما هو) ...