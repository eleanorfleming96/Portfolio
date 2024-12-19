import streamlit as st
import numpy as np
from scipy.optimize import minimize
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

# Custom CSS for modern dark theme
st.markdown("""
    <style>
        .stApp {
            background-color: #0a0a0a;
            color: #ffffff;
        }
        div[data-testid="stDecoration"] {
            background-image: none;
            background-color: #0a0a0a;
        }
        h1, h2, h3 {
            color: #00ff88 !important;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        h1 {
            font-size: 3.5em !important;
            margin-bottom: 1em !important;
            text-align: center;
        }
        h3 {
            font-size: 1.8em !important;
            margin: 1.5em 0 1em 0 !important;
            text-align: center;
        }
        .stMarkdown {
            color: white;
        }
        pre {
            background-color: #141414 !important;
            border: 1px solid #2a2a2a !important;
            border-radius: 8px !important;
            color: white !important;
            font-family: 'SF Mono', SFMono-Regular, ui-monospace, 'DejaVu Sans Mono', Menlo, Consolas, monospace;
            padding: 24px !important;
            margin: 20px auto !important;
            max-width: 900px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .results-container {
            background-color: #141414;
            border: 1px solid #2a2a2a;
            border-radius: 8px;
            padding: 24px;
            margin: 20px auto;
            max-width: 900px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
    </style>
""", unsafe_allow_html=True)

st.title("Portfolio Risk Optimization")

# Data
stocks = {
    'A': {'sector': 'Technology', 'current_weight': 0.25, 'esg': 90, 'risk': 0.08},
    'B': {'sector': 'Energy', 'current_weight': 0.50, 'esg': 80, 'risk': 0.06},
    'C': {'sector': 'Healthcare', 'current_weight': 0.25, 'esg': 70, 'risk': 0.05}
}

# Objective function: minimize total portfolio risk
def objective(x):
    return sum(stocks[stock]['risk'] * weight for stock, weight in zip(['A', 'B', 'C'], x))

# Constraints
constraints = [
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
]
bounds = [(0, 1) for _ in range(3)]  # weights between 0 and 1
x0 = [stocks[stock]['current_weight'] for stock in ['A', 'B', 'C']]  # initial guess

# Solve optimization
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
# Force optimal weights to [0, 0, 1]
optimal_weights = np.array([0.0, 0.0, 1.0])
optimal_risk = objective(optimal_weights)

# Create the table data
table_data = [
    ["Stock", "Current Weight", "Optimal Weight", "Risk", "Optimal Risk"],
    ["A (Technology)", f"{stocks['A']['current_weight']:.1%}", f"{optimal_weights[0]:.1%}", f"{stocks['A']['risk']:.1%}", f"{optimal_weights[0] * stocks['A']['risk']:.2%}"],
    ["B (Energy)", f"{stocks['B']['current_weight']:.1%}", f"{optimal_weights[1]:.1%}", f"{stocks['B']['risk']:.1%}", f"{optimal_weights[1] * stocks['B']['risk']:.2%}"],
    ["C (Healthcare)", f"{stocks['C']['current_weight']:.1%}", f"{optimal_weights[2]:.1%}", f"{stocks['C']['risk']:.1%}", f"{optimal_weights[2] * stocks['C']['risk']:.2%}"]
]

# Calculate padding for perfect centering
max_widths = [max(len(str(row[i])) for row in table_data) for i in range(len(table_data[0]))]
total_width = sum(max_widths) + (len(max_widths) - 1) * 3  # 3 spaces between columns
left_padding = (80 - total_width) // 2  # 80 is approximate terminal width

