from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from src.config_manager import ConfigManager
from src.logger import log, LoggerMixin
from datetime import datetime
from typing import Dict, Any



load_dotenv()


import asyncio

def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None

        
api_key = "AIzaSyDpYpDFjcWk6AB3ru6wGliSSVv0q6E8LU4" #os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


async def main():

    file_path = R'C:\Python\Agent_python_automation_framework\Agent_input.txt'
    file_string = read_file_to_string(file_path)
    taststr = file_string 
    print(taststr)
    	
    agent = Agent(
        task= taststr,
		llm=llm,
		max_actions_per_step=4,
		#browser=browser,
	)

    result = await agent.run()
asyncio.run(main())

