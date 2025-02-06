# lotsawa_transliterator.py

from datasets import load_dataset

# Optional: custom mapping for known exceptions.
custom_map = {
    "zhendön": "གཞན་དོན",  # For example, our override for zhendön.
    # You can add more exceptions here if needed.
}

# Load the Tibetan-to-English dataset from Hugging Face
dataset = load_dataset("billingsmoore/tibetan-to-english-translation-dataset")

# We'll work with the first 10 examples for demonstration.
transliteration_map = []  # List of tuples: (phonetic phrase, Tibetan phrase)

for i in range(10):
    entry = dataset['train'][i]
    phonetic_phrase = entry['phonetic'].strip().lower()  # e.g., "go sum zhendön dzepé lha ding wön"
    tibetan_phrase = entry['tibetan'].strip()            # e.g., "སྒོ་གསུམ་གཞན་དོན་མཛད་པའི་ལྷ་སྡིངས་དབོན།།"
    print(f"Phonetic: {phonetic_phrase} → Tibetan: {tibetan_phrase}")
    transliteration_map.append((phonetic_phrase, tibetan_phrase))


def lookup_token_exact(phonetic_token):
    """
    Given a single phonetic token (for example, "go", "sum", or "yeshe"),
    search our stored mappings.
    
    If the token is found:
      - If the token is short (less than 5 characters), return the corresponding Tibetan token.
      - If the token is longer (>= 5 characters), assume it represents a compound syllable and return
        the Tibetan token at that index concatenated with the next Tibetan token.
    
    Returns the Tibetan token (with a tsek "་" appended to each syllable) or None if not found.
    """
    phonetic_token = phonetic_token.lower().strip()
    
    # Check custom mapping first.
    if phonetic_token in custom_map:
        return custom_map[phonetic_token]
    
    for phonetic_phrase, tibetan_phrase in transliteration_map:
        # Split the stored phonetic phrase into tokens.
        phonetic_tokens = phonetic_phrase.split()  # e.g., ["go", "sum", "zhendön", "dzepé", "lha", "ding", "wön"]
        if phonetic_token in phonetic_tokens:
            idx = phonetic_tokens.index(phonetic_token)
            # Split the Tibetan phrase by the Tibetan tsek "་" and remove empties.
            tibetan_tokens = [tok for tok in tibetan_phrase.split("་") if tok]
            # If the token is "long" (>=5 letters) and there is a following Tibetan token, return two tokens.
            if len(phonetic_token) >= 5 and idx + 1 < len(tibetan_tokens):
                return tibetan_tokens[idx] + "་" + tibetan_tokens[idx+1] + "་"
            elif idx < len(tibetan_tokens):
                return tibetan_tokens[idx] + "་"
    return None


def lookup_segmented(phonetic_input):
    """
    Look up the input token. (In this simple dedicated solution we assume the user enters one token.)
    Uses lookup_token_exact.
    """
    phonetic_input = phonetic_input.lower().strip()
    result = lookup_token_exact(phonetic_input)
    if result:
        return result
    return "No match found"


def transliterate_text(romanized_input):
    """
    Given a full romanized string (which may contain multiple words),
    split it into tokens, transliterate each token, and combine the results.
    """
    tokens = romanized_input.strip().split()
    tibetan_tokens = []
    for token in tokens:
        tib_token = lookup_segmented(token)
        tibetan_tokens.append(tib_token)
    # Combine the transliterated tokens (here we use a space; adjust if needed)
    return " ".join(tibetan_tokens)


# For testing:
if __name__ == '__main__':
    test_inputs = ["go", "sum", "zhendön", "yeshe", "semchen"]
    for token in test_inputs:
        tibetan_output = lookup_segmented(token)
        print(f"{token} → {tibetan_output}")
    # Testing the full function:
    full_text = "yeshe chenden"
    print(f"Full transliteration of '{full_text}' → {transliterate_text(full_text)}")
