# README
## build script
go build gen_pws.go

====

## prompt 2

./gen_pws -model="qwq" -csv="../cleaned_r/password_pairs_1.csv" -output="output-psm-prompt2-qwq.csv" -prompt=2 -variants=25

./gen_pws -model="deepseek-r1:32b" -csv="../cleaned_r/password_pairs_1.csv" -output="output-psm-prompt2-deepseek.csv" -prompt=2 -variants=25

./gen_pws -model="qwen3:32b" -csv="../cleaned_r/password_pairs_1.csv" -output="output-psm-prompt2-qwen3.csv" -prompt=2 -variants=25

====

## prompt 4

./gen_pws -model="qwq" -csv="../cleaned_q/password_pairs_1.csv" -output="output-psm-prompt4-qwq.csv" -prompt=4 -variants=25

./gen_pws -model="deepseek-r1:32b" -csv="../cleaned_q/password_pairs_1.csv" -output="output-psm-prompt4-deepseek.csv" -prompt=4 -variants=25

=====

## cleaning (python3 clean.py)
- clean_csv_file("output-psm-prompt2-deepseek.csv", "output-cleaned-psm-prompt2-deepseek.csv", "output-noise-prompt3-8b.csv")
- clean_csv_file("output-psm-prompt2-qwq.csv", "output-cleaned-psm-prompt2-qwq.csv", "output-noise-prompt3-14b.csv")
- clean_csv_file("output-psm-prompt4-deepseek.csv", "output-cleaned-psm-prompt4-deepseek.csv", "output-noise-prompt3-8b.csv")
- clean_csv_file("output-psm-prompt4-qwq.csv", "output-cleaned-psm-prompt4-qwq.csv", "output-noise-prompt3-14b.csv")


Summary for output-psm-prompt2-deepseek.csv:
  Total rows processed: 215
  Clean rows: 207 (96.28%)
  Noise rows: 8 (3.72%)
  Distribution of cleaned variants per clean row:
    3 cleaned variants: 1 rows (0.47%)
    8 cleaned variants: 1 rows (0.47%)
    10 cleaned variants: 3 rows (1.40%)
    13 cleaned variants: 1 rows (0.47%)
    14 cleaned variants: 1 rows (0.47%)
    15 cleaned variants: 1 rows (0.47%)
    17 cleaned variants: 5 rows (2.33%)
    19 cleaned variants: 1 rows (0.47%)
    20 cleaned variants: 4 rows (1.86%)
    21 cleaned variants: 4 rows (1.86%)
    22 cleaned variants: 5 rows (2.33%)
    23 cleaned variants: 9 rows (4.19%)
    24 cleaned variants: 20 rows (9.30%)
    25 cleaned variants: 151 rows (70.23%)

Summary for output-psm-prompt2-qwq.csv:
  Total rows processed: 210
  Clean rows: 196 (93.33%)
  Noise rows: 14 (6.67%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 7 rows (3.33%)
    2 cleaned variants: 8 rows (3.81%)
    3 cleaned variants: 4 rows (1.90%)
    4 cleaned variants: 1 rows (0.48%)
    5 cleaned variants: 1 rows (0.48%)
    7 cleaned variants: 2 rows (0.95%)
    8 cleaned variants: 2 rows (0.95%)
    9 cleaned variants: 1 rows (0.48%)
    10 cleaned variants: 4 rows (1.90%)
    11 cleaned variants: 1 rows (0.48%)
    12 cleaned variants: 1 rows (0.48%)
    13 cleaned variants: 3 rows (1.43%)
    15 cleaned variants: 3 rows (1.43%)
    16 cleaned variants: 1 rows (0.48%)
    18 cleaned variants: 1 rows (0.48%)
    20 cleaned variants: 1 rows (0.48%)
    22 cleaned variants: 1 rows (0.48%)
    23 cleaned variants: 1 rows (0.48%)
    24 cleaned variants: 4 rows (1.90%)
    25 cleaned variants: 149 rows (70.95%)

Summary for output-psm-prompt4-deepseek.csv:
  Total rows processed: 215
  Clean rows: 214 (99.53%)
  Noise rows: 1 (0.47%)
  Distribution of cleaned variants per clean row:
    1 cleaned variants: 2 rows (0.93%)
    2 cleaned variants: 1 rows (0.47%)
    7 cleaned variants: 2 rows (0.93%)
    11 cleaned variants: 1 rows (0.47%)
    16 cleaned variants: 1 rows (0.47%)
    18 cleaned variants: 1 rows (0.47%)
    19 cleaned variants: 1 rows (0.47%)
    20 cleaned variants: 1 rows (0.47%)
    21 cleaned variants: 2 rows (0.93%)
    22 cleaned variants: 6 rows (2.79%)
    23 cleaned variants: 15 rows (6.98%)
    24 cleaned variants: 28 rows (13.02%)
    25 cleaned variants: 153 rows (71.16%)

Summary for output-psm-prompt4-qwq.csv:
  Total rows processed: 215
  Clean rows: 213 (99.07%)
  Noise rows: 2 (0.93%)
  Distribution of cleaned variants per clean row:
    4 cleaned variants: 2 rows (0.93%)
    7 cleaned variants: 1 rows (0.47%)
    8 cleaned variants: 2 rows (0.93%)
    9 cleaned variants: 1 rows (0.47%)
    12 cleaned variants: 1 rows (0.47%)
    13 cleaned variants: 1 rows (0.47%)
    14 cleaned variants: 1 rows (0.47%)
    15 cleaned variants: 2 rows (0.93%)
    16 cleaned variants: 1 rows (0.47%)
    17 cleaned variants: 1 rows (0.47%)
    18 cleaned variants: 1 rows (0.47%)
    19 cleaned variants: 3 rows (1.40%)
    20 cleaned variants: 1 rows (0.47%)
    22 cleaned variants: 1 rows (0.47%)
    23 cleaned variants: 4 rows (1.86%)
    24 cleaned variants: 13 rows (6.05%)
    25 cleaned variants: 177 rows (82.33%)