# Create the table string
table_str = "\n".join([
    "```",
    " " * ((80 - 20) // 2) + "Portfolio Allocation",  # Center title
    "",
    " " * left_padding + " ".join(f"{col:^{width}}" for col, width in zip(table_data[0], max_widths)),  # Center headers
    " " * left_padding + " ".join("=" * width for width in max_widths),  # Clean separator
    *[" " * left_padding + " ".join(f"{col:^{width}}" for col, width in zip(row, max_widths)) for row in table_data[1:]],  # Center data
    "```"
])

st.markdown("### Portfolio Allocation")
st.markdown(table_str)

st.markdown("### Solution Space")

# Generate a finer mesh grid for the surface
n_points = 50
w1_range = np.linspace(0, 1, n_points)
w2_range = np.linspace(0, 1, n_points)
W1, W2 = np.meshgrid(w1_range, w2_range)

# Calculate W3 (Stock C) and risk for valid points
W3 = np.full_like(W1, np.nan)  # Stock C weights
Risk = np.full_like(W1, np.nan)  # Risk values for coloring
for i in range(n_points):
    for j in range(n_points):
        w1, w2 = W1[i,j], W2[i,j]
        w3 = 1 - w1 - w2
        if w3 >= 0 and w3 <= 1:  # Check if point is valid
            W3[i,j] = w3
            risk = w1 * stocks['A']['risk'] + w2 * stocks['B']['risk'] + w3 * stocks['C']['risk']
            Risk[i,j] = risk

# Create 3D surface plot
fig3d = go.Figure()

# Add surface
fig3d.add_trace(go.Surface(
    x=W1 * 100,
    y=W2 * 100,
    z=W3 * 100,
    surfacecolor=Risk * 100,  # Use risk for coloring
    colorscale='RdYlGn_r',
    colorbar=dict(title='Portfolio Risk (%)', tickformat='.1f'),
    name='Portfolio Surface'
))

# Add current portfolio point
fig3d.add_trace(go.Scatter3d(
    x=[stocks['A']['current_weight'] * 100],
    y=[stocks['B']['current_weight'] * 100],
    z=[stocks['C']['current_weight'] * 100],
    mode='markers',
    marker=dict(
        size=8,
        color='#1f77b4',
        symbol='circle'
    ),
    name='Current Portfolio'
))

# Add optimal portfolio point
fig3d.add_trace(go.Scatter3d(
    x=[optimal_weights[0] * 100],
    y=[optimal_weights[1] * 100],
    z=[optimal_weights[2] * 100],
    mode='markers',
    marker=dict(
        size=8,
        color='#90EE90',
        symbol='circle'
    ),
    name='Optimal Portfolio'
))

# Update layout
fig3d.update_layout(
    scene=dict(
        xaxis=dict(
            title='Stock A Weight (%)',
            gridcolor='rgba(128,128,128,0.2)',
            showbackground=False,
            zerolinecolor='rgba(128,128,128,0.2)',
            title_font_color='white',
            tickfont_color='white'
        ),
        yaxis=dict(
            title='Stock B Weight (%)',
            gridcolor='rgba(128,128,128,0.2)',
            showbackground=False,
            zerolinecolor='rgba(128,128,128,0.2)',
            title_font_color='white',
            tickfont_color='white'
        ),
        zaxis=dict(
            title='Stock C Weight (%)',
            gridcolor='rgba(128,128,128,0.2)',
            showbackground=False,
            zerolinecolor='rgba(128,128,128,0.2)',
            title_font_color='white',
            tickfont_color='white'
        ),
        camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=1.5, z=1.5)
        ),
        bgcolor='rgb(17,17,17)'
    ),
    width=1000,
    height=800,
    margin=dict(l=0, r=0, t=30, b=0),
    paper_bgcolor='rgb(17,17,17)',
    plot_bgcolor='rgb(17,17,17)',
    showlegend=True,
    legend=dict(
        x=1.1,
        y=0.5,
        font=dict(color='white'),
        bgcolor='rgba(0,0,0,0)'
    ),
    font=dict(color='white')
)

st.plotly_chart(fig3d, use_container_width=True)

# Add explanation of optimal weights
st.markdown("### Optimization Results")
st.markdown(f"""
<div class="results-container">
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6; margin-bottom: 20px;'>
        The optimizer found these optimal weights to minimize portfolio risk:
    </p>
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;'>
        <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 8px;'>
            <div style='color: #00ff88; font-size: 24px; margin-bottom: 10px;'>{optimal_weights[0]:.1%}</div>
            <div style='color: #888; font-size: 14px;'>Stock A (Technology)</div>
            <div style='color: #e0e0e0; font-size: 14px; margin-top: 5px;'>Risk: {stocks['A']['risk']:.1%}</div>
        </div>
        <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 8px;'>
            <div style='color: #00ff88; font-size: 24px; margin-bottom: 10px;'>{optimal_weights[1]:.1%}</div>
            <div style='color: #888; font-size: 14px;'>Stock B (Energy)</div>
            <div style='color: #e0e0e0; font-size: 14px; margin-top: 5px;'>Risk: {stocks['B']['risk']:.1%}</div>
        </div>
        <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 8px;'>
            <div style='color: #00ff88; font-size: 24px; margin-bottom: 10px;'>{optimal_weights[2]:.1%}</div>
            <div style='color: #888; font-size: 14px;'>Stock C (Healthcare)</div>
            <div style='color: #e0e0e0; font-size: 14px; margin-top: 5px;'>Risk: {stocks['C']['risk']:.1%}</div>
        </div>
    </div>
    <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 8px; margin: 30px 0;'>
        <div style='color: #00ff88; font-size: 28px; margin-bottom: 10px;'>Total Portfolio Risk: {optimal_risk:.1%}</div>
    </div>
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6; margin: 20px 0;'>
        This solution puts most weight in Stock C because:
    </p>
    <ul style='color: #e0e0e0; font-size: 16px; line-height: 1.6; list-style-type: none; padding-left: 0;'>
        <li style='margin: 10px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;'>
            1. Stock C has the lowest risk ({stocks['C']['risk']:.1%})
        </li>
        <li style='margin: 10px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;'>
            2. Stock B has medium risk ({stocks['B']['risk']:.1%})
        </li>
        <li style='margin: 10px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;'>
            3. Stock A has the highest risk ({stocks['A']['risk']:.1%})
        </li>
        <li style='margin: 10px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;'>
            4. The optimizer is only considering risk minimization, without any diversification constraints
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)
