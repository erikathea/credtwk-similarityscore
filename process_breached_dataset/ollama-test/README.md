cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

##### vast.ai jupyter terminal
./deepseek-generate_pw_var -model="phi4-reasoning" -csv="../cleaned_q/password_pairs_1.csv" -prompt=1 -variants=10 -output="output-psm-prompt1-phi4-reasoning.csv"

./deepseek-generate_pw_var -model="phi4-reasoning" -csv="../cleaned_s-group1/password_pairs_1.csv" -prompt=1 -variants=10 -output="output-psm-prompt1-phi4-reasoning.csv"

./deepseek-generate_pw_var -model="qwen3:1.7b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=1 -variants=10 -output="output-psm-prompt1-qwen3-1.7b.csv"

./deepseek-generate_pw_var -model="qwen3:8b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=1 -variants=10 -output="output-psm-prompt1-qwen3-8b.csv"

./deepseek-generate_pw_var -model="qwen3:14b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=1 -variants=10 -output="output-psm-prompt1-qwen3-14b.csv"
#####

%source ~/myvenv/bin/activate
%python3 clean.py

Summary for output-test-prompt1-8b.csv:
  Total rows processed: 3860
  Clean rows: 3251 (84.22%)
  Noise rows: 609 (15.78%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 9 rows (0.23%)
    2 cleaned variants: 15 rows (0.39%)
    3 cleaned variants: 10 rows (0.26%)
    4 cleaned variants: 16 rows (0.41%)
    5 cleaned variants: 27 rows (0.70%)
    6 cleaned variants: 13 rows (0.34%)
    7 cleaned variants: 41 rows (1.06%)
    8 cleaned variants: 81 rows (2.10%)
    9 cleaned variants: 366 rows (9.48%)
    10 cleaned variants: 2673 rows (69.25%)

===============================================

Summary for output-test-prompt1-14b.csv:
  Total rows processed: 1635
  Clean rows: 1572 (96.15%)
  Noise rows: 63 (3.85%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 1 rows (0.06%)
    3 cleaned variants: 1 rows (0.06%)
    4 cleaned variants: 1 rows (0.06%)
    6 cleaned variants: 3 rows (0.18%)
    7 cleaned variants: 5 rows (0.31%)
    8 cleaned variants: 15 rows (0.92%)
    9 cleaned variants: 70 rows (4.28%)
    10 cleaned variants: 1476 rows (90.28%)

===============================================

Summary for output-psm-prompt1-phi4-reasoning.csv:
  Total rows processed: 1173
  Clean rows: 1042 (88.83%)
  Noise rows: 131 (11.17%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 8 rows (0.68%)
    2 cleaned variants: 10 rows (0.85%)
    3 cleaned variants: 12 rows (1.02%)
    4 cleaned variants: 33 rows (2.81%)
    5 cleaned variants: 97 rows (8.27%)
    6 cleaned variants: 2 rows (0.17%)
    7 cleaned variants: 9 rows (0.77%)
    8 cleaned variants: 15 rows (1.28%)
    9 cleaned variants: 71 rows (6.05%)
    10 cleaned variants: 785 rows (66.92%)

===============================================

Summary for output-psm-prompt1-qwen3-1.7b.csv:
  Total rows processed: 2200
  Clean rows: 2185 (99.32%)
  Noise rows: 15 (0.68%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 8 rows (0.36%)
    2 cleaned variants: 12 rows (0.55%)
    3 cleaned variants: 2 rows (0.09%)
    4 cleaned variants: 1 rows (0.05%)
    6 cleaned variants: 1 rows (0.05%)
    7 cleaned variants: 5 rows (0.23%)
    8 cleaned variants: 13 rows (0.59%)
    9 cleaned variants: 140 rows (6.36%)
    10 cleaned variants: 2003 rows (91.05%)

===============================================

Summary for output-psm-prompt1-qwen3-8b.csv:
  Total rows processed: 3195
  Clean rows: 3107 (97.25%)
  Noise rows: 88 (2.75%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 4 rows (0.13%)
    2 cleaned variants: 3 rows (0.09%)
    3 cleaned variants: 1 rows (0.03%)
    5 cleaned variants: 2 rows (0.06%)
    6 cleaned variants: 2 rows (0.06%)
    7 cleaned variants: 4 rows (0.13%)
    8 cleaned variants: 64 rows (2.00%)
    9 cleaned variants: 48 rows (1.50%)
    10 cleaned variants: 2979 rows (93.24%)

===============================================

Summary for output-psm-prompt1-qwen3-14b.csv:
  Total rows processed: 1670
  Clean rows: 1646 (98.56%)
  Noise rows: 24 (1.44%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 1 rows (0.06%)
    4 cleaned variants: 1 rows (0.06%)
    5 cleaned variants: 2 rows (0.12%)
    7 cleaned variants: 2 rows (0.12%)
    8 cleaned variants: 64 rows (3.83%)
    9 cleaned variants: 45 rows (2.69%)
    10 cleaned variants: 1531 rows (91.68%)

===============================================

%go build compute.go
./compute -csv="output-cleaned-prompt1-8b.csv" -output="output-computed-prompt1-8b.csv"

./compute -csv="output-cleaned-prompt1-14b.csv" -output="output-computed-prompt1-14b.csv"

./compute -csv="output-cleaned-prompt1-phi4.csv" -output="output-computed-prompt1-phi4.csv"

./compute -csv="output-cleaned-prompt1-qwen3-1.7b.csv" -output="output-computed-prompt1-qwen3-1.7.csv"

./compute -csv="output-cleaned-prompt1-qwen3-8b.csv" -output="output-computed-prompt1-qwen3-8.csv"

./compute -csv="output-cleaned-prompt1-qwen3-14b.csv" -output="output-computed-prompt1-qwen3-14.csv"

cp output-computed-prompt1-8b.csv ../eval-prompt1
cp output-computed-prompt1-14b.csv ../eval-prompt1
cp output-computed-prompt1-phi4.csv ../eval-prompt1
cp output-computed-prompt1-qwen3-1.7.csv ../eval-prompt1
cp output-computed-prompt1-qwen3-8.csv ../eval-prompt1
cp output-computed-prompt1-qwen3-14.csv ../eval-prompt1

# check if `output-computed-prompt1-1.5b.csv` is in `eval-prompt1`

### %python3 plot_results.py
%python3 plot_hss2.py