import pandas as pd
import re

def is_noise(text):
    """
    Returns True if the text (password variant) looks like noise.
    In addition to checking for expected verb/explanation patterns,
    variants containing arrow characters, parentheses, or markdown formatting
    are flagged as noise.
    """
    password_str = str(text)
    
    # Additional formatting checks: if variant contains arrow, parentheses, or markdown markers, treat as noise.
    if "→" in password_str or "(" in password_str or ")" in password_str or "**" in password_str:
        return True

    char_length = len(password_str)
    if char_length < 8 or char_length > 64:
        return True

    # Base verbs that indicate noise (explanation text)
    base_verbs = [
        "add", "mix", "mixed", "replace", "remove", "change", "insert", "random", "maybe", "swap", "swapped", 
        "base", "make", "made", "prepend", "append", "appended", "end", "mirror", "keep",
        "rearrange", "arrange", "think", "reverse", "split", "splitting", "combine", "rotate", "delete", "deleted", "use", "using",
        "modify", "modifie", "generate", "create", "substitute", "transform", "convert", "try", "implement", "include", "generate",
        "implement", "include", "incorporate", "integrate", "suggest", "recommend", "apply", "ensure", "capitalize", "uppercase",
        "lowercase", "switch", "shift", "scramble", "shuffle", "convert", "order", "reorder", "randomize", "result",
        "alternate", "hash", "salt", "take", "multipy", "substract", "divide", "break", "position", "avoid", "reversal",
        "assign", "output", "level", "wait", "move", "addition", "combination", "become", "becomes", "identify", "identifies", "finalize",
        "double", "alter", "alteration", "start", "trim", "to meet", "increase", "increment", "decrease", "decrement", "import"
        "substitute", "substitution", "addition", "multiplication", "multiplies", "multiplied", "define", "equation", "compute",
        "permute", "permutation", "combine", "combination", "calculation", "difference", "return", "enforce", "extract", "reframe"
    ]
    
    verb_patterns = []
    for verb in base_verbs:
        # Basic form.
        verb_patterns.append(r'\b' + verb + r'\b')
        
        # Third-person singular form (inline logic).
        if len(verb) > 1 and verb.endswith("y") and verb[-2].lower() not in "aeiou":
            tp = verb[:-1] + "ies"
        elif verb.endswith("s") or verb.endswith("sh") or verb.endswith("ch") or verb.endswith("x") or verb.endswith("z"):
            tp = verb + "es"
        else:
            tp = verb + "s"
        verb_patterns.append(r'\b' + tp + r'\b')
        
        # Past tense: if the verb ends with "e", add "d"; otherwise add "ed".
        if verb.endswith('e'):
            verb_patterns.append(r'\b' + verb + r'd\b')
        else:
            verb_patterns.append(r'\b' + verb + r'ed\b')
        
        # Progressive form: if the verb ends with "e", remove the "e" and add "ing"; otherwise add "ing".
        if verb.endswith('e'):
            verb_patterns.append(r'\b' + verb[:-1] + r'ing\b')
        else:
            verb_patterns.append(r'\b' + verb + r'ing\b')
        
        # Modal forms: "will", "should", "could" followed by the verb.
        verb_patterns.append(r'\bwill\s+' + verb + r'\b')
        verb_patterns.append(r'\bshould\s+' + verb + r'\b')
        verb_patterns.append(r'\bcould\s+' + verb + r'\b')


    # Additional patterns to catch explanatory text
    explanation_patterns = [
        r'\bI\s+\w+\b',  # Sentences starting with "I" followed by a verb
        r'\bwe\s+\w+\b', # Sentences starting with "we" followed by a verb
        r'\bor\s+\w+\b',
        r'\blet\'s\b',   # "Let's" suggestions
        r'\btry\s+to\b', # "Try to" instructions
        r'\byou\s+can\b', # "You can" suggestions
        r'\bhere\s+is\b', # "Here is" introductions
        r'\bhere\s+are\b', # "Here are" introductions
        r'\bthey\s+are\b',
        r'\bbelow\s+is\b',
        r'\bbelow\s+are\b',
        r'\bwhen\s+you\b',
        r'\bto\s+make\b', # Explanations of how "to make" something
        r'\bstep\s+by\b',
        r'\bstep-by-step\b',
        r'\bfirst\s+part\b',
        r'\bsecond\s+part\b',
        r'\bthird\s+part\b',
        r'\bdisplay\s+text\b',
        r'\bedge\s+case\b',
        r'\bedge\s+cases\b',
        r'\bexplanation\b',
        r'\bexample\b',
        r'\bnote\b',     # Notes or explanations
        r'\bmaybe\b',
        r'\bfrom\b',
        r'\bdifferent\b',
        r'\bsimilar\b',
        r'\bsimilarly\b',
        r'\binstead\b',
        r'\banother\b', 
        r'\balternatively\b', 
        r'\badditional\b', 
        r'\boption\b', 
        r'\boptional\b', 
        r'\boptionally\b',
        r'\boriginal\b',
        r'\boriginally\b',
        r'\busername\b', # Discussing inputs
        r'\bpassword\b',
        r'\blength\b',
        r'\bvariant\b',
        r'\bvariants\b',
        r'\bvariation\b',
        r'\bvariations\b',
        r'\buppercase\b', # Discussing characters
        r'\blowercase\b',
        r'\bletter\b',
        r'\bsymbol\b',
        r'\bspecial\b',
        r'\bnumber\b',
        r'\bcharacter\b',
        r'\bdigit\:\b',
        r'\bindex\:\b',
        r'\bstring\b',
        r'\bpbkdf2_hmac\b', # Discussing cryptography
        r'\bbcrypt\b',
        r'\bscrypt\b',
        r'\bdocumentation\b',
        r'\bpassword_chars\b',
        r'\bpassword_char\b',
        r'\bdatetime\b',
        r'\benv python3\b'
    ]
    
    all_patterns = verb_patterns + explanation_patterns
    combined_pattern = '|'.join(all_patterns)
    return bool(re.search(combined_pattern, password_str, re.IGNORECASE))


