import os
import glob
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.lines as mlines

# Optional: Set some global style parameters
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"]   = "white"
plt.rcParams["axes.edgecolor"]   = "#333F4B"
plt.rcParams["axes.labelcolor"]  = "#333F4B"
plt.rcParams["xtick.color"]      = "#333F4B"
plt.rcParams["ytick.color"]      = "#333F4B"
plt.rcParams["text.color"]       = "#333F4B"
plt.rcParams["font.size"]        = 12
plt.rcParams["font.family"]      = "sans-serif"

# 1. Define the expected HSS score ranges
range_keys = [
    "0",
    "0.0001-0.0500",
    "0.0501-0.1000",
    "0.1001-0.1500",
    "0.1501-0.2000",
    "0.2001-0.2500",
    "0.2501-0.3000",
    "0.3001-0.3500",
    "0.3501-0.4000",
    "0.4001-0.4500",
    "0.4501-0.5000",
    "0.5001-0.5500",
    "0.5501-0.6000",
    "0.6001-0.6500",
    "0.6501-0.7000",
    "0.7001-0.7500",
    "0.7501-0.8000",
    "0.8001-0.8500",
    "0.8501-0.9000",
    "0.9001-0.9500",
    "0.9501-0.9999",
    "1"
]

# 2. Initialize dictionaries to hold the summed counts
case_sensitive_sums = {k: 0 for k in range_keys}
case_insensitive_sums = {k: 0 for k in range_keys}

# 3. Loop over all "cleaned_*" folders and read stats.json
for folder in glob.glob("cleaned_*"):
    stats_file = os.path.join(folder, "stats.json")
    if os.path.isfile(stats_file):
        with open(stats_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract case-sensitive and case-insensitive counters
        cs_data = data.get("username_score_range_counter", {})
        ci_data = data.get("username_case_insensitive_score_range_counter", {})

        # Update sums for each range key
        for k, v in cs_data.items():
            if k in case_sensitive_sums:
                case_sensitive_sums[k] += v

        for k, v in ci_data.items():
            if k in case_insensitive_sums:
                case_insensitive_sums[k] += v

# 4. Prepare data for plotting
x_positions = range(len(range_keys))
cs_values = [case_sensitive_sums[k] for k in range_keys]
ci_values = [case_insensitive_sums[k] for k in range_keys]

# 5. Create the figure
plt.figure(figsize=(12, 8))

bar_width = 0.35

# Plot bars WITHOUT automatic legend labels
plt.bar(
    [x - bar_width/2 for x in x_positions],
    cs_values,
    width=bar_width,
    color="teal",
    label="_nolegend_"  # prevents auto legend creation
)
plt.bar(
    [x + bar_width/2 for x in x_positions],
    ci_values,
    width=bar_width,
    color="coral",
    label="_nolegend_"
)

# Configure x-axis
plt.xticks(x_positions, range_keys, rotation=45, ha="right")

# Axis labels
plt.xlabel("HSSuser Score Ranges")
plt.ylabel("Count of Password Pairs")

# Centered title with custom color and spacing
plt.title(
    "Case-Sensitive vs Case-Insensitive Username-to-Password HSSuser Scores Comparison",
    loc="center",
    fontsize=16,
    color="#0C2D48",
    pad=25  # extra spacing above the plot
)

# 6. Format y-axis ticks with commas (e.g., 50,000,000)
ax = plt.gca()
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Create SQUARE markers in the legend using lines.Line2D
cs_marker = mlines.Line2D(
    [], [], color="teal", marker="s", linestyle="None", markersize=10,
    label="Case Sensitive"
)
ci_marker = mlines.Line2D(
    [], [], color="coral", marker="s", linestyle="None", markersize=10,
    label="Case Insensitive"
)

# Place the legend horizontally below the title
plt.legend(
    handles=[cs_marker, ci_marker],
    loc="upper center",
    bbox_to_anchor=(0.5, 1.05),  # adjust vertical offset as needed
    ncol=2,
    frameon=False,              # no box around the legend
    handletextpad=0.5,
    columnspacing=1.0
)

plt.tight_layout()

# 7. Show or save the plot
plt.savefig("hss_score_distribution.png", dpi=150)
plt.show()
