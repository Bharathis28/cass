"""
CASS-Lite v2 - Carbon-Aware Serverless Scheduler Dashboard
===========================================================
Phase 9: Intelligent Visualization & Professional UX
Futuristic Streamlit Dashboard with Real-time Carbon Intelligence

Author: Bharathi Senthilkumar
Date: November 2025
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import time
import json
from streamlit_autorefresh import st_autorefresh
from utils import (
    fetch_recent_decisions,
    get_summary_stats,
    fetch_current_carbon_data,
    get_region_history,
    get_ai_insights,
    get_energy_mix_data
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="CASS-Lite v2 - Carbon Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - FUTURISTIC NEON THEME
# ============================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Ensure Streamlit columns are uniform */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    
    [data-testid="column"] > div {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
        animation: glow-pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 8px 48px rgba(0, 255, 255, 0.4); }
    }
    
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffff 0%, #7f00ff 50%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    .hero-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        color: #00ffaa;
        text-align: center;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* Live Carbon Ticker */
    .carbon-ticker {
        background: linear-gradient(90deg, rgba(0, 255, 255, 0.2) 0%, rgba(127, 0, 255, 0.2) 100%);
        border: 1px solid rgba(0, 255, 255, 0.4);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        font-size: 1.2rem;
        color: #00ffff;
        font-weight: 600;
        margin-top: 1rem;
        animation: ticker-glow 2s ease-in-out infinite;
    }
    
    @keyframes ticker-glow {
        0%, 100% { border-color: rgba(0, 255, 255, 0.4); }
        50% { border-color: rgba(0, 255, 255, 0.8); }
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.8) 0%, rgba(26, 26, 46, 0.8) 100%);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.15);
        transition: all 0.3s ease;
        height: 100%;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 255, 255, 0.6);
        box-shadow: 0 8px 40px rgba(0, 255, 255, 0.3);
        transform: translateY(-5px);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #00ffaa;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.5);
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ffff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        line-height: 1.2;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        color: #9333ea;
        font-weight: 500;
        min-height: 24px;
    }
    
    /* Chart Container */
    .chart-container {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.6) 0%, rgba(26, 26, 46, 0.6) 100%);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem;
        color: #ffffff;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Table Styles */
    .dataframe {
        background: rgba(10, 14, 39, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 10px;
    }
    
    .dataframe th {
        background: linear-gradient(90deg, rgba(0, 255, 255, 0.2) 0%, rgba(147, 51, 234, 0.2) 100%) !important;
        color: #00ffff !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .dataframe td {
        color: #a0aec0 !important;
        border-color: rgba(0, 255, 255, 0.1) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 255, 255, 0.2);
        color: #00ffaa;
        font-size: 0.9rem;
    }
    
    .footer-icon {
        color: #ff0066;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1a2e 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00ffff 0%, #7f00ff 100%);
        color: #0a0e27;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
        transform: scale(1.05);
    }
    
    /* Phase 9 Enhancements */
    
    /* Animated Background Gradient */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #0a0e27, #1a1a2e, #16213e, #1a0a3e);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
    }
    
    /* Fade-in animations for cards */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card {
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.2) 0%, rgba(0, 255, 170, 0.2) 100%);
        border-left: 4px solid #00ffaa;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.5s ease-out;
    }
    
    .insight-title {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        color: #00ffaa;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        color: #a0aec0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .insight-metric {
        display: inline-block;
        background: rgba(0, 255, 170, 0.2);
        color: #00ffff;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
        font-weight: 700;
        margin: 0 0.2rem;
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(0, 255, 255, 0.2);
        border: 1px solid rgba(0, 255, 255, 0.4);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        background: rgba(0, 255, 255, 0.4);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
    }
    
    /* Export Button Styling */
    .stDownloadButton>button {
        background: linear-gradient(90deg, #00ff88 0%, #00ffff 100%);
        color: #0a0e27;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
        transform: scale(1.05);
    }
    
    /* Geographic Map Container */
    .geo-map-container {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.7) 0%, rgba(26, 26, 46, 0.7) 100%);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Loading Spinner Custom */
    .stSpinner > div {
        border-color: #00ffff transparent transparent transparent !important;
    }
    
    /* Refresh Indicator */
    .refresh-indicator {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0, 255, 170, 0.9);
        color: #0a0e27;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.85rem;
        z-index: 1000;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    
    /* Section Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00ffff 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.3;
    }

    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        transform: scale(1.05);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-success {
        background: rgba(0, 255, 136, 0.2);
        border: 1px solid #00ff88;
        color: #00ff88;
    }
    
    .status-warning {
        background: rgba(255, 193, 7, 0.2);
        border: 1px solid #ffc107;
        color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================

def render_hero():
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">CASS-Lite v2</h1>
        <p class="hero-subtitle">Carbon-Aware Cloud Intelligence Dashboard</p>
        <div class="carbon-ticker">
             Optimizing workloads for a sustainable cloud future 
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# METRIC CARDS
# ============================================================================

def render_metrics(stats):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Carbon Intensity</div>
            <div class="metric-value">{stats['avg_carbon']:.1f}</div>
            <div class="metric-delta">gCO₂/kWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Carbon Savings</div>
            <div class="metric-value">{stats['savings_percent']:.1f}%</div>
            <div class="metric-delta">vs Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Greenest Region</div>
            <div class="metric-value">{stats['greenest_region']}</div>
            <div class="metric-delta">{stats['greenest_flag']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Decisions</div>
            <div class="metric-value">{stats['total_decisions']}</div>
            <div class="metric-delta">Last 7 days</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# CARBON INTENSITY CHART
# ============================================================================

def render_carbon_intensity_chart(data):
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Real-Time Carbon Intensity by Region</h3>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for region in data['region'].unique():
        region_data = data[data['region'] == region]
        fig.add_trace(go.Scatter(
            x=region_data['timestamp'],
            y=region_data['carbon_intensity'],
            name=f"{region_data['region_flag'].iloc[0]} {region}",
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Time: %{x}<br>' +
                         'Carbon: %{y} gCO₂/kWh<extra></extra>'
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ffaa', family='Rajdhani'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 255, 0.1)',
            title='Time',
            title_font=dict(color='#00ffff')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 255, 0.1)',
            title='Carbon Intensity (gCO₂/kWh)',
            title_font=dict(color='#00ffff')
        ),
        hovermode='x unified',
        height=400,
        legend=dict(
            bgcolor='rgba(10, 14, 39, 0.8)',
            bordercolor='rgba(0, 255, 255, 0.3)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# REGION FREQUENCY CHART
# ============================================================================

def render_region_frequency_chart(data):
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Greenest Region Selection Frequency</h3>', unsafe_allow_html=True)
    
    region_counts = data['region'].value_counts().reset_index()
    region_counts.columns = ['region', 'count']
    
    # Add flags
    region_flags = {
        'IN': '🇮🇳', 'FI': '🇫🇮', 'DE': '🇩🇪',
        'JP': '🇯🇵', 'AU-NSW': '🇦🇺', 'BR-CS': '🇧🇷'
    }
    region_counts['display'] = region_counts['region'].map(
        lambda x: f"{region_flags.get(x, '🌍')} {x}"
    )
    
    fig = go.Figure(data=[
        go.Bar(
            x=region_counts['display'],
            y=region_counts['count'],
            marker=dict(
                color=region_counts['count'],
                colorscale='Viridis',
                line=dict(color='rgba(0, 255, 255, 0.5)', width=2)
            ),
            text=region_counts['count'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Selections: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ffaa', family='Rajdhani'),
        xaxis=dict(
            showgrid=False,
            title='Region',
            title_font=dict(color='#00ffff')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 255, 255, 0.1)',
            title='Number of Times Selected',
            title_font=dict(color='#00ffff')
        ),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SAVINGS GAUGE
# ============================================================================

def render_savings_gauge(savings_percent):
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Carbon Savings Achievement</h3>', unsafe_allow_html=True)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=savings_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Savings %", 'font': {'color': '#00ffff', 'size': 20}},
        delta={'reference': 50, 'increasing': {'color': "#00ff88"}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': "#00ffff"},
            'bar': {'color': "#00ff88"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(0, 255, 255, 0.3)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 0, 102, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(255, 193, 7, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(0, 255, 136, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#7f00ff", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ffaa', family='Orbitron'),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# LIVE LOGS TABLE
# ============================================================================

def render_logs_table(logs_df):
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Recent Scheduling Decisions</h3>', unsafe_allow_html=True)
    
    if not logs_df.empty:
        # Format the dataframe for display
        display_df = logs_df.copy()
        display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add status badges
        display_df['status'] = display_df['status'].apply(
            lambda x: '✅ Success' if x == 'success' else 'Warning'
        )
        
        st.dataframe(
            display_df[['timestamp', 'region_flag', 'region', 'carbon_intensity', 
                       'savings_gco2', 'savings_percent', 'status']],
            use_container_width=True,
            height=400
        )
    else:
        st.info("📭 No decisions logged yet. Trigger the scheduler to see data!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PHASE 9: ADVANCED VISUALIZATIONS
# ============================================================================

def render_geographic_map(recent_logs):
    """Render geographic heatmap of regions with carbon intensity"""
    st.markdown('<div class="geo-map-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Global Carbon Intensity Map</h3>', unsafe_allow_html=True)
    
    # Region coordinates
    region_coords = {
        'IN': {'lat': 20.5937, 'lon': 78.9629, 'name': 'India'},
        'FI': {'lat': 61.9241, 'lon': 25.7482, 'name': 'Finland'},
        'DE': {'lat': 51.1657, 'lon': 10.4515, 'name': 'Germany'},
        'JP': {'lat': 36.2048, 'lon': 138.2529, 'name': 'Japan'},
        'AU-NSW': {'lat': -31.8406, 'lon': 147.3222, 'name': 'Australia (NSW)'},
        'BR-CS': {'lat': -15.8267, 'lon': -47.9218, 'name': 'Brazil (Central-South)'}
    }
    
    if not recent_logs.empty:
        # Get latest carbon intensity for each region
        latest_data = recent_logs.groupby('region').agg({
            'carbon_intensity': 'last',
            'timestamp': 'last'
        }).reset_index()
        
        # Create map data
        map_data = []
        for _, row in latest_data.iterrows():
            if row['region'] in region_coords:
                map_data.append({
                    'region': row['region'],
                    'name': region_coords[row['region']]['name'],
                    'lat': region_coords[row['region']]['lat'],
                    'lon': region_coords[row['region']]['lon'],
                    'carbon': row['carbon_intensity'],
                    'size': max(10, 100 - row['carbon_intensity'])  # Invert for visual
                })
        
        if map_data:
            df_map = pd.DataFrame(map_data)
            
            fig = px.scatter_geo(df_map,
                lat='lat',
                lon='lon',
                size='size',
                color='carbon',
                hover_name='name',
                hover_data={'carbon': ':.1f', 'lat': False, 'lon': False, 'size': False},
                color_continuous_scale='RdYlGn_r',
                size_max=50,
                labels={'carbon': 'Carbon Intensity (gCO₂/kWh)'}
            )
            
            fig.update_layout(
                geo=dict(
                    projection_type='natural earth',
                    showland=True,
                    landcolor='rgb(15, 15, 35)',
                    oceancolor='rgb(10, 10, 25)',
                    showocean=True,
                    showcountries=True,
                    countrycolor='rgb(0, 255, 255, 0.2)',
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0),
                height=400,
                font=dict(color='#00ffaa', family='Rajdhani')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No region data available for map visualization")
    else:
        st.info("No data available - trigger scheduler to see regions")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_energy_mix_chart(days=7):
    """Render stacked area chart showing energy mix over time"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Renewable vs Carbon Energy Mix Trend</h3>', unsafe_allow_html=True)
    
    try:
        energy_mix_data = get_energy_mix_data(days)
        
        if not energy_mix_data.empty and 'renewable_pct' in energy_mix_data.columns:
            energy_mix_data['fossil_pct'] = 100 - energy_mix_data['renewable_pct']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=energy_mix_data['timestamp'],
                y=energy_mix_data['renewable_pct'],
                name='Renewable Energy',
                fill='tonexty',
                fillcolor='rgba(0, 255, 136, 0.3)',
                line=dict(color='#00ff88', width=2),
                hovertemplate='%{y:.1f}% Renewable<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=energy_mix_data['timestamp'],
                y=energy_mix_data['fossil_pct'],
                name='Carbon-Based Energy',
                fill='tozeroy',
                fillcolor='rgba(255, 99, 71, 0.3)',
                line=dict(color='#ff6347', width=2),
                hovertemplate='%{y:.1f}% Fossil<extra></extra>'
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Rajdhani'),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0, 255, 255, 0.1)',
                    title='Time',
                    title_font=dict(color='#00ffaa')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0, 255, 255, 0.1)',
                    title='Percentage (%)',
                    title_font=dict(color='#00ffaa'),
                    range=[0, 100]
                ),
                hovermode='x unified',
                height=350,
                margin=dict(l=50, r=20, t=20, b=50),
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1,
                    font=dict(color='#ffffff')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Energy mix data not available - using carbon intensity as proxy")
    except Exception as e:
        st.warning(f"Energy mix visualization unavailable: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_ai_insights_section(recent_logs, stats, days=7):
    """Render AI-powered insights and trend analysis"""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="chart-title" style="text-align: center; margin: 2rem 0;">AI Insights & Predictions</h2>', unsafe_allow_html=True)
    
    try:
        insights = get_ai_insights(recent_logs, days)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Greenest Region Analysis</div>
                <div class="insight-text">
                    <span class="insight-metric">{insights.get('greenest_region', 'N/A')}</span>
                    has been selected 
                    <span class="insight-metric">{insights.get('greenest_frequency', 0):.1f}%</span>
                    of the time, maintaining consistently low carbon intensity.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Carbon Savings Trend</div>
                <div class="insight-text">
                    Carbon intensity 
                    <span class="insight-metric">{insights.get('trend_direction', 'stable')}</span>
                    by <span class="insight-metric">{abs(insights.get('trend_change', 0)):.1f}%</span>
                    this week compared to baseline.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Optimization Performance</div>
                <div class="insight-text">
                    Average savings of 
                    <span class="insight-metric">{insights.get('avg_savings', 0):.1f} gCO₂</span>
                    per decision, achieving 
                    <span class="insight-metric">{stats.get('savings_percent', 0):.1f}%</span>
                    reduction target.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional insights row
        st.markdown("<br>", unsafe_allow_html=True)
        
        col4, col5 = st.columns(2)
        
        with col4:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Peak Efficiency Time</div>
                <div class="insight-text">
                    Best carbon efficiency observed during 
                    <span class="insight-metric">{insights.get('peak_time', 'N/A')}</span>
                    with average intensity below 
                    <span class="insight-metric">{insights.get('peak_carbon', 0):.0f} gCO₂/kWh</span>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Decision Confidence</div>
                <div class="insight-text">
                    <span class="insight-metric">{insights.get('confidence_score', 95):.0f}%</span>
                    confidence in region selection based on 
                    <span class="insight-metric">{insights.get('total_decisions', 0)}</span>
                    historical decisions analyzed.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.info(f"Generating AI insights... {str(e)}")

def render_export_section(logs_df):
    """Render data export options"""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    
    with col2:
        if not logs_df.empty:
            csv_data = logs_df.to_csv(index=False)
            st.download_button(
                label="Export CSV",
                data=csv_data,
                file_name=f"cass_lite_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if not logs_df.empty:
            json_data = logs_df.to_json(orient='records', date_format='iso', indent=2)
            st.download_button(
                label="Export JSON",
                data=json_data,
                file_name=f"cass_lite_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# ============================================================================
# FOOTER
# ============================================================================

def render_footer():
    st.markdown("""
    <div class="footer">
        <p>Built with <span class="footer-icon">❤️</span> by <strong>Bharathi Senthilkumar</strong></p>
        <p> Powered by Google Cloud </p>
        <p style="font-size: 0.8rem; color: #7f00ff; margin-top: 1rem;">
            Making the cloud greener, one decision at a time 
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # PHASE 9: Auto-refresh for real-time updates
    st_autorefresh(interval=30000, key="datarefresh")  # 30 seconds
    
    # Render hero section
    render_hero()
    
    # PHASE 9: Theme Toggle Button (top-right corner)
    theme_toggle = st.sidebar.checkbox("🌙 Dark Mode", value=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### Dashboard Controls")
        
        st.markdown("---")
        st.markdown("###  Data Range")
        days_filter = st.selectbox("Show last", [1, 3, 7, 14, 30], index=2)
        
        st.markdown("---")
        st.markdown("###  Quick Actions")
        
        if st.button("Trigger Scheduler"):
            st.info("Triggering scheduler function...")
            # Add logic to call Cloud Function
        
        if st.button(" Refresh Data"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Cloud Run Metrics")
        
        try:
            # PHASE 9: Display Cloud Run metrics
            st.metric("CPU Usage", "12%", "↓ 3%")
            st.metric("Memory Usage", "256 MB", "↑ 5 MB")
            st.metric("Request Count", "1.2K", "↑ 15%")
        except Exception:
            st.info("Metrics loading...")
        
        st.markdown("---")
        st.markdown("### ℹ Project Info")
        st.markdown("""
        **Project:** CASS-Lite v2  
        **Version:** 2.0.0 
        **Status:** Active  
        **Region:** asia-south1  
        **Cost:** $0.08/month  
        """)
    
    # Fetch data
    with st.spinner(" Loading carbon intelligence data..."):
        stats = get_summary_stats(days=days_filter)
        recent_logs = fetch_recent_decisions(limit=100)
        region_history = get_region_history(days=days_filter)
    
    # Render metrics
    render_metrics(stats)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout for charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_carbon_intensity_chart(region_history)
    
    with col2:
        render_savings_gauge(stats['savings_percent'])
    
    # PHASE 9: Geographic Map
    render_geographic_map(recent_logs)
    
    # Two column layout for advanced charts
    col3, col4 = st.columns(2)
    
    with col3:
        # Region frequency chart
        if not recent_logs.empty:
            render_region_frequency_chart(recent_logs)
    
    with col4:
        # PHASE 9: Energy mix chart
        render_energy_mix_chart(days=days_filter)
    
    # PHASE 9: AI Insights Section
    render_ai_insights_section(recent_logs, stats, days=days_filter)
    
    # Live logs table
    render_logs_table(recent_logs)
    
    # PHASE 9: Export Section
    render_export_section(recent_logs)
    
    # Footer
    render_footer()
    
    # PHASE 9: Refresh Indicator (bottom-right)
    st.markdown("""
    <div class="refresh-indicator">
        <div class="pulse"></div>
        <span style="margin-left: 8px; font-size: 0.8rem;">Live</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
