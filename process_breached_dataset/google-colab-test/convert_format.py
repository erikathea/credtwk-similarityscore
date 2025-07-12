import pandas as pd
import re

def convert_format_a_to_b_with_noise_separation(input_file, output_file_b, noise_output_file_a):
    df = pd.read_csv(input_file, sep=',') 
    
    df = df[['username', 'pw1', 'pw2', 'generated_pw', 'generation_time',
             'genpw_username_similarity', 'genpw_pw1_similarity', 'genpw_pw1_case_insensitive_similarity',
             'genpw_pw2_similarity', 'genpw_pw2_case_insensitive_similarity']]
    
    def is_noise(password):
        password_str = str(password)
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
            "modify", "generate", "create", "substitute", "transform", "convert", "try", "implement", "include", "generate",
            "implement", "include", "incorporate", "integrate", "suggest", "recommend", "apply", "ensure", "capitalize", "uppercase",
            "lowercase", "switch", "shift", "scramble", "shuffle", "convert", "order", "reorder", "randomize", "result",
            "alternate", "hash", "salt", "take", "multipy", "substract", "divide", "break", "alternate", "position", "avoid",
            "assign", "output", "level", "wait", "move", "addition", "combination", "become", "becomes", "identify", "identifies", "finalize"
        ]
        
        verb_patterns = []
        for verb in base_verbs:
            # Basic verb
            verb_patterns.append(r'\b' + verb + r'\b')
            # Past tense: if the verb ends with "e" add a "d", else just add "ed"
            if verb.endswith('e'):
                verb_patterns.append(r'\b' + verb + r'd\b')
            else:
                verb_patterns.append(r'\b' + verb + r'ed\b')
            # Progressive form: remove ending "e" if applicable or just add "ing"
            if verb.endswith('e'):
                verb_patterns.append(r'\b' + verb[:-1] + r'ing\b')
            else:
                verb_patterns.append(r'\b' + verb + r'ing\b')
            # Modal forms: "will", "should", "could" followed by the verb
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
            r'\bto\s+make\b', # Explanations of how "to make" something
            r'\bstep\s+by\b',
            r'\bstep-by-step\b',
            r'\bexplanation\b',
            r'\bnote\b',     # Notes or explanations
            r'\bmaybe\b',
            r'\bdifferent\b',
            r'\binstead\b',
            r'\banother\b', 
            r'\balternatively\b', 
            r'\boption\b', 
            r'\boptional\b', 
            r'\boptionally\b',
            r'\boriginal\b',
            r'\boriginally\b',
            r'\busername\b', # Discussing inputs
            r'\bpassword\b',
            r'\bvariant\b',
            r'\buppercase\b', # Discussing characters
            r'\blowercase\b',
            r'\bletter\b',
            r'\bsymbol\b',
            r'\bspecial\b',
            r'\bnumber\b',
            r'\bcharacter\b',
            r'\bpbkdf2_hmac\b', # Discussing cryptography
            r'\bbcrypt\b',
            r'\bscrypt\b'
        ]
        
        all_patterns = verb_patterns + explanation_patterns
        combined_pattern = '|'.join(all_patterns)
        return bool(re.search(combined_pattern, password_str, re.IGNORECASE))
    
    df['is_noise'] = df['generated_pw'].apply(is_noise)
    df['variant_index'] = df.groupby(['username', 'pw1', 'pw2']).cumcount() + 1
    df_clean = df[~df['is_noise']].copy()
    df_noisy = df[df['is_noise']].copy()

    all_combinations = df.groupby(['username', 'pw1', 'pw2']).size().reset_index(name='total_count')
    clean_combinations = df_clean.groupby(['username', 'pw1', 'pw2']).size().reset_index(name='clean_count')
    
    zero_clean_combinations = pd.merge(
        all_combinations,
        clean_combinations,
        on=['username', 'pw1', 'pw2'],
        how='left'
    )
    zero_clean_combinations['clean_count'] = zero_clean_combinations['clean_count'].fillna(0)
    zero_clean_combinations = zero_clean_combinations[zero_clean_combinations['clean_count'] == 0]
    
    if not df_clean.empty:
        df_clean['variant_index'] = df_clean.groupby(['username', 'pw1', 'pw2']).cumcount() + 1
        variant_counts = df_clean.groupby(['username', 'pw1', 'pw2']).size().reset_index(name='count')
        more_than_10_variants = variant_counts[variant_counts['count'] > 10]
        df_clean_limited = df_clean[df_clean['variant_index'] <= 10].copy()
        df_pivot = df_clean_limited.pivot(
            index=['username', 'pw1', 'pw2'], 
            columns='variant_index', 
            values=['generated_pw', 'genpw_pw1_similarity']
        )
        
        df_pivot.columns = [f'variant{col[1]}' if col[0] == 'generated_pw' else f'hybrid_similarity_score{col[1]}' for col in df_pivot.columns]
        df_pivot.reset_index(inplace=True)
        
        #total_generation_time = df_clean.groupby(['username', 'pw1', 'pw2'])['generation_time'].sum().reset_index()
        #df_pivot = df_pivot.merge(total_generation_time, on=['username', 'pw1', 'pw2'], how='left')
        #df_pivot.rename(columns={'generation_time': 'total_duration'}, inplace=True)
        # First, calculate duration for each entry (after your initial sorting and before pivot)
        df_clean = df_clean.sort_values(['username', 'pw1', 'pw2', 'generation_time'])
        df_clean['entry_duration'] = df_clean.groupby(['username', 'pw1', 'pw2'])['generation_time'].diff()
        first_entries = df_clean.groupby(['username', 'pw1', 'pw2']).head(1).index
        df_clean.loc[first_entries, 'entry_duration'] = df_clean.loc[first_entries, 'generation_time']
        # Now sum these entry durations instead of the raw generation_time
        total_generation_time = df_clean.groupby(['username', 'pw1', 'pw2'])['entry_duration'].sum().reset_index()
        df_pivot = df_pivot.merge(total_generation_time, on=['username', 'pw1', 'pw2'], how='left')
        df_pivot.rename(columns={'entry_duration': 'total_duration'}, inplace=True)

        variant_counts = df_clean.groupby(['username', 'pw1', 'pw2']).size().reset_index(name='num_variants')
        df_pivot = df_pivot.merge(variant_counts, on=['username', 'pw1', 'pw2'], how='left')
        
        df_pivot.to_csv(output_file_b, index=False)
        print(f"Clean data saved in format B as {output_file_b}")
    
    if not df_noisy.empty:
        df_noisy = df_noisy.drop(['is_noise', 'variant_index'], axis=1)
        df_noisy.to_csv(noise_output_file_a, index=False)
        print(f"Noisy data saved in format A as {noise_output_file_a}")
    
    total_records = len(df)
    clean_records = len(df_clean)
    noisy_records = len(df_noisy)
    total_combinations = df.groupby(['username', 'pw1', 'pw2']).size().reset_index().shape[0]
    noisy_combinations = df_noisy.groupby(['username', 'pw1', 'pw2']).size().reset_index().shape[0]
    variant_counts = df_clean.groupby(['username', 'pw1', 'pw2']).size().reset_index(name='count')
    less_than_10 = variant_counts[variant_counts['count'] < 10]
    exactly_10 = variant_counts[variant_counts['count'] == 10]
    more_than_10 = variant_counts[variant_counts['count'] > 10]
    zero_clean = len(zero_clean_combinations)
    
    print(f"\nSummary Statistics:")
    print(f"Total combinations processed: {total_combinations}")
    print(f"Total password records: {total_records}")
    print(f"Clean records: {clean_records} ({clean_records/total_records*100:.2f}%)")
    print(f"Noisy records: {noisy_records} ({noisy_records/total_records*100:.2f}%)")
    print("\nComplete breakdown of combinations by clean variant count:")
    print(f"- Combinations with zero clean variants (all noise): {zero_clean} ({zero_clean/total_combinations*100:.2f}%)")
    print(f"--- Combinations with at least one noisy output: {noisy_combinations} ({noisy_combinations/total_combinations*100:.2f}%)")
    print(f"- Combinations with less than 10 clean variants: {len(less_than_10)} ({len(less_than_10)/total_combinations*100:.2f}%)")
    print(f"- Combinations with exactly 10 clean variants: {len(exactly_10)} ({len(exactly_10)/total_combinations*100:.2f}%)")
    print(f"- Combinations with more than 10 clean variants: {len(more_than_10)} ({len(more_than_10)/total_combinations*100:.2f}%)")
    total_percentage = zero_clean/total_combinations*100 + len(less_than_10)/total_combinations*100 + \
                 len(exactly_10)/total_combinations*100 + len(more_than_10)/total_combinations*100
    print(f"\nVerification - Sum of all percentages: {total_percentage:.2f}%")
    
    # Output extra details about combinations with more than 10 variants
    if len(more_than_10) > 0:
        print("\nDetails of combinations with more than 10 variants:")
        for _, row in more_than_10.iterrows():
            print(f"  {row['username']}, {row['pw1']}, {row['pw2']}: {row['count']} variants (limited to 10 in output)")
    
    return {
        "total_combinations": total_combinations,
        "total_records": total_records,
        "clean_records": clean_records,
        "noisy_records": noisy_records,
        "noisy_combinations": noisy_combinations,
        "less_than_10_variants": len(less_than_10),
        "exactly_10_variants": len(exactly_10)
    }

convert_format_a_to_b_with_noise_separation(
    "output-qwen1.5-prompt1-a.csv", 
    "output-test-prompt1-1.5b.csv",
    "output-qwen1.5-prompt1-noise.csv"
)

convert_format_a_to_b_with_noise_separation(
    "output-qwen1.5-prompt2-a.csv", 
    "output-test-prompt2-1.5b.csv",
    "output-qwen1.5-prompt2-noise.csv"
)

convert_format_a_to_b_with_noise_separation(
    "output-qwen1.5-prompt3.csv", 
    "output-test-prompt3-1.5b.csv",
    "output-qwen1.5-prompt3-noise.csv"
)