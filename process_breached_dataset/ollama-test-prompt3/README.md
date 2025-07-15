cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_r/password_pairs_10.csv" -output="output-test-prompt3-8b.csv" -prompt=3 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_r/password_pairs_20.csv" -output="output-test-prompt3-14b.csv" -prompt=3 -variants=10

##### vast.ai jupyter
./deepseek-generate_pw_var -model="phi4-reasoning" -csv="../cleaned_q/password_pairs_1.csv" -prompt=3 -variants=10 -output="output-psm-prompt3-phi4-reasoning.csv"

./deepseek-generate_pw_var -model="qwen3:1.7b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=3 -variants=10 -output="output-psm-prompt3-qwen3-1.7b.csv"

./deepseek-generate_pw_var -model="qwen3:8b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=3 -variants=10 -output="output-psm-prompt3-qwen3-8b.csv"

./deepseek-generate_pw_var -model="qwen3:14b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=3 -variants=10 -output="output-psm-prompt3-qwen3-14b.csv"

#####

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

Summary for output-psm-prompt3-phi4-reasoning.csv:
  Total rows processed: 562
  Clean rows: 471 (83.81%)
  Noise rows: 91 (16.19%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 5 rows (0.89%)
    2 cleaned variants: 4 rows (0.71%)
    3 cleaned variants: 9 rows (1.60%)
    4 cleaned variants: 12 rows (2.14%)
    5 cleaned variants: 92 rows (16.37%)
    6 cleaned variants: 3 rows (0.53%)
    7 cleaned variants: 5 rows (0.89%)
    8 cleaned variants: 12 rows (2.14%)
    9 cleaned variants: 63 rows (11.21%)
    10 cleaned variants: 266 rows (47.33%)
Summary for output-psm-prompt3-qwen3-1.7b.csv:
  Total rows processed: 3655
  Clean rows: 3580 (97.95%)
  Noise rows: 75 (2.05%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 3 rows (0.08%)
    2 cleaned variants: 4 rows (0.11%)
    3 cleaned variants: 1 rows (0.03%)
    5 cleaned variants: 4 rows (0.11%)
    6 cleaned variants: 10 rows (0.27%)
    7 cleaned variants: 9 rows (0.25%)
    8 cleaned variants: 32 rows (0.88%)
    9 cleaned variants: 81 rows (2.22%)
    10 cleaned variants: 3436 rows (94.01%)
Summary for output-psm-prompt3-qwen3-8b.csv:
  Total rows processed: 2545
  Clean rows: 2528 (99.33%)
  Noise rows: 17 (0.67%)
  Distribution of cleaned variants per clean row:
    4 cleaned variants: 1 rows (0.04%)
    5 cleaned variants: 3 rows (0.12%)
    6 cleaned variants: 1 rows (0.04%)
    7 cleaned variants: 6 rows (0.24%)
    8 cleaned variants: 187 rows (7.35%)
    9 cleaned variants: 112 rows (4.40%)
    10 cleaned variants: 2218 rows (87.15%)
Summary for output-psm-prompt3-qwen3-14b.csv:
  Total rows processed: 1600
  Clean rows: 1599 (99.94%)
  Noise rows: 1 (0.06%)
  Distribution of cleaned variants per clean row:
    6 cleaned variants: 1 rows (0.06%)
    8 cleaned variants: 27 rows (1.69%)
    9 cleaned variants: 33 rows (2.06%)
    10 cleaned variants: 1538 rows (96.12%)