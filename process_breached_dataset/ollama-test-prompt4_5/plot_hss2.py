import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Example CSV mapping with defined order
#files = {
#    "Deepseek-R1-32B": "output-computed-prompt2-deepseek.csv",
#    "Qwen-QwQ-32B": "output-computed-prompt2-qwq.csv",
#    "Qwen3-32B": "output-computed-prompt2-qwen3.csv",
#    "Magistral-24B": "output-computed-prompt2-magistral.csv"
#}

files = {
    "Deepseek-R1-32B": "output-computed-prompt4-deepseek.csv",
    "Qwen-QwQ-32B": "output-computed-prompt4-qwq.csv",
    "Qwen3-32B": "output-computed-prompt4-qwen3.csv",
    "Magistral-24B": "output-computed-prompt4-magistral.csv"
}

# Define the specific order for the models
model_order = list(files.keys())

# Define bins and labels for HSS score ranges
bins = [-1e-9, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
        0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.0001]
labels_bin = [
    "0", "0.0001-0.0500", "0.0501-0.1000", "0.1001-0.1500", "0.1501-0.2000",
    "0.2001-0.2500", "0.2501-0.3000", "0.3001-0.3500", "0.3501-0.4000", "0.4001-0.4500",
    "0.4501-0.5000", "0.5001-0.5500", "0.5501-0.6000", "0.6001-0.6500", "0.6501-0.7000",
    "0.7001-0.7500", "0.7501-0.8000", "0.8001-0.8500", "0.8501-0.9000", "0.9001-0.9500",
    "0.9501-0.9999", "1"
]

# Index where 0.5 threshold is located
threshold_index = 10  # "0.4501-0.5000" is at index 10

