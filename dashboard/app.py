"""
CASS-Lite v2 - Carbon-Aware Serverless Scheduler Dashboard
===========================================================
Futuristic Streamlit Dashboard with Real-time Carbon Intelligence

Author: Bharathi Senthilkumar
Date: November 2025
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import time
from utils import (
    fetch_recent_decisions,
    get_summary_stats,
    fetch_current_carbon_data,
    get_region_history
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
# FOOTER
# ============================================================================

def render_footer():
    st.markdown("""
    <div class="footer">
        <p>Built with <span class="footer-icon">❤️</span> by <strong>Bharathi Senthilkumar</strong></p>
        <p> Powered by Google Cloud /p>
        <p style="font-size: 0.8rem; color: #7f00ff; margin-top: 1rem;">
            Making the cloud greener, one decision at a time 
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Render hero section
    render_hero()
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### Dashboard Controls")
        
        auto_refresh = st.checkbox(" Auto-refresh", value=False)
        refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 10)
        
        st.markdown("---")
        st.markdown("###  Data Range")
        days_filter = st.selectbox("Show last", [1, 3, 7, 14, 30], index=2)
        
        st.markdown("---")
        st.markdown("###  Quick Actions")
        
        if st.button(" Trigger Scheduler"):
            st.info("Triggering scheduler function...")
            # Add logic to call Cloud Function
        
        if st.button(" Refresh Data"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("###  Project Info")
        st.markdown("""
        **Project:** CASS-Lite v2  
        **Version:** 2.0.0  
        **Status:**  Active  
        **Region:** asia-south1  
        """)
    
    # Fetch data
    with st.spinner(" Loading carbon intelligence data..."):
        stats = get_summary_stats(days=days_filter)
        recent_logs = fetch_recent_decisions(limit=50)
        
        # Create sample time-series data
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
    
    # Region frequency chart
    if not recent_logs.empty:
        render_region_frequency_chart(recent_logs)
    
    # Live logs table
    render_logs_table(recent_logs)
    
    # Footer
    render_footer()
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
