import gradio as gr 
from dotenv import load_dotenv
from assistant import KnowledgeAssistant 

load_dotenv(override=True)

assistant = KnowledgeAssistant()

def chat_fn(message,history: list[dict]) -> str:
    """ gr.ChatInterface(type="messages) expects this exact signature:
    (mesage: str,history:list[dict]) -> str"""

    answer,docs = assistant.answer(message,history)

    return answer

demo = gr.ChatInterface(
    fn=chat_fn,

    title="My Private Knowledge Assistant",
    description="Ask anything about personla documents (PDF,TXT,Markdown,Word).",
    examples=[
        "Summarize the key point of my documents",

        "What does this knowledge base contain"
    ]
)

if __name__ == "__main__" : 
    demo.launch(inbrowser=True)