import json
import streamlit as st

# =========================================================
# MUST BE FIRST STREAMLIT CALL
# =========================================================
st.set_page_config(page_title="ChangiLink AI - Logic Checker", layout="wide")

# =========================================================
# THEME / CSS (after set_page_config)
# =========================================================
st.markdown(
    """
<style>
/* ---- Global readable text ---- */
html, body, .stApp, p, span, label, div, li, small, h2, h3, h4 {
  color: #F8FAFC !important;
}

/* ---- Background ---- */
.stApp{
  background: radial-gradient(1200px 600px at 20% 0%, #122449 0%, #0B1220 55%, #070B14 100%);
}

/* ---- Title ---- */
h1{
  color: #22D3EE !important;
  font-weight: 800 !important;
  letter-spacing: .2px;
}

[data-testid="stCaptionContainer"]{
  color: rgba(248,250,252,0.82) !important;
}

/* ---- Card-like blocks ---- */
[data-testid="stVerticalBlockBorderWrapper"]{
  background: rgba(15, 27, 51, 0.88) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
}

/* ---- Inputs ---- */
.stTextArea textarea,
.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div{
  background: rgba(9, 14, 26, 0.95) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  color: #FFFFFF !important;
  border-radius: 10px !important;
}

textarea::placeholder,
input::placeholder{
  color: rgba(255,255,255,0.45) !important;
}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"]{
  gap: 0.75rem;
}

.stTabs [data-baseweb="tab"]{
  background: rgba(15, 27, 51, 0.75) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 12px !important;
  padding: 10px 18px !important;
  color: rgba(248,250,252,0.85) !important;
  font-weight: 700 !important;
}

.stTabs [aria-selected="true"]{
  color: #22D3EE !important;
  border-color: rgba(34,211,238,0.65) !important;
  box-shadow: 0 0 0 3px rgba(34,211,238,0.12) !important;
}

/* ---- Buttons ---- */
.stButton button{
  background: linear-gradient(180deg, rgba(34,211,238,0.20), rgba(34,211,238,0.08)) !important;
  border: 1px solid rgba(34,211,238,0.55) !important;
  color: #FFFFFF !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
}

.stButton button:hover{
  border-color: rgba(34,211,238,0.80) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25) !important;
}

/* ---- Checkbox text ---- */
[data-testid="stCheckbox"] span{
  color: #F9FAFB !important;
}

/* ---- Hide Streamlit chrome (optional) ---- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# Helpers (parsers + logger)
# =========================================================
def parse_csv_set(text: str) -> set[str]:
    text = (text or "").strip()
    if not text:
        return set()
    raw = text.replace("\n", ",")
    items = [x.strip() for x in raw.split(",") if x.strip()]
    return set(items)

def parse_edges(text: str) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    text = (text or "").strip()
    if not text:
        return edges

    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    for ln in lines:
        cleaned = ln.replace("->", ",").replace("—", ",").replace("–", ",")
        parts = [p.strip() for p in cleaned.split(",") if p.strip()]
        if len(parts) != 2:
            raise ValueError(f"Bad edge format: '{ln}'. Use 'A,B' or 'A -> B'.")
        edges.add((parts[0], parts[1]))
    return edges

def init_output():
    if "output" not in st.session_state:
        st.session_state.output = []

def log(msg: str, kind: str = "muted"):
    # kind: title | ok | bad | warn | muted
    init_output()
    st.session_state.output.append((kind, msg))

def clear_output():
    st.session_state.output = []

def render_output():
    init_output()
    st.markdown("### Output")
    with st.container(border=True):
        if not st.session_state.output:
            st.caption("No output yet. Load a preset or click Run Both.")
            return

        for kind, msg in st.session_state.output:
            if kind == "title":
                st.markdown(f"**{msg}**")
            elif kind == "ok":
                st.success(msg)
            elif kind == "bad":
                st.error(msg)
            elif kind == "warn":
                st.warning(msg)
            else:
                st.write(msg)

# =========================================================
# Presets
# =========================================================
PRESETS = {
    "scenario1": {
        "mode": "today", "status": "normal", "integration": False,
        "exists": "TanahMerah\nExpo\nChangiAirport",
        "openStations": "TanahMerah\nExpo\nChangiAirport",
        "openEdges": "TanahMerah,Expo\nExpo,ChangiAirport",
        "recommendedRoutes": "",
        "servedTEL": "",
        "routeName": "EWL_AirportBranch",
        "routeStations": "TanahMerah\nExpo\nChangiAirport",
    },
    "scenario2": {
        "mode": "today", "status": "normal", "integration": False,
        "exists": "SungeiBedok\nTanahMerah\nExpo\nChangiAirport",
        "openStations": "SungeiBedok\nTanahMerah\nExpo\nChangiAirport",
        "openEdges": "TanahMerah,Expo\nExpo,ChangiAirport",
        "recommendedRoutes": "",
        "servedTEL": "",
        "routeName": "Future_TEL_To_T5",
        "routeStations": "SungeiBedok\nT5\nTanahMerah",
    },
    "scenario3": {
        "mode": "today", "status": "normal", "integration": False,
        "exists": "TanahMerah\nExpo\nChangiAirport",
        "openStations": "TanahMerah\nExpo\nChangiAirport",
        "openEdges": "TanahMerah,Expo\nExpo,ChangiAirport",
        "recommendedRoutes": "",
        "servedTEL": "",
        "routeName": "Direct_TanahMerah_To_Changi",
        "routeStations": "TanahMerah\nChangiAirport",
    },
    "scenario4": {
        "mode": "future", "status": "normal", "integration": False,
        "exists": "SungeiBedok\nT5\nTanahMerah",
        "openStations": "SungeiBedok\nT5\nTanahMerah",
        "openEdges": "SungeiBedok,T5\nT5,TanahMerah",
        "recommendedRoutes": "",
        "servedTEL": "",
        "routeName": "Future_TEL_To_T5",
        "routeStations": "SungeiBedok\nT5\nTanahMerah",
    },
    "scenario5": {
        "mode": "future", "status": "delay", "integration": True,
        "exists": "TanahMerah\nExpo\nChangiAirport",
        "openStations": "TanahMerah\nExpo\nChangiAirport",
        "openEdges": "TanahMerah,Expo\nExpo,ChangiAirport",
        "recommendedRoutes": "EWL_AirportBranch",
        "servedTEL": "",
        "routeName": "EWL_AirportBranch",
        "routeStations": "TanahMerah\nExpo\nChangiAirport",
    },
    "scenario6": {
        "mode": "future", "status": "scheduled_maintenance", "integration": False,
        "exists": "TanahMerah\nExpo\nChangiAirport\nT5\nSungeiBedok",
        "openStations": "TanahMerah\nChangiAirport\nT5\nSungeiBedok",
        "openEdges": "TanahMerah,Expo\nExpo,ChangiAirport\nSungeiBedok,T5\nT5,TanahMerah",
        "recommendedRoutes": "",
        "servedTEL": "",
        "routeName": "EWL_AirportBranch",
        "routeStations": "TanahMerah\nExpo\nChangiAirport",
    },
}

DEFAULTS = PRESETS["scenario1"]

def ensure_defaults():
    # only set if missing (safe)
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def request_preset_load(preset_key: str):
    """Safe preset loading pattern for Streamlit."""
    st.session_state["_pending_preset"] = preset_key
    st.rerun()

def apply_pending_preset_if_any():
    """Apply presets BEFORE widgets are created."""
    key = st.session_state.get("_pending_preset")
    if not key:
        return
    preset = PRESETS.get(key, {})
    for k, v in preset.items():
        st.session_state[k] = v
    st.session_state["_pending_preset"] = None
    clear_output()
    log(f"Loaded preset: {key}", "muted")
    log("Next: go Route tab and press Run Both.", "muted")

# =========================================================
# Logic placeholders (swap with your actual logic)
# =========================================================
def build_scenario_from_state():
    return {
        "mode": st.session_state["mode"],
        "status": st.session_state["status"],
        "exists": parse_csv_set(st.session_state["exists"]),
        "open_stations": parse_csv_set(st.session_state["openStations"]),
        "open_edges": parse_edges(st.session_state["openEdges"]),
        "integration_works": bool(st.session_state["integration"]),
        "recommended_routes": parse_csv_set(st.session_state["recommendedRoutes"]),
        "served_by_tel": parse_csv_set(st.session_state["servedTEL"]),
    }

def build_route_from_state():
    name = (st.session_state["routeName"] or "").strip() or "UnnamedRoute"
    raw = (st.session_state["routeStations"] or "").strip()
    if not raw:
        raise ValueError("Route stations cannot be empty.")
    stations = [x.strip() for x in raw.replace("\n", ",").split(",") if x.strip()]
    return {"name": name, "stations": stations}

def check_advisory_consistency(scenario: dict):
    log("Advisory consistency check", "title")

    violations = []
    if scenario["mode"] == "today" and scenario["status"] == "normal":
        log("Result: Consistent", "ok")
    else:
        log("Result: Inconsistent", "bad")
        violations.append("Status/mode mismatch detected (placeholder rule)")

    if violations:
        log("Rule violations: " + ", ".join(violations), "bad")

def evaluate_route_logic(route: dict, scenario: dict):
    log("Route evaluation", "title")
    log(f"Route: {route['name']}", "muted")

    violations = []
    valid = True
    warning = False

    if len(route["stations"]) < 2:
        valid = False
        violations.append("Route must have at least 2 stations")

    if valid:
        missing = [s for s in route["stations"] if s not in scenario["exists"]]
        if missing:
            warning = True
            violations.append(f"Stations not in Exists list: {missing}")

    if valid and warning:
        log("Result: Valid (warning)", "warn")
    elif valid:
        log("Result: Valid", "ok")
    else:
        log("Result: Invalid", "bad")

    if violations:
        log("Rule violations: " + ", ".join(map(str, violations)), "bad")

def run_both():
    scenario = build_scenario_from_state()
    route = build_route_from_state()
    check_advisory_consistency(scenario)
    evaluate_route_logic(route, scenario)

# =========================================================
# MAIN FLOW (IMPORTANT ORDER)
# Apply preset -> set defaults -> then create widgets
# =========================================================
init_output()
apply_pending_preset_if_any()
ensure_defaults()

# =========================================================
# UI
# =========================================================
st.markdown("# ChangiLink AI")
st.caption("logical inference checker thingy (pls work)")

tabs = st.tabs(["Scenario", "Route", "Presets"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Mode", ["today", "future"], key="mode")
    with c2:
        st.selectbox(
            "Status",
            ["normal", "delay", "disrupted", "scheduled_maintenance"],
            key="status"
        )

    st.checkbox("Integration Works (systems integration ongoing)", key="integration")
    st.divider()

    colA, colB = st.columns(2)
    with colA:
        st.text_area("Exists (stations that exist)", key="exists", height=140)
    with colB:
        st.text_area("Open Stations", key="openStations", height=140)

    colC, colD = st.columns(2)
    with colC:
        st.text_area("Open Edges (A,B or A -> B)", key="openEdges", height=140)
    with colD:
        st.text_area("Recommended Routes", key="recommendedRoutes", height=140)

    st.text_area("Served by TEL (optional)", key="servedTEL", height=100)

with tabs[1]:
    st.text_input("Route Name", key="routeName")
    st.text_area("Route Stations (in order)", key="routeStations", height=180)

    b1, b2, b3, b4 = st.columns([1, 1, 1, 1])
    with b1:
        if st.button("Run Both", use_container_width=True):
            try:
                run_both()
            except Exception as e:
                log(f"Error: {e}", "bad")
    with b2:
        if st.button("Check Advisory", use_container_width=True):
            try:
                scenario = build_scenario_from_state()
                check_advisory_consistency(scenario)
            except Exception as e:
                log(f"Error: {e}", "bad")
    with b3:
        if st.button("Evaluate Route", use_container_width=True):
            try:
                scenario = build_scenario_from_state()
                route = build_route_from_state()
                evaluate_route_logic(route, scenario)
            except Exception as e:
                log(f"Error: {e}", "bad")
    with b4:
        if st.button("Clear Output", use_container_width=True):
            clear_output()

with tabs[2]:
    st.markdown("### Presets")
    st.caption("Load one of these and then go Route tab → Run Both")

    preset_key = st.selectbox(
        "Pick one",
        list(PRESETS.keys()),
        format_func=lambda k: k.replace("scenario", "Scenario "),
        key="preset_picker",
    )

    if st.button("Load Preset", use_container_width=True):
        request_preset_load(preset_key)

    st.info("Tip: you can still type stuff manually after loading.")

st.divider()
render_output()

with st.expander("Debug: current parsed scenario/route"):
    try:
        scenario_dbg = build_scenario_from_state()
        route_dbg = build_route_from_state()
        st.code(json.dumps({"scenario": scenario_dbg, "route": route_dbg}, default=list, indent=2))
    except Exception as e:
        st.code(str(e))
