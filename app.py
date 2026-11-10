import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Materials Engineering Lab",
    page_icon="🧪",
    layout="wide"
)

# Website title and design
st.title("Materials Engineering Lab")
st.caption("Material testing, comparison, and optimization")

# Store samples while the app is running
columns = [
    "Sample",
    "Binder (%)",
    "Fiber Arrangement",
    "Strength (MPa)",
    "Flexibility (%)",
    "Durability (%)",
    "Repairability (%)",
    "Recovery (%)"
]

if "samples" not in st.session_state:
    st.session_state.samples = pd.DataFrame(columns=columns)

# Navigation
page = st.sidebar.radio(
    "NAVIGATION",
    ["Material Lab", "Compare Materials", "Material Optimizer"]
)

# PAGE 1: MATERIAL LAB
if page == "Material Lab":

    st.header("Material Lab")
    st.write("Enter the measurements for a material sample.")

    with st.form("sample_form"):

        sample = st.text_input("Sample name")

        binder = st.number_input(
            "Binder percentage (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0
        )

        arrangement = st.selectbox(
            "Fiber arrangement",
            ["Random", "Aligned", "Layered"]
        )

        strength = st.number_input(
            "Strength (MPa)",
            min_value=0.0,
            value=0.0
        )

        flexibility = st.number_input(
            "Flexibility (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        durability = st.number_input(
            "Durability (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        repairability = st.number_input(
            "Repairability (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        recovery = st.number_input(
            "Recovery (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        submitted = st.form_submit_button("Add Sample")

    if submitted:
        if sample.strip() == "":
            st.error("Please enter a sample name.")
        elif sample in st.session_state.samples["Sample"].values:
            st.error("That sample name already exists.")
        else:
            new_sample = {
                "Sample": sample,
                "Binder (%)": binder,
                "Fiber Arrangement": arrangement,
                "Strength (MPa)": strength,
                "Flexibility (%)": flexibility,
                "Durability (%)": durability,
                "Repairability (%)": repairability,
                "Recovery (%)": recovery
            }

            st.session_state.samples = pd.concat(
                [
                    st.session_state.samples,
                    pd.DataFrame([new_sample])
                ],
                ignore_index=True
            )

            st.success("Sample added!")

    st.subheader("Your Experimental Samples")
    st.dataframe(st.session_state.samples, use_container_width=True)

    if not st.session_state.samples.empty:
        st.download_button(
            "Download Sample Data (CSV)",
            st.session_state.samples.to_csv(index=False),
            file_name="material_samples.csv",
            mime="text/csv"
        )


# PAGE 2: COMPARE MATERIALS
elif page == "Compare Materials":

    st.header("Compare Materials")

    df = st.session_state.samples

    if df.empty:
        st.info("Add material samples in the Material Lab first.")
    else:
        selected = st.multiselect(
            "Choose samples to compare",
            df["Sample"].tolist(),
            default=df["Sample"].tolist()
        )

        comparison = df[df["Sample"].isin(selected)]

        st.subheader("Sample Comparison")
        st.dataframe(comparison, use_container_width=True)

        metric = st.selectbox(
            "Choose a property to graph",
            [
                "Strength (MPa)",
                "Flexibility (%)",
                "Durability (%)",
                "Repairability (%)",
                "Recovery (%)"
            ]
        )

        if not comparison.empty:
            chart_data = comparison.set_index("Sample")[[metric]]
            st.bar_chart(chart_data)

            best = comparison.loc[comparison[metric].idxmax()]
            st.write(
                f"Highest {metric}: {best['Sample']} "
                f"({best[metric]})"
            )


# PAGE 3: MATERIAL OPTIMIZER
elif page == "Material Optimizer":

    st.header("Material Optimizer")

    df = st.session_state.samples.copy()

    if df.empty:
        st.info("Add material samples in the Material Lab first.")
    else:
        st.write(
            "Rank your tested samples using an equal-weight "
            "score across the five selected properties."
        )

        st.warning(
            "This is a simple comparison score, not a scientifically "
            "validated prediction. It assumes higher values are better "
            "for every property and gives each property equal importance."
        )

        properties = [
            "Strength (MPa)",
            "Flexibility (%)",
            "Durability (%)",
            "Repairability (%)",
            "Recovery (%)"
        ]

        scores = pd.DataFrame(index=df.index)

        for prop in properties:
            maximum = df[prop].max()

            if maximum > 0:
                scores[prop] = df[prop] / maximum
            else:
                scores[prop] = 0.0

        df["Overall Score"] = scores.mean(axis=1)

        ranked = df.sort_values(
            "Overall Score",
            ascending=False
        )

        st.subheader("Ranked Material Samples")

        st.dataframe(
            ranked[
                ["Sample"] + properties + ["Overall Score"]
            ],
            use_container_width=True
        )

        winner = ranked.iloc[0]

        st.success(
            f"Highest scoring sample: {winner['Sample']} "
            f"({winner['Overall Score']:.3f})"
        )

        st.bar_chart(
            ranked.set_index("Sample")[["Overall Score"]]
        )
