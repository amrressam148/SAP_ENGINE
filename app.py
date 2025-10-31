import streamlit as st
# امسح جوجل
from langchain_ollama.llms import OllamaLLM # (ده الجديد)
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever # (ده هيستدعي الـ retriever المحلي)
# امسح os

# --- (الخطوة 1: ظبط الصفحة الأول) ---
st.set_page_config(page_title="Signavio Sage", page_icon="🤖")

# --- (الخطوة 2: تحميل الموديل المحلي) ---
@st.cache_resource
def load_model_chain():
    # (استخدمنا الموديل المحلي الخفيف)
    model = OllamaLLM(model="mistral:7b") 

    # (نفس الـ Prompt بتاعك بالظبط)
    template = """
    You are 'Signavio Sage', ...
    ... (كل الـ template بتاعك) ...
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

try:
    chain = load_model_chain()
    st.success("Ollama model (mistral:7b) loaded successfully!") # (غيرنا الرسالة)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- (الخطوة 3: باقي الـ GUI بتاعك - زي ما هو) ---
st.title("🤖 Signavio Sage Assistant")
st.info("Ask me anything... (Powered by Ollama & RAG - 100% Local)") # (غيرنا الرسالة)

# (باقي كود الـ GUI بتاعك زي ما هو... الـ Select Box والـ Expander والشات)
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
                # (هنا أهم تعديل: شيلنا .content)
                result = chain.invoke({"context": context, "question": question})

            st.markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})