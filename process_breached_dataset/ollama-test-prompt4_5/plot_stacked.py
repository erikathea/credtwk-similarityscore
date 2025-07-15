import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# CSV paths
csv_paths = {
    "Deepseek-R1-32B": "output-computed-prompt2-deepseek.csv",
    "Qwen-QwQ-32B": "output-computed-prompt2-qwq.csv",
    "Qwen3-32B": "output-computed-prompt2-qwen3.csv",
    "Magistral-24B": "output-computed-prompt2-magistral.csv"
}

#csv_paths = {
#    "Deepseek-R1-32B": "output-computed-prompt4-deepseek.csv",
#    "Qwen-QwQ-32B": "output-computed-prompt4-qwq.csv",
#    "Qwen3-32B": "output-computed-prompt4-qwen3.csv",
#    "Magistral-24B": "output-computed-prompt4-magistral.csv"
#}

# Color map
colors = {
    "cs_pw1": "#4E79A7",  # blue
    "ci_pw1": "#F28E2B",  # orange
    "cs_pw2": "#59A14F",  # green
    "ci_pw2": "#E15759",  # red
}

# Load and reshape
records = []
for model, path in csv_paths.items():
    df = pd.read_csv(path)
    for case in ["cs", "ci"]:
        for pw in ["pw1", "pw2"]:
            records.append(pd.DataFrame({
                "Model": model,
                "HSS Score": df[f"ave_{case}_hss_{pw}"],
                "Group": f"{case}_{pw}"
            }))
alldata = pd.concat(records, ignore_index=True)

# Plot
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(20, 6))

sns.violinplot(
    data=alldata,
    x="Model", y="HSS Score", hue="Group",
    order=list(csv_paths.keys()),
    palette=colors,
    scale="width", cut=0, dodge=True, bw=0.2, ax=ax
)

# Add 0.5 threshold
ax.axhline(0.5, color="black", linestyle="--", linewidth=1)
ax.text(-0.65, 0.48, "0.5 Threshold", color="black", fontsize=12, va="bottom")

# Vertical separators between models
xticks = ax.get_xticks()
for i in range(len(xticks) - 1):
    midpoint = (xticks[i] + xticks[i + 1]) / 2
    ax.axvline(midpoint, color='black', linestyle='dashed', linewidth=0.75)
for i in range(len(xticks)):
    plt.plot([xticks[i]], [-0.01], marker='v', color='black', transform=ax.get_xaxis_transform(), clip_on=False)

# Axis formatting
ax.set_title("HSS Scores for Password Variants Generated using Prompt 4", fontsize=16, pad=25)
#ax.set_title("HSS Scores for Password Variants Generated using Prompt 5", fontsize=16, pad=25)
ax.set_xlabel("Reasoning Models", fontsize=14)
ax.set_ylabel("HSS Scores", fontsize=14)
#plt.xticks(rotation=25, ha="right")
plt.ylim(0, 1)

# Custom legend
label_map = {
    "cs_pw1": "Case Sensitive HSS(pw1, pw-var)",
    "cs_pw2": "Case Sensitive HSS(pw2, pw-var)",
    "ci_pw1": "Case Insensitive HSS(pw1, pw-var)",
    "ci_pw2": "Case Insensitive HSS(pw2, pw-var)",
}
label_order = ["cs_pw1", "cs_pw2", "ci_pw1", "ci_pw2"]
handles = [Patch(color=colors[l], label=label_map[l]) for l in label_order]
ax.legend(
    handles=handles,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.07),
    ncol=4,
    frameon=False,
    fontsize=12,
    title_fontsize=14
)

plt.tight_layout()
plt.savefig("hss_violin_prompt4.png", dpi=600, bbox_inches="tight")
#plt.savefig("hss_violin_prompt5.png", dpi=600, bbox_inches="tight")
plt.show()
