# Automata Simulator & Classifier

A web application that simulates and classifies **Deterministic Finite Automata (DFA)**, **Nondeterministic Finite Automata (NFA)**, and **ε-NFA (Epsilon-NFA)**.

> Final Project — Theory of Languages and Automata

---

## Features

- **Automata Definition** — Define states, alphabet, start state, final states, and transitions via an interactive table.
- **Automatic Classification** — The system automatically classifies the automaton as DFA, NFA, or ε-NFA based on its transition structure.
- **String Simulation** — Enter an input string and simulate step-by-step processing with a detailed trace log.
- **State Diagram Visualization** — Interactive graph rendered with Cytoscape.js showing states, transitions, and active path highlighting during simulation.
- **Step-by-Step Trace** — Navigate through simulation steps with Previous/Next controls to observe state transitions.

---

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python, FastAPI                     |
| Frontend | HTML, Tailwind CSS (CDN), Vanilla JS |
| Diagram  | Cytoscape.js + Dagre Layout         |
| Fonts    | Inter, JetBrains Mono (Google Fonts) |

---

## Project Structure

```
automata-app/
├── main.py            # FastAPI backend — routing & endpoints
├── automata.py        # Core logic: cleaning, validation, classification, simulation
├── index.html         # Frontend: input form, transition table, diagram, results
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd project-tba
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**

   ```bash
   uvicorn main:app --reload
   ```

4. **Open the application**

   Navigate to [http://localhost:8000](http://localhost:8000) in your web browser.

---

## How to Use

### Step 1 — Define the Automaton

1. Enter **States** (comma-separated, e.g. `q0, q1, q2`)
2. Enter **Alphabet** (comma-separated, e.g. `a, b`)
3. Select the **Start State** from the dropdown
4. Enter **Final States** (comma-separated, e.g. `q2`)
5. Click **Generate Table** to create the transition table

### Step 2 — Fill in Transitions

- Each cell represents a transition: `source state × symbol → target state(s)`
- Leave a cell empty if there is no transition
- For multiple targets (NFA), use comma-separated values (e.g. `q0, q1`)
- The `ε` column is for epsilon transitions

### Step 3 — Analyze

- Click **Analyze Automaton** to classify the automaton
- The system displays the **type** (DFA / NFA / ε-NFA) and the **reason** for classification
- A state diagram is rendered below

### Step 4 — Simulate

- Enter an input string (e.g. `aab`) in the simulation panel
- Click **Simulate** to see if the string is **ACCEPTED** or **REJECTED**
- Use the **Prev / Next** buttons to step through the trace

---

## Classification Logic

| Type   | Condition                                                                 |
|--------|---------------------------------------------------------------------------|
| **ε-NFA** | At least one non-self-loop epsilon transition exists                      |
| **NFA**   | Any state has multiple targets for a symbol, or missing transitions       |
| **DFA**   | Every state has exactly one transition per symbol, no epsilon transitions  |

> **Note:** Epsilon self-loops (e.g. `q0 --ε--> q0`) are automatically cleaned and do not count toward ε-NFA classification.

---

## API Endpoints

### `GET /`
Serves the single-page application (`index.html`).

### `POST /analyze`
Cleans, validates, and classifies the automaton.

**Request Body:**
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": {
    "q0": { "a": ["q1"], "b": ["q0"], "ε": [] },
    "q1": { "a": ["q1"], "b": ["q2"], "ε": [] },
    "q2": { "a": ["q2"], "b": ["q2"], "ε": [] }
  }
}
```

**Response Body:**
```json
{
  "cleaned_transitions": { "..." : "..." },
  "type": "DFA",
  "reason": "Every state has exactly one transition for each symbol in the alphabet, and no epsilon transitions exist.",
  "validation_errors": []
}
```

### `POST /simulate`
Simulates string processing on the automaton.

**Request Body:**
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": { "...": "..." },
  "automata_type": "DFA",
  "input_string": "aab"
}
```

**Response Body:**
```json
{
  "accepted": true,
  "trace": [
    { "step": 0, "current_states": ["q0"], "symbol": "a" },
    { "step": 1, "current_states": ["q1"], "symbol": "a" },
    { "step": 2, "current_states": ["q1"], "symbol": "b" },
    { "step": 3, "current_states": ["q2"], "symbol": null }
  ],
  "message": "String 'aab' ACCEPTED. Ended in state q2."
}
```

---

## Test Cases

### Test Case 1 — DFA

| State | a   | b   | ε |
|-------|-----|-----|---|
| q0    | q1  | q0  |   |
| q1    | q1  | q2  |   |
| q2    | q2  | q2  |   |

- Start: `q0` | Final: `q2`
- `"aab"` → **ACCEPTED** ✅
- `"b"` → **REJECTED** ❌

### Test Case 2 — NFA

| State | a      | b   | ε |
|-------|--------|-----|---|
| q0    | q0, q1 | q0  |   |
| q1    |        | q2  |   |
| q2    |        |     |   |

- Start: `q0` | Final: `q2`
- `"aab"` → **ACCEPTED** ✅
- `"bb"` → **REJECTED** ❌

### Test Case 3 — ε-NFA

| State | a   | b   | ε   |
|-------|-----|-----|-----|
| q0    |     |     | q1  |
| q1    | q2  |     |     |
| q2    |     |     |     |

- Start: `q0` | Final: `q2`
- `"a"` → **ACCEPTED** ✅
- `"b"` → **REJECTED** ❌
