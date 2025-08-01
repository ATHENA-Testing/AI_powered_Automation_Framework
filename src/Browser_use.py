import asyncio
import sys
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
import streamlit as st
import os
from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use.browser import BrowserProfile, BrowserSession
from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin


class GeminiLLMWrapper():
    #self, config: ConfigManager
    def __init__(self):

#    def __init__(self, model_name, api_key):
        model_name='gemini-2.0-flash-exp'
        api_key="AIzaSyDpYpDFjcWk6AB3ru6wGliSSVv0q6E8LU4"  # Replace with your actual key
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=SecretStr(api_key),
            temperature=0.7
        )
        self.provider = "google"
        self.model = model_name
        self.model_name = model_name
    
    async def ainvoke(self, prompt):
        return await asyncio.to_thread(self.llm.invoke, prompt)

# Async function to run the browser agent
async def run_browser_task(task):
    browser_profile = BrowserProfile(
	# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir='~/.config/browseruse/profiles/default',
    headless=False,
    )
    browser_session = BrowserSession(browser_profile=browser_profile)

    try:
        llm = GeminiLLMWrapper()
            # model_name='gemini-2.0-flash-exp',
            # api_key="AIzaSyDpYpDFjcWk6AB3ru6wGliSSVv0q6E8LU4"  # Replace with your actual key
            # model_name='gemini-pro',  # Using a stable model; replace if needed
            # api_key=GOOGLE_API_KEY
        agent = Agent(
            task=task,
            llm=llm,
            max_actions_per_step=4,
            verbose=True,  # Enable verbose output for debugging
            browser_session=browser_session,
        )

        result = await agent.run()
        #await browser_session.close()
        return result
    except Exception as e:
        raise Exception(f"Agent execution failed: {str(e)}")

# Sync wrapper for Streamlit
def run_task_sync(task):
    try:
        return asyncio.run(run_browser_task(task))
    except Exception as e:
        raise e


