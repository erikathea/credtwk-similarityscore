import pandas as pd
import plotly.express as px

df = pd.read_csv('country-data.csv')

# if pandas doesn't automatically strip the quotes, clean the country names
if df['country'].str.startswith('"').any() and df['country'].str.endswith('"').any():
    df['country'] = df['country'].str.strip('"')

df = df[df['country'] != 'Global']

# create the choropleth map
fig = px.choropleth(
    df,
    locations='country',
    locationmode='country names',
    color='count',
    hover_name='country',
    color_continuous_scale=px.colors.sequential.Plasma,
    #title='Country Count Map'
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)

# Show the map
fig.show()