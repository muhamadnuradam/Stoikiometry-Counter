import streamlit as st
import pandas as pd
import altair as alt


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Mass Balance",
    page_icon="⚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@font-face {
    font-family: "Helvetica";
    src: local("Helvetica"),
         local("Helvetica Neue"),
         local("Arial");
}


/* =====================================================
    GLOBAL
    ===================================================== */

html,
body,
.stApp,
.stApp *,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *,
[data-testid="stMain"],
[data-testid="stMain"] * {

    font-family:
        "Helvetica",
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}


/* =====================================================
    COLORS
    ===================================================== */

:root {

    --navy: #071A33;
    --blue: #0B3A6E;
    --blue-light: #EAF2FA;

    --black: #111111;
    --gray: #667085;
    --line: #D9E0E8;

    --white: #FFFFFF;
}


/* =====================================================
    APP
    ===================================================== */

.stApp {
    background: #FFFFFF !important;
    color: var(--black) !important;
}


/* =====================================================
    MAIN CONTENT
    ===================================================== */

[data-testid="stAppViewContainer"] {
    background: #FFFFFF !important;
}

[data-testid="stMain"] {
    background: #FFFFFF !important;
}


/* =====================================================
    HEADER
    ===================================================== */

[data-testid="stHeader"] {
    background: #FFFFFF !important;
}


/* =====================================================
    SIDEBAR
    ===================================================== */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #071A33 0%,
            #0A2342 100%
        ) !important;

    border-right: 1px solid #102E50 !important;
}


[data-testid="stSidebar"] * {

    color: #FFFFFF !important;

    font-family:
        "Helvetica",
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}


/* sidebar title */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {

    color: #FFFFFF !important;
    font-weight: 600 !important;
}


/* sidebar input */

[data-testid="stSidebar"] input {

    background: #102E50 !important;

    color: #FFFFFF !important;

    border:
        1px solid
        #2B4D70 !important;

    border-radius: 6px !important;

    font-size: 13px !important;
}


/* sidebar number */

[data-testid="stSidebar"] [data-baseweb="input"] {

    background: #102E50 !important;
}


/* sidebar labels */

[data-testid="stSidebar"] label {

    color: #D9E5F2 !important;

    font-size: 12px !important;

    font-weight: 400 !important;
}


.main-title {
    font-family:
        "Helvetica",
        "Helvetica Neue",
        Arial,
        sans-serif !important;

    font-size: 27px !important;
    line-height: 1.3 !important;

    font-weight: 600 !important;

    letter-spacing: -0.5px;

    color: #071A33 !important;

    margin-top: 0 !important;
    margin-bottom: 3px !important;

    padding-top: 2px !important;

    overflow: visible !important;
}

.subtitle {

    font-size: 13px;

    color: #667085;

    margin-bottom: 20px;
}


/* =====================================================
    SECTION TITLE
    ===================================================== */

.section-title {

    font-size: 16px;

    font-weight: 600;

    color: #071A33;

    margin-top: 5px;

    margin-bottom: 10px;
}


/* =====================================================
    CARD
    ===================================================== */

.card {

    background: #FFFFFF;

    border:
        1px solid
        #D9E0E8;

    border-radius: 9px;

    padding: 17px 19px;

    margin-bottom: 13px;
}


.card-blue {

    background: #EAF2FA;

    border:
        1px solid
        #C9DBED;

    border-radius: 9px;

    padding: 17px 19px;

    margin-bottom: 13px;
}


/* =====================================================
    SMALL LABEL
    ===================================================== */

.small-label {

    font-size: 11px;

    color: #667085;

    letter-spacing: 0.3px;

    text-transform: uppercase;

    margin-bottom: 4px;
}


/* =====================================================
    RESULT NUMBER
    ===================================================== */

.result-number {

    font-size: 21px;

    line-height: 1.1;

    font-weight: 600;

    color: #071A33;
}


/* =====================================================
    NORMAL NUMBER
    ===================================================== */

.number {

    font-size: 13px;

    color: #111111;

    font-weight: 500;
}


/* =====================================================
    BODY
    ===================================================== */

.body-text {

    font-size: 13px;

    line-height: 1.55;

    color: #303846;
}


/* =====================================================
    FORMULA
    ===================================================== */

