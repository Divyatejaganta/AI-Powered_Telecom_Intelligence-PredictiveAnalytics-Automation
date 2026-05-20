import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Page configuration
st.set_page_config(
    page_title="Telecom Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #d32f2f;
        padding: 15px;
        border-radius: 4px;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #f57c00;
        padding: 15px;
        border-radius: 4px;
    }
    .alert-success {
        background-color: #e8f5e9;
        border-left: 4px solid #388e3c;
        padding: 15px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

@st.cache_data
def generate_sample_data(n_records=1000):
    """Generate sample telecom data"""
    dates = [datetime.now() - timedelta(days=x) for x in range(n_records)]
    data = {
        'date': sorted(dates),
        'customers_active': np.random.randint(50000, 100000, n_records),
        'revenue': np.random.uniform(500000, 1500000, n_records),
        'network_uptime': np.random.uniform(98, 99.99, n_records),
        'avg_latency_ms': np.random.uniform(10, 50, n_records),
        'bandwidth_used_gbps': np.random.uniform(500, 1000, n_records),
        'support_tickets': np.random.randint(100, 500, n_records),
        'fraud_cases': np.random.randint(5, 50, n_records),
        'at_risk_customers': np.random.randint(100, 500, n_records)
    }
    return pd.DataFrame(data)

@st.cache_data
def generate_customer_data(n_customers=500):
    """Generate sample customer data"""
    return pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'tenure_months': np.random.randint(1, 60, n_customers),
        'monthly_charges': np.random.uniform(20, 150, n_customers),
        'total_charges': np.random.uniform(100, 5000, n_customers),
        'usage_gb': np.random.uniform(0.5, 100, n_customers),
        'support_calls': np.random.randint(0, 20, n_customers),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_customers),
        'churn_risk': np.random.uniform(0, 1, n_customers)
    })

@st.cache_data
def generate_network_data(n_records=500):
    """Generate network performance data"""
    return pd.DataFrame({
        'timestamp': [datetime.now() - timedelta(minutes=x) for x in range(n_records)],
        'cell_id': np.random.randint(1000, 2000, n_records),
        'bandwidth_usage': np.random.uniform(30, 100, n_records),
        'latency': np.random.uniform(5, 100, n_records),
        'packet_loss': np.random.uniform(0, 5, n_records),
        'connected_users': np.random.randint(100, 1000, n_records)
    })

@st.cache_data
def generate_fraud_data(n_records=200):
    """Generate fraud detection data"""
    fraud_types = ['SIM Swap', 'Call Spoofing', 'Billing Fraud', 'Data Theft', 'Unauthorized Access']
    return pd.DataFrame({
        'incident_id': range(1, n_records + 1),
        'fraud_type': np.random.choice(fraud_types, n_records),
        'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], n_records),
        'customer_impact': np.random.randint(1, 1000, n_records),
        'financial_loss': np.random.uniform(100, 50000, n_records),
        'detected_at': [datetime.now() - timedelta(hours=x) for x in range(n_records)],
        'status': np.random.choice(['Detected', 'Resolved', 'In Progress'], n_records)
    })

