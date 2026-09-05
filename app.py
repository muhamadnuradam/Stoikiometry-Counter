import streamlit as st
import pandas as pd
import altair as alt
import re
import json
import os
import requests
from collections import OrderedDict

# Import dictionary dari file compounds.py
from compounds import COMPOUND_LIBRARY

# =========================================================
# SAFE HTML RENDERER
# =========================================================
def render_html(markup, **kwargs):
    cleaned_markup = "\n".join(line.strip() for line in markup.split('\n'))
    st.markdown(cleaned_markup, **kwargs)

def render_sidebar(markup, **kwargs):
    cleaned_markup = "\n".join(line.strip() for line in markup.split('\n'))
    st.sidebar.markdown(cleaned_markup, **kwargs)

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Alloy Calculator",
    page_icon="⚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PERIODIC TABLE DATA
# =========================================================

ELEMENTS_DATA = {
    "H": {"name": "Hydrogen", "ar": 1.008},
    "He": {"name": "Helium", "ar": 4.0026},
    "Li": {"name": "Lithium", "ar": 6.94},
    "Be": {"name": "Beryllium", "ar": 9.0122},
    "B": {"name": "Boron", "ar": 10.81},
    "C": {"name": "Carbon", "ar": 12.011},
    "N": {"name": "Nitrogen", "ar": 14.007},
    "O": {"name": "Oxygen", "ar": 15.999},
    "F": {"name": "Fluorine", "ar": 18.998},
    "Ne": {"name": "Neon", "ar": 20.180},
    "Na": {"name": "Sodium", "ar": 22.990},
    "Mg": {"name": "Magnesium", "ar": 24.305},
    "Al": {"name": "Aluminium", "ar": 26.982},
    "Si": {"name": "Silicon", "ar": 28.085},
    "P": {"name": "Phosphorus", "ar": 30.974},
    "S": {"name": "Sulfur", "ar": 32.06},
    "Cl": {"name": "Chlorine", "ar": 35.45},
    "Ar": {"name": "Argon", "ar": 39.948},
    "K": {"name": "Potassium", "ar": 39.098},
    "Ca": {"name": "Calcium", "ar": 40.078},
    "Sc": {"name": "Scandium", "ar": 44.956},
    "Ti": {"name": "Titanium", "ar": 47.867},
    "V": {"name": "Vanadium", "ar": 50.942},
    "Cr": {"name": "Chromium", "ar": 51.996},
    "Mn": {"name": "Manganese", "ar": 54.938},
    "Fe": {"name": "Iron", "ar": 55.845},
    "Co": {"name": "Cobalt", "ar": 58.933},
    "Ni": {"name": "Nickel", "ar": 58.693},
    "Cu": {"name": "Copper", "ar": 63.546},
    "Zn": {"name": "Zinc", "ar": 65.38},
    "Ga": {"name": "Gallium", "ar": 69.723},
    "Ge": {"name": "Germanium", "ar": 72.630},
    "As": {"name": "Arsenic", "ar": 74.922},
    "Se": {"name": "Selenium", "ar": 78.971},
    "Br": {"name": "Bromine", "ar": 79.904},
    "Kr": {"name": "Krypton", "ar": 83.798},
    "Rb": {"name": "Rubidium", "ar": 85.468},
    "Sr": {"name": "Strontium", "ar": 87.62},
    "Y": {"name": "Yttrium", "ar": 88.906},
    "Zr": {"name": "Zirconium", "ar": 91.224},
    "Nb": {"name": "Niobium", "ar": 92.906},
    "Mo": {"name": "Molybdenum", "ar": 95.95},
    "Ru": {"name": "Ruthenium", "ar": 101.07},
    "Rh": {"name": "Rhodium", "ar": 102.91},
    "Pd": {"name": "Palladium", "ar": 106.42},
    "Ag": {"name": "Silver", "ar": 107.87},
    "Cd": {"name": "Cadmium", "ar": 112.41},
    "In": {"name": "Indium", "ar": 114.82},
    "Sn": {"name": "Tin", "ar": 118.71},
    "Sb": {"name": "Antimony", "ar": 121.76},
    "Te": {"name": "Tellurium", "ar": 127.60},
    "I": {"name": "Iodine", "ar": 126.90},
    "Xe": {"name": "Xenon", "ar": 131.29},
    "Cs": {"name": "Caesium", "ar": 132.91},
    "Ba": {"name": "Barium", "ar": 137.33},
    "La": {"name": "Lanthanum", "ar": 138.91},
    "Ce": {"name": "Cerium", "ar": 140.12},
    "Pr": {"name": "Praseodymium", "ar": 140.91},
    "Nd": {"name": "Neodymium", "ar": 144.24},
    "Sm": {"name": "Samarium", "ar": 150.36},
    "Eu": {"name": "Europium", "ar": 151.96},
    "Gd": {"name": "Gadolinium", "ar": 157.25},
    "Tb": {"name": "Terbium", "ar": 158.93},
    "Dy": {"name": "Dysprosium", "ar": 162.50},
    "Ho": {"name": "Holmium", "ar": 164.93},
    "Er": {"name": "Erbium", "ar": 167.26},
    "Tm": {"name": "Thulium", "ar": 168.93},
    "Yb": {"name": "Ytterbium", "ar": 173.05},
    "Lu": {"name": "Lutetium", "ar": 174.97},
    "Hf": {"name": "Hafnium", "ar": 178.49},
    "Ta": {"name": "Tantalum", "ar": 180.95},
    "W": {"name": "Tungsten", "ar": 183.84},
    "Re": {"name": "Rhenium", "ar": 186.21},
    "Os": {"name": "Osmium", "ar": 190.23},
    "Ir": {"name": "Iridium", "ar": 192.22},
    "Pt": {"name": "Platinum", "ar": 195.08},
    "Au": {"name": "Gold", "ar": 196.97},
    "Hg": {"name": "Mercury", "ar": 200.59},
    "Tl": {"name": "Thallium", "ar": 204.38},
    "Pb": {"name": "Lead", "ar": 207.2},
    "Bi": {"name": "Bismuth", "ar": 208.98},
    "Th": {"name": "Thorium", "ar": 232.04},
    "U": {"name": "Uranium", "ar": 238.03}
}

