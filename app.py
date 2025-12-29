"""
HR Attrition Analytics – Driver & Pattern Explorer

PURPOSE
-------
This Streamlit app presents explainable attrition insights derived from
a detailed exploratory and multivariate analysis.

The app focuses on:
1. Understanding individual attrition drivers
2. Exploring dangerous feature combinations
3. Providing ready-to-present insights

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(
    page_title="HR Attrition Analytics",
    layout="wide"
)
# -------------------------------------------------
# UI Styling
# -------------------------------------------------
st.markdown(
    """
    <style>
        div[data-baseweb="select"] > div {
            font-size: 16px;
            min-height: 55px;
        }
        .stSelectbox label {
            font-size: 16px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)
sns.set_theme(style="whitegrid")

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data():
    scores = pd.read_csv("data/attrition_scored.csv")
    pairs = pd.read_csv("data/attrition_pairwise_patterns.csv")
    return scores, pairs

df_scores, df_pairs = load_data()

# ---------------------------
# Feature lists
# ---------------------------
driver_features = sorted(
    df_pairs["feature_1"].unique().tolist() +
    df_pairs["feature_2"].unique().tolist()
)
driver_features = sorted(list(set(driver_features)))

# ===========================
# TABS
# ===========================
tab1, tab2, tab3 = st.tabs([
    "🔍 Attrition Driver Explorer",
    "🧪 Heatmap Laboratory",
    "📌 Executive Summary"
])

# =====================================================
# TAB 1 — DRIVER EXPLORER
# =====================================================
with tab1:
    st.header("Attrition Driver Explorer")

    st.markdown(
        "Select a driver to understand **how it contributes to attrition**, "
        "and which combinations make it more dangerous."
    )

    selected_feature = st.selectbox(
        "Select Attrition Driver",
        driver_features
    )

    # ---------------------------
    # Univariate impact
    # ---------------------------
    st.subheader("Attrition Rate by Driver Values")

    uni = df_pairs[
        (df_pairs["feature_1"] == selected_feature)
    ][["feature_1_value", "attrition_rate", "support"]]

    uni = (
        uni.groupby("feature_1_value")
        .agg(
            attrition_rate=("attrition_rate", "mean"),
            support=("support", "sum")
        )
        .sort_values("attrition_rate", ascending=False)
        .head(5)
    )

    # Guard against empty data (important for binary engineered features)
    if uni.empty:
        st.warning(
            f"No sufficient data available to plot univariate impact for '{selected_feature}'."
        )
    else:
        fig, ax = plt.subplots(figsize=(4.5, 3))

        uni["attrition_rate"].plot(kind="bar", ax=ax)

        ax.set_ylabel("Attrition Rate")
        ax.set_xlabel(selected_feature.replace("_", " ").title())
        ax.set_title(f"Top Contributors – {selected_feature.replace('_', ' ').title()}")
        ax.tick_params(axis="x", rotation=45)

        col_left, col_mid, col_right = st.columns([1, 2, 1])
        with col_mid:
            st.pyplot(fig)

    # ---------------------------
    # Top combinations
    # ---------------------------
    st.subheader("Top Risk Combinations Involving This Driver")

    top_combos = df_pairs[
        (df_pairs["feature_1"] == selected_feature) |
        (df_pairs["feature_2"] == selected_feature)
    ].sort_values("attrition_rate", ascending=False).head(3)

   # Rename feature_1_value column to selected feature name for clarity
    display_df = top_combos[
        [
            "feature_1", "feature_1_value",
            "feature_2", "feature_2_value",
            "attrition_rate", "support"
        ]
    ].copy()

    display_df = display_df.rename(
        columns={
            "feature_1_value": f"{selected_feature} Value"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

# =====================================================
# TAB 2 — HEATMAP LAB
# =====================================================
with tab2:
    st.header("Heatmap Laboratory")

    st.markdown(
        "Explore **any pairwise interaction** to understand how two factors "
        "together influence attrition."
    )

    col1, col2 = st.columns(2)

    with col1:
        f1 = st.selectbox("Feature 1", driver_features, index=0)
    with col2:
        f2 = st.selectbox("Feature 2", driver_features, index=1)

    subset = df_pairs[
        (df_pairs["feature_1"] == f1) &
        (df_pairs["feature_2"] == f2)
    ]

    if not subset.empty:
        pivot = subset.pivot_table(
            index="feature_1_value",
            columns="feature_2_value",
            values="attrition_rate"
        )

        fig, ax = plt.subplots(figsize=(5, 4))

        sns.heatmap(
            pivot,
            annot=True,
            fmt=".2f",
            cmap="Reds",
            ax=ax
        )

        # Dynamic axis labels for business clarity
        ax.set_xlabel(f2.replace("_", " ").title())
        ax.set_ylabel(f1.replace("_", " ").title())

        # Title
        ax.set_title(
            f"Attrition Heatmap: {f1.replace('_', ' ').title()} vs {f2.replace('_', ' ').title()}"
        )

        # Improve tick readability
        ax.tick_params(axis="x", rotation=45)
        ax.tick_params(axis="y", rotation=0)

        # Center the plot in Streamlit
        col_left, col_mid, col_right = st.columns([1, 2, 1])
        with col_mid:
            st.pyplot(fig)
    else:
        st.info("No data available for this combination.")

# =====================================================
# TAB 3 — SUMMARY
# =====================================================
with tab3:
    st.header("Inferences & Key Insights")

    top_drivers = (
        df_pairs.groupby("feature_1")["attrition_rate"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader("Top Attrition Drivers")
    for i, drv in enumerate(top_drivers.index, 1):
        st.markdown(f"**{i}. {drv}**")

    st.subheader("High-Risk Employee Profiles")
    top_profiles = df_pairs.sort_values(
        "attrition_rate", ascending=False
    ).head(5)

    for _, row in top_profiles.iterrows():
        st.markdown(
            f"- Employees with **{row.feature_1} = {row.feature_1_value}** "
            f"and **{row.feature_2} = {row.feature_2_value}** "
            f"show attrition rate of **{row.attrition_rate:.0%}**")


    st.subheader("What ACME Can Take Steps to Reduce Attrition")

    st.markdown("""
    Based on the identified attrition drivers and high-risk employee profiles,
    ACME can consider the following targeted actions:

        **1. Improve Work-Life Balance**
        - Review overtime policies for high-risk roles
        - Introduce flexible working hours for impacted teams

        **2. Strengthen Career Progression**
        - Address role stagnation with internal mobility programs
        - Define clearer promotion and growth paths

        **3. Managerial Effectiveness**
        - Train managers in departments with high attrition signals
        - Introduce regular check-ins for employee sentiment

        **4. Compensation & Commute Considerations**
        - Re-evaluate compensation bands for high-risk income segments
        - Offer commute flexibility (hybrid / transport benefits)

        These actions are **data-backed**, prioritizable, and measurable.
        """)
