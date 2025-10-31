from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are 'Signavio Sage', a helpful AI assistant for the SAP Signavio Product Excellence team.
Your job is to answer questions about internal processes, practices, and onboarding.
You must answer *ONLY* based on the provided context documents.

Here is the relevant context: {context}

Here is the question to answer: {question}

Follow these rules:
1. If the answer is not in the context, clearly state: 'I am sorry, I do not have information on that topic in my knowledge base.'
2. If the answer is in the context, be concise and helpful.
3. At the end of your answer, *always* cite the source document (e.g., 'Source: roadmapping.md' or 'Source: onboarding.md' or 'Source: project_phoenix.md' ).
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Ask Signavio Sage (q to quit): ") 
    print("\n\n")
    if question == "q":
        break
    
    context = retriever.invoke(question) 
    
    result = chain.invoke({"context": context, "question": question}) 
    print(result)