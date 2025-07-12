cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_r/password_pairs_10.csv" -output="output-test-prompt3-8b.csv" -prompt=3 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_r/password_pairs_20.csv" -output="output-test-prompt3-14b.csv" -prompt=3 -variants=10

## note: total duration is nanoseconds
%source ~/myvenv/bin/activate
%python3 clean.py

Summary for output-test-prompt3-8b.csv:
  Total rows processed: 2650
  Clean rows: 2484 (93.74%)
  Noise rows: 166 (6.26%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 1 rows (0.04%)
    2 cleaned variants: 8 rows (0.30%)
    3 cleaned variants: 7 rows (0.26%)
    4 cleaned variants: 1 rows (0.04%)
    5 cleaned variants: 11 rows (0.42%)
    6 cleaned variants: 16 rows (0.60%)
    7 cleaned variants: 33 rows (1.25%)
    8 cleaned variants: 82 rows (3.09%)
    9 cleaned variants: 257 rows (9.70%)
    10 cleaned variants: 2068 rows (78.04%)

Summary for output-test-prompt3-14b.csv:
  Total rows processed: 2450
  Clean rows: 2413 (98.49%)
  Noise rows: 37 (1.51%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 2 rows (0.08%)
    2 cleaned variants: 3 rows (0.12%)
    3 cleaned variants: 2 rows (0.08%)
    4 cleaned variants: 2 rows (0.08%)
    5 cleaned variants: 5 rows (0.20%)
    6 cleaned variants: 5 rows (0.20%)
    7 cleaned variants: 5 rows (0.20%)
    8 cleaned variants: 42 rows (1.71%)
    9 cleaned variants: 153 rows (6.24%)
    10 cleaned variants: 2194 rows (89.55%)