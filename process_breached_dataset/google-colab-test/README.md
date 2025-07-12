# run in google colab - test cases prompt1, prompt2, prompt3

# clean output - responses that do not follow the format are considered noise
## note: total duration is in seconds
%source ~/myvenv/bin/activate
%python3 convert_format.py

Clean data saved in format B as output-test-prompt1-1.5b.csv
Noisy data saved in format A as output-qwen1.5-prompt1-noise.csv

Summary Statistics:
Total combinations processed: 3472
Total password records: 146570
Clean records: 78306 (53.43%)
Noisy records: 68264 (46.57%)

Complete breakdown of combinations by clean variant count:
- Combinations with zero clean variants (all noise): 1224 (35.25%)
--- Combinations with at least one noisy output: 1909 (54.98%)
- Combinations with less than 10 clean variants: 837 (24.11%)
- Combinations with exactly 10 clean variants: 1079 (31.08%)
- Combinations with more than 10 clean variants: 332 (9.56%)

Verification - Sum of all percentages: 100.00%
===============================================

Clean data saved in format B as output-test-prompt2-1.5b.csv
Noisy data saved in format A as output-qwen1.5-prompt2-noise.csv

Summary Statistics:
Total combinations processed: 3488
Total password records: 94410
Clean records: 56577 (59.93%)
Noisy records: 37833 (40.07%)

Complete breakdown of combinations by clean variant count:
- Combinations with zero clean variants (all noise): 1016 (29.13%)
--- Combinations with at least one noisy output: 1773 (50.83%)
- Combinations with less than 10 clean variants: 1107 (31.74%)
- Combinations with exactly 10 clean variants: 1078 (30.91%)
- Combinations with more than 10 clean variants: 287 (8.23%)

Verification - Sum of all percentages: 100.00%
===============================================

Clean data saved in format B as output-test-prompt3-1.5b.csv
Noisy data saved in format A as output-qwen1.5-prompt3-noise.csv

Summary Statistics:
Total combinations processed: 3520
Total password records: 93740
Clean records: 52616 (56.13%)
Noisy records: 41124 (43.87%)

Complete breakdown of combinations by clean variant count:
- Combinations with zero clean variants (all noise): 946 (26.88%)
--- Combinations with at least one noisy output: 1792 (50.91%)
- Combinations with less than 10 clean variants: 1150 (32.67%)
- Combinations with exactly 10 clean variants: 1190 (33.81%)
- Combinations with more than 10 clean variants: 234 (6.65%)

Verification - Sum of all percentages: 100.00%
===============================================

%source ~/myvenv/bin/activate
% python3 clean.py
Summary for output-test-prompt1-1.5b.csv:
  Total rows processed: 2248
  Clean rows: 2241 (99.69%)
  Noise rows: 7 (0.31%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 83 rows (3.69%)
    2 cleaned variants: 78 rows (3.47%)
    3 cleaned variants: 52 rows (2.31%)
    4 cleaned variants: 70 rows (3.11%)
    5 cleaned variants: 74 rows (3.29%)
    6 cleaned variants: 77 rows (3.43%)
    7 cleaned variants: 90 rows (4.00%)
    8 cleaned variants: 116 rows (5.16%)
    9 cleaned variants: 197 rows (8.76%)
    10 cleaned variants: 1404 rows (62.46%)

Summary for output-test-prompt2-1.5b.csv:
  Total rows processed: 2472
  Clean rows: 2465 (99.72%)
  Noise rows: 7 (0.28%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 141 rows (5.70%)
    2 cleaned variants: 150 rows (6.07%)
    3 cleaned variants: 111 rows (4.49%)
    4 cleaned variants: 110 rows (4.45%)
    5 cleaned variants: 136 rows (5.50%)
    6 cleaned variants: 82 rows (3.32%)
    7 cleaned variants: 82 rows (3.32%)
    8 cleaned variants: 127 rows (5.14%)
    9 cleaned variants: 163 rows (6.59%)
    10 cleaned variants: 1363 rows (55.14%)

Summary for output-test-prompt3-1.5b.csv:
  Total rows processed: 2574
  Clean rows: 2566 (99.69%)
  Noise rows: 8 (0.31%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 137 rows (5.32%)
    2 cleaned variants: 128 rows (4.97%)
    3 cleaned variants: 98 rows (3.81%)
    4 cleaned variants: 109 rows (4.23%)
    5 cleaned variants: 134 rows (5.21%)
    6 cleaned variants: 115 rows (4.47%)
    7 cleaned variants: 135 rows (5.24%)
    8 cleaned variants: 132 rows (5.13%)
    9 cleaned variants: 158 rows (6.14%)
    10 cleaned variants: 1420 rows (55.17%)

%go build compute.go
./compute -csv="output-cleaned-prompt1-1.5b.csv" -output="output-computed-prompt1-1.5b.csv"


%go build compute2.go
./compute2 -csv="output-cleaned-prompt2-1.5b.csv" -output="output-computed-prompt2-1.5b.csv"

cp output-computed-prompt1-1.5b.csv ../eval-prompt1
cp output-computed-prompt2-1.5b.csv ../eval-prompt2
cp output-computed-prompt3-1.5b.csv ../eval-prompt3

# check if `output-computed-prompt1-8b.csv` & `output-computed-prompt1-14b.csv` are in `eval-prompt1`
# check if `output-computed-prompt2-8b.csv` & `output-computed-prompt2-14b.csv` are in `eval-prompt2`
# check if `output-computed-prompt3-8b.csv` & `output-computed-prompt3-14b.csv` are in `eval-prompt3`
