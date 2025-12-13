import seaborn as sns

df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())
possible_values = list(set(df.select_dtypes(include=['object','int','bool','category']).columns) - set(['survived']))
possible_values
var = 'who'
pdf = df.groupby([var], dropna=False, observed=False).agg(
    **{
        "n": ("survived", "size"),
        "survived_rate": ("survived", "mean"),
    }
)
pdf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bar chart for count
fig.add_trace(
    go.Bar(x=pdf.index, y=pdf["n"], name="Count", marker_color='teal'),
    secondary_y=False,
)

# Add line chart for survival rate
fig.add_trace(
    go.Scatter(x=pdf.index, y=pdf["survived_rate"], name="Survival Rate", 
               mode='lines+markers', line=dict(color='red'), marker=dict(size=8)),
    secondary_y=True,
)

# Set axis titles
fig.update_xaxes(title_text=var)
fig.update_yaxes(title_text="Count", secondary_y=False)
fig.update_yaxes(title_text="Survival Rate", secondary_y=True)

fig.update_layout(title_text="Titanic Survival Analysis")

# Save to HTML file
fig.write_html("output_plotly.html")
# Or show interactively
# fig.show()