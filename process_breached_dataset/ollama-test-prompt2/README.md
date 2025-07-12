cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_s-group1/password_pairs_1.csv" -output="output-test-prompt2-8b.csv" -prompt=2 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_s-group2/password_pairs_1.csv" -output="output-test-prompt2-14b.csv" -prompt=2 -variants=10

## note: total duration is nanoseconds
%source ~/myvenv/bin/activate
%python3 clean.py

Summary for output-test-prompt2-8b.csv:
  Total rows processed: 2159
  Clean rows: 2017 (93.42%)
  Noise rows: 142 (6.58%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 4 rows (0.19%)
    2 cleaned variants: 6 rows (0.28%)
    3 cleaned variants: 6 rows (0.28%)
    4 cleaned variants: 1 rows (0.05%)
    5 cleaned variants: 14 rows (0.65%)
    6 cleaned variants: 10 rows (0.46%)
    7 cleaned variants: 33 rows (1.53%)
    8 cleaned variants: 76 rows (3.52%)
    9 cleaned variants: 278 rows (12.88%)
    10 cleaned variants: 1589 rows (73.60%)
Summary for output-test-prompt2-14b.csv:
  Total rows processed: 2240
  Clean rows: 2195 (97.99%)
  Noise rows: 45 (2.01%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 3 rows (0.13%)
    2 cleaned variants: 8 rows (0.36%)
    3 cleaned variants: 2 rows (0.09%)
    4 cleaned variants: 2 rows (0.09%)
    5 cleaned variants: 3 rows (0.13%)
    6 cleaned variants: 6 rows (0.27%)
    7 cleaned variants: 13 rows (0.58%)
    8 cleaned variants: 67 rows (2.99%)
    9 cleaned variants: 184 rows (8.21%)
    10 cleaned variants: 1907 rows (85.13%)

% python3 compute.py
Saved computed averages to output-computed-prompt2-8b.csv
Saved computed averages to output-computed-prompt2-14b.csv

cp output-computed-prompt2-8b.csv ../eval-prompt2
cp output-computed-prompt2-14b.csv ../eval-prompt2