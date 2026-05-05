from smolagents import CodeAgent, Tool, LiteLLMModel, tool, DuckDuckGoSearchTool, FinalAnswerTool
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GROQ_KEY = os.getenv('GROQ_API_KEY')
NVIDIA_KEY = os.getenv('NVIDIA_NIM_KEY')

if not GROQ_KEY:    
    raise ValueError("[FATAL ERROR] GROQ_API_KEY missing from vault.")
print("[INFO] Successfully loaded GROQ_API_KEY from vault.")

if not NVIDIA_KEY:
    raise ValueError("[FATAL ERROR] NVIDIA_NIM_KEY missing from vault.")
print("[INFO] Successfully loaded NVIDIA_NIM_KEY from vault.")

print("[INFO] Initializing CodeAgent with LiteLLMModel and tools...")

#checks if Groq is available.

try:
    response = requests.get("https://api.groq.com", headers={"Authorization": f"Bearer {GROQ_KEY}"})
    if response.status_code == 200:
        print("[INFO] GROQ API service is ONLINE.")
    else:
        print("[WARNING] GROQ API service is OFFLINE. Primary engine will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to GROQ API service. Primary engine will fail.")

#Checks if NVIDIA is available.
try:
    response = requests.get("https://integrate.api.nvidia.com/v1/models", headers={"Authorization": f"Bearer {NVIDIA_KEY}"})
    if response.status_code == 200:
        print("[INFO] NVIDIA API service is ONLINE.")
    else:
        print("[WARNING] NVIDIA API service is OFFLINE. Secondary engine will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to NVIDIA API service. Secondary engine will fail.")

print(f"[INFO] GROQ Vault Status: {'ARMED' if GROQ_KEY else 'EMPTY'}")
print(f"[INFO] NVIDIA Vault Status: {'ARMED' if NVIDIA_KEY else 'EMPTY'}")

# Slices the first 4 chars, adds stars, and slices the last 4 chars
masked_groq = GROQ_KEY[:4] + "*" * (len(GROQ_KEY) - 8) + GROQ_KEY[-4:]  
masked_nvidia = NVIDIA_KEY[:4] + "*" * (len(NVIDIA_KEY) - 8) + NVIDIA_KEY[-4:]

print(f"[INFO] GROQ_API_KEY: {masked_groq}")
print(f"[INFO] NVIDIA_NIM_KEY: {masked_nvidia}")

search_tool = DuckDuckGoSearchTool()

@tool
def web_scraper(url: str) -> str:
    """Scrapes the text content from a given web URL.
    
    Args:
        url: The full http/https URL of the website to scrape.
    """
    response = requests.get(url)
    return response.text[:2000]


primary_engine = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant",
)

secondary_engine = LiteLLMModel(    
    model_id="hosted_vllm/meta/llama-3.1-70b-instruct",
    api_base="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_KEY,
)

agent = CodeAgent(
    model = primary_engine,
    tools = [search_tool, web_scraper, FinalAnswerTool()],
    max_steps=3,
    add_base_tools=True,
)
response = agent.run(
    "Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering."
)
print(response)