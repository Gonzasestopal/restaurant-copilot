from langchain_openai import ChatOpenAI

from app.config import settings

llm = ChatOpenAI(model="gpt-4.1-mini", api_key=settings.openai_api_key)
print(llm.invoke("hola"))