def display_dashboard():
    """Display main dashboard"""
    st.title("📊 Telecom Intelligence Dashboard")
    
    df = generate_sample_data()
    latest = df.iloc[-1]
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Active Customers",
            f"{int(latest['customers_active']):,}",
            "+2.5%",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Network Uptime",
            f"{latest['network_uptime']:.2f}%",
            "+0.1%",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "Monthly Revenue",
            f"${latest['revenue']/1e6:.2f}M",
            "+1.8%",
            delta_color="off"
        )
    
    with col4:
        churn_rate = (latest['at_risk_customers'] / latest['customers_active']) * 100
        st.metric(
            "Churn Rate",
            f"{churn_rate:.2f}%",
            "-0.5%",
            delta_color="inverse"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['revenue']/1e6,
            mode='lines+markers',
            name='Revenue (M)',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))
        fig.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Date",
            yaxis_title="Revenue ($M)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Network Performance
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['network_uptime'],
            mode='lines',
            name='Uptime %',
            line=dict(color='#2ca02c', width=2)
        ))
        fig.add_hline(y=99.5, line_dash="dash", line_color="red", annotation_text="SLA Threshold")
        fig.update_layout(
            title="Network Uptime Performance",
            xaxis_title="Date",
            yaxis_title="Uptime (%)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Service Usage Distribution
        usage_data = pd.DataFrame({
            'Service': ['Data', 'Voice', 'SMS', 'Video Streaming', 'IoT'],
            'Usage %': [45, 25, 10, 15, 5]
        })
        fig = px.pie(usage_data, values='Usage %', names='Service', title="Service Usage Distribution")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Latency Distribution
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['avg_latency_ms'],
            nbinsx=30,
            name='Latency',
            marker_color='#ff7f0e'
        ))
        fig.update_layout(
            title="Latency Distribution (ms)",
            xaxis_title="Latency (ms)",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def display_customer_support():
    """Display customer support assistant"""
    st.title("🤖 AI Customer Support Assistant")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Chat Assistant")
        
        # Chat interface
        customer_query = st.text_input(
            "Enter your query:",
            placeholder="e.g., 'How do I upgrade my plan?', 'I'm having connection issues'"
        )
        
        if customer_query:
            st.info("🤖 Assistant: Thank you for contacting us! I'm analyzing your query...")
            
            # Simulate AI response
            if 'billing' in customer_query.lower() or 'charge' in customer_query.lower():
                st.success("""Based on your account:
                - Current Plan: Premium 50GB
                - Monthly Charges: $79.99
                - Next Billing Date: June 1, 2026
                - Would you like to upgrade or modify your plan?""")
            elif 'connection' in customer_query.lower() or 'issue' in customer_query.lower():
                st.warning("""Let's troubleshoot:
                1. Try restarting your modem (unplug for 30 seconds)
                2. Check if you're within service area
                3. Restart your device
                - If issue persists, I can escalate to a technician""")
            else:
                st.info("I can help you with billing, technical support, plan upgrades, or general inquiries. What specifically can I assist with?")
    
    with col2:
        st.subheader("Quick Stats")
        st.metric("Avg Response Time", "2.3s")
        st.metric("Resolution Rate", "87%")
        st.metric("Escalations", "13%")
    
    st.divider()
    
    # Support tickets
    st.subheader("Recent Support Tickets")
    tickets = pd.DataFrame({
        'Ticket ID': ['T001', 'T002', 'T003', 'T004', 'T005'],
        'Category': ['Billing', 'Technical', 'Billing', 'Service', 'Technical'],
        'Status': ['Resolved', 'In Progress', 'Resolved', 'Pending', 'In Progress'],
        'Created': ['Today', 'Today', 'Yesterday', 'Yesterday', '2 days ago'],
        'Priority': ['High', 'Medium', 'Low', 'High', 'Medium']
    })
    st.dataframe(tickets, use_container_width=True)

def display_network_maintenance():
    """Display predictive network maintenance"""
    st.title("🔧 Predictive Network Maintenance")
    
    # Network Health Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Network Health", "94%", "-2%", delta_color="inverse")
    with col2:
        st.metric("Avg Latency", "23ms", "+1ms", delta_color="inverse")
    with col3:
        st.metric("Packet Loss", "0.3%", "-0.1%", delta_color="off")
    with col4:
        st.metric("Active Alerts", "3", "+1", delta_color="inverse")
    
    st.divider()
    
    df_network = generate_network_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bandwidth utilization
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_network['timestamp'],
            y=df_network['bandwidth_usage'],
            mode='lines',
            name='Usage %',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="Warning Threshold")
        fig.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Critical")
        fig.update_layout(
            title="Bandwidth Utilization",
            xaxis_title="Time",
            yaxis_title="Usage (%)",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Latency monitoring
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df_network['latency'],
            name='Latency (ms)',
            marker_color='#ff7f0e'
        ))
        fig.update_layout(
            title="Latency Distribution by Cell",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Anomaly Detection Alerts
    st.subheader("🚨 Anomaly Detection Alerts")
    
    alerts = pd.DataFrame({
        'Cell ID': [1205, 1089, 1456],
        'Anomaly Type': ['High Latency', 'Bandwidth Spike', 'Packet Loss Increase'],
        'Severity': ['Medium', 'High', 'Critical'],
        'Confidence': ['92%', '95%', '98%'],
        'Action': ['Monitor', 'Investigate', 'Escalate']
    })
    
    for idx, row in alerts.iterrows():
        if row['Severity'] == 'Critical':
            st.markdown(f"<div class='alert-critical'><b>{row['Anomaly Type']}</b> - Cell {row['Cell ID']} ({row['Severity']}) - Confidence: {row['Confidence']}</div>", unsafe_allow_html=True)
        elif row['Severity'] == 'High':
            st.markdown(f"<div class='alert-warning'><b>{row['Anomaly Type']}</b> - Cell {row['Cell ID']} ({row['Severity']}) - Confidence: {row['Confidence']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='alert-success'><b>{row['Anomaly Type']}</b> - Cell {row['Cell ID']} ({row['Severity']}) - Confidence: {row['Confidence']}</div>", unsafe_allow_html=True)

def display_fraud_detection():
    """Display fraud detection system"""
    st.title("🛡️ Fraud Detection & Security")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Threats Detected", "47", "+5", delta_color="inverse")
    with col2:
        st.metric("Prevention Rate", "99.2%", "+0.3%")
    with col3:
        st.metric("Financial Loss Prevented", "$125K", "+$12K")
    with col4:
        st.metric("Active Cases", "12", "-2")
    
    st.divider()
    
    df_fraud = generate_fraud_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fraud type distribution
        fraud_counts = df_fraud['fraud_type'].value_counts()
        fig = px.bar(
            x=fraud_counts.values,
            y=fraud_counts.index,
            orientation='h',
            title="Fraud Cases by Type",
            labels={'x': 'Count', 'y': 'Fraud Type'},
            color=fraud_counts.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Severity distribution
        severity_counts = df_fraud['severity'].value_counts()
        fig = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Incident Severity Distribution",
            color_discrete_sequence=['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Recent fraud incidents
    st.subheader("Recent Fraud Incidents")
    
    recent_fraud = df_fraud.head(10).copy()
    recent_fraud['detected_at'] = recent_fraud['detected_at'].dt.strftime('%Y-%m-%d %H:%M')
    recent_fraud['financial_loss'] = '$' + (recent_fraud['financial_loss'].astype(int).astype(str))
    
    st.dataframe(
        recent_fraud[['incident_id', 'fraud_type', 'severity', 'financial_loss', 'customer_impact', 'status']],
        use_container_width=True
    )

def display_churn_prediction():
    """Display churn prediction module"""
    st.title("📊 Customer Churn Prediction")
    
    df_customers = generate_customer_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        at_risk_count = len(df_customers[df_customers['churn_risk'] > 0.7])
        st.metric("At-Risk Customers", at_risk_count, "-5")
    
    with col2:
        high_risk = len(df_customers[df_customers['churn_risk'] > 0.8])
        st.metric("High Risk", high_risk, "+2")
    
    with col3:
        avg_risk = df_customers['churn_risk'].mean() * 100
        st.metric("Avg Risk Score", f"{avg_risk:.1f}%", "-1.2%")
    
    with col4:
        retention_value = at_risk_count * 79.99 * 12
        st.metric("Potential Revenue at Risk", f"${retention_value/1e6:.2f}M", "-$0.3M")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df_customers['churn_risk'],
            nbinsx=20,
            name='Risk Score',
            marker_color='#ff7f0e'
        ))
        fig.add_vline(x=0.7, line_dash="dash", line_color="orange", annotation_text="At-Risk Threshold")
        fig.add_vline(x=0.8, line_dash="dash", line_color="red", annotation_text="High Risk")
        fig.update_layout(
            title="Customer Churn Risk Distribution",
            xaxis_title="Risk Score",
            yaxis_title="Count",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tenure vs Risk
        fig = px.scatter(
            df_customers,
            x='tenure_months',
            y='churn_risk',
            size='monthly_charges',
            color='churn_risk',
            hover_data=['monthly_charges'],
            title="Customer Tenure vs Churn Risk",
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # At-risk customers
    st.subheader("Customers at High Risk of Churn")
    
    high_risk_customers = df_customers[df_customers['churn_risk'] > 0.7].head(10).copy()
    high_risk_customers['churn_risk'] = (high_risk_customers['churn_risk'] * 100).round(1).astype(str) + '%'
    high_risk_customers['monthly_charges'] = '$' + high_risk_customers['monthly_charges'].round(2).astype(str)
    
    st.dataframe(
        high_risk_customers[['customer_id', 'tenure_months', 'monthly_charges', 'churn_risk', 'support_calls']],
        use_container_width=True
    )
    
    st.info("💡 **Recommendation:** Offer personalized retention packages to high-risk customers to prevent churn.")

def display_workforce_optimization():
    """Display workforce optimization"""
    st.title("👥 Workforce Optimization & Scheduling")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Field Engineers", "250", "+5")
    with col2:
        st.metric("Service Requests", "1,245", "+120")
    with col3:
        st.metric("Avg Resolution Time", "2.3h", "-0.5h")
    with col4:
        st.metric("Efficiency Score", "87%", "+3%")
    
    st.divider()
    
    # Demand forecast
    dates = pd.date_range(start='2026-05-20', periods=30)
    forecast_data = pd.DataFrame({
        'date': dates,
        'forecasted_demand': np.random.randint(100, 300, 30) + np.arange(30) * 2,
        'available_engineers': np.random.randint(200, 250, 30)
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Demand forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_data['date'],
            y=forecast_data['forecasted_demand'],
            mode='lines+markers',
            name='Forecasted Demand',
            line=dict(color='#1f77b4', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=forecast_data['date'],
            y=forecast_data['available_engineers'],
            mode='lines+markers',
            name='Available Engineers',
            line=dict(color='#2ca02c', width=2)
        ))
        fig.update_layout(
            title="30-Day Demand Forecast",
            xaxis_title="Date",
            yaxis_title="Count",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Shift distribution
        shift_data = pd.DataFrame({
            'Shift': ['Morning\n(6AM-2PM)', 'Afternoon\n(2PM-10PM)', 'Night\n(10PM-6AM)'],
            'Assigned': [85, 110, 55],
            'Utilization': [92, 88, 78]
        })
        fig = go.Figure(data=[
            go.Bar(name='Assigned Engineers', x=shift_data['Shift'], y=shift_data['Assigned'], marker_color='#1f77b4'),
            go.Bar(name='Utilization %', x=shift_data['Shift'], y=shift_data['Utilization'], marker_color='#ff7f0e')
        ])
        fig.update_layout(
            title="Shift Allocation",
            height=400,
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Scheduling recommendations
    st.subheader("📋 Scheduling Recommendations")
    
    recommendations = pd.DataFrame({
        'Date': ['2026-05-22', '2026-05-24', '2026-05-27'],
        'Predicted Demand': ['280 requests', '310 requests', '295 requests'],
        'Current Staff': ['220 engineers', '220 engineers', '220 engineers'],
        'Action': ['Hire 60+ temporary staff', 'Hire 90+ temporary staff', 'Hire 75+ temporary staff'],
        'Priority': ['High', 'Critical', 'High']
    })
    
    st.dataframe(recommendations, use_container_width=True)

def main():
    """Main application"""
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100?text=Telecom+Logo", use_column_width=True)
        st.title("Navigation")
        
        page = st.radio(
            "Select Module:",
            [
                "📊 Dashboard",
                "🤖 Customer Support",
                "🔧 Network Maintenance",
                "🛡️ Fraud Detection",
                "📊 Churn Prediction",
                "👥 Workforce Optimization"
            ],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        st.markdown("### System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Uptime", "99.92%")
        with col2:
            st.metric("API Health", "Healthy")
        
        st.markdown("### Quick Links")
        st.markdown("- [Documentation](https://docs.example.com)")
        st.markdown("- [Support](https://support.example.com)")
        st.markdown("- [Settings](#)")
    
    # Route to appropriate page
    if page == "📊 Dashboard":
        display_dashboard()
    elif page == "🤖 Customer Support":
        display_customer_support()
    elif page == "🔧 Network Maintenance":
        display_network_maintenance()
    elif page == "🛡️ Fraud Detection":
        display_fraud_detection()
    elif page == "📊 Churn Prediction":
        display_churn_prediction()
    elif page == "👥 Workforce Optimization":
        display_workforce_optimization()

if __name__ == "__main__":
    main()
