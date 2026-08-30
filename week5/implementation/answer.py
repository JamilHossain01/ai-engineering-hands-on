from pathlib import Path
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # আগে paid OpenAI ব্যবহার হতো
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
 
from dotenv import load_dotenv



load_dotenv(override=True)
#%%
MODEL = "qwen3:8b"
DB_NAME = str(Path(__file__).parent.parent / "vector_db")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
RETREVAL_K = 10


SYSTEM_PROMPT = """ 
You are a knowledgble, friendly assitant represnting the comapany Insurellm .
You are chatting with a iser about Insurellm.
If relevant, use the given context to anwser any question .
if dont know anser, say so

Context:
{context}
"""
vectorstore = Chroma(persist_directory=DB_NAME,embedding_function=embeddings)
retriever = vectorstore.as_retriever()
llm = ChatOllama(model=MODEL,temperature=0)

def fetch_context (question:str) -> list[Document]:
    """
    Retrieve context for documents for a question.
    """
    return retriever.invoke(question,k=RETREVAL_K)


def combined_question(question: str,history:list[dict] = []) -> str:
    """ 
    Combine all the user message into a single string"""
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question

def answer_question (question:str, history:list[dict] = []) -> tuple[str,list[Document]]:
    """ 
    Anser the given question wtih  Rag: return the anser an the context documents
    """

    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content, docs