# We'll store binned data for each model, for all four metrics separately
model_data = {}
for model, filename in files.items():
    df = pd.read_csv(filename)
    
    # Convert columns to numeric
    for col in ["ave_cs_hss_pw1", "ave_ci_hss_pw1", "ave_cs_hss_pw2", "ave_ci_hss_pw2"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Keep pw1 and pw2 separate
    cs_pw1_data = df["ave_cs_hss_pw1"].dropna()
    ci_pw1_data = df["ave_ci_hss_pw1"].dropna()
    cs_pw2_data = df["ave_cs_hss_pw2"].dropna()
    ci_pw2_data = df["ave_ci_hss_pw2"].dropna()
    
    # Bin the data
    cs_pw1_binned = pd.cut(cs_pw1_data, bins=bins, labels=labels_bin, include_lowest=True)
    ci_pw1_binned = pd.cut(ci_pw1_data, bins=bins, labels=labels_bin, include_lowest=True)
    cs_pw2_binned = pd.cut(cs_pw2_data, bins=bins, labels=labels_bin, include_lowest=True)
    ci_pw2_binned = pd.cut(ci_pw2_data, bins=bins, labels=labels_bin, include_lowest=True)

    # Count occurrences in each bin
    cs_pw1_counts = cs_pw1_binned.value_counts().sort_index()
    ci_pw1_counts = ci_pw1_binned.value_counts().sort_index()
    cs_pw2_counts = cs_pw2_binned.value_counts().sort_index()
    ci_pw2_counts = ci_pw2_binned.value_counts().sort_index()
    
    # Convert to lists (in the same bin order)
    cs_pw1_vals = [cs_pw1_counts.get(lb, 0) for lb in labels_bin]
    ci_pw1_vals = [ci_pw1_counts.get(lb, 0) for lb in labels_bin]
    cs_pw2_vals = [cs_pw2_counts.get(lb, 0) for lb in labels_bin]
    ci_pw2_vals = [ci_pw2_counts.get(lb, 0) for lb in labels_bin]
    
    model_data[model] = {
        "cs_pw1": cs_pw1_vals, 
        "ci_pw1": ci_pw1_vals,
        "cs_pw2": cs_pw2_vals,
        "ci_pw2": ci_pw2_vals
    }

# Create a figure with 3 subplots (one per model)
fig = make_subplots(
    rows=1, cols=len(model_data),
    subplot_titles=[f"<b>{model}</b>" for model in model_order],
    horizontal_spacing=0.05
)

# Color scheme for the four different traces - using a more professional palette
colors = {
    "cs_pw1": "#4E79A7",  # blue
    "ci_pw1": "#F28E2B",  # orange
    "cs_pw2": "#59A14F",  # green
    "ci_pw2": "#E15759",   # red
}

# Names for the legend
names = {
    "cs_pw1": "Case Sensitive HSS PW1",
    "ci_pw1": "Case Insensitive HSS PW1",
    "cs_pw2": "Case Sensitive HSS PW2",
    "ci_pw2": "Case Insensitive HSS PW2",
}

# Order in which to stack the bars (bottom to top)
stack_order = ["cs_pw1", "ci_pw1", "cs_pw2", "ci_pw2"]

col_index = 1
for model in model_order:  # Use the defined order
    data = model_data[model]
    
    # Add bars in stacked format
    for key in stack_order:
        fig.add_trace(
            go.Bar(
                x=labels_bin,  # Use the full labels
                y=data[key],
                name=names[key],
                marker_color=colors[key],
                marker_line_width=0.5,
                marker_line_color="rgba(0,0,0,0.3)",
                opacity=0.9,
                showlegend=(col_index == 1),  # show legend only in the first subplot
                width=0.7,  # Make bars wider (80% of bin width)
            ),
            row=1, col=col_index
        )
    
    # Add the 0.5 threshold line
    max_y_value = sum([max(data[key]) for key in stack_order])  # Sum for stacked
    fig.add_shape(
        type="line",
        x0=labels_bin[threshold_index],
        y0=0,
        x1=labels_bin[threshold_index],
        y1=max_y_value * 0.95,
        line=dict(
            color="rgba(0, 0, 0, 0.8)",
            width=2,
            dash="dash",
        ),
        row=1, col=col_index
    )
    
    # Add annotation for the threshold
    fig.add_annotation(
        x=labels_bin[threshold_index],
        y=max_y_value * 0.95,
        text="<b>0.5 threshold</b>",
        showarrow=False,
        textangle=-90,
        font=dict(size=11, color="black"),
        row=1, col=col_index
    )
    
    col_index += 1

# Add a light gray background to the area above 0.5
for i in range(1, len(model_data) + 1):
    fig.add_shape(
        type="rect",
        x0=labels_bin[threshold_index],  # Start at the 0.5 threshold
        y0=0,
        x1=labels_bin[-1],  # End at the last bin
        y1=1,  # Will be adjusted with relayout
        fillcolor="rgba(230, 230, 230, 0.5)",  # Light gray with transparency
        line=dict(width=0),
        layer="below",
        row=1, col=i
    )
    
    # Add a label for the higher values region
    fig.add_annotation(
        x=labels_bin[threshold_index + 5],  # Position in the middle of the high region
        y=5,
        text="Higher HSS Scores",
        showarrow=False,
        font=dict(size=12, color="rgba(0,0,0,0.5)"),
        row=1, col=i
    )
    
    fig.update_xaxes(
        title_text="HSS Score",
        title_font=dict(size=14),
        tickangle=-45,
        tickfont=dict(size=9),
        gridcolor="rgba(220, 220, 220, 0.5)",
        showgrid=True,
        zeroline=True,
        zerolinecolor="rgba(0, 0, 0, 0.2)",
        row=1, col=i
    )
    
    fig.update_yaxes(
        title_text="Count" if i == 1 else "",
        title_font=dict(size=14),
        tickfont=dict(size=10),
        gridcolor="rgba(220, 220, 220, 0.5)",
        showgrid=True,
        zeroline=True,
        zerolinecolor="rgba(0, 0, 0, 0.2)",
        row=1, col=i
    )

# Update overall layout
fig.update_layout(
    title={
        #'text': '<b>Hybrid Similarity Score (HSS) Distribution for Test Case 4 - Prompt 4 (Prompt 2)</b>',
        'text': '<b>Hybrid Similarity Score (HSS) Distribution for Test Case 5 - Prompt 5 (Prompt 4)</b>',
        'y': 0.98,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    barmode="stack",  # Change to stacked bar mode
    bargap=0.2,       # Gap between bins (20% of bin width)
    height=650,
    width=1800,
    margin=dict(l=50, r=40, t=80, b=120),  # Increased bottom margin for labels
    paper_bgcolor="white",
    plot_bgcolor="white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="rgba(0, 0, 0, 0.2)",
        borderwidth=1
    ),
    font=dict(family="Arial, sans-serif")
)

# Add a caption/note below the plot
fig.add_annotation(
    x=0.5,
    y=-0.25,
    xref="paper",
    yref="paper",
    text="Note: HSS scores indicate the matching quality between model responses and references.Higher scores (>0.5) generally indicate better matching.",
    showarrow=False,
    font=dict(size=12),
    align="center"
)

fig.show()

def export_tpr_fnr_csv(model_data, labels_bin, output_filename="tpr_fnr_prompt.csv"):
    import numpy as np

    thresholds = np.round(np.arange(0.1, 0.96, 0.05), 2)
    data = []

    for model, counts in model_data.items():
        for key in ["cs_pw1", "ci_pw1", "cs_pw2", "ci_pw2"]:
            label = f"{model} ({key.upper()})"
            total = sum(counts[key])
            row = {"model": label}
            for t in thresholds:
                fn_count = 0
                for i, bin_label in enumerate(labels_bin):
                    try:
                        upper = float(bin_label.split("-")[-1])
                        if upper < t:
                            fn_count += counts[key][i]
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

#export_tpr_fnr_csv(model_data, labels_bin, "tpr_fnr_prompt2-testcase4.csv")
export_tpr_fnr_csv(model_data, labels_bin, "tpr_fnr_prompt4-testcase5.csv")
