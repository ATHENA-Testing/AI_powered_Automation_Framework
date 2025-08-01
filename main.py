"""
Main Streamlit Application for Python Automation Framework
Provides a futuristic UI for all automation tasks.
"""
import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
import streamlit as st
import pandas as pd
import json
import os
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile
import zipfile
import io
import asyncio
from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
import subprocess



# Import custom modules
from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin
from src.ollama_manager import OllamaManager
from src.browser_agent import BrowserAutomationAgent
from src.git_manager import GitManager
from src.file_processor import FileProcessor
from src.report_generator import ReportGenerator
#from src.Browser_use import GeminiLLMWrapper
# from src.Browser_use import run_task_sync
# from src.Browser_use import run_browser_task
from src.logger import FrameworkLogger

# Page configuration
st.set_page_config(
    page_title="Python Automation Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitApp(LoggerMixin):
    """Main Streamlit application class"""
    
    def __init__(self):
        """Initialize the Streamlit application"""
        # Initialize configuration and managers
        self.config = ConfigManager()
        self.ollama_manager = OllamaManager(self.config)
        self.browser_agent = BrowserAutomationAgent(self.config)
        self.git_manager = GitManager(self.config)
        self.file_processor = FileProcessor(self.config)
        self.report_generator = ReportGenerator(self.config)
       # self.Browser_use = GeminiLLMWrapper()
        
        #self.logger = FrameworkLogger()
        # Initialize session state
        self._initialize_session_state()
        
        self.logger.info("Streamlit application initialized")
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'generated_prompt' not in st.session_state:
            st.session_state.generated_prompt = ""
        if 'test_cases' not in st.session_state:
            st.session_state.test_cases = []
        if 'test_scripts' not in st.session_state:
            st.session_state.test_scripts = {}
        if 'execution_results' not in st.session_state:
            st.session_state.execution_results = {}
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []
    
    def render_header(self):
        """Render the application header"""
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; text-align: center; margin: 0; font-size: 3rem;">
                🤖 Python Automation Framework
            </h1>
            <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
                AI-Powered Test Generation & Execution Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with navigation and settings"""
        with st.sidebar:
            st.markdown("## 🚀 Navigation")
            
            # Navigation menu
            page = st.selectbox(
                "Select Section",
                [
                    "📄 Embedding & Knowledge Base",
                    "❓ Query Knowledge Base", 
                    "✨ Prompt Generation",
                    "📝 Test Case Generator",
                    "🔧 Test Script Generator",
                    "▶️ Executor",
                    "📊 Reports",
                    "🔄 Git Integration"
                ]
            )
            
            st.markdown("---")
            
            # Settings
            st.markdown("## ⚙️ Settings")
            
            # Ollama settings
            st.markdown("### 🧠 Ollama Settings")
            ollama_status = st.button("Check Ollama Status")
            if ollama_status:
                if self.ollama_manager._check_ollama_connection():
                    st.success("✅ Ollama is running")
                else:
                    st.error("❌ Ollama is not accessible")
            
            # Browser settings
            st.markdown("### 🌐 Browser Settings")
            headless_mode = st.checkbox("Headless Mode", value=self.config.get_boolean("BROWSER", "headless"))
            capture_screenshots = st.checkbox("Capture Screenshots", value=self.config.get_boolean("BROWSER", "capture_screenshots"))
            
            if st.button("Update Browser Settings"):
                self.config.set("BROWSER", "headless", str(headless_mode))
                self.config.set("BROWSER", "capture_screenshots", str(capture_screenshots))
                self.config.save_config()
                st.success("Settings updated!")
            
            return page
    
    def render_embedding_section(self):
        """Render the embedding and knowledge base section"""
        st.markdown("## 📄 Embedding & Knowledge Base")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Text Input")
            user_text = st.text_area(
                "Enter text to add to knowledge base:",
                height=200,
                placeholder="Enter your text content here..."
            )
            
            if st.button("Add Text to Knowledge Base", type="primary"):
                if user_text:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    doc_name = f"text_input_{timestamp}.txt"
                    self.ollama_manager.add_document_to_knowledge_base(doc_name, user_text)
                    st.success(f"Text added to knowledge base as {doc_name}")
                else:
                    st.warning("Please enter some text")
        
        with col2:
            st.markdown("### File Upload")
            uploaded_files = st.file_uploader(
                "Upload documents",
                accept_multiple_files=True,
                type=['pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls']
            )
            
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    if st.button(f"Process {uploaded_file.name}", key=f"process_{uploaded_file.name}"):
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Process the file
                        try:
                            content = self.file_processor.extract_text_from_file(tmp_path)
                            self.ollama_manager.add_document_to_knowledge_base(uploaded_file.name, content)
                            st.success(f"✅ {uploaded_file.name} processed and added to knowledge base")
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {e}")
                        finally:
                            os.unlink(tmp_path)
        
        # Display knowledge base info
        st.markdown("### 📚 Knowledge Base Status")
        try:
            # This would need to be implemented in the OllamaManager
            kb_info = self.ollama_manager.get_knowledge_base_info()
            st.info(f"Documents in knowledge base: {kb_info.get('doc_count', 'Unknown')}")
        except:
            st.info("Knowledge base information not available")
    
    def render_query_section(self):
        """Render the query knowledge base section"""
        st.markdown("## ❓ Query Knowledge Base")
        
        query = st.text_input(
            "Enter your query:",
            placeholder="Ask a question about your documents..."
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            num_results = st.slider("Number of results", 1, 10, 4)
        
        with col2:
            if st.button("Search Knowledge Base", type="primary"):
                if query:
                    with st.spinner("Searching knowledge base..."):
                        results = self.ollama_manager.query_knowledge_base(query, k=num_results)
                    
                    if results:
                        st.markdown("### 📋 Search Results")
                        for i, result in enumerate(results, 1):
                            with st.expander(f"Result {i}"):
                                st.write(result)
                    else:
                        st.warning("No relevant documents found")
                else:
                    st.warning("Please enter a query")
    
    def render_prompt_generation_section(self):
        """Render the prompt generation section"""
        st.markdown("## ✨ Prompt Generation")
        
        user_input = st.text_area(
            "Enter your requirements:",
            height=150,
            placeholder="Describe what you want to test or automate..."
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            use_context = st.checkbox("Use knowledge base context", value=True)
        
        with col2:
            if st.button("Generate Prompt", type="primary"):
                if user_input:
                    with st.spinner("Generating prompt..."):
                        context = None
                        if use_context:
                            context_docs = self.ollama_manager.query_knowledge_base(user_input, k=2)
                            context = " ".join(context_docs) if context_docs else None
                        
                        generated_prompt = self.ollama_manager.generate_prompt(user_input, context)
                        st.session_state.generated_prompt = generated_prompt
                else:
                    st.warning("Please enter your requirements")
        
        # Display generated prompt
        if st.session_state.generated_prompt:
            st.markdown("### 📝 Generated Prompt")
            st.text_area(
                "Generated Prompt:",
                value=st.session_state.generated_prompt,
                height=200,
                disabled=True
            )
    
    def render_testcase_generator_section(self):
        """Render the test case generator section"""
        st.markdown("## 📝 Test Case Generator")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Input options
            input_method = st.radio("Input Method", ["Use Generated Prompt", "Upload Document", "Direct Input"])
            
            if input_method == "Direct Input":
                direct_input = st.text_area("Enter test requirements:", height=150)
                prompt_to_use = direct_input
            elif input_method == "Upload Document":
                uploaded_doc = st.file_uploader("Upload document for test case generation", type=['pdf', 'txt', 'doc', 'docx'])
                if uploaded_doc:
                    # Process uploaded document
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(uploaded_doc.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        content = self.file_processor.extract_text_from_file(tmp_path)
                        prompt_to_use = content
                        st.success(f"Document {uploaded_doc.name} loaded")
                    except Exception as e:
                        st.error(f"Error processing document: {e}")
                        prompt_to_use = ""
                    finally:
                        os.unlink(tmp_path)
                else:
                    prompt_to_use = ""
            else:
                prompt_to_use = st.session_state.generated_prompt
        
        with col2:
            # Advanced options
            st.markdown("### ⚙️ Advanced Options")
            testcase_level = st.selectbox("Test Case Level", ["Beginner", "Intermediate", "Advanced"])
            testcase_type = st.selectbox("Test Case Type", ["Functional", "UI", "API", "Mobile"])
            testcase_count = st.slider("Number of Test Cases", 1, 20, 5)
        
        # Generate test cases
        if st.button("Generate Test Cases", type="primary"):
            if prompt_to_use:
                with st.spinner("Generating test cases..."):
                    test_cases = self.ollama_manager.generate_test_cases(
                        prompt_to_use, testcase_level, testcase_type, testcase_count
                    )
                    st.session_state.test_cases = test_cases
                
                if test_cases:
                    st.success(f"✅ Generated {len(test_cases)} test cases")
                else:
                    st.error("❌ Failed to generate test cases")
            else:
                st.warning("Please provide input for test case generation")
        
        # Display generated test cases
        if st.session_state.test_cases:
            st.markdown("### 📋 Generated Test Cases")
            
            # Format selection
            format_type = st.radio("Display Format", ["JSON", "Table"])
            
            if format_type == "JSON":
                st.json(st.session_state.test_cases)
            else:
                # Convert to DataFrame for table display
                df_data = []
                for tc in st.session_state.test_cases:
                    df_data.append({
                        "ID": tc.get("id", ""),
                        "Title": tc.get("title", ""),
                        "Description": tc.get("description", "")[:100] + "..." if len(tc.get("description", "")) > 100 else tc.get("description", ""),
                        "Priority": tc.get("priority", ""),
                        "Tags": ", ".join(tc.get("tags", []))
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            
            # Save test cases
            if st.button("Save Test Cases"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Save JSON format
                json_path = Path(self.config.get("PATHS", "testcase_output")) / f"testcases_{timestamp}.json"
                json_path.parent.mkdir(parents=True, exist_ok=True)
                with open(json_path, 'w') as f:
                    json.dump(st.session_state.test_cases, f, indent=2)
                
                # Save text format
                text_path = Path(self.config.get("PATHS", "testcase_output")) / f"testcases_{timestamp}.txt"
                with open(text_path, 'w') as f:
                    for i, tc in enumerate(st.session_state.test_cases, 1):
                        f.write(f"Test Case {i}: {tc.get('title', '')}\n")
                        f.write(f"Description: {tc.get('description', '')}\n")
                        f.write(f"Steps: {' -> '.join(step['step'] for step in tc.get('steps', []))}\n")
                        f.write(f"Expected Result: {tc.get('expected_result', '')}\n")
                        f.write("-" * 50 + "\n")
                
                st.success(f"✅ Test cases saved to {json_path} and {text_path}")
    

    def load_test_cases_from_folder(folder_path='testcase_generator'):
        if 'test_cases' not in st.session_state:
            st.session_state.test_cases = {}
        folder_path = 'testcase_generator'
        file_paths = glob.glob(os.path.join(folder_path, '*.json'))
        for path in file_paths:
            file_name = os.path.basename(path)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Store the loaded test case(s) under the filename key
                # If the JSON contains a list of test cases, you can customize accordingly
                st.session_state.test_cases[file_name] = data
            except Exception as e:
                st.error(f"Failed to load {file_name}: {e}")


    def render_testscript_generator_section(self):
        """Render the test script generator section"""
        st.markdown("## 🔧 Test Script Generator")
    
        col1, col2 = st.columns([1, 1])
    
        with col1:
            folder_path = 'testcase_generator'
            file_paths = glob.glob(os.path.join(folder_path, '*.json'))
            file_names = [os.path.basename(fp) for fp in file_paths]
    
            if file_paths:
                selected_file_idx = st.selectbox(
                    "Select Test Case File",
                    options=range(len(file_names)),
                    format_func=lambda idx: file_names[idx]
                )
                selected_file_path = file_paths[selected_file_idx]
    
                # Load all test cases from the selected JSON file
                with open(selected_file_path, 'r') as f:
                    try:
                        test_cases = json.load(f)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format in selected file.")
                        test_cases = []
    
                if isinstance(test_cases, list) and test_cases:
                    selected_case_idx = st.selectbox(
                        "Select Test Case",
                        options=range(len(test_cases)),
                        format_func=lambda idx: test_cases[idx].get("title", f"Test Case {idx+1}")
                    )
                    selected_testcase = test_cases[selected_case_idx]
                else:
                    st.warning("No valid test cases found in the selected file.")
                    selected_testcase = None
            else:
                st.warning("No test case files found. Please add JSON files to the folder.")
                selected_testcase = None
    
            uploaded_testcase = st.file_uploader("Or upload test case file", type=['json', 'txt'])
    
        with col2:
            st.markdown("### 🛠️ Tool Selection")
            tool_selection = st.selectbox("Automation Tool", ["Selenium", "Playwright", "RestAssured", "Appium"])
            browser_selection = st.selectbox("Browser/Platform", ["Chrome", "Firefox", "Safari", "Edge", "iOS", "Android"])
    
        if st.button("Generate Test Script", type="primary"):
            testcase_to_use = None
    
            if uploaded_testcase:
                content = uploaded_testcase.getvalue().decode()
                if uploaded_testcase.name.endswith('.json'):
                    try:
                        parsed = json.loads(content)
                        testcase_to_use = parsed[0] if isinstance(parsed, list) and parsed else None
                    except json.JSONDecodeError:
                        st.error("Uploaded JSON file is not valid.")
                else:
                    testcase_to_use = {
                        "title": "Uploaded Test Case",
                        "description": content,
                        "steps": content.split('\n'),
                        "expected_result": "Test should pass"
                    }
            elif selected_testcase:
                testcase_to_use = selected_testcase
            if testcase_to_use:
                with st.spinner("Generating test script..."):
                    test_script = self.ollama_manager.generate_test_script(
                        testcase_to_use, tool_selection, browser_selection
                    )
    
                    script_id = testcase_to_use.get('id', f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    st.session_state.test_scripts[script_id] = {
                        "script": test_script,
                        "testcase": testcase_to_use,
                        "tool": tool_selection,
                        "browser": browser_selection
                    }
    
                st.success("✅ Test script generated successfully")
            else:
                st.warning("Please select or upload a valid test case.")
    
        if st.session_state.test_scripts:
            st.markdown("### 📜 Generated Test Scripts")
    
            script_id = st.selectbox(
                "Select Script to View",
                options=list(st.session_state.test_scripts.keys())
            )
    
            if script_id:
                script_data = st.session_state.test_scripts[script_id]
                st.code(script_data["script"], language="python")
    
                if st.button(f"Save Script {script_id}"):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    script_path = Path(self.config.get("PATHS", "testscript_output")) / f"script_{script_id}_{timestamp}.py"
                    script_path.parent.mkdir(parents=True, exist_ok=True)
    
                    with open(script_path, 'w') as f:
                        f.write(script_data["script"])
    
                    st.success(f"✅ Script saved to {script_path}")

    def render_executor_section(self):
        """Render the executor section"""
        st.markdown("## ▶️ Executor")
        folder_path = 'testcase_generator'
        # Get all json and txt files under the folder
        file_paths = glob.glob(os.path.join(folder_path, '*.txt'))
        # Optional: Just show the filenames (not full paths) in dropdown
        file_names = [os.path.basename(fp) for fp in file_paths]
        if os.listdir(folder_path):
            script_to_execute = st.selectbox(
            "Select Test Case File",
            options=range(len(file_names)),
            format_func=lambda idx: file_names[idx] if idx < len(file_names) else 'Unknown'
            )
            selected_testcase_withpath = file_paths[script_to_execute]
        else:
            st.warning("No test cases available. Please generate test cases first.")
            script_to_execute = None
        

        uploaded_script = st.file_uploader("Or upload script file", type=['py', 'txt'])
        direct_script = st.text_area("Or enter script directly:", height=200, placeholder="Enter browser automation commands...")
        # Execute button
        if st.button("Execute Script", type="primary"):
            script_content = None
            script_id = "unknown"

            if uploaded_script:
                script_content = uploaded_script.getvalue().decode()
                script_id = uploaded_script.name.replace('.*', '')
            if direct_script:
                script_content = direct_script
                script_id = f"direct_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            elif selected_testcase_withpath:
                current_directory = os.getcwd()
                script_id =  current_directory +"\\"+ selected_testcase_withpath
                with open(selected_testcase_withpath, 'r') as file:
                        script_content = file.read()

            file_path =current_directory +"\\"+"Agent_input.txt"
            with open(file_path, 'w') as file:
                file.write(script_content)
            with st.spinner("Running browser agent..."):
                try:
                    script_path = current_directory +"\\"+"agent.py"
                    print(file_path)
                    print(script_content)
                    print(script_path)
                    
                    #C:/Users/Kasi.Reddy/AppData/Local/Programs/Python/Python313/python.exe
                    result = subprocess.run(['Python', script_path], capture_output=True, text=True)
                    st.success("✅ Task executed successfully!")
                    st.subheader("Result")
                    #st.markdown(result)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    def render_reports_section(self):
        """Render the reports section"""
        st.markdown("## 📊 Reports")
        
        if st.session_state.execution_results:
            # Generate report button
            if st.button("Generate HTML Report", type="primary"):
                with st.spinner("Generating report..."):
                    report_path = self.report_generator.generate_html_report(st.session_state.execution_results)
                
                st.success(f"✅ Report generated: {report_path}")
                
                # Display report preview
                if os.path.exists(report_path):
                    with open(report_path, 'r') as f:
                        report_html = f.read()
                    
                    st.markdown("### 📄 Report Preview")
                    st.components.v1.html(report_html, height=600, scrolling=True)
                    
                    # Download button
                    with open(report_path, 'rb') as f:
                        st.download_button(
                            label="Download Report",
                            data=f.read(),
                            file_name=os.path.basename(report_path),
                            mime="text/html"
                        )
            
            # Display execution summary
            st.markdown("### 📈 Execution Summary")
            
            total_executions = len(st.session_state.execution_results)
            passed_executions = sum(1 for result in st.session_state.execution_results.values() if result["status"] == "PASSED")
            failed_executions = total_executions - passed_executions
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Executions", total_executions)
            
            with col2:
                st.metric("Passed", passed_executions)
            
            with col3:
                st.metric("Failed", failed_executions)
            
            # Detailed results
            st.markdown("### 📋 Detailed Results")
            for script_id, result in st.session_state.execution_results.items():
                with st.expander(f"Script: {script_id} - {result['status']}"):
                    st.json(result)
        else:
            st.info("No execution results available. Please execute some scripts first.")
    
    def render_git_integration_section(self):
        """Render the Git integration section"""
        st.markdown("## 🔄 Git Integration")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📁 Repository Status")
            
            if st.button("Check Git Status"):
                try:
                    status = self.git_manager.get_status()
                    st.code(status)
                except Exception as e:
                    st.error(f"Error checking Git status: {e}")
            
            # File selection for commit
            st.markdown("### 📝 Select Files to Commit")
            
            # Get list of modified files (this would need to be implemented in GitManager)
            try:
                modified_files = self.git_manager.get_modified_files()
                if modified_files:
                    selected_files = st.multiselect("Select files to commit:", modified_files)
                else:
                    st.info("No modified files found")
                    selected_files = []
            except:
                st.info("Git repository not initialized or no changes detected")
                selected_files = []
        
        with col2:
            st.markdown("### 🚀 Commit & Push")
            
            commit_message = st.text_area(
                "Commit Message:",
                value=f"Automated commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                height=100
            )
            
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                if st.button("Commit Changes"):
                    if selected_files and commit_message:
                        try:
                            self.git_manager.commit_files(selected_files, commit_message)
                            st.success("✅ Changes committed successfully")
                        except Exception as e:
                            st.error(f"❌ Commit failed: {e}")
                    else:
                        st.warning("Please select files and enter a commit message")
            
            with col2_2:
                if st.button("Push to Remote"):
                    try:
                        self.git_manager.push_changes()
                        st.success("✅ Changes pushed to remote repository")
                    except Exception as e:
                        st.error(f"❌ Push failed: {e}")
        
        # Auto-commit settings
        st.markdown("### ⚙️ Auto-Commit Settings")
        auto_commit_enabled = st.checkbox("Enable auto-commit on successful test execution")
        
        if auto_commit_enabled and st.session_state.execution_results:
            # Check if all tests passed
            all_passed = all(result["status"] == "PASSED" for result in st.session_state.execution_results.values())
            
            if all_passed:
                st.success("✅ All tests passed - Auto-commit available")
                if st.button("Auto-Commit All Changes"):
                    try:
                        self.git_manager.auto_commit_on_success()
                        st.success("✅ Auto-commit completed")
                    except Exception as e:
                        st.error(f"❌ Auto-commit failed: {e}")
            else:
                st.warning("⚠️ Some tests failed - Auto-commit disabled")
    


    def run(self):
        """Run the Streamlit application"""
        # Render header
        self.render_header()
        
        # Render sidebar and get selected page
        selected_page = self.render_sidebar()
        
        # Render selected page
        if selected_page == "📄 Embedding & Knowledge Base":
            self.render_embedding_section()
        elif selected_page == "❓ Query Knowledge Base":
            self.render_query_section()
        elif selected_page == "✨ Prompt Generation":
            self.render_prompt_generation_section()
        elif selected_page == "📝 Test Case Generator":
            self.render_testcase_generator_section()
        elif selected_page == "🔧 Test Script Generator":
            self.render_testscript_generator_section()
        elif selected_page == "▶️ Executor":
            self.render_executor_section()
        elif selected_page == "📊 Reports":
            self.render_reports_section()
        elif selected_page == "🔄 Git Integration":
            self.render_git_integration_section()



    # Main execution
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()

