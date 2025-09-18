from web3 import Web3
import wikipedia
import json
import time
import os
import sys

# Add parent folder to import AI/validator code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_model.factspeak_ai import get_fact_based_answer
from validator.truth_checker import check_truth

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    raise Exception("❌ Unable to connect to Ganache. Make sure it's running!")

# Load contract ABI
abi_path = os.path.join(os.path.dirname(__file__), "EthicalValidationABI.json")

if not os.path.exists(abi_path):
    raise FileNotFoundError(f"❌ ABI file not found at: {abi_path}")
if os.path.getsize(abi_path) == 0:
    raise ValueError("❌ ABI file is empty.")

with open(abi_path, "r", encoding="utf-8") as f:
    abi = json.load(f)
    print("✅ ABI loaded successfully.")

# Contract
contract_address = web3.to_checksum_address("0x9231b35bA1143f3a61CDA79fA386D562B1b09b83")
contract = web3.eth.contract(address=contract_address, abi=abi)

account_address = web3.eth.accounts[0]
private_key = "0x1b8c0867f8819e6b67361c1693fc3c217370a266f166bc147d781f1f18551e1f"  # ⚠️ Not secure

def log_validation_result(question, ai_answer, is_truthful):
    tx = contract.functions.logValidation(
        question,
        ai_answer,
        is_truthful
    ).build_transaction({
        'from': account_address,
        'nonce': web3.eth.get_transaction_count(account_address),
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("✅ Logged to blockchain. Tx hash:", web3.to_hex(tx_hash))
    time.sleep(2)

def get_all_validations():
    total = contract.functions.getTotalValidations().call()
    print(f"\n📜 Total Validations: {total}\n")
    for i in range(total):
        q, a, tf, ts = contract.functions.getValidation(i).call()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        print(f"{i+1}. ❓ Q: {q}\n   🤖 A: {a}\n   ✅ Truthful? {tf}\n   🕒 Time: {time_str}\n")

# Main program
if __name__ == "__main__":
    print("\n=== Blockchain-Based Ethical AI Validator ===")
    choice = input("Choose action: [1] Ask and validate  [2] View all validations\n> ")

    if choice == "1":
        question = input("\n❓ Enter your question:\n> ")

        try:
            context = wikipedia.summary(question, sentences=2)
            print("\n📚 Context from Wikipedia:\n", context)
        except Exception as e:
            print(f"⚠️ Could not fetch Wikipedia context: {e}")
            context = question

        print("\n🤖 Getting answer from FactSpeak AI...")
        ai_answer = get_fact_based_answer(question, context)

        print(f"\n🧠 Answer: {ai_answer}")

        is_truthful, message = check_truth(question, ai_answer)
        print(f"\n🔍 Validation result: {message}")

        log_validation_result(question, ai_answer, is_truthful)

    elif choice == "2":
        get_all_validations()
    else:
        print("❌ Invalid option. Try again.")
