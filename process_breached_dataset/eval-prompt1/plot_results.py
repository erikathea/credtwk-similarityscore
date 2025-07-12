import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = {
    "Qwen-1.5B": "output-computed-prompt1-1.5b.csv",
    "Llama-8B": "output-computed-prompt1-8b.csv",
    "Qwen-14B": "output-computed-prompt1-14b.csv"
}

summary = {}
for model, filename in files.items():
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue
    
    df['average_case_sensitive_hss'] = pd.to_numeric(df['average_case_sensitive_hss'], errors='coerce')
    df['average_case_insensitive_hss'] = pd.to_numeric(df['average_case_insensitive_hss'], errors='coerce')
    
    avg_cs = df['average_case_sensitive_hss'].mean()
    avg_ci = df['average_case_insensitive_hss'].mean()
    
    summary[model] = {"cs": avg_cs, "ci": avg_ci}

models = list(summary.keys())
cs_values = [summary[m]["cs"] for m in models]
ci_values = [summary[m]["ci"] for m in models]

x = np.arange(len(models))  # x locations for the groups
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(8, 6))

rects1 = ax.bar(x - width/2, cs_values, width, color="#008080")  # teal
rects2 = ax.bar(x + width/2, ci_values, width, color="#FF7F50")  # coral

ax.text(0.4, 1.01, "■ Case Sensitive", color="#008080", 
        transform=ax.transAxes, ha='center', fontsize=10)
ax.text(0.6, 1.01, "■ Case Insensitive", color="#FF7F50", 
        transform=ax.transAxes, ha='center', fontsize=10)

ax.set_ylabel("Average Hybrid Similarity Score (Prompt 1)")
ax.set_xlabel("DeepSeek-R1 Distilled Model")
ax.set_xticks(x)
ax.set_xticklabels(models)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")

autolabel(rects1)
autolabel(rects2)

ax.set_facecolor('white')
fig.patch.set_facecolor('white')

plt.subplots_adjust(top=0.92)

plt.tight_layout()
plt.show()