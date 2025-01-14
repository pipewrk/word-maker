import ollama
from nltk.corpus import words, stopwords
from spellchecker import SpellChecker

# Ensure the stopwords and words corpus are available
try:
    stop_words = set(stopwords.words('english'))
    word_list = set(words.words())
except LookupError:
    import nltk
    nltk.download('stopwords')
    nltk.download('words')
    stop_words = set(stopwords.words('english'))
    word_list = set(words.words())

# Initialize SpellChecker for dictionary-based validation
spell = SpellChecker()

# Function to get unique letters from a string
def get_unique_letters(input_string):
    """
    Extracts unique letters from the input string, ignoring spaces and special characters.
    
    Args:
    input_string (str): The string to extract letters from.
    
    Returns:
    list: A sorted list of unique letters.
    """
    return sorted(set(filter(str.isalpha, input_string.lower())))

# Check if a word can be formed using the available letters
def can_form_word(word, letters, allow_repeats):
    """
    Checks if a word can be formed using the available letters.
    
    Args:
    word (str): The word to check.
    letters (list): The available letters.
    allow_repeats (bool): Whether repeated letters are allowed.
    
    Returns:
    bool: True if the word can be formed, False otherwise.
    """
    word_letter_counts = {letter: word.count(letter) for letter in set(word)}
    
    if allow_repeats:
        # If repeats are allowed, check that all letters in the word are part of the available set
        return set(word).issubset(set(letters))
    else:
        # If repeats are not allowed, ensure that the letter counts in the word do not exceed what's in the available letters
        return all(word_letter_counts[letter] <= letters.count(letter) for letter in word_letter_counts)

# Main function to generate words from a valid dictionary
def generate_words(letters, min_length=3, max_length=7, num_words=50, allow_repeats=True, allow_stopwords=True, blacklisted_words=None):
    """
    Generate valid anagram-like words using the provided letters and word criteria.
    
    Args:
    letters (list): Available letters.
    min_length (int): Minimum word length.
    max_length (int): Maximum word length.
    num_words (int): Number of words to generate.
    allow_repeats (bool): Whether repeated letters are allowed.
    allow_stopwords (bool): Whether to include stopwords.
    blacklisted_words (list): Words to exclude from the results.
    
    Returns:
    list: List of filtered valid words.
    """
    if blacklisted_words is None:
        blacklisted_words = []

    # We double the number of words we want to generate to avoid aggressive filtering cutting the list too short
    target_word_count = num_words * 2

    valid_words = [
        word for word in word_list
        if set(word).issubset(set(letters)) and
        min_length <= len(word) <= max_length and
        can_form_word(word, letters, allow_repeats) and
        (allow_stopwords or word not in stop_words) and
        word not in blacklisted_words
    ]

    # Limit the results to the requested number of words after filtering
    return valid_words[:num_words]

# Function to query LLM to filter words based on a given context
def query_llm_to_filter_words(words_list, context, model="mistral-nemo:latest"):
    """
    Queries the LLM to filter the generated words based on a given context.
    
    Args:
    words_list (list): List of words generated.
    context (str): The context for the LLM to filter words (e.g., "words related to technology").
    model (str): The model to use for querying the LLM (default: mistral-nemo:latest).
    
    Returns:
    list: The list of words that fit the context provided by the LLM.
    """
    
    # Query the LLM to filter words based on the context
    response = ollama.chat(model, messages=[
      {'role': 'system', 'content': f"The user will provide you with a list of words. Please filter and return the words that are most related to the following context: '{context}'."},
      {'role': 'user', 'content': f"Here is a list of words: {', '.join(words_list)}.\n"},
    ])
    
    # Return filtered words as a list
    return response['message']['content'].strip().split(", ")

# Example usage
if __name__ == "__main__":
    # Input string from which to extract unique letters
    input_string = "Simran Kaur Jason Joseph Nathan"
    
    # Get unique letters from the input string
    unique_letters = get_unique_letters(input_string)
    print(f"Unique letters: {unique_letters}")
    
    # Set parameters for word generation
    min_length = 3
    max_length = 7
    num_words = 50
    allow_repeats = True
    allow_stopwords = False
    blacklisted_words = ['auntie', 'stoat']

    # Generate words based on criteria
    generated_words = generate_words(
        unique_letters,
        min_length=min_length,
        max_length=max_length,
        allow_repeats=allow_repeats,
        num_words=num_words,
        allow_stopwords=allow_stopwords,
        blacklisted_words=blacklisted_words
    )
    
    # Print the final list of generated valid words
    print(f"Generated valid words: {generated_words}")
    
    # Query the LLM for filtering words based on context
    context = "words related to AI, Law, Forensics"
    filtered_words = query_llm_to_filter_words(generated_words, context)
    
    # Print the filtered list of words based on the context
    print(f"Filtered words based on context '{context}': {filtered_words}")

