from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, convert_to_messages
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

load_dotenv(override=True)

MODEL = "qwen3:8b"
DB_NAME = "../vector_db"
RETRIEVAL_K = 6

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

SYSTEM_PROMPT = """You are a private knowledge assistant. Answer the user's question using ONLY the context provided below, extracted from the user's own documents.

Rules (must follow strictly):
1. Base your answer strictly on the provided context. Do not use any outside/general knowledge.
2. If the answer is not present in the context, respond exactly: "I couldn't find this information in your documents."
3. Never guess, invent facts, or make assumptions beyond what the context states.
4. If helpful, mention which document/source the information came from.
5. Be concise, clear, and directly answer what was asked.

Context:
{context}
"""


class KnowledgeAssistant:
    """
    The RAG engine is wrapped in a class so the vectorstore, retriever, and
    llm are created once (at object creation time) and reused for every
    question, instead of being rebuilt each time.
    """

    def __init__(self, db_name: str = DB_NAME, model: str = MODEL, k: int = RETRIEVAL_K):
        self.vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        self.llm = ChatOllama(model=model, temperature=0)

    def _extract_text(self, content) -> str:
        """
        Content might be a plain string, or (in newer Gradio versions) a list
        of content blocks for multimodal messages. This safely extracts text
        either way.
        """
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
            return " ".join(parts)
        return str(content)

    def _contextualize_question(self, question: str, history: list[dict]) -> str:
        """
        Combine all prior user messages with the new question into a single
        standalone query, so pronouns like "she"/"it" still retrieve well
        (Context Fusion).
        """
        prior_user_messages = "\n".join(
            self._extract_text(m["content"]) for m in history if m["role"] == "user"
        )
        if not prior_user_messages:
            return question
        return f"{prior_user_messages}\n\n{question}"

    def _fetch_context(self, question: str) -> list[Document]:
        """Retrieve the top k documents from the vectorstore that are most relevant to the question."""
        return self.retriever.invoke(question)

    def answer(self, question: str, history: list[dict] = None) -> tuple[str, list[Document]]:
        """Main entrypoint: takes a question and history, runs RAG, and returns (answer_text, retrieved_docs)."""
        history = history or []
        standalone_query = self._contextualize_question(question, history)
        docs = self._fetch_context(standalone_query)

        context_text = "\n\n---\n\n".join(
            f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
            for doc in docs
        )

        system_prompt = SYSTEM_PROMPT.format(
            context=context_text if context_text else "No relevant context found"
        )

        messages = [SystemMessage(content=system_prompt)]
        messages.extend(convert_to_messages(history))
        messages.append(HumanMessage(content=question))

        response = self.llm.invoke(messages)
        return response.content, docs


if __name__ == "__main__":
    assistant = KnowledgeAssistant()
    answer, docs = assistant.answer("What is this knowledge base about?", [])
    print(answer)
    print(f"\nRetrieved {len(docs)} documents")