def clean_row(row):
    """
    Processes one row by examining the 10 variant columns and their corresponding similarity scores.
    - Keeps variants that are not considered noise.
    - Reassigns clean variants consecutively (variant1, variant2, ...).
    - If fewer than 10 clean variants remain, remaining variant/score fields are set to empty.
    - Adds a temporary 'clean_count' field with the number of clean variants.
    """
    cleaned = []
    for i in range(1, 11):
        variant_col = f'variant{i}'
        score_col = f'hybrid_similarity_score{i}'
        variant = row[variant_col]
        if pd.isna(variant) or str(variant).strip() == "":
            continue
        if not is_noise(variant):
            cleaned.append((variant, row[score_col]))
    # Reassign cleaned variants into the same columns.
    for i in range(1, 11):
        variant_col = f'variant{i}'
        score_col = f'hybrid_similarity_score{i}'
        if i <= len(cleaned):
            row[variant_col] = cleaned[i-1][0]
            row[score_col] = cleaned[i-1][1]
        else:
            row[variant_col] = ""
            row[score_col] = ""
    row['clean_count'] = len(cleaned)
    return row


def clean_csv_file(input_file, output_clean_file, noise_output_file):
    """
    Reads the input CSV (with header including pw1, variant1..10, hybrid_similarity_score1..10, 
    total_duration, load_duration, prompt_eval_count, prompt_eval_duration, eval_count, eval_duration),
    converts eval_duration from nanoseconds to seconds,
    applies row cleaning, and then splits the data:
      - Clean rows: rows with at least one non-noise variant.
      - Noise rows: rows with no clean (non-empty) variant.
    Writes both outputs to separate CSV files (keeping the original header) and prints summary statistics.
    """
    df = pd.read_csv(input_file)
    
    # Convert eval_duration from nanoseconds to seconds, if the column exists.
    if 'eval_duration' in df.columns:
        df['eval_duration'] = df['eval_duration'] / 1e9

    # Process each row to clean variants.
    df = df.apply(clean_row, axis=1)
    
    # Split the DataFrame:
    df_clean = df[df['clean_count'] > 0].copy()
    df_noise = df[df['clean_count'] == 0].copy()
    
    # Drop the temporary 'clean_count' column before saving.
    df_clean.drop(columns=['clean_count'], inplace=True)
    df_noise.drop(columns=['clean_count'], inplace=True)
    
    df_clean.to_csv(output_clean_file, index=False)
    df_noise.to_csv(noise_output_file, index=False)
    
    # --- Summary Statistics ---
    total_rows = df.shape[0]
    clean_rows = df_clean.shape[0]
    noise_rows = df_noise.shape[0]
    
    print(f"Summary for {input_file}:")
    print(f"  Total rows processed: {total_rows}")
    print(f"  Clean rows: {clean_rows} ({clean_rows / total_rows * 100:.2f}%)")
    print(f"  Noise rows: {noise_rows} ({noise_rows / total_rows * 100:.2f}%)")
    
    # Distribution of cleaned variants per clean row.
    distribution = df[df['clean_count'] > 0]['clean_count'].value_counts().sort_index()
    print("  Distribution of cleaned variants per clean row:")
    for count, num_rows in distribution.items():
        percentage = num_rows / total_rows * 100
        print(f"    {count} cleaned variants: {num_rows} rows ({percentage:.2f}%)")
    
    return {
        "total_rows": total_rows,
        "clean_rows": clean_rows,
        "noise_rows": noise_rows
    }


# Process the input files.
#clean_csv_file("output-test-prompt1-8b.csv", "output-cleaned-prompt1-8b.csv", "output-noise-prompt1-8b.csv")
#clean_csv_file("output-test-prompt1-14b.csv", "output-cleaned-prompt1-14b.csv", "output-noise-prompt1-14b.csv")
clean_csv_file("output-psm-prompt1-phi4-reasoning.csv", "output-cleaned-prompt1-phi4.csv", "output-noise-prompt1-phi4.csv")
clean_csv_file("output-psm-prompt1-qwen3-1.7b.csv", "output-cleaned-prompt1-qwen3-1.7b.csv", "output-noise-prompt1-qwen3-1.7b.csv")
clean_csv_file("output-psm-prompt1-qwen3-8b.csv", "output-cleaned-prompt1-qwen3-8b.csv", "output-noise-prompt1-qwen3-8b.csv")
clean_csv_file("output-psm-prompt1-qwen3-14b.csv", "output-cleaned-prompt1-qwen3-14b.csv", "output-noise-prompt1-qwen3-14b.csv")
