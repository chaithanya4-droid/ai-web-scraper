import logging
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from scraper import scrape_url
from parser import parse_html
from llm import analyze_web_content

# Set up logging
logger = logging.getLogger(__name__)

class ScraperState(TypedDict):
    """
    Represents the state of the web scraping workflow.
    
    Attributes:
        url (str): The target webpage URL.
        question (str): The extraction query or question for the LLM.
        raw_html (Optional[str]): The raw HTML source obtained from Selenium.
        cleaned_text (Optional[str]): The readable text extracted from HTML.
        analysis_result (Optional[str]): The structured answer returned by the LLM.
        error (Optional[str]): Error message if any node fails.
    """
    url: str
    question: str
    raw_html: Optional[str]
    cleaned_text: Optional[str]
    analysis_result: Optional[str]
    error: Optional[str]


def scrape_node(state: ScraperState) -> ScraperState:
    """
    Node for scraping the URL content via Selenium.
    """
    logger.info("Executing 'scrape' node.")
    url = state.get("url")
    if not url:
        return {**state, "error": "URL is missing."}
        
    try:
        raw_html = scrape_url(url)
        return {**state, "raw_html": raw_html, "error": None}
    except Exception as e:
        logger.error(f"Scrape Node failed: {e}")
        return {**state, "error": f"Scraping error: {str(e)}"}


def parse_node(state: ScraperState) -> ScraperState:
    """
    Node for parsing the raw HTML content using BeautifulSoup.
    """
    logger.info("Executing 'parse' node.")
    if state.get("error"):
        logger.info("Skipping 'parse' node due to previous error.")
        return state
        
    raw_html = state.get("raw_html")
    if not raw_html:
        return {**state, "error": "Raw HTML is missing in state."}
        
    try:
        cleaned_text = parse_html(raw_html)
        return {**state, "cleaned_text": cleaned_text}
    except Exception as e:
        logger.error(f"Parse Node failed: {e}")
        return {**state, "error": f"Parsing error: {str(e)}"}


def llm_analysis_node(state: ScraperState) -> ScraperState:
    """
    Node for generating analysis with Groq LLM using the user's question.
    """
    logger.info("Executing 'llm_analysis' node.")
    if state.get("error"):
        logger.info("Skipping 'llm_analysis' node due to previous error.")
        return state
        
    cleaned_text = state.get("cleaned_text")
    question = state.get("question")
    
    if not cleaned_text:
        return {**state, "error": "Cleaned text content is missing for analysis."}
    if not question:
        return {**state, "error": "User question is missing for analysis."}
        
    try:
        analysis_result = analyze_web_content(cleaned_text, question)
        return {**state, "analysis_result": analysis_result}
    except Exception as e:
        logger.error(f"LLM Analysis Node failed: {e}")
        return {**state, "error": f"LLM Analysis error: {str(e)}"}


def output_node(state: ScraperState) -> ScraperState:
    """
    Node for finalizing workflow, auditing, or logging results.
    """
    logger.info("Executing 'output' node.")
    if state.get("error"):
        logger.warning(f"Workflow completed with errors: {state['error']}")
    else:
        logger.info("Workflow completed successfully.")
    return state


# Initialize the state graph
workflow = StateGraph(ScraperState)

# Add all nodes to the graph
workflow.add_node("scrape", scrape_node)
workflow.add_node("parse", parse_node)
workflow.add_node("llm_analysis", llm_analysis_node)
workflow.add_node("output", output_node)

# Set execution flow and entry point
workflow.set_entry_point("scrape")
workflow.add_edge("scrape", "parse")
workflow.add_edge("parse", "llm_analysis")
workflow.add_edge("llm_analysis", "output")
workflow.add_edge("output", END)

# Compile graph into a runnable application
app_workflow = workflow.compile()
