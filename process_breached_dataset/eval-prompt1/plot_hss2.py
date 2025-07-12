import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Model files mapping
files = {
    "Qwen-1.5B": "output-computed-prompt1-1.5b.csv",
    "Llama-8B": "output-computed-prompt1-8b.csv",
    "Qwen-14B": "output-computed-prompt1-14b.csv"
}

# Define bins and labels for histogram
bins = [-1e-9, 0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 
        0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.0001]

labels = [
    "0", "0.0001-0.0500", "0.0501-0.1000", "0.1001-0.1500", "0.1501-0.2000",
    "0.2001-0.2500", "0.2501-0.3000", "0.3001-0.3500", "0.3501-0.4000", "0.4001-0.4500",
    "0.4501-0.5000", "0.5001-0.5500", "0.5501-0.6000", "0.6001-0.6500", "0.6501-0.7000",
    "0.7001-0.7500", "0.7501-0.8000", "0.8001-0.8500", "0.8501-0.9000", "0.9001-0.9500",
    "0.9501-0.9999", "1"
]

# Process data for each model
hist_data = {}
for model, filename in files.items():
    df = pd.read_csv(filename)
    
    # Ensure numeric conversion with proper error handling
    df["average_case_sensitive_hss"] = pd.to_numeric(df["average_case_sensitive_hss"], errors="coerce")
    df["average_case_insensitive_hss"] = pd.to_numeric(df["average_case_insensitive_hss"], errors="coerce")
    
    # Create binned data
    cs_bins = pd.cut(df["average_case_sensitive_hss"].dropna(), bins=bins, labels=labels, include_lowest=True)
    ci_bins = pd.cut(df["average_case_insensitive_hss"].dropna(), bins=bins, labels=labels, include_lowest=True)
    
    # Count occurrences in each bin
    cs_counts = cs_bins.value_counts().sort_index()
    ci_counts = ci_bins.value_counts().sort_index()
    
    hist_data[model] = {"cs": cs_counts, "ci": ci_counts}

# Create subplots with better spacing
fig = make_subplots(
    rows=1, 
    cols=len(hist_data),
    subplot_titles=[f"<b>{model}</b>" for model in hist_data.keys()],
    horizontal_spacing=0.05  # Reduced spacing
)

# Define colors for consistency
colors = {"cs": "#4E79A7", "ci": "#F28E2B"}

# Add traces for each model
col = 1
for model, counts in hist_data.items():
    x_vals = labels
    
    # Get y values, defaulting to 0 for missing labels
    cs_y = [counts["cs"].get(label, 0) for label in labels]
    ci_y = [counts["ci"].get(label, 0) for label in labels]
    
    # Add case sensitive bars
    fig.add_trace(
        go.Bar(
            x=x_vals,
            y=cs_y,
            name="Case Sensitive PW1",
            marker_color=colors["cs"],
            marker_line_width=0.5,
            marker_line_color="rgba(0,0,0,0.3)",
            opacity=0.9,
            width=0.7, 
            showlegend=(col == 1)  # Only show legend for first column
        ),
        row=1, col=col
    )
    
    # Add case insensitive bars
    fig.add_trace(
        go.Bar(
            x=x_vals,
            y=ci_y,
            name="Case Insensitive PW1",
            marker_color=colors["ci"],
            marker_line_width=0.5,
            marker_line_color="rgba(0,0,0,0.3)",
            opacity=0.9,
            width=0.7, 
            showlegend=(col == 1)  # Only show legend for first column
        ),
        row=1, col=col
    )
    
    # Add the 0.5 threshold line
    # Find appropriate index for 0.5 threshold
    threshold_index = labels.index("0.4501-0.5000")  # Label that contains 0.5
    
    # Calculate maximum y value for this column (sum of both series)
    max_y_value = max(sum(x) for x in zip(cs_y, ci_y))
    
    fig.add_shape(
        type="line",
        x0=x_vals[threshold_index],
        y0=0,
        x1=x_vals[threshold_index],
        y1=max_y_value * 1.1,
        line=dict(
            color="rgba(0, 0, 0, 0.8)",
            width=2,
            dash="dash",
        ),
        row=1, col=col
    )
    
    # Add annotation for the threshold
    fig.add_annotation(
        x=x_vals[threshold_index],
        y=max_y_value * 1.25,
        text="<b>0.5 threshold</b>",
        showarrow=False,
        textangle=-90,
        font=dict(size=11, color="black"),
        row=1, col=col
    )
    
    col += 1
        

# Update layout with improved parameters
fig.update_layout(
    barmode="stack",
    height=600,
    width=1500,  # Slightly reduced width
    title={
        'text': "<b>Hybrid Similarity Score (HSS) Distribution for Test Case: Prompt 1</b>",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    margin=dict(l=40, r=40, t=80, b=120),  # Increased top margin for title
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
    font=dict(family="Arial, sans-serif"),
    template="plotly_white"  # Cleaner background
)

# Update x and y axes with consistent formatting
for i in range(1, len(hist_data) + 1):
    # X-axis formatting
    if threshold_index + 5 < len(labels):  # Ensure index is within range
        fig.add_annotation(
            x=labels[threshold_index + 5],  # Position in the higher region
            y=5,  # Adjust y for visibility
            text="Higher HSS Scores",
            showarrow=False,
            font=dict(size=12, color="rgba(0,0,0,0.5)"),
            row=1, col=i
        )
    fig.update_xaxes(
        title_text="HSS Score",
        tickangle=-45,
        tickfont=dict(size=8),  # Slightly smaller font
        title_font=dict(size=12),
        row=1,
        col=i
    )
    
    # Y-axis formatting - only add title to first column
    fig.update_yaxes(
        title_text="Count" if i == 1 else "",
        title_font=dict(size=12),
        row=1,
        col=i
    )

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

# Save the figure (optional)
# fig.write_image("hss_distribution.png", scale=2)

# Display the figure
fig.show()