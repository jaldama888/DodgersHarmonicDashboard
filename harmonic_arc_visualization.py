
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="wide")
st.title("Harmonic Arc Visualization – Octaves 1 to 4")

# Harmonic status of each octave
octaves = ["Octave 1", "Octave 2", "Octave 3", "Octave 4"]
statuses = ["Braided", "Braided", "Braided", "Sealed"]
colors = ["blue", "blue", "blue", "gold"]

fig, ax = plt.subplots(figsize=(12, 6))

# Draw arc segments for each octave
for i, (label, status, color) in enumerate(zip(octaves, statuses, colors)):
    x = i * 2.5
    arc = patches.Arc((x + 1, 0), 2, 2, theta1=0, theta2=180,
                      color=color, lw=4, alpha=0.8)
    ax.add_patch(arc)
    ax.text(x + 1, 1.2, label, ha='center', fontsize=12, color='black')
    ax.text(x + 1, 0.4, status, ha='center', fontsize=10, color=color)

# Add annotation showing full arc closure
ax.text(5, 2.2, "← First Harmonic Arc Sealed →", fontsize=14, color="gold", ha="center", weight='bold')

# Format plot
ax.set_xlim(-0.5, 10)
ax.set_ylim(-0.5, 2.5)
ax.axis('off')
st.pyplot(fig)
