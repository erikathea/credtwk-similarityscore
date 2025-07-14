cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_s-group1/password_pairs_1.csv" -output="output-test-prompt2-8b.csv" -prompt=2 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_s-group2/password_pairs_1.csv" -output="output-test-prompt2-14b.csv" -prompt=2 -variants=10

##### vast.ai jupyter terminal
./deepseek-generate_pw_var -model="phi4-reasoning" -csv="../cleaned_q/password_pairs_1.csv" -prompt=2 -variants=10 -output="output-psm-prompt2-phi4-reasoning.csv"

./deepseek-generate_pw_var -model="phi4-reasoning" -csv="../cleaned_s-group1/password_pairs_1.csv" -prompt=2 -variants=10 -output="output-psm-prompt2-phi4-reasoning.csv"

./deepseek-generate_pw_var -model="qwen3:1.7b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=2 -variants=10 -output="output-psm-prompt2-qwen3-1.7b.csv"

./deepseek-generate_pw_var -model="qwen3:8b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=2 -variants=10 -output="output-psm-prompt2-qwen3-8b.csv"

./deepseek-generate_pw_var -model="qwen3:14b" -csv="../cleaned_q/password_pairs_1.csv" -prompt=2 -variants=10 -output="output-psm-prompt2-qwen3-14b.csv"

#####

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

Summary for output-psm-prompt2-phi4-reasoning.csv:
  Total rows processed: 930
  Clean rows: 820 (88.17%)
  Noise rows: 110 (11.83%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 10 rows (1.08%)
    2 cleaned variants: 12 rows (1.29%)
    3 cleaned variants: 10 rows (1.08%)
    4 cleaned variants: 9 rows (0.97%)
    5 cleaned variants: 44 rows (4.73%)
    6 cleaned variants: 5 rows (0.54%)
    7 cleaned variants: 13 rows (1.40%)
    8 cleaned variants: 28 rows (3.01%)
    9 cleaned variants: 94 rows (10.11%)
    10 cleaned variants: 595 rows (63.98%)
Summary for output-psm-prompt2-qwen3-1.7b.csv:
  Total rows processed: 6125
  Clean rows: 5997 (97.91%)
  Noise rows: 128 (2.09%)
  Distribution of cleaned variants per clean row:
    2 cleaned variants: 3 rows (0.05%)
    3 cleaned variants: 2 rows (0.03%)
    4 cleaned variants: 3 rows (0.05%)
    5 cleaned variants: 8 rows (0.13%)
    6 cleaned variants: 30 rows (0.49%)
    7 cleaned variants: 27 rows (0.44%)
    8 cleaned variants: 55 rows (0.90%)
    9 cleaned variants: 251 rows (4.10%)
    10 cleaned variants: 5618 rows (91.72%)
Summary for output-psm-prompt2-qwen3-8b.csv:
  Total rows processed: 2710
  Clean rows: 2696 (99.48%)
  Noise rows: 14 (0.52%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 1 rows (0.04%)
    3 cleaned variants: 1 rows (0.04%)
    4 cleaned variants: 1 rows (0.04%)
    6 cleaned variants: 4 rows (0.15%)
    7 cleaned variants: 1 rows (0.04%)
    8 cleaned variants: 71 rows (2.62%)
    9 cleaned variants: 91 rows (3.36%)
    10 cleaned variants: 2526 rows (93.21%)
Summary for output-psm-prompt2-qwen3-14b.csv:
  Total rows processed: 2525
  Clean rows: 2518 (99.72%)
  Noise rows: 7 (0.28%)
  Distribution of cleaned variants per clean row:
    6 cleaned variants: 1 rows (0.04%)
    7 cleaned variants: 2 rows (0.08%)
    8 cleaned variants: 100 rows (3.96%)
    9 cleaned variants: 100 rows (3.96%)
    10 cleaned variants: 2315 rows (91.68%)

% python3 compute.py
Saved computed averages to output-computed-prompt2-8b.csv
Saved computed averages to output-computed-prompt2-14b.csv

cp output-computed-prompt2-8b.csv ../eval-prompt2
cp output-computed-prompt2-14b.csv ../eval-prompt2

% python3 plot_hss.py