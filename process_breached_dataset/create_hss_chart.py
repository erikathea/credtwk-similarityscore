import plotly.graph_objects as go

# Data
hss_ranges = [
    "0", "0.0001-0.0500", "0.0501-0.1000", "0.1001-0.1500", "0.1501-0.2000",
    "0.2001-0.2500", "0.2501-0.3000", "0.3001-0.3500", "0.3501-0.4000", "0.4001-0.4500",
    "0.4501-0.5000", "0.5001-0.5500", "0.5501-0.6000", "0.6001-0.6500", "0.6501-0.7000",
    "0.7001-0.7500", "0.7501-0.8000", "0.8001-0.8500", "0.8501-0.9000", "0.9001-0.9500",
    "0.9501-0.9999", "1"
]

case_sensitive = [
    395656323, 163481779, 298551477, 352394316, 361746144, 323499716, 275099666,
    222228157, 177527989, 145493041, 131111049, 131197515, 136772076, 150793961,
    165239926, 171803486, 148834063, 131715673, 105585494, 86079611, 14221318, 0
]

case_insensitive = [
    307731723, 151968935, 278766712, 348215780, 369308116, 335057001, 287280384,
    231832311, 184559043, 150147325, 133700725, 134908380, 141870541, 155791295,
    169540812, 176742320, 153828163, 137241762, 109486798, 99627839, 21424140, 10002675
]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=hss_ranges,
    y=case_sensitive,
    name="Case Sensitive",
    marker=dict(color="teal")
))

fig.add_trace(go.Bar(
    x=hss_ranges,
    y=case_insensitive,
    name="Case Insensitive",
    marker=dict(color="coral")
))

fig.update_layout(
    template="plotly_white",
    title="Case-Sensitive vs Case-Insensitive Password-to-Password HSS Scores Comparison",
    title_x=0.5,
    xaxis_title="HSS Score Ranges",
    yaxis_title="Count of Password Pairs",
    barmode="group",
    xaxis=dict(tickangle=-45),
    height=600,
    width=1000,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=80, b=80)
)

# Format y-axis ticks with commas
fig.update_yaxes(tickformat=",")

fig.show()
