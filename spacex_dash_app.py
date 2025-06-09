import pandas as pd
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Initialize the app
app = dash.Dash(__name__)

# Load data (replace with your actual file path)
# spacex_df = pd.read_csv("spacex_launch_geo.csv")

# Sample data for demonstration (replace with your actual data loading)
spacex_df = pd.DataFrame({
    'Launch Site': ['CCAFS LC-40', 'KSC LC-39A', 'VAFB SLC-4E', 'CCAFS SLC-40'] * 25,
    'Payload Mass (kg)': [5000, 6000, 4500, 7000, 3000, 8000, 2500, 9000] * 12 + [5500, 6500, 4000, 7500],
    'class': [1, 1, 0, 1, 0, 1, 0, 1] * 12 + [1, 0, 1, 1],
    'Booster Version': ['Falcon 9 v1.1', 'Falcon 9 v1.2', 'Falcon Heavy'] * 33 + ['Falcon 9 v1.2']
})

# Calculate payload range
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Color theme
colors = {
    'bg': '#0f1419',
    'surface': '#1a1f2e',
    'primary': '#00d4ff',
    'success': '#00ff88',
    'error': '#ff6b6b',
    'text': '#ffffff',
    'text_muted': '#8b949e'
}

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🚀 SpaceX Launch Analytics", 
                style={'color': colors['text'], 'textAlign': 'center', 'margin': '0'}),
        html.P("Interactive Dashboard for Mission Analysis", 
               style={'color': colors['text_muted'], 'textAlign': 'center', 'margin': '10px 0 0 0'})
    ], style={
        'background': colors['surface'],
        'padding': '30px',
        'marginBottom': '20px',
        'borderRadius': '10px'
    }),
    
    # Controls Row
    html.Div([
        # Site Dropdown
        html.Div([
            html.Label("Launch Site:", style={'color': colors['text'], 'marginBottom': '10px', 'display': 'block'}),
            dcc.Dropdown(
                id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                ],
                value='ALL',
                style={'backgroundColor': colors['surface'], 'color': colors['text']}
            )
        ], style={'width': '48%'}),
        
        # Payload Slider
        html.Div([
            html.Label("Payload Range (kg):", style={'color': colors['text'], 'marginBottom': '10px', 'display': 'block'}),
            dcc.RangeSlider(
                id='payload-slider',
                min=0,
                max=10000,
                step=500,
                value=[min_payload, max_payload],
                marks={
                    0: '0',
                    2500: '2.5k',
                    5000: '5k',
                    7500: '7.5k',
                    10000: '10k'
                },
                tooltip={'placement': 'bottom', 'always_visible': True}
            )
        ], style={'width': '48%'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'marginBottom': '30px',
        'gap': '20px'
    }),
    
    # Charts Row
    html.Div([
        # Pie Chart
        html.Div([
            dcc.Graph(id='success-pie-chart')
        ], style={'width': '48%'}),
        
        # Scatter Plot
        html.Div([
            dcc.Graph(id='success-payload-scatter-chart')
        ], style={'width': '48%'})
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '20px',
        'marginBottom': '30px'
    }),
    
    # Statistics Cards
    html.Div([
        html.Div([
            html.H3(f"{len(spacex_df)}", style={'color': colors['primary'], 'margin': '0', 'fontSize': '2.5em'}),
            html.P("Total Launches", style={'color': colors['text_muted'], 'margin': '5px 0 0 0'})
        ], style={
            'background': colors['surface'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'width': '22%'
        }),
        
        html.Div([
            html.H3(f"{len(spacex_df[spacex_df['class'] == 1])}", 
                   style={'color': colors['success'], 'margin': '0', 'fontSize': '2.5em'}),
            html.P("Successful", style={'color': colors['text_muted'], 'margin': '5px 0 0 0'})
        ], style={
            'background': colors['surface'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'width': '22%'
        }),
        
        html.Div([
            html.H3(f"{len(spacex_df[spacex_df['class'] == 0])}", 
                   style={'color': colors['error'], 'margin': '0', 'fontSize': '2.5em'}),
            html.P("Failed", style={'color': colors['text_muted'], 'margin': '5px 0 0 0'})
        ], style={
            'background': colors['surface'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'width': '22%'
        }),
        
        html.Div([
            html.H3(f"{round((len(spacex_df[spacex_df['class'] == 1]) / len(spacex_df)) * 100, 1)}%", 
                   style={'color': colors['primary'], 'margin': '0', 'fontSize': '2.5em'}),
            html.P("Success Rate", style={'color': colors['text_muted'], 'margin': '5px 0 0 0'})
        ], style={
            'background': colors['surface'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'width': '22%'
        })
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'gap': '15px'
    })
    
], style={
    'backgroundColor': colors['bg'],
    'padding': '20px',
    'minHeight': '100vh',
    'fontFamily': 'Arial, sans-serif'
})

# Callbacks
@callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Show success by site
        df_grouped = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(df_grouped, 
                    values='class', 
                    names='Launch Site',
                    title='Total Successful Launches by Site',
                    color_discrete_sequence=px.colors.qualitative.Set3)
    else:
        # Show success/failure for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts['status'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
        
        fig = px.pie(success_counts, 
                    values='count', 
                    names='status',
                    title=f'Success Rate: {selected_site}',
                    color_discrete_map={'Success': colors['success'], 'Failure': colors['error']})
    
    # Style the chart
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=colors['text'],
        title_font_size=16
    )
    
    return fig

@callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter by payload range
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    
    # Filter by site if not ALL
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        title=f'Payload vs Success Rate - {selected_site if selected_site != "ALL" else "All Sites"}',
        hover_data=['Launch Site'] if selected_site == 'ALL' else None,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Style the chart
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=colors['text'],
        title_font_size=16,
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=['Failure', 'Success']
        )
    )
    
    fig.update_traces(marker_size=8)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)


    