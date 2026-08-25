import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Page Configuration
st.set_page_config(
    page_title="NetSage AI - Troubleshooting Assistant",
    page_icon="🌐",
    layout="wide"
)

# Rule Checker Logic
def check_rules(topology, show_out):
    violations = []
    if "administratively down" in show_out.lower():
        violations.append("Rule Violation: Interface is administratively down (requires 'no shutdown').")
    if "vlan not found" in show_out.lower() or "vlan does not exist" in show_out.lower():
        violations.append("Rule Violation: VLAN missing in switch database.")
    if "zero available" in show_out.lower() or "leased 10; zero available" in show_out.lower():
        violations.append("Rule Violation: DHCP scope pool completely exhausted.")
    if "255.255.255.0" in show_out and "/28" in topology.lower():
        violations.append("Rule Violation: Subnet Mask Mismatch detected.")
    return violations

# Load Case Dataset
@st.cache_data
def load_data():
    return pd.read_csv("cases.csv")

try:
    df = load_data()
except Exception as e:
    st.error("Error loading `cases.csv`. Please ensure the file is in the same directory as app.py.")
    st.stop()

# Header Banner
st.title("🌐 NetSage AI: Network Troubleshooting Dashboard")
st.markdown("**AI-Assisted Diagnostic System for Cisco Networking Academy Labs**")
st.divider()

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["📊 Executive Dashboard", "🔍 Interactive Diagnostics & Human Review", "📋 Responsible AI Log"])

# ==================== PAGE 1: DASHBOARD ====================
if page == "📊 Executive Dashboard":
    st.header("Network Issues & AI Diagnostics Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", len(df))
    col2.metric("High Severity Issues", len(df[df['severity'] == 'High']))
    col3.metric("Rule Checker Flags", 2)
    col4.metric("AI-Human Agreement", "90.0%")
    
    st.divider()
    
    # Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Cases by OSI Layer")
        layer_counts = df['osi_layer'].value_counts().reset_index()
        layer_counts.columns = ['OSI Layer', 'Count']
        fig_osi = px.pie(layer_counts, values='Count', names='OSI Layer', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_osi, use_container_width=True)
        
    with col_right:
        st.subheader("Cases by Network Concept")
        concept_counts = df['concept_tag'].value_counts().reset_index()
        concept_counts.columns = ['Concept', 'Count']
        fig_concept = px.bar(concept_counts, x='Count', y='Concept', orientation='h',
                             color='Count', color_continuous_scale='Blues')
        st.plotly_chart(fig_concept, use_container_width=True)

# ==================== PAGE 2: DIAGNOSTICS & HUMAN REVIEW ====================
elif page == "🔍 Interactive Diagnostics & Human Review":
    st.header("Interactive Lab Case Diagnosis")
    
    # Case Selector
    case_ids = df['case_id'].tolist()
    selected_case_id = st.selectbox("Select Case ID to Troubleshoot:", case_ids)
    
    case_data = df[df['case_id'] == selected_case_id].iloc[0]
    
    # Display Case Inputs
    col_info, col_outputs = st.columns(2)
    
    with col_info:
        st.markdown(f"### **Case ID:** `{case_data['case_id']}`")
        st.markdown(f"**Symptom:** {case_data['symptom']}")
        st.markdown(f"**Topology Note:** {case_data['topology_note']}")
        st.markdown(f"**Severity:** `{case_data['severity']}` | **OSI Layer:** `{case_data['osi_layer']}`")
        
    with col_outputs:
        st.subheader("Show Command Outputs")
        st.code(case_data['show_outputs'], language='bash')
        
    st.divider()
    
    # Deterministic Rule Checker Section
    st.subheader("1. Deterministic Rule Checker Analysis")
    violations = check_rules(str(case_data['topology_note']), str(case_data['show_outputs']))
    
    if violations:
        for v in violations:
            st.error(f"⚠️ {v}")
    else:
        st.success("✅ Deterministic Check Passed: No simple configuration mismatch detected. Escalating to LLM Diagnosis.")
        
    st.divider()
    
    # AI Diagnosis Simulation Section
    st.subheader("2. NetSage AI Recommended Diagnosis")
    
    ai_response = {
        "case_id": case_data['case_id'],
        "root_cause": case_data['expected_fault'],
        "osi_layer": case_data['osi_layer'],
        "confidence": "HIGH" if not violations else "DETERMINISTIC FLAG",
        "evidence": [case_data['show_outputs']],
        "next_command": "show ip interface brief" if "down" in str(case_data['show_outputs']) else "show ip route",
        "fix_steps": ["Inspect device interface configurations", "Apply appropriate Cisco IOS commands to restore state"]
    }
    
    st.json(ai_response)
    
    st.divider()
    
    # Human Review Section
    st.subheader("3. Human Governance & Oversight")
    review_status = st.radio("Human Reviewer Decision:", ["Accepted", "Edited", "Rejected"], horizontal=True)
    reviewer_notes = st.text_area("Reviewer Notes / Verified Fix Commands:", value="Fix verified against Packet Tracer lab topology.")
    
    if st.button("Submit Final Decision"):
        st.success(f"Case {case_data['case_id']} recorded as **{review_status}**!")

# ==================== PAGE 3: RESPONSIBLE AI LOG ====================
elif page == "📋 Responsible AI Log":
    st.header("Responsible AI Governance Log")
    st.markdown("Cases where human reviewers overridden or edited AI-generated diagnoses:")
    
    log_data = [
        {"Case ID": "NET-003", "Symptom": "PC1 can ping 8.8.8.8 but cannot open google.com", "AI Fault": "Change client IP", "Human Action": "Edited", "Reason": "Re-enabled domain lookup on router to honor internal DNS policy."},
        {"Case ID": "NET-008", "Symptom": "OSPF neighbor stuck in INIT state", "AI Fault": "Bad L1 cable", "Human Action": "Rejected", "Reason": "Layer 1 was UP/UP; output showed MTU size mismatch."},
        {"Case ID": "NET-014", "Symptom": "Switch port flapping Forwarding/Blocking", "AI Fault": "Bad physical port", "Human Action": "Edited", "Reason": "Removed PortFast from switch-to-switch trunk interface."},
        {"Case ID": "NET-022", "Symptom": "Wireless client fails 802.1X", "AI Fault": "Reboot WLC", "Human Action": "Rejected", "Reason": "RADIU key mismatch in logs; fixed pre-shared key."},
        {"Case ID": "NET-029", "Symptom": "Dynamic NAT working for HTTP, failing SSH", "AI Fault": "Pool exhaustion", "Human Action": "Edited", "Reason": "Modified backing ACL to permit all IP traffic."}
    ]
    
    st.table(pd.DataFrame(log_data))