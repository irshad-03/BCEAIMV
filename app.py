from ai_model.factspeak_ai import get_fact_based_answer
from validator.truth_checker import check_truth
from blockchain.interact_with_contract import log_validation_result, get_all_validations
import wikipedia

def main():
    print("🧠 Welcome to FactSpeak AI Validator!")
    
    while True:
        print("\nChoose an option:")
        print("1. Ask a question and validate")
        print("2. View all validations")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            question = input("\nEnter your question: ")
            
            # Get context from Wikipedia
            try:
                context = wikipedia.summary(question, sentences=2)
                print(f"\n📚 Context from Wikipedia:\n{context}")
            except Exception as e:
                print(f"⚠️ Could not fetch Wikipedia context: {e}")
                context = question  # Fallback to using question as context
            
            # Step 1: Get AI answer
            ai_answer = get_fact_based_answer(question, context)
            print(f"\n🤖 FactSpeak AI Answer:\n{ai_answer}\n")
            
            # Step 2: Validate truthfulness
            is_truthful, validation_message = check_truth(question, ai_answer)
            print(f"✅ Validation Result: {validation_message}\n")
            
            # Step 3: Log to blockchain
            log_validation_result(question, ai_answer, is_truthful)
            
        elif choice == "2":
            get_all_validations()
            
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
