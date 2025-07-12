cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

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


%go build compute.go
./compute -csv="output-cleaned-prompt1-8b.csv" -output="output-computed-prompt1-8b.csv"

./compute -csv="output-cleaned-prompt1-14b.csv" -output="output-computed-prompt1-14b.csv"

cp output-computed-prompt1-8b.csv ../eval-prompt1
cp output-computed-prompt1-14b.csv ../eval-prompt1

# check if `output-computed-prompt1-1.5b.csv` is in `eval-prompt1`

%python3 plot_results.py