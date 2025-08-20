from dotenv import load_dotenv
import os

load_dotenv()  # baca file .env

# from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain_community.embeddings.bedrock import BedrockEmbeddings

from langchain_openai import OpenAIEmbeddings


def get_embedding_function():
    return OpenAIEmbeddings()