# =========================================================
# CSS
# =========================================================

render_html(
    """
<style>

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    font-family: Arial, Helvetica, sans-serif !important;
    background-color: #0B0F19 !important;
    color: #F3F4F6 !important;
}

/* Header tetap ditampilkan agar tombol sidebar Streamlit tidak ikut hilang. */
[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #071A33 0%,
        #0A2342 100%
    ) !important;
    border-right: 1px solid #102E50 !important;

    /* Pastikan sidebar benar-benar dirender dan punya lebar. */
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    min-width: 21rem !important;
    width: 21rem !important;
}

/* Jika state sidebar sebelumnya tersimpan sebagai collapsed,
   jangan biarkan CSS Streamlit membuatnya tidak terlihat. */
[data-testid="stSidebar"][aria-expanded="false"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    min-width: 21rem !important;
    width: 21rem !important;
    transform: none !important;
}

/* Isi sidebar tetap bisa discroll kalau kontennya panjang. */
[data-testid="stSidebar"] > div:first-child {
    width: 100% !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] input {
    background: #102E50 !important;
    color: #FFFFFF !important;
    border: 1px solid #2B4D70 !important;
    border-radius: 7px !important;
}

[data-testid="stSidebar"] label {
    color: #D9E5F2 !important;
    font-size: 12px !important;
}

.main-title {
    font-size: 27px;
    font-weight: 600;
    color: white;
    margin-bottom: 3px;
}

.subtitle {
    font-size: 13px;
    color: #9CA3AF;
    margin-bottom: 20px;
}

.section-title {
    font-size: 16px;
    font-weight: 600;
    color: white;
    margin-top: 8px;
    margin-bottom: 10px;
}

.card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 9px;
    padding: 17px 19px;
    margin-bottom: 13px;
}

.card-blue {
    background: #0F233D;
    border: 1px solid #1D3B66;
    border-radius: 9px;
    padding: 17px 19px;
    margin-bottom: 13px;
}

.card-warning {
    background: #2A2110;
    border: 1px solid #705B24;
    border-radius: 9px;
    padding: 17px 19px;
    margin-bottom: 13px;
}

.card-success {
    background: #10251B;
    border: 1px solid #245B3B;
    border-radius: 9px;
    padding: 17px 19px;
    margin-bottom: 13px;
}

.small-label {
    font-size: 11px;
    color: #9CA3AF;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.result-number {
    font-size: 21px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 5px;
}

.body-text {
    font-size: 13px;
    color: #D1D5DB;
    margin-top: 3px;
}

[data-testid="stMetric"] {
    background: #111827 !important;
    border: 1px solid #1F2937 !important;
    border-radius: 8px;
    padding: 11px 14px;
}

[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    color: #9CA3AF !important;
}

[data-testid="stMetricValue"] {
    font-size: 20px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

.stNumberInput button {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    border: none !important;
}

hr {
    border-top: 1px solid #1F2937 !important;
}

</style>
"""
, unsafe_allow_html=True
)

# =========================================================
# FORMULA PARSER
# =========================================================

def parse_formula(formula):
    formula = formula.strip()
    if not formula:
        return None

    tokens = re.findall(r"[A-Z][a-z]?|\d+|\(|\)", formula)
    if not tokens:
        return None

    if "".join(tokens) != formula:
        return None

    stack = [OrderedDict()]
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Opening parenthesis
        if token == "(":
            stack.append(OrderedDict())

        # Closing parenthesis
        elif token == ")":
            if len(stack) <= 1:
                return None
            
            group = stack.pop()
            multiplier = 1

            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                multiplier = int(tokens[i + 1])
                i += 1

            if multiplier <= 0:
                return None

            for element, amount in group.items():
                stack[-1][element] = stack[-1].get(element, 0) + amount * multiplier

        # Number without element
        elif token.isdigit():
            return None

        # Element
        else:
            if token not in ELEMENTS_DATA:
                return None
            
            amount = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                amount = int(tokens[i + 1])
                i += 1

                if amount <= 0:
                    return None

            stack[-1][token] = stack[-1].get(token, 0) + amount

        i += 1

    if len(stack) != 1:
        return None

    return dict(stack[0])

# =========================================================
# FORMULA FORMATTERS
# =========================================================

def format_formula_html(counts):
    parts = []
    for element, qty in counts.items():
        qty = float(qty)
        if abs(qty - 1) < 1e-12:
            parts.append(element)
        else:
            q = str(int(qty)) if qty.is_integer() else f"{qty:g}"
            parts.append(f"{element}<sub>{q}</sub>")
    return "".join(parts)


