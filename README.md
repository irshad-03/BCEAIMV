BCEAIMV: Blockchain-for Ethical AI Model Validation
BCEAIMV is an innovative framework designed to solve the problem of AI hallucinations and lack of accountability. It validates the factual accuracy of AI-generated responses using decentralized verification and logs the results immutably on a blockchain to ensure a transparent and auditable record of AI performance.




🚀 Key Features

Fact-Based Q&A: Utilizes FactSpeak AI (DistilBERT-based) to generate context-aware answers to user queries.



Automated Truth Verification: Integrates with external knowledge bases (Wikipedia) to cross-reference and validate AI responses for factual consistency.





Immutable Blockchain Logging: Every validation verdict is recorded on the Ethereum blockchain via smart contracts, providing a permanent audit trail.



Transparent Metrics: Includes functions to retrieve the total number of validations and specific historical records directly from the ledger.

🛠️ Technical Architecture
1. AI Layer (factspeak_ai.py)

Model: distilbert-base-cased-distilled-squad from Hugging Face.



Function: Processes questions using retrieved context to provide a concise answer.

2. Validation Layer (truth_checker.py)

Verification: Uses the wikipedia API to fetch ground-truth context.



Logic: Compares the AI output against the verified context to generate a "Truthful" or "Differing" verdict.



3. Blockchain Layer (EhticalValidation.sol)

Smart Contract: Written in Solidity, it stores the question, AI response, truthfulness flag, and a timestamp.


Integration: Python scripts interact with the contract using Web3.py via local Ethereum providers like Ganache.

💻 Tech Stack

Programming: Python, Solidity.



AI Frameworks: Hugging Face Transformers, Wikipedia-API.



Blockchain: Ethereum, Web3.py, Ganache, Remix.


Libraries: NumPy, Pandas.

📁 Repository Structure
Plaintext

├── ai_model/

│   └── factspeak_ai.py      # Q&A logic using DistilBERT 

├── validator/

│   └── truth_checker.py     # Logic for Wikipedia verification 

├── blockchain/

│   ├── EhticalValidation.sol # Smart contract for logging results 

│   ├── EthicalValidationABI.json # Compiled contract ABI

│   └── interact_with_contract.py # Web3.py interaction script

└── app.py                   # Main CLI entry point for the system 
🔧 Installation & Setup
Prerequisites: Install Ganache to run a local blockchain.

Install Dependencies:

Bash

pip install web3 transformers wikipedia torch
Deploy Contract: Deploy EhticalValidation.sol in Remix or Truffle and update the contract_address in your Python scripts.

Run the Application:

Bash

python app.py
