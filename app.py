import os
import streamlit as st
import urllib.parse
from dotenv import load_dotenv

# Import workflow and graph
from workflow import app_workflow

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="v7scrapeAI",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styling for a professional, polished design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist+Sans:wght@400;500;600;700&display=swap');

/* Base style overrides */
.stApp {
    background: #f8f9fa;
    font-family: 'Geist Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: #1a1a1a;
}

/* Titles and Headers */
h1, h2, h3 {
    font-family: 'Geist Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
    margin-top: 0.5rem !important;
    margin-bottom: 1rem !important;
    letter-spacing: -0.02em !important;
}

h1 { font-size: 32px !important; }
h2 { font-size: 24px !important; }
h3 { font-size: 18px !important; }

/* Card styling */
.glass-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.glass-card:hover {
    border-color: #d1d5db;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Streamlit container borders */
[data-testid="stContainer"] {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

/* Button styling */
div.stButton > button:first-child {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-family: 'Geist Sans', sans-serif;
    font-weight: 600;
    font-size: 15px;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    width: 100%;
    letter-spacing: -0.01em;
}

div.stButton > button:first-child:hover {
    background: #1d4ed8;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    transform: translateY(-1px);
}

div.stButton > button:first-child:active {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(37, 99, 235, 0.2);
}

/* Download button */
div.stDownloadButton > button {
    background: #f3f4f6 !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

div.stDownloadButton > button:hover {
    background: #e5e7eb !important;
    border-color: #9ca3af !important;
}

/* Input fields */
input[type="text"],
textarea,
select {
    background: white !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
    font-size: 15px !important;
    color: #1a1a1a !important;
    transition: all 0.2s ease !important;
}

input[type="text"]:focus,
textarea:focus,
select:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
}

textarea {
    font-family: 'Menlo', 'Monaco', monospace !important;
    font-size: 13px !important;
}

/* Status and alerts */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid !important;
    padding: 12px 16px !important;
}

.stSuccess {
    background-color: #f0fdf4 !important;
    border-color: #86efac !important;
    color: #166534 !important;
}

.stError {
    background-color: #fef2f2 !important;
    border-color: #fca5a5 !important;
    color: #991b1b !important;
}

.stWarning {
    background-color: #fefce8 !important;
    border-color: #facd34 !important;
    color: #854d0e !important;
}

.stInfo {
    background-color: #f0f9ff !important;
    border-color: #bae6fd !important;
    color: #0c4a6e !important;
}

/* Expander styling */
details > summary {
    cursor: pointer;
    padding: 12px;
    border-radius: 8px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    font-weight: 500;
    transition: all 0.2s ease;
}

details > summary:hover {
    background: #f3f4f6;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

[data-testid="stSidebar"] h2 {
    color: #1a1a1a !important;
    margin-top: 1.5rem !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #6b7280;
}

/* Status container */
div[data-testid="stStatus"] {
    background: white !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
}

/* Footer style */
.footer-text {
    font-size: 13px;
    color: #9ca3af;
    text-align: center;
    margin-top: 48px;
    border-top: 1px solid #e5e7eb;
    padding-top: 24px;
    letter-spacing: -0.01em;
}

/* Badge styling */
.badge {
    display: inline-block;
    padding: 6px 12px;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    color: #374151;
}

.badge-success {
    background: #f0fdf4 !important;
    border-color: #86efac !important;
    color: #166534 !important;
}

/* Streamlit divider */
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)


# Sidebar Configuration
with st.sidebar:
    st.markdown("### Settings")
    
    # API Key Handling
    groq_api_key_env = os.getenv("GROQ_API_KEY", "")
    
    # If key exists in env, mask it and show status
    if groq_api_key_env:
        api_key_input = groq_api_key_env
    else:
        api_key_input = st.text_input(
            "Groq API Key", 
            type="password",
            placeholder="Enter your key...",
            help="Your API key from Groq"
        )
        if api_key_input:
            os.environ["GROQ_API_KEY"] = api_key_input
        else:
            st.warning("⚠️ API key required to proceed")
            
    st.markdown("---")
    
    st.markdown("#### Configuration")
    
    # Model Selection
    model_env = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    st.markdown(f"**Model:** `{model_env}`")
    st.markdown("**Engine:** `LangGraph`")
    st.markdown("**Browser:** `Selenium`")


# Main Layout Header
st.markdown("""
<div style='text-align: center; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid #e5e7eb;'>
    <h1 style='margin-bottom: 8px;'>v7scrapeAI</h1>
    <p style='color: #6b7280; font-size: 15px; margin: 0; font-weight: 400; letter-spacing: -0.01em;'>
        Advanced Web Scraping & Semantic Data Extraction
    </p>
</div>
""", unsafe_allow_html=True)


# Main Interface Cards
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("#### Configuration")
    
    # Target URL
    url = st.text_input(
        "Website URL", 
        placeholder="https://example.com",
        help="Enter the full URL of the webpage to scrape",
        label_visibility="collapsed"
    )
    
    # User Action selection
    question_preset = st.selectbox(
        "Extract Type",
        options=[
            "Summarize Page Content",
            "Extract Company Information",
            "Extract Job Roles",
            "Extract Contact Details",
            "Custom Query"
        ],
        index=0,
        help="Select the type of information to extract",
        label_visibility="collapsed"
    )
    
    # Determine query based on option
    if question_preset == "Summarize Page Content":
        final_question = "Provide a concise summary of the page content, highlighting the main purpose, sections, and key takeaways."
    elif question_preset == "Extract Company Information":
        final_question = "Extract company information. Focus on: Name, Industry, Mission/Vision, Headquarters/Location, Team size, Year founded, and Key products/services."
    elif question_preset == "Extract Job Roles":
        final_question = "Identify and extract all job openings or career opportunities mentioned on the page, along with descriptions, location, and requirements/qualifications for each role."
    elif question_preset == "Extract Contact Details":
        final_question = "Extract contact details from the page. Locate and list: Email addresses, Phone numbers, Physical address/headquarters, Social media profile links, and Contact forms."
    else:
        final_question = st.text_area(
            "Custom Query",
            placeholder="Describe what you'd like to extract...",
            help="Type exactly what you want the AI to extract from the webpage",
            label_visibility="collapsed",
            height=120
        )
    
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    # Trigger Button
    run_pipeline = st.button("Start Extraction", use_container_width=True)

with col2:
    st.markdown("#### Processing")
    
    if run_pipeline:
        # Validate inputs
        if not url:
            st.error("Please enter a valid URL.")
        elif not url.startswith(("http://", "https://")):
            st.error("Invalid URL format. Please start with 'http://' or 'https://'.")
        elif not os.environ.get("GROQ_API_KEY"):
            st.error("Groq API Key is not set. Please set it in the sidebar or a `.env` file.")
        else:
            # Setup State Graph Input
            inputs = {
                "url": url,
                "question": final_question,
                "raw_html": None,
                "cleaned_text": None,
                "analysis_result": None,
                "error": None
            }
            
            # Run stream
            has_error = False
            final_state = {}
            
            with st.status("Processing...", expanded=True) as status:
                try:
                    for output in app_workflow.stream(inputs):
                        for node_name, state_update in output.items():
                            # Merge updates to form latest state
                            final_state = {**inputs, **state_update}
                            
                            if "error" in state_update and state_update["error"]:
                                has_error = True
                                status.update(label=f"Failed at {node_name}", state="error")
                                st.error(f"❌ {node_name.capitalize()}: {state_update['error']}")
                                break
                            
                            # Custom status logging for nodes
                            if node_name == "scrape":
                                status.write("✓ Webpage rendered and loaded")
                            elif node_name == "parse":
                                status.write(f"✓ Content extracted and cleaned ({len(state_update.get('cleaned_text', ''))} characters)")
                            elif node_name == "llm_analysis":
                                status.write("✓ Processing with AI model")
                            elif node_name == "output":
                                status.write("✓ Extraction completed")
                                
                        if has_error:
                            break
                            
                    if not has_error:
                        status.update(label="Complete!", state="complete")
                        
                except Exception as e:
                    status.update(label="Processing failed", state="error")
                    st.error(f"❌ Error: {str(e)}")
                    has_error = True
            
            # If successful, show results
            if not has_error and final_state:
                # Store final results in session state to persist across rerenders
                st.session_state["analysis_result"] = final_state.get("analysis_result")
                st.session_state["cleaned_text"] = final_state.get("cleaned_text")
                st.session_state["executed_url"] = url
                st.session_state["executed_query"] = question_preset
            else:
                # Clear session state if failed
                st.session_state["analysis_result"] = None
                st.session_state["cleaned_text"] = None


# Results section
if st.session_state.get("analysis_result"):
    st.markdown("---")
    st.markdown("#### Results")
    
    # Details card
    st.markdown(f"""
    <div style='display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;'>
        <span class='badge badge-success'>✓ Success</span>
        <span class='badge'>URL: {st.session_state.get('executed_url')}</span>
        <span class='badge'>Task: {st.session_state.get('executed_query')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Outer container for markdown result
    with st.container(border=True):
        st.markdown(st.session_state["analysis_result"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as Markdown",
                data=st.session_state["analysis_result"],
                file_name="extraction_result.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.success("Copied! (Use Ctrl+V to paste)")
        
    # Optional raw preview
    with st.expander("📄 View Raw Text (Sent to AI)"):
        st.text_area(
            "Content",
            value=st.session_state["cleaned_text"],
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

# Footer
st.markdown("""
<div class="footer-text">
    v7scrapeAI • Powered by Selenium, BeautifulSoup, LangChain, and Groq Llama
</div>
""", unsafe_allow_html=True)