def format_formula_plain(counts):
    parts = []
    for element, qty in counts.items():
        qty = float(qty)
        if abs(qty - 1) < 1e-12:
            parts.append(element)
        else:
            q = str(int(qty)) if qty.is_integer() else f"{qty:g}"
            parts.append(f"{element}{q}")
    return "".join(parts)

# =========================================================
# CALCULATE MR
# =========================================================

def calculate_mr(parsed):
    return sum(amount * ELEMENTS_DATA[element]["ar"] for element, amount in parsed.items())

# =========================================================
# AI COMPOUND ADVISOR
# =========================================================

def _get_openai_api_key():
    """Read the API key from Streamlit secrets or environment variables."""
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("OPENAI_API_KEY", "")


def ai_compound_advisor(target_elements, target_formula, max_results=8):
    """
    Ask an AI model for precursor/compound hints.

    The AI is used only for suggestions. All formula validation and numerical
    calculations remain deterministic in this application.
    """
    api_key = _get_openai_api_key()
    if not api_key:
        return {
            "error": (
                "OPENAI_API_KEY belum ditemukan. Tambahkan API key ke "
                "Streamlit secrets atau environment variable."
            )
        }

    element_text = ", ".join(
        f"{el} ({ELEMENTS_DATA[el]['name']})"
        for el in target_elements
        if el in ELEMENTS_DATA
    )

    prompt = f"""
You are a chemistry/materials precursor advisor inside an alloy stoichiometry
calculator.

Target composition: {target_formula}
Target elements: {element_text}

Suggest up to {max_results} plausible precursor compounds that could supply
one or more of the target elements.

Prioritize:
1. elemental precursors,
2. simple binary/ternary inorganic compounds,
3. common oxides, sulfides, selenides, tellurides, halides, carbonates,
   nitrates, or other practical inorganic precursor families when chemically
   reasonable.

Avoid inventing exotic compounds. Do not recommend compounds that contain
target-unrelated elements unless they are a clearly useful precursor and
explain the foreign element.

Return ONLY valid JSON in this exact shape:
{{
  "hints": [
    {{
      "formula": "Bi2O3",
      "name": "Bismuth(III) oxide",
      "role": "Bi source",
      "reason": "Short reason",
      "confidence": "high"
    }}
  ]
}}

Do not calculate masses. Do not claim that a reaction is experimentally
validated. These are candidate hints for the user to verify.
"""

    endpoint = "https://api.openai.com/v1/responses"

    payload = {
        "model": "gpt-5.6-luna",
        "input": prompt,
        "max_output_tokens": 1200,
    }

    try:
        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()

        # Responses API normally exposes the generated text through output.
        output_text = data.get("output_text", "")
        if not output_text:
            parts = []
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        parts.append(content.get("text", ""))
            output_text = "".join(parts)

        if not output_text:
            return {"error": "AI tidak mengembalikan teks hasil."}

        # Handle accidental markdown code fences.
        cleaned = output_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        result = json.loads(cleaned)
        hints = result.get("hints", [])

        validated = []
        for hint in hints:
            formula = str(hint.get("formula", "")).strip()
            parsed = parse_formula(formula)
            if parsed is None:
                continue

            # Keep suggestions relevant to the target.
            shared = set(parsed).intersection(set(target_elements))
            if not shared:
                continue

            validated.append({
                "formula": formula,
                "name": str(hint.get("name", formula)),
                "role": str(hint.get("role", "Potential precursor")),
                "reason": str(hint.get("reason", "")),
                "confidence": str(hint.get("confidence", "medium")),
                "shared": ", ".join(sorted(shared)),
            })

        return {"hints": validated[:max_results]}

    except requests.RequestException as exc:
        return {"error": f"Gagal menghubungi AI: {exc}"}
    except json.JSONDecodeError:
        return {"error": "Respons AI bukan JSON yang valid."}
    except Exception as exc:
        return {"error": f"AI advisor error: {exc}"}


# =========================================================
# LIBRARY RECOMMENDATION
# =========================================================

