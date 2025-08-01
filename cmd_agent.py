<<<<<<< HEAD
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


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


api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


#llm = ChatOpenAI(model="gpt-4o")


async def main():

    file_path = R'C:\Python\python_automation_framework\report.txt'
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
    print(result)

asyncio.run(main())




=======
from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr


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


api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


#llm = ChatOpenAI(model="gpt-4o")


async def main():

    file_path = R'C:\Python\python_automation_framework\report.txt'
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
    print(result)

asyncio.run(main())




>>>>>>> 765b006 (Updated)
