# JJN-INFO: WORD-MAKER

---

### **Purpose**

WORD-MAKER is a playful yet practical project for generating meaningful words from a given set of input letters. It uses AI, natural language processing (NLP), and customizable parameters to create words and filter them based on specific contexts. This tool is perfect for exploring creative ideas, generating word games, or finding contextually relevant terms.

---

## **Folder Structure**

```plaintext
/Users/jasonnathan/Repos/word-maker
├── LICENSE             # License for the project
├── README.md           # Brief description and usage examples
└── word-maker
    ├── generate.py     # Core logic for word generation and filtering
    └── uber_tui.py     # Interactive terminal-based user interface (TUI)

2 directories, 4 files
```

---

## **File Breakdown**

### **1. File: `generate.py`**

#### **Overview**
This script contains the core logic for:
- Generating words based on a set of input letters.
- Validating words using the NLTK corpus and SpellChecker.
- Filtering words using an AI model (via Ollama) based on contextual relevance.

#### **Key Functions**
1. **Letter Extraction**:
   - **`get_unique_letters(input_string)`**:
     - Extracts unique letters from a string, ignoring special characters.
     - Returns a sorted list of unique letters.

2. **Word Validation**:
   - **`can_form_word(word, letters, allow_repeats)`**:
     - Checks if a word can be formed using the available letters, with or without repeats.

3. **Word Generation**:
   - **`generate_words(letters, ...)`**:
     - Generates valid words based on:
       - Minimum and maximum length.
       - Inclusion or exclusion of stopwords.
       - Blacklisted words.

4. **AI Filtering**:
   - **`query_llm_to_filter_words(words_list, context, model)`**:
     - Uses **Ollama** to filter generated words based on a user-defined context.

#### **Purpose**
Provides the foundational logic for creating and refining word lists using both traditional NLP techniques and AI-driven contextual analysis.

#### **Example Usage**
```python
# Generate words
input_string = "Jason Nathan"
unique_letters = get_unique_letters(input_string)
generated_words = generate_words(unique_letters, min_length=3, max_length=7)

# Filter words using AI
context = "words related to technology"
filtered_words = query_llm_to_filter_words(generated_words, context)
print(filtered_words)
```

---

### **2. File: `uber_tui.py`**

#### **Overview**
This script provides a terminal-based user interface (TUI) for interacting with the word generator. It offers a hacker-movie-style experience with custom styling and animations.

#### **Key Features**
1. **Interactive Inputs**:
   - Asks users for input strings, contexts, and parameters via prompts and dialogs.

2. **Visual Effects**:
   - Simulates typing with "hacker-style" animations using `print_hacker_style`.

3. **Parameter Configuration**:
   - Allows users to configure:
     - Minimum and maximum word lengths.
     - Number of words to generate.
     - Whether to allow repeated letters or stopwords.

4. **Word Generation and Filtering**:
   - Integrates with `generate.py` to generate and filter words.
   - Displays results in a fun, engaging manner.

#### **Purpose**
Transforms the word-generation process into an interactive and entertaining experience, making it more accessible and enjoyable.

#### **Example Usage**
Run the script and follow the prompts:
```bash
python uber_tui.py
```

---

### **File: README.md**

#### **Overview**
Provides a high-level summary of the project. Minimal in content, it briefly describes the tool as a word generator in Python.

---

## **How It Works**

### **Workflow**

1. **Input Processing**:
   - Extract unique letters from user input.
   - Optionally define contexts and blacklist specific words.

2. **Word Generation**:
   - Validate and generate words based on:
     - Length constraints.
     - Letter availability.
     - Stopword inclusion/exclusion.

3. **AI Filtering**:
   - Refine generated words by querying a model for contextually relevant terms.

4. **Interactive Mode**:
   - Use `uber_tui.py` for an interactive experience.
   - Configure parameters dynamically through the terminal.

---

### **Key Dependencies**

- **Ollama**: AI-driven contextual word filtering.
- **NLTK**: NLP library for word validation and stopword handling.
- **SpellChecker**: For additional dictionary-based validation.
- **Prompt Toolkit**: For building the terminal-based interface.

---

### **Example Workflow**

1. **Input**:
   - "Jason Nathan"
2. **Unique Letters**:
   - `['a', 'h', 'j', 'n', 'o', 's', 't']`
3. **Generated Words**:
   - `['nation', 'aston', 'jonah', 'host', 'john']`
4. **Filtered Words (Context: "Law")**:
   - `['nation', 'host']`

---

### **Notes**

WORD-MAKER is as much about fun as it is about functionality. The integration of a playful TUI and AI filtering adds an engaging twist to what might otherwise be a simple utility. Ideal for exploring creative wordplay or testing the limits of AI-powered contextual understanding.