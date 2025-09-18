import wikipedia

def check_truth(question, ai_answer):
    try:
        # Get summary from Wikipedia for the given question/topic
        wiki_summary = wikipedia.summary(question, sentences=2)
        
        # Convert both texts to lowercase for basic comparison
        ai_text = ai_answer.lower()
        wiki_text = wiki_summary.lower()

        # Check if AI's answer is mostly contained in Wikipedia summary
        if ai_text in wiki_text or wiki_text in ai_text:
            return False, "Answer is consistent with Wikipedia."
        else:
            return True, "Answer differs from Wikipedia."

    except Exception as e:
        return False, f"Error accessing Wikipedia: {str(e)}"