def recommend_compounds(target_elements):
    recommendations = []
    target_set = set(target_elements)

    for formula, name in COMPOUND_LIBRARY.items():
        parsed = parse_formula(formula)
        if parsed is None:
            continue

        compound_set = set(parsed.keys())
        shared = target_set.intersection(compound_set)

        if not shared:
            continue

        coverage = len(shared) / len(target_set)
        foreign = len(compound_set - target_set)
        score = (coverage * 100 - foreign * 15)

        recommendations.append({
            "formula": formula,
            "name": name,
            "coverage": coverage,
            "foreign": foreign,
            "score": score,
            "shared": shared
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:8]

# =========================================================
# SESSION STATE
# =========================================================

if "precursor_count" not in st.session_state:
    st.session_state.precursor_count = 1

if "target_count" not in st.session_state:
    st.session_state.target_count = 2

if "precursor_0_formula" not in st.session_state:
    st.session_state.precursor_0_formula = "K2Te"

if "precursor_0_coeff" not in st.session_state:
    st.session_state.precursor_0_coeff = 1.0

default_targets = [("Te", 1.0), ("K", 2.0)]

for i in range(10):
    if f"target_{i}_element" not in st.session_state:
        if i < len(default_targets):
            st.session_state[f"target_{i}_element"] = default_targets[i][0]
        else:
            st.session_state[f"target_{i}_element"] = "Te"

    if f"target_{i}_coeff" not in st.session_state:
        if i < len(default_targets):
            st.session_state[f"target_{i}_coeff"] = default_targets[i][1]
        else:
            st.session_state[f"target_{i}_coeff"] = 1.0

# =========================================================
# CALLBACKS
# =========================================================

def add_precursor():
    if st.session_state.precursor_count < 6:
        new_i = st.session_state.precursor_count
        st.session_state[f"precursor_{new_i}_formula"] = "K2Te"
        st.session_state[f"precursor_{new_i}_coeff"] = 1.0
        st.session_state.precursor_count += 1

def remove_precursor():
    if st.session_state.precursor_count > 1:
        st.session_state.precursor_count -= 1

def add_target():
    if st.session_state.target_count < 6:
        new_i = st.session_state.target_count
        st.session_state[f"target_{new_i}_element"] = "Te"
        st.session_state[f"target_{new_i}_coeff"] = 1.0
        st.session_state.target_count += 1

def remove_target():
    if st.session_state.target_count > 1:
        st.session_state.target_count -= 1
def use_library_precursor(formula):
    """Masukkan senyawa library langsung ke input precursor."""
    
    # Cari slot precursor kosong terlebih dahulu
    for i in range(st.session_state.precursor_count):
        key = f"precursor_{i}_formula"
        current = st.session_state.get(key, "").strip()

        if not current:
            st.session_state[key] = formula
            st.session_state[f"precursor_{i}_coeff"] = 1.0
            return

    # Kalau semua slot terisi, tambah slot baru
    if st.session_state.precursor_count < 6:
        new_i = st.session_state.precursor_count

        st.session_state[f"precursor_{new_i}_formula"] = formula
        st.session_state[f"precursor_{new_i}_coeff"] = 1.0

        st.session_state.precursor_count += 1
    else:
        st.session_state["library_precursor_message"] = (
            "Maksimal 6 precursor sudah digunakan."
        )
# =========================================================
# SIDEBAR
# =========================================================

render_sidebar(
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
    """
, unsafe_allow_html=True)

# =========================================================
# PRECURSOR INPUT
# =========================================================

render_sidebar("**PRECURSOR A (SENYAWA)**")

render_sidebar(
    """
    <div style="
        font-size:11px;
        color:#9CA3AF;
        margin-bottom:10px;
    ">
        Tambahkan precursor dari library atau masukkan formula sendiri.
    </div>
    """
, unsafe_allow_html=True)

precursors = []

for i in range(st.session_state.precursor_count):
    render_sidebar(f"### Precursor {i + 1}")

    formula = st.sidebar.text_input(
        "Formula",
        key=f"precursor_{i}_formula",
        placeholder="Contoh: BaCO3"
    ).strip()

    coefficient = st.sidebar.number_input(
        "Koefisien",
        min_value=0.0001,
        step=0.1,
        format="%.4f",
        key=f"precursor_{i}_coeff"
    )

    precursors.append({
        "index": i,
        "formula": formula,
        "coefficient": coefficient
    })

pc1, pc2 = st.sidebar.columns(2)

pc1.button(
    "➕ Precursor",
    key="add_precursor_button",
    on_click=add_precursor,
    use_container_width=True
)

pc2.button(
    "➖ Kurang",
    key="remove_precursor_button",
    on_click=remove_precursor,
    disabled=(st.session_state.precursor_count <= 1),
    use_container_width=True
)

render_sidebar("---")

# =========================================================
# TARGET INPUT
# =========================================================

render_sidebar("**TARGET B (KOMPOSISI ALLOY)**")

render_sidebar(
    """
    <div style="
        font-size:11px;
        color:#9CA3AF;
        margin-bottom:10px;
    ">
        Tambahkan atau kurangi unsur target.
    </div>
    """
, unsafe_allow_html=True)

target_elements_dict = OrderedDict()

for i in range(st.session_state.target_count):
    col_e, col_q = st.sidebar.columns([1.1, 0.9])

    element = col_e.selectbox(
        f"Unsur {i + 1}",
        options=list(ELEMENTS_DATA.keys()),
        key=f"target_{i}_element"
    )

    coefficient = col_q.number_input(
        f"Koef {i + 1}",
        min_value=0.0001,
        step=0.1,
        format="%.4f",
        key=f"target_{i}_coeff"
    )

    target_elements_dict[element] = target_elements_dict.get(element, 0) + coefficient


tc1, tc2 = st.sidebar.columns(2)

tc1.button(
    "➕ Unsur Target",
    key="add_target_button",
    on_click=add_target,
    use_container_width=True
)

tc2.button(
    "➖ Kurang",
    key="remove_target_button",
    on_click=remove_target,
    disabled=(st.session_state.target_count <= 1),
    use_container_width=True
)

render_sidebar("---")

# =========================================================
# TARGET MASS
# =========================================================

render_sidebar("**TARGET MASS**")

massa_target = st.sidebar.number_input(
    "Mass (g)",
    min_value=0.01,
    value=1000.0,
    step=10.0,
    format="%.2f",
    key="target_mass"
)

# =========================================================
# VALIDATE PRECURSORS
# =========================================================

valid_precursors = []
invalid_precursors = []

for p in precursors:
    formula = p["formula"]
    parsed = parse_formula(formula)

    if parsed is None:
        invalid_precursors.append(p)
    else:
        mr = calculate_mr(parsed)
        valid_precursors.append({
            **p,
            "parsed": parsed,
            "mr": mr
        })

# =========================================================
# TARGET DATA
# =========================================================

target_elements = list(target_elements_dict.keys())
mr_target = calculate_mr(target_elements_dict)

target_wt = {
    element: (qty * ELEMENTS_DATA[element]["ar"] / mr_target) * 100
    for element, qty in target_elements_dict.items()
}

mass_demand = {
    element: (wt / 100) * massa_target
    for element, wt in target_wt.items()
}

# =========================================================
# MAIN TITLE
# =========================================================

render_html(
    """
    <div class="main-title">
        ALLOY PREPARATION SIMULATION
    </div>
    <div class="subtitle">
        Stoichiometric Mass Balance with Custom Precursor & Target
    </div>
    """
, unsafe_allow_html=True)

# =========================================================
# INVALID PRECURSOR WARNING
# =========================================================

if invalid_precursors:
    names = ", ".join([p["formula"] if p["formula"] else "(kosong)" for p in invalid_precursors])
    st.error(
        f"Formula precursor berikut tidak valid: {names}. "
        "Gunakan format seperti BaCO3, K2Te, Al2O3, atau Ca(OH)2."
    )

# =========================================================
# TARGET FORMULA
# =========================================================

target_html = format_formula_html(target_elements_dict)

# =========================================================
# FORMULA CARDS
# =========================================================

render_html(
    """
    <div class="section-title">
        Input Summary
    </div>
    """
, unsafe_allow_html=True)

summary_cols = st.columns(2)

with summary_cols[0]:
    render_html(
        f"""
        <div class="card">
            <div class="small-label">
                Precursor
            </div>
            <div class="body-text">
                {len(valid_precursors)} precursor aktif
            </div>
        </div>
        """
    , unsafe_allow_html=True)

with summary_cols[1]:
    render_html(
        f"""
        <div class="card-blue">
            <div class="small-label">
                Target Alloy
            </div>
            <div class="result-number">
                {target_html}
            </div>
            <div class="body-text">
                Mr = {mr_target:.4f} g/mol
            </div>
        </div>
        """
    , unsafe_allow_html=True)

# =========================================================
# AI COMPOUND ADVISOR
# =========================================================

def _get_openai_api_key():
    """Read the API key from Streamlit secrets or environment variables."""
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("OPENAI_API_KEY", "")


def ai_compound_advisor(target_elements, target_formula, max_results=8):
    """
    Ask an AI model for precursor/compound hints.

    The AI is used only for suggestions. All formula validation and numerical
    calculations remain deterministic in this application.
    """
    api_key = _get_openai_api_key()
    if not api_key:
        return {
            "error": (
                "OPENAI_API_KEY belum ditemukan. Tambahkan API key ke "
                "Streamlit secrets atau environment variable."
            )
        }

    element_text = ", ".join(
        f"{el} ({ELEMENTS_DATA[el]['name']})"
        for el in target_elements
        if el in ELEMENTS_DATA
    )

    prompt = f"""
You are a chemistry/materials precursor advisor inside an alloy stoichiometry
calculator.

Target composition: {target_formula}
Target elements: {element_text}

Suggest up to {max_results} plausible precursor compounds that could supply
one or more of the target elements.

Prioritize:
1. elemental precursors,
2. simple binary/ternary inorganic compounds,
3. common oxides, sulfides, selenides, tellurides, halides, carbonates,
   nitrates, or other practical inorganic precursor families when chemically
   reasonable.

Avoid inventing exotic compounds. Do not recommend compounds that contain
target-unrelated elements unless they are a clearly useful precursor and
explain the foreign element.

Return ONLY valid JSON in this exact shape:
{{
  "hints": [
    {{
      "formula": "Bi2O3",
      "name": "Bismuth(III) oxide",
      "role": "Bi source",
      "reason": "Short reason",
      "confidence": "high"
    }}
  ]
}}

Do not calculate masses. Do not claim that a reaction is experimentally
validated. These are candidate hints for the user to verify.
"""

    endpoint = "https://api.openai.com/v1/responses"

    payload = {
        "model": "gpt-5.6-luna",
        "input": prompt,
        "max_output_tokens": 1200,
    }

    try:
        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        data = response.json()

        # Responses API normally exposes the generated text through output.
        output_text = data.get("output_text", "")
        if not output_text:
            parts = []
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        parts.append(content.get("text", ""))
            output_text = "".join(parts)

        if not output_text:
            return {"error": "AI tidak mengembalikan teks hasil."}

        # Handle accidental markdown code fences.
        cleaned = output_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        result = json.loads(cleaned)
        hints = result.get("hints", [])

        validated = []
        for hint in hints:
            formula = str(hint.get("formula", "")).strip()
            parsed = parse_formula(formula)
            if parsed is None:
                continue

            # Keep suggestions relevant to the target.
            shared = set(parsed).intersection(set(target_elements))
            if not shared:
                continue

            validated.append({
                "formula": formula,
                "name": str(hint.get("name", formula)),
                "role": str(hint.get("role", "Potential precursor")),
                "reason": str(hint.get("reason", "")),
                "confidence": str(hint.get("confidence", "medium")),
                "shared": ", ".join(sorted(shared)),
            })

        return {"hints": validated[:max_results]}

    except requests.RequestException as exc:
        return {"error": f"Gagal menghubungi AI: {exc}"}
    except json.JSONDecodeError:
        return {"error": "Respons AI bukan JSON yang valid."}
    except Exception as exc:
        return {"error": f"AI advisor error: {exc}"}


# =========================================================
# LIBRARY RECOMMENDATION
# =========================================================

render_html(
    """
    <div class="section-title">
        Saran Precursor dari Library
    </div>
    """
, unsafe_allow_html=True)

recommendations = recommend_compounds(target_elements)

if recommendations:
    render_html(
        """
        <div class="card-blue">
            <div class="small-label">
                RECOMMENDATION ENGINE
            </div>
            <div class="body-text">
                Saran di bawah berasal dari library senyawa dan dipilih berdasarkan unsur target yang dapat disediakan oleh masing-masing senyawa.
            </div>
        </div>
        """
    , unsafe_allow_html=True)

    rec_df = pd.DataFrame([
    {
        "Senyawa": r["formula"],
        "Nama": r["name"],
        "Unsur Target": ", ".join(sorted(r["shared"])),
        "Coverage": f"{r['coverage'] * 100:.0f}%"
    }
    for r in recommendations
])

# Header tabel
header_cols = st.columns([1.2, 2.5, 1.5, 1.0, 1.0])

header_cols[0].markdown("**Senyawa**")
header_cols[1].markdown("**Nama**")
header_cols[2].markdown("**Unsur Target**")
header_cols[3].markdown("**Coverage**")
header_cols[4].markdown("**Aksi**")

# Isi tabel
for idx, r in enumerate(recommendations):

    cols = st.columns([1.2, 2.5, 1.5, 1.0, 1.0])

    cols[0].write(r["formula"])
    cols[1].write(r["name"])
    cols[2].write(", ".join(sorted(r["shared"])))
    cols[3].write(f"{r['coverage'] * 100:.0f}%")

    cols[4].button(
        "＋ Gunakan",
        key=f"use_library_{idx}",
        on_click=use_library_precursor,
        args=(r["formula"],),
        use_container_width=True
    )
else:
    st.info("Belum ada senyawa library yang cocok dengan unsur target.")

# =========================================================
# AI COMPOUND ADVISOR UI
# =========================================================

render_html(
    """
    <div class="section-title">
        🤖 AI Compound Advisor
    </div>
    """
    , unsafe_allow_html=True
)

render_html(
    """
    <div class="card-blue">
        <div class="small-label">
            AI HINT
        </div>
        <div class="body-text">
            AI dapat menyarankan kandidat precursor berdasarkan unsur target.
            Hasil AI adalah <b>hint</b>, bukan validasi eksperimen; perhitungan
            massa tetap dilakukan oleh calculator.
        </div>
    </div>
    """
    , unsafe_allow_html=True
)

if st.button(
    "🤖 Cari Hint Senyawa dengan AI",
    key="ai_compound_button",
    use_container_width=True,
):
    with st.spinner("AI sedang mencari kandidat precursor..."):
        ai_result = ai_compound_advisor(
            target_elements=target_elements,
            target_formula=format_formula_plain(target_elements_dict),
            max_results=8,
        )
    st.session_state["ai_compound_result"] = ai_result

ai_result = st.session_state.get("ai_compound_result")

if ai_result:
    if ai_result.get("error"):
        st.warning(ai_result["error"])
        st.caption(
            "Untuk mengaktifkan AI: set OPENAI_API_KEY pada Streamlit secrets "
            "atau environment variable."
        )
    else:
        hints = ai_result.get("hints", [])
        if hints:
            ai_df = pd.DataFrame([
                {
                    "Senyawa": h["formula"],
                    "Nama": h["name"],
                    "Peran": h["role"],
                    "Unsur Target": h["shared"],
                    "Confidence": h["confidence"],
                    "Alasan": h["reason"],
                }
                for h in hints
            ])
            st.dataframe(
                ai_df,
                hide_index=True,
                use_container_width=True,
            )

            for h in hints:
                render_html(
                    f"""
                    <div class="card">
                        <div class="small-label">{h["role"]}</div>
                        <div class="result-number">{format_formula_html(parse_formula(h["formula"]))}</div>
                        <div class="body-text">{h["name"]}</div>
                        <div class="body-text">{h["reason"]}</div>
                    </div>
                    """
                    , unsafe_allow_html=True
                )
        else:
            st.info("AI tidak menemukan kandidat yang lolos validasi formula.")


# =========================================================
# PRECURSOR CARDS
# =========================================================

render_html(
    """
    <div class="section-title">
        Precursor yang Digunakan
    </div>
    """
, unsafe_allow_html=True)

if valid_precursors:
    precursor_cols = st.columns(min(3, len(valid_precursors)))

    for idx, p in enumerate(valid_precursors):
        parsed = p["parsed"]
        formula_html = format_formula_html(parsed)

        with precursor_cols[idx % len(precursor_cols)]:
            render_html(
                f"""
                <div class="card">
                    <div class="small-label">
                        PRECURSOR {p["index"] + 1}
                    </div>
                    <div class="result-number">
                        {formula_html}
                    </div>
                    <div class="body-text">
                        Mr = {p["mr"]:.4f} g/mol
                    </div>
                    <div class="body-text">
                        Koefisien = {p["coefficient"]:.4f}
                    </div>
                </div>
                """
            , unsafe_allow_html=True)
else:
    st.warning("Masukkan minimal satu precursor yang valid.")

# =========================================================
# TARGET COMPOSITION
# =========================================================

render_html(
    """
    <div class="section-title">
        Analisis Komposisi Target
    </div>
    """
, unsafe_allow_html=True)


comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    with st.container(border=True):
        render_html(
            f"""
            <div class="small-label">
                TARGET
            </div>
            <div class="result-number">
                {target_html}
            </div>
            <div class="body-text">
                Mr = {mr_target:.4f} g/mol
            </div>
            """
        , unsafe_allow_html=True)

        render_html("<hr>", unsafe_allow_html=True)

        for element, wt in target_wt.items():
            render_html(
                f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:6px 0;
                ">
                    <span style="color:#D1D5DB;">
                        {element} ({ELEMENTS_DATA[element]["name"]})
                    </span>
                    <span style="
                        color:white;
                        font-weight:600;
                    ">
                        {wt:.2f} wt%
                    </span>
                </div>
                """
            , unsafe_allow_html=True)


with comp_col2:
    with st.container(border=True):
        render_html(
            """
            <div class="small-label">
                MASS DEMAND
            </div>
            """
        , unsafe_allow_html=True)

        for element, mass in mass_demand.items():
            render_html(
                f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:6px 0;
                ">
                    <span style="color:#D1D5DB;">
                        {element}
                    </span>
                    <span style="
                        color:white;
                        font-weight:600;
                    ">
                        {mass:.2f} g
                    </span>
                </div>
                """
            , unsafe_allow_html=True)

# =========================================================
# MASS BALANCE
# =========================================================

render_html(
    """
    <div class="section-title">
        Mass Balance
    </div>
    """
, unsafe_allow_html=True)

material_rows = []
remaining_demand = dict(mass_demand)

# =========================================================
# PROCESS EACH PRECURSOR
# =========================================================

for p in valid_precursors:
    parsed = p["parsed"]
    mr = p["mr"]

    target_shared = set(parsed.keys()).intersection(set(target_elements))
    foreign_elements = set(parsed.keys()) - set(target_elements)

    if foreign_elements:
        material_rows.append({
            "name": p["formula"],
            "display": p["formula"],
            "mass": 0.0,
            "type": "Precursor",
            "usable": False,
            "reason": "Mengandung unsur di luar target"
        })
        continue

    if not target_shared:
        material_rows.append({
            "name": p["formula"],
            "display": p["formula"],
            "mass": 0.0,
            "type": "Precursor",
            "usable": False,
            "reason": "Tidak mengandung unsur target"
        })
        continue

    possible_masses = []

    for element in target_shared:
        precursor_fraction = (parsed[element] * ELEMENTS_DATA[element]["ar"] / mr)
        if precursor_fraction > 0:
            possible_mass = (remaining_demand[element] / precursor_fraction)
            possible_masses.append(possible_mass)

    if possible_masses:
        mass_used = min(possible_masses)
    else:
        mass_used = 0.0

    mass_used *= p["coefficient"]

    for element in target_shared:
        fraction = (parsed[element] * ELEMENTS_DATA[element]["ar"] / mr)
        supplied = (mass_used * fraction)
        remaining_demand[element] = max(0.0, remaining_demand[element] - supplied)

    material_rows.append({
        "name": p["formula"],
        "display": p["formula"],
        "mass": mass_used,
        "type": "Precursor",
        "usable": True,
        "reason": ""
    })

# =========================================================
# PURE ELEMENT ADDITIONS
# =========================================================

for element, remaining in remaining_demand.items():
    if remaining > 0.000001:
        material_rows.append({
            "name": f"Pure {element}",
            "display": f"Pure {element}",
            "mass": remaining,
            "type": "Pure Element",
            "usable": True,
            "reason": ""
        })

# =========================================================
# FILTER MATERIALS
# =========================================================

active_materials = [row for row in material_rows if row["mass"] > 0.000001]
total_mass = sum(row["mass"] for row in active_materials)

# =========================================================
# MASS METRICS
# =========================================================

if active_materials:
    metric_cols = st.columns(len(active_materials) + 1)
    for i, row in enumerate(active_materials):
        metric_cols[i].metric(row["name"], f'{row["mass"]:.2f} g')
    metric_cols[-1].metric("Total Mass", f"{total_mass:.2f} g")
else:
    st.info("Belum ada material yang dapat digunakan.")

# =========================================================
# COMPATIBILITY WARNING
# =========================================================

unused_precursors = [row for row in material_rows if (row["type"] == "Precursor" and not row["usable"])]

if unused_precursors:
    render_html(
        """
        <div class="card-warning">
            <div class="small-label">
                CATATAN PRECURSOR
            </div>
            <div class="body-text">
        """
    , unsafe_allow_html=True)

    for row in unused_precursors:
        render_html(
            f"""
            • <b>{row["name"]}</b> tidak digunakan otomatis karena {row["reason"]}.<br>
            """
        , unsafe_allow_html=True)

    render_html(
        """
            </div>
        </div>
        """
    , unsafe_allow_html=True)

# =========================================================
# VISUALIZATION
# =========================================================

st.divider()

left, right = st.columns([1.618, 1])

# =========================================================
# LEFT — MASS COMPOSITION
# =========================================================

with left:
    render_html(
        """
        <div class="section-title">
            Komposisi Berat Precursor
        </div>
        """
    , unsafe_allow_html=True)

    for p in valid_precursors:
        parsed = p["parsed"]
        formula_html = format_formula_html(parsed)

        render_html(
            f"""
            <div class="card">
                <div class="small-label">
                    {p["formula"]}
                </div>
                <div class="result-number">
                    {formula_html}
                </div>
                <div class="body-text">
                    Mr = {p["mr"]:.4f} g/mol
                </div>
                <div class="body-text">
                    Koefisien = {p["coefficient"]:.4f}
                </div>
            </div>
            """
        , unsafe_allow_html=True)

        wt_precursor = {
            e: (qty * ELEMENTS_DATA[e]["ar"] / p["mr"]) * 100
            for e, qty in parsed.items()
        }

        with st.container(border=True):
            for e, wt in wt_precursor.items():
                render_html(
                    f"""
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        padding:4px 0;
                    ">
                        <span>
                            {e}
                        </span>
                        <span>
                            <b>{wt:.2f}%</b>
                        </span>
                    </div>
                    """
                , unsafe_allow_html=True)

# =========================================================
# RIGHT — CHART
# =========================================================

with right:
    render_html(
        """
        <div class="section-title">
            Visualisasi Batch Penimbangan
        </div>
        """
    , unsafe_allow_html=True)

    chart_names = [row["name"] for row in active_materials]
    chart_masses = [row["mass"] for row in active_materials]

    if total_mass > 0:
        chart_percent = [(mass / total_mass * 100) for mass in chart_masses]
    else:
        chart_percent = [0 for _ in chart_masses]

    chart_data = pd.DataFrame({
        "Material": chart_names,
        "Mass": chart_masses,
        "Batch": chart_percent
    })

    if not chart_data.empty:
        chart = (
            alt.Chart(chart_data)
            .mark_bar(cornerRadiusEnd=5)
            .encode(
                y=alt.Y(
                    "Material:N",
                    title=None,
                    sort="-x",
                    axis=alt.Axis(
                        labelColor="#E5E7EB",
                        labelFontSize=11,
                        labelLimit=160
                    )
                ),
                x=alt.X(
                    "Mass:Q",
                    title="Mass (g)",
                    axis=alt.Axis(
                        labelColor="#E5E7EB",
                        titleColor="#E5E7EB",
                        gridColor="#1F2937"
                    )
                ),
                tooltip=[
                    alt.Tooltip("Material:N", title="Material"),
                    alt.Tooltip("Mass:Q", title="Mass (g)", format=".2f"),
                    alt.Tooltip("Batch:Q", title="Kontribusi (%)", format=".2f")
                ]
            )
            .properties(
                background="transparent",
                height=max(180, len(chart_data) * 48)
            )
            .configure_view(stroke=None)
        )

        st.altair_chart(chart, use_container_width=True)

        summary_df = pd.DataFrame({
            "Komponen": chart_names,
            "Massa (g)": chart_masses,
            "Batch (%)": chart_percent
        })

        total_row = pd.DataFrame({
            "Komponen": ["TOTAL"],
            "Massa (g)": [total_mass],
            "Batch (%)": [100.0]
        })

        summary_df = pd.concat([summary_df, total_row], ignore_index=True)

        st.dataframe(
            summary_df.style.format({
                "Massa (g)": "{:.2f}",
                "Batch (%)": "{:.2f}%"
            }),
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("Belum ada massa yang dapat divisualisasikan.")

# =========================================================
# FINAL PREPARATION FORMULA
# =========================================================

render_html(
    """
    <div class="section-title">
        Formula Penimbangan Akhir
    </div>
    """
, unsafe_allow_html=True)

if active_materials:
    preparation_parts = [f'{row["mass"]:.2f} g {row["name"]}' for row in active_materials]
    preparation_text = " + ".join(preparation_parts)

    render_html(
        f"""
        <div style="
            background:#0F233D;
            border:1px solid #1D3B66;
            border-radius:9px;
            padding:18px 20px;
        ">
            <div style="
                font-size:11px;
                color:#93C5FD;
                text-transform:uppercase;
                letter-spacing:0.5px;
                margin-bottom:8px;
            ">
                Preparation Formula
            </div>
            <div style="
                font-size:16px;
                color:white;
                line-height:1.6;
                font-weight:600;
            ">
                {preparation_text}
            </div>
            <div style="
                margin-top:10px;
                font-size:12px;
                color:#9CA3AF;
            ">
                Total batch = {total_mass:.2f} g
            </div>
        </div>
        """
    , unsafe_allow_html=True)
else:
    st.warning("Formula penimbangan belum dapat dibuat.")

# =========================================================
# TARGET DEMAND TABLE
# =========================================================

render_html(
    """
    <div class="section-title">
        Target Demand Detail
    </div>
    """
, unsafe_allow_html=True)

demand_rows = []

for element in target_elements:
    demand_rows.append({
        "Unsur": element,
        "Koefisien": target_elements_dict[element],
        "Ar (g/mol)": ELEMENTS_DATA[element]["ar"],
        "wt (%)": target_wt[element],
        "Demand (g)": mass_demand[element]
    })

demand_df = pd.DataFrame(demand_rows)

st.dataframe(
    demand_df.style.format({
        "Koefisien": "{:.4f}",
        "Ar (g/mol)": "{:.3f}",
        "wt (%)": "{:.2f}%",
        "Demand (g)": "{:.2f}"
    }),
    hide_index=True,
    use_container_width=True
)

# =========================================================
# FOOTER / THEORY
# =========================================================

render_html(
    """
    <div style="
        margin-top:25px;
        padding:15px 18px;
        border-top:1px solid #1F2937;
        color:#6B7280;
        font-size:11px;
        line-height:1.6;
    ">
        <b>Basis perhitungan:</b>
        Hukum Kekekalan Massa dan Hukum Perbandingan Tetap.
        Komposisi massa dihitung dari massa atom relatif (Ar) dan stoikiometri formula kimia.
    </div>
    """
, unsafe_allow_html=True)