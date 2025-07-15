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

    if re.match(r'^\s*testing\b', password_str, re.IGNORECASE):
        return True

    if re.match(
        r'^\s*(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|'
        r'eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|'
        r'twentieth|twenty[-\s]*first|twenty[-\s]*second|twenty[-\s]*third|twenty[-\s]*fourth|twenty[-\s]*fifth)'
        r'(?:\s+(word|example|part))?:?',
        password_str,
        re.IGNORECASE
    ):
        return True

    if re.match(r'^\s*(example:|for example\b|examples\b)', password_str, re.IGNORECASE):
        return True

    char_length = len(password_str)
    if char_length < 8 or char_length > 64:
        return True

    # Base verbs that indicate noise (explanation text)
    base_verbs = [
        "add", "mix", "mixed", "replace", "remove", "change", "insert", "insertion", "random", "maybe", "swap", "swapped", "swapping", "manipulate", "manipulation",
        "base", "make", "made", "prepend", "append", "appended", "end", "mirror", "keep", "list", "operate", "operation", "strategy", "strategize",
        "rearrange", "arrange", "think", "reverse", "split", "splitting", "combine", "rotate", "delete", "deleted", "deletion", "use", "using", "contain",
        "modify", "modifie", "modification", "create", "substitute", "transform", "transformation", "convert", "try", "implement", "include", "generate",
        "implement", "include", "incorporate", "integrate", "suggest", "recommend", "apply", "ensure", "capitalize", "capitalization", "uppercase", "all caps",
        "lowercase", "switch", "shift", "scramble", "shuffle", "convert", "order", "reorder", "randomize", "result", "approach", "duplicate",
        "alternate", "hash", "salt", "take", "multipy", "substract", "divide", "break", "position", "avoid", "handle", "understand", "resemble",
        "assign", "output", "level", "wait", "move", "addition", "combination", "become", "becomes", "identify", "identifies", "finalize",
        "double", "alter", "alteration", "start", "trim", "to meet", "increase", "increment", "decrease", "decrement", "difference", "analyze",
        "substitute", "substitution", "addition", "multiplication", "multiplies", "multiplied", "interleave", "interleaving", "looking", "generate", "generation",
        "permute", "permutation", "combine", "combination", "concatenate", "concatenation", "repeat", "embed", "separate", "alternative", "assume", "brainstorm",
        "randomness", "verify", "verification", "attempt", "summarize"
    ]
    base_verbs = list(set(base_verbs))
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
        r'\bthere\s+are\b',
        r'\bbelow\s+is\b',
        r'\bbelow\s+are\b',
        r'\bit\s+has\b',
        r'\bfocus\s+on\b',
        r'\bsome\s+idea\b',
        r'\bmight\s+be\b',
        r'\bcould\s+be\b',
        r'\bwhen\s+you\b',
        r'\bthe\s+same\b',
        r'\bthe\s+rest\b',
        r'\bbase\s+word\b',
        r'\bbase\s+words\b',
        r'\bbase\s+form\b',
        r'\bbase\s+forms\b',
        r'\bbase\s+pattern\b',
        r'\bbase\s+patterns\b',
        r'\bbase\s+password\b',
        r'\bbase\s+passwords\b',
        r'\bbased\s+on\b',
        r'\bnumerical\b',
        r'\bgiven\s+password\b',
        r'\bgiven\s+passwords\b',
        r'\bcharacters\s+long\b',
        r'\btoo\s+long\b',
        r'\btoo\s+short\b',
        r'\btoo\s+common\b',
        r'\bvary\s+length\b',
        r'\bfor\s+\:\b',
        r'\bletters\s+\:\b',
        r'\bwords\s+\:\b',
        r'\bword\s+part\b',
        r'\bdigits\s+\:\b',
        r'\bnumbers\s+\:\b',
        r'\bnumeric\s+\:\b',
        r'\bnumbers\s+and\s+letters\b',
        r'\bhas\s+number\b',
        r'\bhas\s+letter\b',
        r'\bare\s+number\b',
        r'\bare\s+letter\b',
        r'\bare\s+digit\b',
        r'\bhas\s+letter\b',
        r'\bSummary\:\b',
        r'\bstep\s+\:\b',
        r'\bsteps\s+\:\b',
        r'\bfinal\s+answer\b',
        r'\bto\s+make\b', # Explanations of how "to make" something
        r'\bstep\s+by\b',
        r'\bstep\s+\:\b',
        r'\bstep-by-step\b',
        r'\bunderstand\s+the\b',
        r'\bstructure\s+is\b',
        r'\bfollowed\s+by\b',
        r'\blooking\s+at\b',
        r'\blooks\s+better\b',
        r'\blet\s+me\b',
        r'\bbut\s+actually\b',
        r'\bbut\s+that\b',
        r'\bcheck\s+for\b',
        r'\bunique\s+for\b',
        r'\buniqueness\b',
        r'\bfirst\s+part\b',
        r'\bfirst\s+one\b',
        r'\bfirst\s+1\b',
        r'\bfirst\s+2\b',
        r'\bfirst\s+3\b',
        r'\bfirst\s+4\b',
        r'\bfirst\s+5\b',
        r'\bfirst\s+6\b',
        r'\bfirst\s+7\b',
        r'\bfirst\s+8\b',
        r'\bfirst\s+base\b',
        r'\bfirst\s+phrase\b',
        r'\bfirst\s+character\b',
        r'\bone\s+word\b',
        r'\bone\s+base\b',
        r'\bsecond\s+part\b',
        r'\bsecond\s+one\b',
        r'\bsecond\s+base\b',
        r'\bsecond\s+phrase\b',
        r'\bsecond\s+character\b',
        r'\btwo\s+word\b',
        r'\btwo\s+base\b',
        r'\bthird\s+part\b',
        r'\bdisplay\s+text\b',
        r'\bedge\s+case\b',
        r'\bedge\s+cases\b',
        r'\b\-\s+for\b',
        r'\b\-\s+then\b',
        r'\bfor\s+\"\b',
        r'\bfor\s+\:\b',
        r'\bpossible\s+approaches\b',
        r'\bpossible\s+approach\b',
        r'\b\s+new\s+password\b',
        r'\b\s+longer\s+password\b',
        r'\bcurrent\s+password\b',
        r'\b\s+provided\s+password\b',
        r'\buser\s+password\b',
        r'\bboth\s+have\b',
        r'\bcould\s+mean\b',
        r'\bexplanation\b',
        r'\bexample\b',
        r'\bexamples\b',
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
        r'\bcommon\s+prefix\b',
        r'\busername\b', # Discussing inputs
        r'\bpassword\b',
        r'\blength\b',
        r'\bvariant\b',
        r'\bvariants\b',
        r'\bvariation\b',
        r'\bvariations\b',
        r'\bseparator\b',
        r'\bseparators\b',
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
        r'\benv python3\b',
        r'\bsummary\b[:]?',
        r'#+\s*summary\b',
        r'\bSummary\b[:]?',
        r'#+\s*Summary\b',
        r'^-+\s*(new|common|Current|current|longer|strong|stronger|better|existing)\s+passwords?\b',
        r'\bissues?\b[:]?',
        r'\bsome\s+issues\b',
        r'\bpassword\s+(is|has|was|looks|seems)\b'
    ]
    explanation_patterns.extend([
        r'^\s*(some|few|other|various)\s+(ideas|steps|examples|criteria)\s*[:]?$',               # "Some ideas:", "Other steps:"
        r'^\s*(for|about|regarding|concerning)\s+(the\s+)?(passwords?|new passwords?)\s*[:]',     # "For the new passwords:"
        r'^\s*(so,?\s*)?(my|your|our)\s+(passwords?|variants?)\s+.*\bmust\s+(not|never|be)\b',    # "So, my new passwords must not..."
        r'^\s*#+\s*(steps|criteria|summary|instructions|guidelines|tips)\b\s*[:]?$',             # "### Steps:", "## Criteria:"
        r'^\s*-\s*\w[\w\s]+\s*[:]',                                                              # "- Extend it:", "- Make sure:"
        r'\b(some|vary)\s+(longer|shorter)\b',                                                   # "Some longer", "Vary shorter"
        r'^\s*#+\s*(summary|steps|criteria|instructions|guidelines|tips|step|method|methods)(\s+for\b.*)?[:]?$', 
        r'\b(my|your|our)\s+(passwords?|variants?)\b.*\bmust\s+(not|never|avoid|exclude|be)\b',
        r'^\s*(passwords?|current passwords?|new passwords?)\s*[:]',
        r'^\s*given\s+(the\s+)?(passwords?|current passwords?)\s*[:]',
        r'\bi(\'ll| will| aim| plan| want|try)\s+(to\s+)?(use|generate|create|choose|pick|avoid|target)\b.*passwords?',
        r'^\s*[-*]\s*(again|entirely|mostly|sometimes|often|maybe|just|some|only|symbols?|digits?|numbers?|letters?)\b',
        r'\bpasswords?\s+could\s+(have|use|contain|include)\b',
    ])
    
    all_patterns = verb_patterns + explanation_patterns
    combined_pattern = '|'.join(all_patterns)
    return bool(re.search(combined_pattern, password_str, re.IGNORECASE))

