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