.formula-box {

    background: #F5F8FB;

    border-left:
        3px solid
        #0B3A6E;

    padding: 9px 13px;

    margin: 9px 0;

    border-radius: 3px;
}


/* =====================================================
    SUCCESS
    ===================================================== */

.final-box {

    background: #071A33;

    color: white;

    border-radius: 9px;

    padding: 17px 19px;

    margin-top: 10px;
}


.final-title {

    font-size: 12px;

    color: #AFC9E5;

    text-transform: uppercase;

    letter-spacing: 0.5px;

    margin-bottom: 7px;
}


.final-main {

    font-size: 15px;

    color: white;

    line-height: 1.5;
}


/* =====================================================
    METRIC
    ===================================================== */

[data-testid="stMetric"] {

    background: #FFFFFF;

    border:
        1px solid
        #D9E0E8;

    border-radius: 8px;

    padding: 11px 14px;
}


[data-testid="stMetricLabel"] {

    font-size: 10px !important;

    color: #667085 !important;

    font-weight: 400 !important;
}


[data-testid="stMetricValue"] {

    font-size: 20px !important;

    color: #071A33 !important;

    font-weight: 600 !important;
}


[data-testid="stMetricDelta"] {

    font-size: 10px !important;
}


/* =====================================================
    INPUT
    ===================================================== */

.stTextInput input,
.stNumberInput input {

    font-family:
        "Helvetica",
        "Helvetica Neue",
        Arial,
        sans-serif !important;

    font-size: 13px !important;

    color: #111111 !important;

    background: #F4F6F8 !important;

    border:
        1px solid
        #D9E0E8 !important;

    border-radius: 6px !important;
}


/* =====================================================
    BUTTON
    ===================================================== */

button,
button * {

    font-family:
        "Helvetica",
        "Helvetica Neue",
        Arial,
        sans-serif !important;
}


/* =====================================================
    DATAFRAME
    ===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 7px;

    overflow: hidden;
}


/* =====================================================
    CAPTION
    ===================================================== */

[data-testid="stCaptionContainer"] {

    color: #667085 !important;

    font-size: 11px !important;
}


/* =====================================================
    DIVIDER
    ===================================================== */

hr {

    border: none !important;

    border-top:
        1px solid
        #E2E7ED !important;

    margin:
        14px 0 !important;
}


/* =====================================================
    REMOVE EXTRA SPACE
    ===================================================== */

.block-container {

    padding-top: 28px !important;

    padding-bottom: 25px !important;

    max-width: 1450px !important;
}


/* =====================================================
    LATEX
    ===================================================== */

.katex {

    font-size: 0.90em !important;
}


/* =====================================================
    ALERT
    ===================================================== */

[data-testid="stAlert"] {

    border-radius: 8px !important;

    font-size: 13px !important;
}
/* =====================================================
    NUMBER INPUT - TOMBOL PLUS MINUS HITAM
    ===================================================== */

.stNumberInput button {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    border: none !important;
}

.stNumberInput button:hover {
    color: #000000 !important;
    background-color: #E5E7EB !important;
}

.stNumberInput button svg {
    color: #000000 !important;
    stroke: #000000 !important;
}

