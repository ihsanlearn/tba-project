from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
from automata import clean_transitions, validate_automata, classify_automata, simulate_automata

app = FastAPI(title="Automata Simulator")

class AnalyzeRequest(BaseModel):
    states: List[str]
    alphabet: List[str]
    start_state: str
    final_states: List[str]
    transitions: Dict[str, Dict[str, List[str]]]

class SimulateRequest(BaseModel):
    states: List[str]
    alphabet: List[str]
    start_state: str
    final_states: List[str]
    transitions: Dict[str, Dict[str, List[str]]]
    automata_type: str
    input_string: str

@app.get("/")
def read_root():
    """Serve the single-page application."""
    return FileResponse("index.html")

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """
    Cleans, validates, and classifies the given automaton.
    """
    cleaned_transitions = clean_transitions(req.transitions)
    
    errors = validate_automata(req.states, req.alphabet, req.start_state, req.final_states, cleaned_transitions)
    if errors:
        return {
            "cleaned_transitions": cleaned_transitions,
            "type": None,
            "reason": None,
            "validation_errors": errors
        }
        
    automata_type, reason = classify_automata(req.states, req.alphabet, cleaned_transitions)
    
    return {
        "cleaned_transitions": cleaned_transitions,
        "type": automata_type,
        "reason": reason,
        "validation_errors": []
    }

@app.post("/simulate")
def simulate(req: SimulateRequest):
    """
    Simulates the processing of an input string on the automaton.
    """
    cleaned_transitions = clean_transitions(req.transitions)
    result = simulate_automata(
        req.states, 
        req.alphabet, 
        req.start_state, 
        req.final_states, 
        cleaned_transitions, 
        req.automata_type, 
        req.input_string
    )
    return result
