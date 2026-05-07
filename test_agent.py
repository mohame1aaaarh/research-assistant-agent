import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agent import get_agent

if __name__ == "__main__":
    agent = get_agent()
    response = agent.run("مرحبا")
    print("AGENT RESPONSE:")
    if hasattr(response, 'content'):
        print(response.content)
    else:
        print(response)
