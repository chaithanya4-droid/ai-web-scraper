import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load env variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class GroqLLMService:
    """Service class for interacting with Llama 3.3 on Groq via LangChain."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY environment variable is not set. The tool will require it to function.")

    def analyze_content(self, content: str, question: str) -> str:
        """
        Sends the scraped and parsed content to the LLM to answer the user's question.

        Args:
            content (str): The cleaned text from the webpage.
            question (str): The question or query from the user.

        Returns:
            str: The LLM's structured response.

        Raises:
            ValueError: If the API key is missing.
            RuntimeError: If the API call fails.
        """
        if not self.api_key:
            raise ValueError(
                "Groq API Key is missing. Please set GROQ_API_KEY in your environment or .env file."
            )

        if not content.strip():
            return "No webpage content is available for analysis."

        # Limit content size to keep prompt within reasonable limits (approx 20,000 tokens)
        max_chars = 80000
        if len(content) > max_chars:
            logger.warning(f"Content length ({len(content)} chars) exceeds limit. Truncating to {max_chars} chars.")
            content = content[:max_chars] + "\n\n[Content truncated due to length limits...]"

        try:
            # Initialize ChatGroq LLM
            llm = ChatGroq(
                api_key=self.api_key,
                model_name=self.model_name,
                temperature=0.1,
            )

            # Create prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are a professional AI web scraping and data extraction assistant.\n"
                    "Your task is to analyze the provided webpage text content and answer the user's question or perform the request.\n"
                    "Extract and structure the requested information accurately based ONLY on the provided webpage content.\n"
                    "If the requested information is not found in the content, state that clearly.\n"
                    "Format your response professionally using Markdown (with headers, bullet points, or tables as appropriate)."
                )),
                ("human", (
                    "Webpage Content:\n"
                    "---------------------\n"
                    "{content}\n"
                    "---------------------\n\n"
                    "User Request/Question: {question}\n\n"
                    "Response:"
                ))
            ])

            # Chain implementation using LCEL
            chain = prompt_template | llm | StrOutputParser()

            # Execute chain
            response = chain.invoke({"content": content, "question": question})
            logger.info("Successfully obtained response from Groq LLM.")
            return response

        except Exception as e:
            logger.error(f"Error querying Groq LLM: {str(e)}")
            raise RuntimeError(f"LLM analysis failed: {str(e)}")

def analyze_web_content(content: str, question: str) -> str:
    """Helper function to run LLM analysis."""
    service = GroqLLMService()
    return service.analyze_content(content, question)
