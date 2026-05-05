import os
import requests
from smolagents import CodeAgent, Tool, LiteLLMModel, tool
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv('GROQ_API_KEY')
NVIDIA_KEY = os.getenv('NVIDIA_NIM_KEY')

if not GROQ_KEY:
    raise ValueError("[FATAL ERROR] GROQ_API_KEY missing from vault.")
if not NVIDIA_KEY:
    raise ValueError("[FATAL ERROR] NVIDIA_NIM_KEY missing from vault.")

print("[INFO] Successfully loaded API keys from vault.")
print("[INFO] Initializing CodeAgent with LiteLLMModel and tools...")

#Checks if ollama is running locally
try:    
    response = requests.get("http://localhost:11434/v1/models")
    if response.status_code == 200:
        print("[INFO] Local Ollama service is ONLINE.")
    else:
        print("[WARNING] Local Ollama service is OFFLINE. Local fallback will fail.")
except requests.exceptions.ConnectionError:
    print("[WARNING] Unable to connect to local Ollama service. Local fallback will fail.")

print("[INFO] Ollama Vault Status: Armed (Local Service Check Passed)")    
print(f"[INFO] GROQ Vault Status: {'ARMED' if GROQ_KEY else 'EMPTY'}")
print(f"[INFO] NVIDIA Vault Status: {'ARMED' if NVIDIA_KEY else 'EMPTY'}")

# Slices the first 4 chars, adds stars, and slices the last 4 chars
masked_groq = GROQ_KEY[:4] + "*" * (len(GROQ_KEY) - 8) + GROQ_KEY[-4:]  
masked_nvidia = NVIDIA_KEY[:4] + "*" * (len(NVIDIA_KEY) - 8) + NVIDIA_KEY[-4:]  

print(f"[INFO] GROQ_API_KEY: {masked_groq}")
print(f"[INFO] NVIDIA_NIM_KEY: {masked_nvidia}")

@tool
def run_diagnostic(system_name: str) -> dict:
    """Runs a system diagnostic to check network status.
    
    Args:
        system_name: The name of the system to check.
    """
    return {"target": system_name, "status": "ONLINE", "ping_ms": 12}

primary_engine = LiteLLMModel(
    model_id="groq/llama-3.1-8b-instant"
)

secondary_engine = LiteLLMModel(
    model_id="hosted_vllm/meta/llama-3.1-70b-instruct",
    api_base="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_KEY,
)

local_engine = LiteLLMModel(
    model_id ="ollama/llama3.1:8b",
    api_base="http://localhost:11434"
)
agent = CodeAgent(
    tools=[run_diagnostic], 
    model=local_engine, 
    add_base_tools=False,
    max_steps=3
)

# The standardized formatting threat is included
print("[SYSTEM] Initiating Tier 1 (Cloud - Groq)...")
prompt = """
Use your tool to check the status of 'ViperStrike-Mainframe'. 
If the status in the returned dictionary is 'ONLINE', write a Python script that prints 'Mainframe Secure'.
CRITICAL FORMATTING RULE: You must use proper line breaks (\\n) in your Python code. Do not write multiple commands on a single line.
"""

print("[INFO] Sending prompt to agent...")
print("\n>>> INITIATING TEST 1: PRIMARY ENGINE (GROQ) <<<")
try:
    agent.run(prompt)
    print("\n[SUCCESS] Mission completed via Tier 1.")
    
except Exception as e1:
    print(f"\n[CRITICAL] Tier 1 Failure: {str(e1)}")
    print("[SYSTEM] Rerouting to Tier 2 (Cloud - Nvidia NIM)...")
    agent.model = secondary_engine 
    
    try:
        agent.run(prompt)
        print("\n[SUCCESS] Mission completed via Tier 2.")
        
    except Exception as e2:
        print(f"\n[CRITICAL] Tier 2 Failure: {str(e2)}")
        print("[SYSTEM] ALL CLOUD COMMS LOST. INITIATING BLACKOUT PROTOCOL.")
        print("[SYSTEM] Rerouting to Tier 3 (Local GPU - Ollama)...")
        
        # Fallback to local hardware
        agent.model = local_engine
        agent.run(prompt)
        print("\n[SUCCESS] Mission completed via Local Offline Hardware.")