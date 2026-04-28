from smolagents import InferenceClientModel, ToolCallingAgent, WebSearchTool, LiteLLMModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

NVIDIA_KEY = os.getenv('NVIDIA_NIM_KEY')

try:    
    response = requests.get("http://localhost:11434/v1/models")
    if response.status_code == 200:
        print("[INFO] Local Ollama service is ONLINE.")
    else:
        print("[WARNING] Local Ollama service is OFFLINE. Local fallback will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to local Ollama service. Local fallback will fail.")


try:
    response = requests.get("https://integrate.api.nvidia.com/v1/models", headers={"Authorization": f"Bearer {NVIDIA_KEY}"})
    if response.status_code == 200:
        print("[INFO] NVIDIA API service is ONLINE.")
    else:
        print("[WARNING] NVIDIA API service is OFFLINE. Secondary engine will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to NVIDIA API service. Secondary engine will fail.")


try:
    response = requests.get("https://api.groq.com", headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"})
    if response.status_code == 200:
        print("[INFO] GROQ API service is ONLINE.")
    else:
        print("[WARNING] GROQ API service is OFFLINE. Primary engine will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to GROQ API service. Primary engine will fail.")         

primary_engine = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant"
)

local_engine = LiteLLMModel(
    model_id ="ollama/llama3.1:8b",
    api_base="http://localhost:11434",
)

secondary_engine = LiteLLMModel(
    model_id="hosted_vllm/meta/llama-3.1-70b-instruct",
    api_base="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_KEY,
)
agent = ToolCallingAgent(tools=[WebSearchTool()], model=local_engine, max_steps=3)

agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")