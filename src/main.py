from wechat.app import app

from dotenv import load_dotenv, find_dotenv
import openai
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser

load_dotenv(find_dotenv())
"""
Need to load the environment file here ".env" file
The environment file should include all the api key.
As we may need pinecone, it should include as following:
OPEN_AI_KEY
PINECONE_ENV = 'gcp-starter'
PINECONE_API_KEY = 'c048cc32-1098-4de3-8ad7-a7e5e60ce0d0'
Just use my PINECONE api key here, it's free.
"""
class CommaSeparatedListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        return text.strip().split(", ")  

template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])
category_chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
