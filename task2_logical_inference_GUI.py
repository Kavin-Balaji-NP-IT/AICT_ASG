import tkinter as tk
from tkinter import ttk, messagebox

from task2_logical_inference import Scenario, Route, evaluate_route, check_advisory_consistency


def parse_csv_set(text: str):
    """
    Parses: "A, B, C" or multiline "A\nB\nC" into a set of strings.
    """
    if not text.strip():
        return set()
    raw = text.replace("\n", ",")
    items = [x.strip() for x in raw.split(",")]
    return {x for x in items if x}


def parse_edges(text: str):
    """
    Parses edges from multiline:
      TanahMerah,Expo
      Expo,ChangiAirport
    or with arrows:
      TanahMerah -> Expo
    Returns set of (a,b) tuples.
    """
    edges = set()
    if not text.strip():
        return edges

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        ln = ln.replace("->", ",").replace("—", ",").replace("–", ",")
        parts = [p.strip() for p in ln.split(",") if p.strip()]
        if len(parts) != 2:
            raise ValueError(f"Bad edge format: '{ln}'. Use 'A,B' or 'A -> B'.")
        edges.add((parts[0], parts[1]))
    return edges


class LogicGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ChangiLink AI — Logical Inference Checker (Frontend)")
        self.geometry("980x640")

        self._build_ui()
        self._load_preset("Scenario 1 (A1)")

    def _build_ui(self):
        # Main vertical layout:
        # [Notebook on top]
        # [Output panel below]
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        # Make container rows stretch nicely
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=3)  # notebook area
        container.rowconfigure(1, weight=2)  # output area

        # ---- Inputs notebook (TOP) ----
        nb = ttk.Notebook(container)
        nb.grid(row=0, column=0, sticky="nsew")

        tab_scenario = ttk.Frame(nb, padding=10)
        tab_route = ttk.Frame(nb, padding=10)
        tab_presets = ttk.Frame(nb, padding=10)

        nb.add(tab_scenario, text="Scenario")
        nb.add(tab_route, text="Route")
        nb.add(tab_presets, text="Presets")

        # ---- Scenario tab ----
        row = 0
        ttk.Label(tab_scenario, text="Mode").grid(row=row, column=0, sticky="w")
        self.mode_var = tk.StringVar(value="today")
        ttk.Combobox(
            tab_scenario, textvariable=self.mode_var,
            values=["today", "future"], state="readonly", width=18
        ).grid(row=row, column=1, sticky="w", padx=8)

        ttk.Label(tab_scenario, text="Status").grid(row=row, column=2, sticky="w")
        self.status_var = tk.StringVar(value="normal")
        ttk.Combobox(
            tab_scenario, textvariable=self.status_var,
            values=["normal", "delay", "disrupted", "scheduled_maintenance"],
            state="readonly", width=22
        ).grid(row=row, column=3, sticky="w", padx=8)

        row += 1
        self.integration_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            tab_scenario, text="Integration Works (systems integration ongoing)",
            variable=self.integration_var
        ).grid(row=row, column=0, columnspan=4, sticky="w", pady=(8, 10))

        row += 1
        ttk.Label(tab_scenario, text="Exists (stations that exist in this mode)\n(comma or newline separated)").grid(
            row=row, column=0, sticky="nw"
        )
        self.exists_text = tk.Text(tab_scenario, height=6, width=36)
        self.exists_text.grid(row=row, column=1, sticky="we", padx=8)

        ttk.Label(tab_scenario, text="Open Stations\n(comma or newline separated)").grid(
            row=row, column=2, sticky="nw"
        )
        self.open_stations_text = tk.Text(tab_scenario, height=6, width=36)
        self.open_stations_text.grid(row=row, column=3, sticky="we", padx=8)

        row += 1
        ttk.Label(tab_scenario, text="Open Edges (one per line)\nFormat: A,B or A -> B").grid(
            row=row, column=0, sticky="nw", pady=(12, 0)
        )
        self.open_edges_text = tk.Text(tab_scenario, height=7, width=36)
        self.open_edges_text.grid(row=row, column=1, sticky="we", padx=8, pady=(12, 0))

        ttk.Label(tab_scenario, text="Recommended Routes\n(e.g. EWL_AirportBranch, ...)").grid(
            row=row, column=2, sticky="nw", pady=(12, 0)
        )
        self.recommended_text = tk.Text(tab_scenario, height=7, width=36)
        self.recommended_text.grid(row=row, column=3, sticky="we", padx=8, pady=(12, 0))

        row += 1
        ttk.Label(tab_scenario, text="(Optional) Served by TEL stations\n(for Rule 10 checking)").grid(
            row=row, column=0, sticky="w", pady=(12, 0)
        )
        self.served_tel_text = tk.Text(tab_scenario, height=2, width=36)
        self.served_tel_text.grid(row=row, column=1, sticky="we", padx=8, pady=(12, 0))

        # ---- Route tab ----
        rrow = 0
        ttk.Label(tab_route, text="Route Name").grid(row=rrow, column=0, sticky="w")
        self.route_name_var = tk.StringVar(value="EWL_AirportBranch")
        ttk.Entry(tab_route, textvariable=self.route_name_var, width=35).grid(row=rrow, column=1, sticky="w", padx=8)

        rrow += 1
        ttk.Label(tab_route, text="Route Stations (ordered)\nFormat: A,B,C or newline").grid(
            row=rrow, column=0, sticky="nw", pady=(12, 0)
        )
        self.route_stations_text = tk.Text(tab_route, height=6, width=55)
        self.route_stations_text.grid(row=rrow, column=1, sticky="we", padx=8, pady=(12, 0))

        rrow += 1
        btns = ttk.Frame(tab_route)
        btns.grid(row=rrow, column=0, columnspan=2, sticky="w", pady=(14, 0))

        ttk.Button(btns, text="Check Advisory Consistency", command=self.on_check_advisory).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Evaluate Route", command=self.on_evaluate_route).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Run Both", command=self.on_run_both).pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Clear Output", command=self.clear_output).pack(side="left")

        # ---- Presets tab ----
        ttk.Label(tab_presets, text="Load preset scenario quickly (good for demos/screenshots):").pack(anchor="w")
        self.preset_var = tk.StringVar(value="Scenario 1 (A1)")
        ttk.Combobox(
            tab_presets, textvariable=self.preset_var, state="readonly",
            values=[
                "Scenario 1 (A1)",
                "Scenario 2 (A2)",
                "Scenario 3 (A3)",
                "Scenario 4 (A4)",
                "Scenario 5 (A5)",
                "Scenario 6 (A6) - you should add",
            ],
            width=34
        ).pack(anchor="w", pady=10)

        ttk.Button(tab_presets, text="Load Preset", command=lambda: self._load_preset(self.preset_var.get())).pack(anchor="w")

        ttk.Label(
            tab_presets,
            text=(
                "Tip: Your assignment requires at least 6 scenarios.\n"
                "You already have A1–A5. Use A6 and tweak it to create another case."
            )
        ).pack(anchor="w", pady=16)

        # ---- Output panel (BOTTOM, FULL WIDTH) ----
        out_frame = ttk.LabelFrame(container, text="Output / Results", padding=10)
        out_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        out_frame.columnconfigure(0, weight=1)
        out_frame.rowconfigure(0, weight=1)

        self.output = tk.Text(out_frame, height=10, wrap="word")
        self.output.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scroll = ttk.Scrollbar(out_frame, orient="vertical", command=self.output.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=scroll.set)


    def clear_output(self):
        self.output.delete("1.0", "end")

    def log(self, msg: str, tag=None):
        self.output.insert("end", msg + "\n")
        self.output.see("end")

    def build_scenario(self) -> Scenario:
        mode = self.mode_var.get().strip()
        status = self.status_var.get().strip()

        exists = parse_csv_set(self.exists_text.get("1.0", "end"))
        open_stations = parse_csv_set(self.open_stations_text.get("1.0", "end"))
        open_edges = parse_edges(self.open_edges_text.get("1.0", "end"))
        recommended_routes = parse_csv_set(self.recommended_text.get("1.0", "end"))
        served_by_tel = parse_csv_set(self.served_tel_text.get("1.0", "end"))

        return Scenario(
            mode=mode,
            status=status,
            exists=exists,
            open_stations=open_stations,
            open_edges=open_edges,
            integration_works=bool(self.integration_var.get()),
            recommended_routes=recommended_routes,
            served_by_tel=served_by_tel
        )

    def build_route(self) -> Route:
        name = self.route_name_var.get().strip() or "UnnamedRoute"

        raw = self.route_stations_text.get("1.0", "end").strip()
        if not raw:
            raise ValueError("Route stations cannot be empty.")

        raw = raw.replace("\n", ",")
        stations = [x.strip() for x in raw.split(",") if x.strip()]
        return Route(name=name, stations=stations)

    def on_check_advisory(self):
        try:
            self.log("Advisory consistency check")
            sc = self.build_scenario()
            res = check_advisory_consistency(sc)

            if res["consistent"]:
                self.log("Result: Consistent")
            else:
                self.log("Result: Inconsistent")

            if res["violations"]:
                self.log(f"Rule violations: {res['violations']}")

            if res["notes"]:
                self.log("Notes:")
                for n in res["notes"]:
                    self.log(f"- {n}")

            self.log("")  # blank line
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log("=== Advisory Consistency Check ===", "title")
        try:
            sc = self.build_scenario()
            res = check_advisory_consistency(sc)

            if res["consistent"]:
                self.log("Advisories: CONSISTENT ✅", "ok")
            else:
                self.log("Advisories: INCONSISTENT ❌", "bad")

            if res["violations"]:
                self.log(f"Rule violations: {res['violations']}", "bad")

            for n in res["notes"]:
                self.log(f"- {n}")
            self.log("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_evaluate_route(self):
        try:
            self.log("Route evaluation")
            sc = self.build_scenario()
            r = self.build_route()
            res = evaluate_route(r, sc)

            if res["valid"] and res["warning"]:
                self.log(f"Route: {r.name}")
                self.log("Result: Valid (warning)")
            elif res["valid"]:
                self.log(f"Route: {r.name}")
                self.log("Result: Valid")
            else:
                self.log(f"Route: {r.name}")
                self.log("Result: Invalid")

            if res["violations"]:
                self.log(f"Rule violations: {res['violations']}")

            if res["notes"]:
                self.log("Notes:")
                for n in res["notes"]:
                    self.log(f"- {n}")

            self.log("")  # blank line
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_run_both(self):
        self.on_check_advisory()
        self.on_evaluate_route()

    def _load_preset(self, name: str):
        presets = self._preset_data()
        if name not in presets:
            messagebox.showwarning("Preset not found", f"No preset named: {name}")
            return

        p = presets[name]
        self.mode_var.set(p["mode"])
        self.status_var.set(p["status"])
        self.integration_var.set(p["integration_works"])

        self._set_text(self.exists_text, p["exists"])
        self._set_text(self.open_stations_text, p["open_stations"])
        self._set_text(self.open_edges_text, p["open_edges"])
        self._set_text(self.recommended_text, p.get("recommended_routes", ""))
        self._set_text(self.served_tel_text, p.get("served_by_tel", ""))

        self.route_name_var.set(p["route_name"])
        self._set_text(self.route_stations_text, p["route_stations"])

        self.clear_output()
        self.log(f"Loaded preset: {name}")
        self.log("Next: click Run Both")
        self.log("")

    def _set_text(self, widget: tk.Text, value: str):
        widget.delete("1.0", "end")
        widget.insert("1.0", value)

    def _preset_data(self):
        return {
            "Scenario 1 (A1)": {
                "mode": "today",
                "status": "normal",
                "integration_works": False,
                "exists": "TanahMerah\nExpo\nChangiAirport",
                "open_stations": "TanahMerah\nExpo\nChangiAirport",
                "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
                "recommended_routes": "",
                "route_name": "EWL_AirportBranch",
                "route_stations": "TanahMerah\nExpo\nChangiAirport",
            },
            "Scenario 2 (A2)": {
                "mode": "today",
                "status": "normal",
                "integration_works": False,
                "exists": "SungeiBedok\nTanahMerah\nExpo\nChangiAirport",
                "open_stations": "SungeiBedok\nTanahMerah\nExpo\nChangiAirport",
                "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
                "recommended_routes": "",
                "route_name": "Future_TEL_To_T5",
                "route_stations": "SungeiBedok\nT5\nTanahMerah",
            },
            "Scenario 3 (A3)": {
                "mode": "today",
                "status": "normal",
                "integration_works": False,
                "exists": "TanahMerah\nExpo\nChangiAirport",
                "open_stations": "TanahMerah\nExpo\nChangiAirport",
                "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
                "recommended_routes": "",
                "route_name": "Direct_TanahMerah_To_Changi",
                "route_stations": "TanahMerah\nChangiAirport",
            },
            "Scenario 4 (A4)": {
                "mode": "future",
                "status": "normal",
                "integration_works": False,
                "exists": "SungeiBedok\nT5\nTanahMerah",
                "open_stations": "SungeiBedok\nT5\nTanahMerah",
                "open_edges": "SungeiBedok,T5\nT5,TanahMerah",
                "recommended_routes": "",
                "route_name": "Future_TEL_To_T5",
                "route_stations": "SungeiBedok\nT5\nTanahMerah",
            },
            "Scenario 5 (A5)": {
                "mode": "future",
                "status": "delay",
                "integration_works": True,
                "exists": "TanahMerah\nExpo\nChangiAirport",
                "open_stations": "TanahMerah\nExpo\nChangiAirport",
                "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport",
                "recommended_routes": "EWL_AirportBranch",
                "route_name": "EWL_AirportBranch",
                "route_stations": "TanahMerah\nExpo\nChangiAirport",
            },
            "Scenario 6 (A6) - you should add": {
                "mode": "future",
                "status": "scheduled_maintenance",
                "integration_works": False,
                "exists": "TanahMerah\nExpo\nChangiAirport\nT5\nSungeiBedok",
                "open_stations": "TanahMerah\nChangiAirport\nT5\nSungeiBedok",
                "open_edges": "TanahMerah,Expo\nExpo,ChangiAirport\nSungeiBedok,T5\nT5,TanahMerah",
                "recommended_routes": "",
                "route_name": "EWL_AirportBranch",
                "route_stations": "TanahMerah\nExpo\nChangiAirport",
            },
        }


if __name__ == "__main__":
    app = LogicGUI()
    app.mainloop()
