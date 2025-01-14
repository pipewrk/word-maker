# META: WORD-MAKER

## Folder Structure

```plaintext
/Users/jasonnathan/Repos/word-maker
├── LICENSE
├── README.md
└── word-maker
    ├── generate.py
    └── uber_tui.py

2 directories, 4 files
```
## File: word-maker/generate.py
```python
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

```
## File: word-maker/uber_tui.py
```python
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style
import time
import random
from generate import get_unique_letters, generate_words, query_llm_to_filter_words

# Define custom style for the prompt
style = Style.from_dict({
    'question': 'ansigreen bold',   # Green color for questions
    'response': 'ansiblack bg:#ffffff',  # White color for responses (like in hacker movies)
    'hacker': 'ansired',  # Hacker-style red for certain outputs
    'cyan': 'ansicyan bold',  # Cyan for headings
    'yellow': 'ansiyellow bold',  # Yellow for highlights
})

# Hacker movie style output (with fake progress animation)
def print_hacker_style(text, delay=0.03):
    """Simulate hacker-style typing."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(0.01, delay))  # Simulate typing speed
    print("\n")

# Interactive TUI
def interactive_tui():
    # Ask for the words input
    words_input = prompt([
        ('class:question', 'Please enter the words you want to use?\n'),
        ('class:response', '')
    ], style=style)
    
    # Process unique letters from the input
    unique_letters = get_unique_letters(words_input)
    print_hacker_style(f"\nUnique letters are: {unique_letters}", delay=0.01)

    # Ask for the context input
    context_input = prompt([
        ('class:question', 'Please enter the context you\'d like to use?\n'),
        ('class:response', '')
    ], style=style)

    # Default settings
    default_repeat_letters = "yes"
    default_stopwords = "no"

    # Gather other parameters interactively using radiolist for Yes/No
    repeat_letters = radiolist_dialog(
        title="Repeat Letters?",
        text="Allow repeated letters?",
        values=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        default=default_repeat_letters  # Set default value
    ).run() == "yes"
    
    allow_stopwords = radiolist_dialog(
        title="Allow Stop Words?",
        text="Allow stop words?",
        values=[
            ("yes", "Yes"),
            ("no", "No"),
        ],
        default=default_stopwords  # Set default value
    ).run() == "yes"

    # Other inputs
    min_letters = int(prompt([
        ('class:question', 'Min Letters?\n'),
        ('class:response', '')
    ], style=style, default="5"))  # Default value for min letters

    max_letters = int(prompt([
        ('class:question', 'Max Letters?\n'),
        ('class:response', '')
    ], style=style, default="7"))  # Default value for max letters

    min_words = int(prompt([
        ('class:question', 'Min Words?\n'),
        ('class:response', '')
    ], style=style, default="50"))  # Default value for min words

    # Show the "GENERATING" effect
    print_hacker_style(f"\nGENERATING\n", delay=0.1)

    # Show the parameters
    print_hacker_style(f"Context: {context_input}", delay=0.01)
    print_hacker_style(f"Repeat Letters: {repeat_letters}", delay=0.01)
    print_hacker_style(f"Min Letters: {min_letters}", delay=0.01)
    print_hacker_style(f"Max Letters: {max_letters}", delay=0.01)
    print_hacker_style(f"Min Words: {min_words}", delay=0.01)
    print_hacker_style(f"Allow Stop Words: {allow_stopwords}", delay=0.01)

    # Generate words based on input
    generated_words = generate_words(
        unique_letters,
        min_length=min_letters,
        max_length=max_letters,
        allow_repeats=repeat_letters,
        num_words=min_words,
        allow_stopwords=allow_stopwords,
        blacklisted_words=[]
    )
    
    print_hacker_style(f"Generated words: {generated_words}", delay=0.01)
    
    print_hacker_style(f"\nFINDING CONTEXTUAL RELATED WORDS\n", delay=0.1)

    # Query the LLM with context and generated words
    formatted_output = query_llm_to_filter_words(generated_words, context_input)

    # Display the model's formatted output in hacker-style
    print_hacker_style(formatted_output, delay=0.02)

if __name__ == '__main__':
    interactive_tui()


```
## File: README.md

# word-maker
A fun word generator in python

## Git Repository

```plaintext
origin	git@github.com:jasonnathan/word-maker.git (fetch)
origin	git@github.com:jasonnathan/word-maker.git (push)
```