.stNumberInput button svg path {
    stroke: #000000 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================

def format_formula(u1, q1, u2, q2):
    f1 = u1 if q1 == 1 else f"{u1}<sub>{q1}</sub>"
    f2 = u2 if q2 == 1 else f"{u2}<sub>{q2}</sub>"
    return f"{f1}{f2}"

def format_formula_plain(u1, q1, u2, q2):
    f1 = u1 if q1 == 1 else f"{u1}{q1}"
    f2 = u2 if q2 == 1 else f"{u2}{q2}"
    return f"{f1}{f2}"


def calculate_mass_balance(
    ar1,
    ar2,
    a_qty_1,
    a_qty_2,
    b_qty_1,
    b_qty_2,
    target_mass
):
    mr_a = (
        a_qty_1 * ar1
        +
        a_qty_2 * ar2
    )

    mr_b = (
        b_qty_1 * ar1
        +
        b_qty_2 * ar2
    )

    wt_a1 = (
        a_qty_1 * ar1 / mr_a
    ) * 100

    wt_a2 = (
        a_qty_2 * ar2 / mr_a
    ) * 100

    wt_b1 = (
        b_qty_1 * ar1 / mr_b
    ) * 100

    wt_b2 = (
        b_qty_2 * ar2 / mr_b
    ) * 100

    massa_u1 = (
        wt_b1 / 100
    ) * target_mass

    massa_u2 = (
        wt_b2 / 100
    ) * target_mass

    massa_a = (
        massa_u1 /
        (wt_a1 / 100)
    )

    u2_dari_a = (
        wt_a2 / 100
    ) * massa_a

    defisit_u2 = (
        massa_u2 -
        u2_dari_a
    )

    tambahan_u2 = max(
        defisit_u2,
        0
    )

    total = (
        massa_a +
        tambahan_u2
    )

    return {
        "mr_a": mr_a,
        "mr_b": mr_b,
        "wt_a1": wt_a1,
        "wt_a2": wt_a2,
        "wt_b1": wt_b1,
        "wt_b2": wt_b2,
        "massa_u1": massa_u1,
        "massa_u2": massa_u2,
        "massa_a": massa_a,
        "u2_dari_a": u2_dari_a,
        "defisit_u2": defisit_u2,
        "tambahan_u2": tambahan_u2,
        "total": total
    }


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:20px;
        font-weight:600;
        margin-bottom:4px;
    ">
        Alloy Calculator
    </div>

    <div style="
        font-size:11px;
        color:#AFC9E5;
        margin-bottom:22px;
    ">
        Stoichiometric Mass Balance
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# ELEMENTS
# ---------------------------------------------------------

st.sidebar.markdown("**ELEMENTS**")

col1, col2 = st.sidebar.columns(2)

unsur_1 = col1.text_input(
    "Symbol",
    value="Sm"
)

ar_1 = col2.number_input(
    "Ar",
    value=150.36,
    min_value=0.01,
    step=0.01
)


col1, col2 = st.sidebar.columns(2)

unsur_2 = col1.text_input(
    "Symbol",
    value="Co"
)

ar_2 = col2.number_input(
    "Ar",
    value=58.93,
    min_value=0.01,
    step=0.01
)


st.sidebar.markdown("---")


# ---------------------------------------------------------
# PRECURSOR
# ---------------------------------------------------------

st.sidebar.markdown("**PRECURSOR A**")

col1, col2 = st.sidebar.columns(2)

a_qty_1 = col1.number_input(
    f"{unsur_1}",
    value=1,
    min_value=1,
    step=1
)

a_qty_2 = col2.number_input(
    f"{unsur_2}",
    value=5,
    min_value=1,
    step=1
)


# ---------------------------------------------------------
# TARGET
# ---------------------------------------------------------

st.sidebar.markdown("**TARGET B**")

col1, col2 = st.sidebar.columns(2)

b_qty_1 = col1.number_input(
    f"{unsur_1}",
    value=2,
    min_value=1,
    step=1
)

b_qty_2 = col2.number_input(
    f"{unsur_2}",
    value=17,
    min_value=1,
    step=1
)


st.sidebar.markdown("---")


# ---------------------------------------------------------
# MASS
# ---------------------------------------------------------

st.sidebar.markdown("**TARGET MASS**")

massa_target = st.sidebar.number_input(
    "Mass (g)",
    value=1000.0,
    min_value=0.01,
    step=10.0
)


# =========================================================
# VALIDATION
# =========================================================

unsur_1 = unsur_1.strip()
unsur_2 = unsur_2.strip()


if not unsur_1 or not unsur_2:
    st.error("Symbols cannot be empty.")
    st.stop()


if unsur_1 == unsur_2:
    st.error("Symbols must be different.")
    st.stop()


# =========================================================
# FORMULA
# =========================================================

mat_a = format_formula(
    unsur_1,
    a_qty_1,
    unsur_2,
    a_qty_2
)

mat_b = format_formula(
    unsur_1,
    b_qty_1,
    unsur_2,
    b_qty_2
)

mat_a_plain = format_formula_plain(
    unsur_1,
    a_qty_1,
    unsur_2,
    a_qty_2
)

mat_b_plain = format_formula_plain(
    unsur_1,
    b_qty_1,
    unsur_2,
    b_qty_2
)


# =========================================================
# CALCULATION
# =========================================================

r = calculate_mass_balance(
    ar_1,
    ar_2,
    a_qty_1,
    a_qty_2,
    b_qty_1,
    b_qty_2,
    massa_target
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    'ALLOY PREPARATION SIMULATION'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Stoichiometric mass balance'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# MATERIAL HEADER
# =========================================================

col_a, col_b = st.columns(
    [1, 1]
)


with col_a:
    st.markdown(
        f"""
        <div class="card">

        <div class="small-label">
        Precursor
        </div>

        <div class="result-number">
        {mat_a}
        </div>

        <div class="body-text">
        Mr {r["mr_a"]:.2f} g/mol
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col_b:
    st.markdown(
        f"""
        <div class="card-blue">

        <div class="small-label">
        Target
        </div>

        <div class="result-number">
        {mat_b}
        </div>

        <div class="body-text">
        Mr {r["mr_b"]:.2f} g/mol
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KEY RESULTS
# =========================================================

st.markdown(
    '<div class="section-title">Mass balance</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(
    [1, 1, 1]
)


with col1:
    st.metric(
        "Precursor",
        f'{r["massa_a"]:.2f} g'
    )


with col2:
    st.metric(
        f'Pure {unsur_2}',
        f'{r["tambahan_u2"]:.2f} g'
    )


with col3:
    st.metric(
        "Total",
        f'{r["total"]:.2f} g'
    )


st.divider()


# =========================================================
# GOLDEN RATIO LAYOUT
# =========================================================

left, right = st.columns(
    [1.618, 1]
)


# =========================================================
# LEFT
# =========================================================

with left:
    st.markdown(
        '<div class="section-title">'
        'Composition'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="small-label">
            PRECURSOR {mat_a}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"Ar {unsur_1} = {ar_1:.2f} g/mol"
        )

        st.write(
            f"Ar {unsur_2} = {ar_2:.2f} g/mol"
        )

        st.latex(
            rf"""
            M_r =
            ({a_qty_1}\times{ar_1:.2f})
            +
            ({a_qty_2}\times{ar_2:.2f})
            =
            {r["mr_a"]:.2f}
            """
        )

        st.write(
            f"{unsur_1}: **{r['wt_a1']:.2f}%**"
        )

        st.write(
            f"{unsur_2}: **{r['wt_a2']:.2f}%**"
        )

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="small-label">
            TARGET {mat_b}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.latex(
            rf"""
            M_r =
            ({b_qty_1}\times{ar_1:.2f})
            +
            ({b_qty_2}\times{ar_2:.2f})
            =
            {r["mr_b"]:.2f}
            """
        )

        st.write(
            f"{unsur_1}: **{r['wt_b1']:.2f}%**"
        )

        st.write(
            f"{unsur_2}: **{r['wt_b2']:.2f}%**"
        )

    st.markdown(
        '<div class="section-title">'
        'Element Demand'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.write(
            f"{unsur_1}"
        )

        st.latex(
            rf"""
            m_{{{unsur_1}}}
            =
            {r["wt_b1"]:.2f}\%
            \times
            {massa_target:.2f}
            =
            {r["massa_u1"]:.2f}\ g
            """
        )

        st.write(
            f"{unsur_2}"
        )

        st.latex(
            rf"""
            m_{{{unsur_2}}}
            =
            {r["wt_b2"]:.2f}\%
            \times
            {massa_target:.2f}
            =
            {r["massa_u2"]:.2f}\ g
            """
        )

    st.markdown(
        '<div class="section-title">'
        'Mass balance'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown(f"**Mass of {mat_a}**", unsafe_allow_html=True)
        st.latex(
            rf"""
            m_A = \frac{{{r["massa_u1"]:.2f}}}{{{{r["wt_a1"]:.2f}}/100}} = {r["massa_a"]:.2f}\ \text{{g}}
            """
        )

    with st.container(border=True):
        st.markdown(f"**{unsur_2} from {mat_a}**", unsafe_allow_html=True)
        st.latex(
            rf"""
            m_{{{unsur_2},A}} = {r["wt_a2"]:.2f}\% \times {r["massa_a"]:.2f} = {r["u2_dari_a"]:.2f}\ \text{{g}}
            """
        )

    with st.container(border=True):
        st.markdown(f"**{unsur_2} Deficit**", unsafe_allow_html=True)
        st.latex(
            rf"""
            \Delta m = {r["massa_u2"]:.2f} - {r["u2_dari_a"]:.2f} = {r["defisit_u2"]:.2f}\ \text{{g}}
            """
        )


# =========================================================
# RIGHT
# =========================================================

with right:
    st.markdown(
        '<div class="section-title">'
        'Visualization'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # CHART 1
    # -----------------------------------------------------

    chart_1_data = pd.DataFrame({
        "Material": [
            mat_a_plain,
            f"Pure {unsur_2}"
        ],
        "Mass": [
            r["massa_a"],
            r["tambahan_u2"]
        ]
    })

    chart_1 = (
        alt.Chart(chart_1_data)
        .mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4
        )
        .encode(
            x=alt.X(
                "Material:N",
                title=None,
                axis=alt.Axis(
                    labelFont="Helvetica",
                    labelFontSize=11
                )
            ),
            y=alt.Y(
                "Mass:Q",
                title="g",
                axis=alt.Axis(
                    labelFont="Helvetica",
                    titleFont="Helvetica",
                    labelFontSize=10,
                    titleFontSize=10
                )
            ),
            tooltip=[
                alt.Tooltip(
                    "Material:N",
                    title="Material"
                ),
                alt.Tooltip(
                    "Mass:Q",
                    title="Mass",
                    format=".2f"
                )
            ]
        )
        .properties(
            height=260
        )
        .configure_view(
            stroke=None
        )
    )

    st.altair_chart(
        chart_1,
        use_container_width=True
    )

    # -----------------------------------------------------
    # DISTRIBUTION — STACKED BAR
    # -----------------------------------------------------

    chart_2_data = pd.DataFrame({
        "Source": [
            mat_a_plain,
            mat_a_plain,
            f"Pure {unsur_2}"
        ],

        "Element": [
            unsur_1,
            unsur_2,
            unsur_2
        ],

        "Mass": [
            r["massa_u1"],
            r["u2_dari_a"],
            r["tambahan_u2"]
        ]
    })


    chart_2 = (
        alt.Chart(chart_2_data)

        .mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        )

        .encode(

            x=alt.X(
                "Source:N",
                title=None,

                sort=[
                    mat_a_plain,
                    f"Pure {unsur_2}"
                ],

                axis=alt.Axis(
                    labelFont="Helvetica",
                    labelFontSize=10,
                    labelAngle=0
                )
            ),

            y=alt.Y(
                "Mass:Q",
                title="g",
                stack="zero",

                axis=alt.Axis(
                    labelFont="Helvetica",
                    titleFont="Helvetica",
                    labelFontSize=10,
                    titleFontSize=10
                )
            ),

            color=alt.Color(
                "Element:N",
                title="Element",

                scale=alt.Scale(
                    range=[
                        "#071A33",
                        "#0B3A6E"
                    ]
                ),

                legend=alt.Legend(
                    labelFont="Helvetica",
                    labelFontSize=10,
                    titleFont="Helvetica",
                    titleFontSize=10
                )
            ),

            tooltip=[
                alt.Tooltip(
                    "Source:N",
                    title="Source"
                ),

                alt.Tooltip(
                    "Element:N",
                    title="Element"
                ),

                alt.Tooltip(
                    "Mass:Q",
                    title="Mass",
                    format=".2f"
                )
            ]
        )

        .properties(
            height=250
        )

        .configure_view(
            stroke=None
        )
    )


    st.altair_chart(
        chart_2,
        use_container_width=True
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    summary = pd.DataFrame({
        "Component": [
            mat_a_plain,
            f"Pure {unsur_2}",
            "Total"
        ],
        "Mass (g)": [
            r["massa_a"],
            r["tambahan_u2"],
            r["total"]
        ]
    })

    st.dataframe(
        summary.style.format({
            "Mass (g)": "{:.2f}"
        }),
        hide_index=True,
        use_container_width=True
    )


# =========================================================
# FINAL RESULT
# =========================================================

st.markdown(
    f"""
    <div style="background-color: #071A33; color: white; border-radius: 9px; padding: 17px 19px; margin-top: 10px;">
        <div style="font-size: 12px; color: #AFC9E5; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 7px;">
            Preparation
        </div>
        <div style="font-size: 15px; color: white; line-height: 1.5;">
            {r["massa_a"]:.2f} g {mat_a} &nbsp;+&nbsp; {r["tambahan_u2"]:.2f} g pure {unsur_2}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#98A2B3;
        font-size:10px;
        margin-top:18px;
    ">
        Stoichiometric calculation · Mass balance
    </div>
    """,
    unsafe_allow_html=True
)