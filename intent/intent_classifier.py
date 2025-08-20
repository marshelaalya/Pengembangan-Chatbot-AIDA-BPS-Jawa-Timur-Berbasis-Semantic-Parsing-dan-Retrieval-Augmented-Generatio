from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import json
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class IntentOutputParser(BaseOutputParser):
    """Parse the LLM output to extract intent and confidence"""
    
    def parse(self, text: str) -> Dict:
        try:
            # Try to parse JSON response
            result = json.loads(text.strip())
            return result
        except:
            # Fallback parsing if not valid JSON
            text_lower = text.lower()
            if "permintaan-data" in text_lower or "semantic" in text_lower:
                return {"intent": "permintaan-data", "confidence": 0.7}
            elif "knowledge-bps" in text_lower or "rag" in text_lower:
                return {"intent": "knowledge-bps", "confidence": 0.7}
            else:
                return {"intent": "other", "confidence": 0.5}

class LangChainIntentClassifier:
    def __init__(self, model_name="gpt-3.5-turbo", temperature=0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.parser = IntentOutputParser()
        
        # Define the classification prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Kamu adalah intent classifier untuk chatbot BPS (Badan Pusat Statistik).
                    
        Klasifikasikan pertanyaan pengguna ke dalam salah satu intent berikut:
        1. "permintaan-data": Pertanyaan yang meminta data numerik spesifik, statistik, rasio, persentase, atau informasi kuantitatif. 
             Biasanya diawali dengan kata seperti "berapa", "jumlah", "data", "rasio", "total", dll.
        2. "knowledge-bps": Pertanyaan yang meminta definisi, penjelasan, prosedur, atau pengetahuan umum. 
             Biasanya diawali dengan kata seperti "apa", "bagaimana", "jelaskan", "dari mana", dll.
        3. "other": Pertanyaan yang tidak termasuk dalam kategori di atas.

        Contoh:
        - "Berapa jumlah penduduk Jakarta?" → permintaan-data
        - "Apa itu sensus penduduk?" → knowledge-bps
        - "Data ekspor tahun 2020" → permintaan-data
        - "Bagaimana cara menghitung IPM?" → knowledge-bps

        Jawablah HANYA dengan objek JSON: {{"intent": "kategori", "confidence": 0.0-1.0}}"""),
            ("user", "{query}")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def classify(self, query: str) -> Dict:
        """Classify a single query"""
        try:
            result = self.chain.invoke({"query": query})
            result["query"] = query
            return result
        except Exception as e:
            # Fallback response
            return {
                "intent": "knowledge-bps",  # Default to RAG
                "confidence": 0.5,
                "query": query,
                "error": str(e)
            }

# Simple keyword-based fallback (if OpenAI not available)
class SimpleIntentClassifier:
    def classify(self, query: str) -> Dict:
        query_lower = query.lower()
        
        # Simple keyword matching
        semantic_keywords = ["berapa", "jumlah", "data", "rasio", "total", "nilai", "angka", "apk", "apm", "aps"]
        rag_keywords = ["apa", "siapa", "bagaimana", "kapan", "mengapa", "jelaskan", "definisi", "sumber"]
        
        # Check first word
        first_word = query_lower.split()[0] if query_lower.split() else ""
        
        if any(keyword in first_word for keyword in semantic_keywords):
            return {
                "intent": "permintaan-data",
                "confidence": 0.8,
                "query": query
            }
        elif any(keyword in first_word for keyword in rag_keywords):
            return {
                "intent": "knowledge-bps",
                "confidence": 0.8,
                "query": query
            }
        else:
            return {
                "intent": "other",
                "confidence": 0.5,
                "query": query
            }

# Factory function to get appropriate classifier
def get_intent_classifier(use_llm=True):
    """Get intent classifier based on availability"""
    if use_llm:
        try:
            return LangChainIntentClassifier()
        except Exception as e:
            print(f"Warning: Could not initialize LLM classifier: {e}")
            print("Falling back to simple classifier")
    
    return SimpleIntentClassifier()