def clean_row(row):
    """
    Processes one row by examining the 25 variant columns and their corresponding similarity scores.
    - Keeps variants that are not considered noise.
    - Reassigns clean variants consecutively (variant1, variant2, ...).
    - If fewer than 10 clean variants remain, remaining variant/score fields are set to empty.
    - Adds a temporary 'clean_count' field with the number of clean variants.
    """
    cleaned = []
    for i in range(1, 26):
        variant_col = f'variant{i}'
        cs_hss_pw1_col = f'cs_hss_pw1_{i}'
        ci_hss_pw1_col = f'ci_hss_pw1_{i}'
        cs_hss_pw2_col = f'cs_hss_pw2_{i}'
        ci_hss_pw2_col = f'ci_hss_pw2_{i}'
        variant = row[variant_col]
        if pd.isna(variant) or str(variant).strip() == "":
            continue
        if not is_noise(variant):
            cleaned.append((variant, 
                row[cs_hss_pw1_col], row[ci_hss_pw1_col],
                row[cs_hss_pw2_col], row[ci_hss_pw2_col]))
    # Reassign cleaned variants into the same columns.
    for i in range(1, 26):
        variant_col = f'variant{i}'
        cs_hss_pw1_col = f'cs_hss_pw1_{i}'
        ci_hss_pw1_col = f'ci_hss_pw1_{i}'
        cs_hss_pw2_col = f'cs_hss_pw2_{i}'
        ci_hss_pw2_col = f'ci_hss_pw2_{i}'
        if i <= len(cleaned):
            row[variant_col] = cleaned[i-1][0]
            row[cs_hss_pw1_col] = cleaned[i-1][1]
            row[ci_hss_pw1_col] = cleaned[i-1][2]
            row[cs_hss_pw2_col] = cleaned[i-1][3]
            row[ci_hss_pw2_col] = cleaned[i-1][4]
        else:
            row[variant_col] = ""
            row[cs_hss_pw1_col] = ""
            row[ci_hss_pw1_col] = ""
            row[cs_hss_pw2_col] = ""
            row[ci_hss_pw2_col] = ""
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
#clean_csv_file("output-psm-prompt2-deepseek.csv", "output-cleaned-prompt2-deepseek.csv", "output-noise-prompt3-8b.csv")
#clean_csv_file("output-psm-prompt2-qwq.csv", "output-cleaned-prompt2-qwq.csv", "output-noise-prompt3-14b.csv")
#clean_csv_file("output-psm-prompt4-deepseek.csv", "output-cleaned-prompt4-deepseek.csv", "output-noise-prompt3-8b.csv")
#clean_csv_file("output-psm-prompt4-qwq.csv", "output-cleaned-prompt4-qwq.csv", "output-noise-prompt3-14b.csv")
clean_csv_file("output-psm-prompt2-qwen3.csv", "output-cleaned-prompt2-qwen3.csv", "output-noise-prompt2-qwen3.csv")
clean_csv_file("output-psm-prompt2-magistral.csv", "output-cleaned-prompt2-magistral.csv", "output-noise-prompt2-magistral.csv")
clean_csv_file("output-psm-prompt4-qwen3.csv", "output-cleaned-prompt4-qwen3.csv", "output-noise-prompt4-qwen3.csv")
clean_csv_file("output-psm-prompt4-magistral.csv", "output-cleaned-prompt4-magistral.csv", "output-noise-prompt4-magistral.csv")
