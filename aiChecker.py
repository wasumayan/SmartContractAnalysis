from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os

# check
if not os.path.exists("input.txt"):
    raise FileNotFoundError("input.txt not found!")

# Set your API key
os.environ["OPENAI_API_KEY"] = "BLANK"
# Initialize chat model
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.7)

system_prompt = """
You are a secure smart contract auditor and Solidity expert. Your task is to help developers remediate vulnerabilities in their Solidity code. 

Given a code snippet and a description of the vulnerability (including an SWC-ID where available), do the following:
- Identify where and why the vulnerability exists.
- Suggest a corrected version of the code that fixes the issue, following security best practices (e.g., checks-effects-interactions pattern, access control, etc.).
- Ensure your fix is syntactically valid Solidity and conservatively secure.
- If applicable, apply common defenses such as using `nonReentrant` modifiers, `require` statements, or safe math patterns.
- Do NOT hallucinate fixes or invent variables not shown in the snippet.
- Keep external interfaces and function signatures unchanged unless absolutely required by the fix.
- Return only the fixed code unless specifically asked for explanations.

Example input:
<code>
function withdraw(uint amount) public {{
require(balances[msg.sender] >= amount);
(bool success, ) = msg.sender.call{{value: amount}}("");
require(success);
balances[msg.sender] -= amount;
}}
</code>

<bug>
SWC-107: Reentrancy vulnerability. The external call occurs before state update.
</bug>

Your output should look like this:

```solidity
function withdraw(uint amount) public nonReentrant {{
require(balances[msg.sender] >= amount);
balances[msg.sender] -= amount;
(bool success, ) = msg.sender.call{{value: amount}}("");
require(success);
}}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{text}")
    ])

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt)
# Read Input
with open("input.txt", "r") as f:
    file_input = f.read()
    
# Run the chain
response = chain.invoke({"text": file_input})
with open("output.txt", "w") as file:
    file.write(response["text"])
