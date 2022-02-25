from custom_dynamics.enums import MillerDynamics
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
from utils import my_traces

df_results = pd.read_pickle("Dataframe_results_metrics.pkl")

df_results["dynamics_type_label"] = None
df_results.loc[df_results["dynamics_type"] == MillerDynamics.EXPLICIT, "dynamics_type_label"] = r"$\text{Exp-Full}$"
df_results.loc[
    df_results["dynamics_type"] == MillerDynamics.ROOT_EXPLICIT, "dynamics_type_label"
] = r"$\text{Exp-Base}$"
df_results.loc[
    df_results["dynamics_type"] == MillerDynamics.IMPLICIT, "dynamics_type_label"
] = r"$\text{Imp-Full-}\ddot{q}$"
df_results.loc[
    df_results["dynamics_type"] == MillerDynamics.ROOT_IMPLICIT, "dynamics_type_label"
] = r"$\text{Imp-Base-}\ddot{q}$"
df_results.loc[
    df_results["dynamics_type"] == MillerDynamics.IMPLICIT_TAU_DRIVEN_QDDDOT, "dynamics_type_label"
] = r"$\text{Imp-Full-}\dddot{q}$"
df_results.loc[
    df_results["dynamics_type"] == MillerDynamics.ROOT_IMPLICIT_QDDDOT, "dynamics_type_label"
] = r"$\text{Imp-Base-}\dddot{q}$"

dyn = df_results["dynamics_type_label"].unique()
grps = ["Explicit", "Explicit", "Implicit_qddot", "Implicit_qddot", "Implicit_qdddot", "Implicit_qdddot"]
dyn = dyn[[2, 4, 3, 5, 0, 1]]

fig = make_subplots(rows=1, cols=2)

# select only the one who converged
df_results = df_results[df_results["status"] == 0]

fig = my_traces(fig, dyn, grps, df_results, "T1", 1, 1, r"$T_1 \; \text{(s)}$")
fig = my_traces(fig, dyn, grps, df_results, "T2", 1, 2, r"$T_2 \; \text{(s)}$")

fig.update_layout(
    # xaxis_title=r'$\text{Transcription}$',
    height=400,
    width=800,
    paper_bgcolor="rgba(255,255,255,1)",
    plot_bgcolor="rgba(255,255,255,1)",
    legend=dict(
        title_font_family="Times New Roman",
        font=dict(family="Times New Roman", color="black", size=11),
        orientation="h",
        xanchor="center",
        x=0.5,
        y=-0.05,
    ),
    font=dict(
        size=12,
        family="Times New Roman",
    ),
    yaxis=dict(color="black"),
    template="simple_white",
    # showlegend=False,
    # violingap=0.1,
    boxgap=0.2,
)
fig.show()
