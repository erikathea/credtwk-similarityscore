import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

files = {
    "Qwen-1.5B": "output-computed-prompt2-1.5b.csv",
    "Llama-8B": "output-computed-prompt2-8b.csv",
    "Qwen-14B": "output-computed-prompt2-14b.csv"
}

# Dictionaries to hold model-level results.
overall_avg = {}  # For overall average HSS per model
user_avg = {}     # For average user HSS per model
dist_combined = {}  # For combined distribution: for each model, combined CS and CI

# Process each model's CSV file.
for model, filename in files.items():
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    # Convert relevant columns to numeric.
    for col in ["ave_cs_hss_pw1", "ave_ci_hss_pw1", "ave_cs_hss_pw2", "ave_ci_hss_pw2"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Compute per-row overall HSS as the average of pw1 and pw2 (for CS and CI separately)
    df["overall_cs"] = (df["ave_cs_hss_pw1"] + df["ave_cs_hss_pw2"]) / 2.0
    df["overall_ci"] = (df["ave_ci_hss_pw1"] + df["ave_ci_hss_pw2"]) / 2.0
    overall_cs_mean = df["overall_cs"].mean()
    overall_ci_mean = df["overall_ci"].mean()
    overall_avg[model] = {"cs": overall_cs_mean, "ci": overall_ci_mean}

    # Compute user averages if available.
    if "ave_cs_hss_user" in df.columns and "ave_ci_hss_user" in df.columns:
        df["ave_cs_hss_user"] = pd.to_numeric(df["ave_cs_hss_user"], errors="coerce")
        df["ave_ci_hss_user"] = pd.to_numeric(df["ave_ci_hss_user"], errors="coerce")
        user_cs_mean = df["ave_cs_hss_user"].mean()
        user_ci_mean = df["ave_ci_hss_user"].mean()
        user_avg[model] = {"cs": user_cs_mean, "ci": user_ci_mean}

    # For distributions, combine the case-sensitive columns (pw1 & pw2) and similarly for case-insensitive.
    cs_combined = pd.concat([df["ave_cs_hss_pw1"].dropna(), df["ave_cs_hss_pw2"].dropna()])
    ci_combined = pd.concat([df["ave_ci_hss_pw1"].dropna(), df["ave_ci_hss_pw2"].dropna()])
    dist_combined[model] = {"cs": cs_combined, "ci": ci_combined}

# --------------------------
# Figure 1: Overall Average HSS per Model
models = list(overall_avg.keys())
overall_cs_vals = [overall_avg[m]["cs"] for m in models]
overall_ci_vals = [overall_avg[m]["ci"] for m in models]

x = np.arange(len(models))
width = 0.35

fig1, ax1 = plt.subplots(figsize=(8, 6))
rects1 = ax1.bar(x - width/2, overall_cs_vals, width, color="#008080")  # teal
rects2 = ax1.bar(x + width/2, overall_ci_vals, width, color="#FF7F50")  # coral

ax1.text(0.4, 1.01, "■ Case Sensitive", color="#008080", 
        transform=ax1.transAxes, ha='center', fontsize=10)
ax1.text(0.6, 1.01, "■ Case Insensitive", color="#FF7F50", 
        transform=ax1.transAxes, ha='center', fontsize=10)

ax1.set_ylabel("Average Hybrid Similarity Score (Prompt 2)")
ax1.set_xlabel("DeepSeek-R1 Distilled Model")
ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.legend().remove()
#ax1.set_title("Overall Average HSS per Model")
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax1.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")

autolabel(rects1)
autolabel(rects2)
ax1.set_facecolor('white')
fig1.patch.set_facecolor('white')
plt.subplots_adjust(top=0.92)
plt.tight_layout()
plt.show()

# --------------------------
# Figure 2: Average User HSS per Model (if available)
if user_avg:
    models_user = list(user_avg.keys())
    user_cs_vals = [user_avg[m]["cs"] for m in models_user]
    user_ci_vals = [user_avg[m]["ci"] for m in models_user]

    x_user = np.arange(len(models_user))
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    r1 = ax2.bar(x_user - width/2, user_cs_vals, width, color="teal")
    r2 = ax2.bar(x_user + width/2, user_ci_vals, width, color="coral")
    ax2.text(0.4, 1.01, "■ Case Sensitive", color="#008080", 
        transform=ax2.transAxes, ha='center', fontsize=10)
    ax2.text(0.6, 1.01, "■ Case Insensitive", color="#FF7F50", 
        transform=ax2.transAxes, ha='center', fontsize=10)

    ax2.set_ylabel("Average User HSS (Prompt 2)")
    ax2.set_xlabel("DeepSeek-R1 Distilled Model")
    ax2.set_xticks(x_user)
    ax2.set_xticklabels(models_user)
    ax2.legend().remove()
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax2.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom")

    autolabel(r1)
    autolabel(r2)
    ax2.set_facecolor('white')
    fig2.patch.set_facecolor('white')
    plt.subplots_adjust(top=0.92)
    plt.tight_layout()
    plt.show()

# --------------------------
# Figure 3: Distribution of Combined Variant HSS per Model
# (Combined from ave_cs_hss_pw1 & ave_cs_hss_pw2 for CS and similarly for CI)

# Define bins and labels.
bins = [-1e-9, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
        0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.0001]
labels_bin = [
    "0", "0.0001-0.0500", "0.0501-0.1000", "0.1001-0.1500", "0.1501-0.2000",
    "0.2001-0.2500", "0.2501-0.3000", "0.3001-0.3500", "0.3501-0.4000", "0.4001-0.4500",
    "0.4501-0.5000", "0.5001-0.5500", "0.5501-0.6000", "0.6001-0.6500", "0.6501-0.7000",
    "0.7001-0.7500", "0.7501-0.8000", "0.8001-0.8500", "0.8501-0.9000", "0.9001-0.9500",
    "0.9501-1.0000", "1"
]

# Create one figure with one subplot per model.
n_models = len(dist_combined)
fig3, axs3 = plt.subplots(n_models, 1, figsize=(12, 4 * n_models))
if n_models == 1:
    axs3 = [axs3]

for i, model in enumerate(sorted(dist_combined.keys())):
    cs_data = dist_combined[model]["cs"]
    ci_data = dist_combined[model]["ci"]

    # Bin the data.
    cs_binned = pd.cut(cs_data, bins=bins, labels=labels_bin, include_lowest=True)
    ci_binned = pd.cut(ci_data, bins=bins, labels=labels_bin, include_lowest=True)
    
    cs_counts = cs_binned.value_counts().sort_index()
    ci_counts = ci_binned.value_counts().sort_index()

    # Create a grouped bar chart for this model.
    x_vals = np.arange(len(labels_bin))
    bar_width = 0.4
    ax = axs3[i]
    rects_cs = ax.bar(x_vals - bar_width/2, cs_counts.values, bar_width, label="Case Sensitive", color="teal", alpha=0.7)
    rects_ci = ax.bar(x_vals + bar_width/2, ci_counts.values, bar_width, label="Case Insensitive", color="coral", alpha=0.7)
    ax.set_xticks(x_vals)
    ax.set_xticklabels(labels_bin, rotation=-45, fontsize=8)
    ax.set_ylabel("Count")
    ax.set_xlabel("HSS Score Ranges")
    ax.set_title(f"{model} - Distribution of Combined Variant HSS")
    ax.legend()
    # Annotate bars with counts.
    for rect in list(rects_cs) + list(rects_ci):
        height = rect.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', 
                        xy=(rect.get_x() + rect.get_width()/2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom")
plt.tight_layout()
plt.show()
