import plotly.graph_objects as go
import google_sheets_API_func as api

df = api.downloadSheet('1JLS4Xw8Y_diX6hravLxDR3fdTLHl5hC_DK2nomyc8Is', 'calc')
source = df['source'].tolist()
target = df['target'].tolist()
values = df['value'].tolist()
color_link = df['color'].tolist()

df = api.downloadSheet('1JLS4Xw8Y_diX6hravLxDR3fdTLHl5hC_DK2nomyc8Is', 'misc')
label = df['result'].tolist()
color_node = df['color'].tolist()

fig = go.Figure(go.Sankey(
    arrangement="freeform",
    node=dict(
        pad=1, thickness=5, line=dict(color="black", width=0.5),
        label=label, color=color_node
    ),
    link = dict(
        arrowlen=25, source = source, target = target, value = values, color = color_link
    )
))

fig.update_traces(textfont_size = 20, textfont_shadow = "white 1px 0 20px", textfont_weight = 600)

fig.update_layout(title_text="Job Search Results",
    font_size=10,
    margin=dict(
        l=200,
        r=200,
        t=200
    )
)
fig.show()

