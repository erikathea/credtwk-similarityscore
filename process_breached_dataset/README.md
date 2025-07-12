go mod init process_breached_dataset
go mod tidy
go build process_breached_dataset.go

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/a/group1 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/a/group1 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_a-group1

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/a/group2 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/a/group2 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_a-group2

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/a/group3 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/a/group3 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_a-group3

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/a/group4 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/a/group4 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_a-group4

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/e \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/e \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_e

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/o \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/o \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_o

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/p \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/p \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_p

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/q \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/q \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_q

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/r \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/r \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_r

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/s/group1 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/s/group1 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_s-group1

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/s/group2 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/s/group2 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_s-group2

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/s/group3 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/s/group3 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_s-group3

find ../COMB-pw-dump/CompilationOfManyBreaches/COMB-data/s/group4 \
     ../4iQ-pw-dump/BreachCompilation/4iQ-data/s/group4 \
     -type f -print0 | xargs -0 cat | ./process_breached_dataset cleaned_s-group4

----

# ollama tests

source ~/myvenv/bin/activate
python -m http.server 8000

cd ollama-test
ollama serve
go build deepseek-generate_pw_var.go

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group2/password_pairs_1.csv" -prompt=2 -variants=10

./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group3/password_pairs_1.csv" -prompt=3-variants=10


./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_a-group1/password_pairs_1.csv" -prompt=1 -variants=10

cd process_breached_dataset/ollama-test-prompt2-14b
./deepseek-generate_pw_var -model="deepseek-r1:14b" -csv="../cleaned_a-group2/password_pairs_1.csv" -prompt=2 -variants=10

cd process_breached_dataset/ollama-test-prompt3-14b
./deepseek-generate_pw_var -model="deepseek-r1:8b" -csv="../cleaned_a-group3/password_pairs_1.csv" -prompt=3 -variants=10

