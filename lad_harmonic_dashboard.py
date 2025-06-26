
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("LAD Harmonic Octave Dashboard (2025)")

# Sidebar for octave selection
octave = st.sidebar.selectbox("Select Octave", [1, 2, 3, 4, 5])

# Load corresponding CSV
octave_file = f"LAD_Octave{octave}_Harmonic_Marking.csv"
if not os.path.exists(octave_file):
    st.error(f"Missing data file: {octave_file}")
    st.stop()

df = pd.read_csv(octave_file)

# Compute metrics
df["Resonance"] = 1 - abs(df["Projection"] - df["Reception"]) / df[["Projection", "Reception"]].max(axis=1)
df["Neutron"] = (df["Projection"] * df["Reception"]) ** 0.5
df["Proton"] = (df["Projection"] + df["Reception"]) / 2
df["Electron"] = (df["Reception"] - df["Projection"]) / 2

# Layout
col1, col2 = st.columns(2)

# Resonance waveform
fig1 = px.line(df, x="Game", y="Resonance", markers=True, color_discrete_sequence=["deepskyblue"])
fig1.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)
fig1.add_scatter(x=df[df["Nodal"] == "Yes"]["Game"], y=df[df["Nodal"] == "Yes"]["Resonance"],
                 mode='markers', marker=dict(size=12, color='gold', line=dict(color='black', width=1)), name="Nodal")
fig1.add_scatter(x=df[df["Echo"] == "Yes"]["Game"], y=df[df["Echo"] == "Yes"]["Resonance"],
                 mode='markers', marker=dict(size=10, color='blue', line=dict(color='white', width=1)), name="Echo")
fig1.add_scatter(x=df[df["WalkOff"] == "Yes"]["Game"], y=df[df["WalkOff"] == "Yes"]["Resonance"],
                 mode='markers', marker=dict(size=14, color='magenta', symbol='star'), name="Walk-Off")
fig1.update_layout(title=f"Octave {octave} – Resonance Profile", xaxis_title="Game", yaxis_title="Resonance")
fig1.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)

# Collapse metrics
fig2 = px.line(df, x="Game", y=["Neutron", "Proton", "Electron"], markers=True)
fig2.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)
fig2.add_scatter(x=df[df["Collapse"] == "Yes"]["Game"], y=df[df["Collapse"] == "Yes"]["Neutron"],
                 mode='markers', marker=dict(size=12, color='red', symbol='triangle-down'), name="Collapse")
fig2.update_layout(title=f"Octave {octave} – Collapse Metrics", xaxis_title="Game", yaxis_title="Metric Value")
fig2.update_xaxes(type='category', tickmode='linear', tick0=1, dtick=1)

col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# Octave state label
last_game = df["Game"].max()
last_res = df[df["Game"] == last_game]["Resonance"].values[0]
state = "SEALED" if last_res >= 0.95 and (df["Nodal"] == "Yes").sum() >= 2 else "BRAIDED / LIVE"
color = "gold" if state == "SEALED" else "blue"

st.markdown(f"### Octave Status: <span style='color:{color}; font-weight:bold'>{state}</span>", unsafe_allow_html=True)
