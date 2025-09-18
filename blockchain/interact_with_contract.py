from web3 import Web3
import json
import os
import time
import sys

# Add parent directory to path to import other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Check connection
if not w3.is_connected():
    print("❌ Not connected to blockchain")
    exit(1)
else:
    print("✅ Connected to blockchain")

# Load ABI
abi_path = os.path.join(os.path.dirname(__file__), "EthicalValidationABI.json")
if not os.path.exists(abi_path) or os.path.getsize(abi_path) == 0:
    print("❌ ABI file missing or empty!")
    exit(1)

with open(abi_path, "r", encoding="utf-8") as f:
    abi = json.load(f)

# Set contract address - you need to update this with the correct address from Remix
contract_address = w3.to_checksum_address("0xB22764738cce7e52fe53D8DE5a1Bf105CFe6A354")
print(f"✅ Contract address set to: {contract_address}")

# Check if contract is deployed at this address
contract_code = w3.eth.get_code(contract_address)
if contract_code == b'':
    print("❌ No contract deployed at this address")
    print("Please deploy your contract in Remix and update the address in this file")
else:
    print("✅ Contract is deployed at this address")

# Set contract
contract = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.accounts[0]

def log_validation_result(question, ai_answer, is_truthful):
    try:
        # Check if contract is deployed
        contract_code = w3.eth.get_code(contract_address)
        if contract_code == b'':
            print("❌ Cannot log to blockchain: No contract deployed")
            return False
            
        tx = contract.functions.logValidation(
            question,
            ai_answer,
            is_truthful
        ).transact({'from': account})
        receipt = w3.eth.wait_for_transaction_receipt(tx)
        print("✅ Logged to blockchain. Tx hash:", w3.to_hex(tx))
        return True
    except Exception as e:
        print("❌ Error during blockchain transaction:", e)
        return False

def get_all_validations():
    try:
        # Check if contract is deployed
        contract_code = w3.eth.get_code(contract_address)
        if contract_code == b'':
            print("❌ Cannot retrieve validations: No contract deployed")
            return
            
        # Try to get the total number of validations
        total_validations = contract.functions.getTotalValidations().call()
        print(f"\n📜 Total Validations: {total_validations}\n")
        
        if total_validations == 0:
            print("No validations found.")
            return
        
        # Get each validation
        for i in range(total_validations):
            question, ai_answer, is_truthful, timestamp = contract.functions.getValidation(i).call()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            print(f"{i+1}. ❓ Q: {question}\n   🤖 A: {ai_answer}\n   ✅ Truthful? {is_truthful}\n   🕒 Time: {time_str}\n")
            
    except Exception as e:
        print("❌ Error retrieving validations:", e)
        # Fallback: try to get events with correct parameter name
        try:
            events = contract.events.ValidationLogged.get_logs(from_block=0)
            print(f"\n📜 Found {len(events)} validation events:\n")
            
            if len(events) == 0:
                print("No validation events found.")
                return
            
            for i, event in enumerate(events):
                args = event['args']
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(args['timestamp']))
                print(f"{i+1}. ❓ Q: {args['question']}\n   🤖 A: {args['aiAnswer']}\n   ✅ Truthful? {args['isTruthful']}\n   🕒 Time: {time_str}\n")
        except Exception as event_error:
            print("❌ Also failed to get events:", event_error)

# Test function to verify connection
def test_connection():
    try:
        if w3.is_connected():
            print("✅ Connected to blockchain")
            # Check if contract is deployed
            contract_code = w3.eth.get_code(contract_address)
            if contract_code == b'':
                print("❌ No contract deployed at address")
                return False
            else:
                print("✅ Contract is deployed")
                return True
        else:
            print("❌ Not connected to blockchain")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

# Initialize connection test when module is imported
if __name__ != "__main__":
    test_connection()
