import pandas as pd

def compute_averages(input_file, output_file):
    """
    Reads the 'cleaned' CSV with headers like:
      username, pw1, pw2,
      variant1, cs_hss_pw1_1, ci_hss_pw1_1, cs_hss_pw2_1, ci_hss_pw2_1, cs_hss_user_1, ci_hss_user_1,
      ...
      variant10, cs_hss_pw1_10, ci_hss_pw1_10, cs_hss_pw2_10, ci_hss_pw2_10, cs_hss_user_10, ci_hss_user_10,
      total_duration

    Computes per-row averages:
      ave_cs_hss_pw1, ave_ci_hss_pw1, ave_cs_hss_pw2, ave_ci_hss_pw2, ave_cs_hss_user, ave_ci_hss_user

    The 'num_variants' is the count of non-empty variants in that row.
    Saves output to a new CSV with header:
      username, pw1, pw2, num_variants, ave_cs_hss_pw1, ave_ci_hss_pw1, ave_cs_hss_pw2, ave_ci_hss_pw2, ave_cs_hss_user, ave_ci_hss_user, total_duration
    """
    df = pd.read_csv(input_file)

    usernames = []
    pw1s = []
    pw2s = []
    num_variants_list = []
    ave_cs_hss_pw1_list = []
    ave_ci_hss_pw1_list = []
    ave_cs_hss_pw2_list = []
    ave_ci_hss_pw2_list = []
    ave_cs_hss_user_list = []
    ave_ci_hss_user_list = []
    total_durations = []

    for idx, row in df.iterrows():
        username = row["username"]
        pw1 = row["pw1"]
        pw2 = row["pw2"]
        total_duration = row["total_duration"]

        # Accumulators
        sum_cs_hss_pw1 = 0.0
        sum_ci_hss_pw1 = 0.0
        sum_cs_hss_pw2 = 0.0
        sum_ci_hss_pw2 = 0.0
        sum_cs_hss_user = 0.0
        sum_ci_hss_user = 0.0
        count_variants = 0

        for i in range(1, 11):
            variant_col = f"variant{i}"
            if pd.isna(row[variant_col]) or str(row[variant_col]).strip() == "":
                continue  # skip empty variant

            count_variants += 1

            # Accumulate scores (converting to float in case they're strings)
            sum_cs_hss_pw1 += float(row.get(f"cs_hss_pw1_{i}", 0) or 0)
            sum_ci_hss_pw1 += float(row.get(f"ci_hss_pw1_{i}", 0) or 0)
            sum_cs_hss_pw2 += float(row.get(f"cs_hss_pw2_{i}", 0) or 0)
            sum_ci_hss_pw2 += float(row.get(f"ci_hss_pw2_{i}", 0) or 0)
            sum_cs_hss_user += float(row.get(f"cs_hss_user_{i}", 0) or 0)
            sum_ci_hss_user += float(row.get(f"ci_hss_user_{i}", 0) or 0)

        if count_variants > 0:
            ave_cs_pw1 = sum_cs_hss_pw1 / count_variants
            ave_ci_pw1 = sum_ci_hss_pw1 / count_variants
            ave_cs_pw2 = sum_cs_hss_pw2 / count_variants
            ave_ci_pw2 = sum_ci_hss_pw2 / count_variants
            ave_cs_user = sum_cs_hss_user / count_variants
            ave_ci_user = sum_ci_hss_user / count_variants
        else:
            ave_cs_pw1 = 0.0
            ave_ci_pw1 = 0.0
            ave_cs_pw2 = 0.0
            ave_ci_pw2 = 0.0
            ave_cs_user = 0.0
            ave_ci_user = 0.0

        usernames.append(username)
        pw1s.append(pw1)
        pw2s.append(pw2)
        num_variants_list.append(count_variants)
        ave_cs_hss_pw1_list.append(ave_cs_pw1)
        ave_ci_hss_pw1_list.append(ave_ci_pw1)
        ave_cs_hss_pw2_list.append(ave_cs_pw2)
        ave_ci_hss_pw2_list.append(ave_ci_pw2)
        ave_cs_hss_user_list.append(ave_cs_user)
        ave_ci_hss_user_list.append(ave_ci_user)
        total_durations.append(total_duration)

    out_df = pd.DataFrame({
        "username": usernames,
        "pw1": pw1s,
        "pw2": pw2s,
        "num_variants": num_variants_list,
        "ave_cs_hss_pw1": ave_cs_hss_pw1_list,
        "ave_ci_hss_pw1": ave_ci_hss_pw1_list,
        "ave_cs_hss_pw2": ave_cs_hss_pw2_list,
        "ave_ci_hss_pw2": ave_ci_hss_pw2_list,
        "ave_cs_hss_user": ave_cs_hss_user_list,
        "ave_ci_hss_user": ave_ci_hss_user_list,
        "total_duration": total_durations
    })

    out_df.to_csv(output_file, index=False)
    print(f"Saved computed averages to {output_file}")

#compute_averages("output-cleaned-prompt2-8b.csv", "output-computed-prompt2-8b.csv")
#compute_averages("output-cleaned-prompt2-14b.csv", "output-computed-prompt2-14b.csv")
compute_averages("output-cleaned-prompt2-phi4.csv", "output-computed-prompt2-phi4.csv")
compute_averages("output-cleaned-prompt2-qwen3-1.7b.csv", "output-computed-prompt2-qwen3-1.7b.csv")
compute_averages("output-cleaned-prompt2-qwen3-8b.csv", "output-computed-prompt2-qwen3-8b.csv")
compute_averages("output-cleaned-prompt2-qwen3-14b.csv", "output-computed-prompt2-qwen3-14b.csv")
