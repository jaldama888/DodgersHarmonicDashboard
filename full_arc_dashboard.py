
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Harmonic Field – Full Arc Explorer (Octaves 1 to 4)")

# Load combined dataset
df = pd.read_csv("LAD_Combined_Octaves_1_to_4.csv")

# Sidebar filter
selected_octaves = st.sidebar.multiselect("Filter by Octave", options=df["Octave"].unique(), default=list(df["Octave"].unique()))
df_filtered = df[df["Octave"].isin(selected_octaves)]

# Harmonic markers
df["Resonance"] = 1 - abs(df["Projection"] - df["Reception"]) / df[["Projection", "Reception"]].max(axis=1)
nodal = df[df["Nodal"] == "Yes"]
echo = df[df["Echo"] == "Yes"]
collapse = df[df["Collapse"] == "Yes"]
walkoff = df[df["WalkOff"] == "Yes"]

# Resonance plot
fig1 = px.line(df_filtered, x="Game", y="Resonance", color="Octave", markers=True)
fig1.add_scatter(x=nodal["Game"], y=nodal["Resonance"], mode='markers',
                 marker=dict(size=12, color='gold', line=dict(color='black', width=1)), name="Nodal")
fig1.add_scatter(x=echo["Game"], y=echo["Resonance"], mode='markers',
                 marker=dict(size=10, color='blue', line=dict(color='white', width=1)), name="Echo")
fig1.add_scatter(x=walkoff["Game"], y=walkoff["Resonance"], mode='markers',
                 marker=dict(size=14, color='magenta', symbol='star'), name="Walk-Off")
fig1.update_layout(title="Combined Octaves – Resonance Waveform", xaxis_title="Game", yaxis_title="Resonance")
fig1.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)

# Collapse metrics
fig2 = px.line(df_filtered, x="Game", y=["Neutron", "Proton", "Electron"], markers=True, color_discrete_sequence=["purple", "orange", "green"])
fig2.add_scatter(x=collapse["Game"], y=collapse["Neutron"],
                 mode='markers', marker=dict(size=12, color='red', symbol='triangle-down'), name="Collapse")
fig2.update_layout(title="Combined Octaves – Collapse Metrics", xaxis_title="Game", yaxis_title="Field Metric Value")
fig2.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)

# Layout
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
