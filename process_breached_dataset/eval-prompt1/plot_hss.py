import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil

# Model files mapping
files = {
    "DeepSeek-R1-Qwen-1.5B": "output-computed-prompt1-1.5b.csv",
    "DeepSeek-R1-Llama-8B": "output-computed-prompt1-8b.csv",
    "DeepSeek-R1-Qwen-14B": "output-computed-prompt1-14b.csv",
    "Qwen3-1.7B": "output-computed-prompt1-qwen3-1.7.csv",
    "Qwen3-8B": "output-computed-prompt1-qwen3-8.csv",
    "Qwen3-14B": "output-computed-prompt1-qwen3-14.csv",
    "Phi4-Reasoning-14B": "output-computed-prompt1-phi4.csv",
}

# Define histogram bins and labels
bins = [-1e-9, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
        0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.0001]

labels = [
    "0", "0.0001-0.0500", "0.0501-0.1000", "0.1001-0.1500", "0.1501-0.2000",
    "0.2001-0.2500", "0.2501-0.3000", "0.3001-0.3500", "0.3501-0.4000", "0.4001-0.4500",
    "0.4501-0.5000", "0.5001-0.5500", "0.5501-0.6000", "0.6001-0.6500", "0.6501-0.7000",
    "0.7001-0.7500", "0.7501-0.8000", "0.8001-0.8500", "0.8501-0.9000", "0.9001-0.9500",
    "0.9501-0.9999", "1"
]

# Process histogram data
hist_data = {}
for model, filename in files.items():
    df = pd.read_csv(filename)
    df["average_case_sensitive_hss"] = pd.to_numeric(df["average_case_sensitive_hss"], errors="coerce")
    df["average_case_insensitive_hss"] = pd.to_numeric(df["average_case_insensitive_hss"], errors="coerce")
    
    cs_bins = pd.cut(df["average_case_sensitive_hss"].dropna(), bins=bins, labels=labels, include_lowest=True)
    ci_bins = pd.cut(df["average_case_insensitive_hss"].dropna(), bins=bins, labels=labels, include_lowest=True)
    
    cs_counts = cs_bins.value_counts().sort_index()
    ci_counts = ci_bins.value_counts().sort_index()
    
    hist_data[model] = {"cs": cs_counts, "ci": ci_counts}

# Layout for subplots
cols_per_row = 3
total_models = len(hist_data)
rows = ceil(total_models / cols_per_row)

fig = make_subplots(
    rows=rows,
    cols=cols_per_row,
    subplot_titles=[f"<b>{model}</b>" for model in hist_data.keys()],
    horizontal_spacing=0.075,
    vertical_spacing=0.115
)

colors = {"cs": "#4E79A7", "ci": "#F28E2B"}
threshold_index = labels.index("0.4501-0.5000")

# Add histograms
row, col = 1, 1
for model, counts in hist_data.items():
    x_vals = labels
    cs_y = [counts["cs"].get(label, 0) for label in labels]
    ci_y = [counts["ci"].get(label, 0) for label in labels]
    
    fig.add_trace(go.Bar(
        x=x_vals, y=cs_y, name="Case Sensitive", marker_color=colors["cs"],
        showlegend=(row == 1 and col == 1), opacity=0.9),
        row=row, col=col
    )
    fig.add_trace(go.Bar(
        x=x_vals, y=ci_y, name="Case Insensitive", marker_color=colors["ci"],
        showlegend=(row == 1 and col == 1), opacity=0.9),
        row=row, col=col
    )
    
    max_y = max(cs_y[i] + ci_y[i] for i in range(len(labels)))
    
    fig.add_shape(type="line", x0=x_vals[threshold_index], y0=0,
                  x1=x_vals[threshold_index], y1=max_y * 1.1,
                  line=dict(color="black", width=2, dash="dash"),
                  row=row, col=col)
    
    fig.add_annotation(x=x_vals[threshold_index], y=max_y * 1.15,
                       text="<b>0.50</b>", showarrow=False, textangle=-90,
                       font=dict(size=11, color="black"), row=row, col=col)
    
    fig.update_xaxes(title_text="HSS Score", tickangle=-45, tickfont=dict(size=8), row=row, col=col)
    fig.update_yaxes(title_text="Count" if col == 1 else "", row=row, col=col)
    
    col += 1
    if col > cols_per_row:
        col = 1
        row += 1

fig.update_layout(
    barmode="stack",
    height=1450,
    width=1024,
    title={'text': "<b>Hybrid Similarity Score (HSS) Distribution for Test Case: Prompt 1</b>",
           'x': 0.5, 'y': 0.99, 'xanchor': 'center', 'yanchor': 'top'},
    margin=dict(l=40, r=40, t=80, b=120),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    template="plotly_white"
)

fig.add_annotation(
    x=0.5, y=-0.25, xref="paper", yref="paper",
    text="Note: HSS ≥ 0.5 indicates likely tweaks. Case-insensitive scores reveal capitalization-based reuse.",
    showarrow=False, font=dict(size=12), align="center"
)

# ---- Export CSV for Line Plot (False Negative Rate vs Threshold) ----
def frange(start, stop, step):
    while start < stop:
        yield round(start, 10)
        start += step

def export_tpr_fnr_csv(hist_data, output_filename="tpr_fnr_prompt1.csv"):
    thresholds = [round(x, 2) for x in list(frange(0.1, 0.96, 0.05))]
    data = []

    for model, counts in hist_data.items():
        for mode in ["cs", "ci"]:
            total = sum(counts[mode].values)
            row = {"model": f"{model} ({'CS' if mode == 'cs' else 'CI'})"}
            for t in thresholds:
                fn_count = 0
                for label, count in counts[mode].items():
                    try:
                        upper_bound = float(label.split("-")[-1])
                        if upper_bound < t:
                            fn_count += count
                    except ValueError:
                        continue
                tp_count = total - fn_count
                fnr = (fn_count / total) * 100 if total > 0 else 0
                tpr = (tp_count / total) * 100 if total > 0 else 0
                row[f"TPR@{t:.2f}"] = round(tpr, 2)
                row[f"FNR@{t:.2f}"] = round(fnr, 2)
            data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(output_filename, index=False)
    print(f"✅ TPR & FNR CSV saved as: {output_filename}")

# Generate and export TPR-FNR CSV
export_tpr_fnr_csv(hist_data)


# Show plot
fig.show()
