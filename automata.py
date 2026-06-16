from typing import List, Dict, Set, Any, Tuple

EPSILON = "ε"

def clean_transitions(transitions: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict[str, List[str]]]:
    """
    Remove redundant epsilon self-loops.
    Input format: transitions[source_state][symbol] = [target_state1, target_state2, ...]
    """
    cleaned = {}
    for state, paths in transitions.items():
        cleaned_paths = {}
        for symbol, targets in paths.items():
            if symbol == EPSILON:
                # Remove self-loops
                cleaned_targets = [t for t in targets if t != state]
                cleaned_paths[symbol] = cleaned_targets
            else:
                cleaned_paths[symbol] = [t for t in targets]
        cleaned[state] = cleaned_paths
    return cleaned

def validate_automata(states: List[str], alphabet: List[str], start_state: str, final_states: List[str], transitions: Dict[str, Dict[str, List[str]]]) -> List[str]:
    """
    Validates the automata structure. Returns a list of error messages (empty if valid).
    """
    errors = []
    if not states:
        errors.append("States list must not be empty.")
    if not alphabet:
        errors.append("Alphabet must not be empty.")
    if start_state not in states:
        errors.append(f"Start state '{start_state}' is not in the states list.")
    
    for fs in final_states:
        if fs not in states:
            errors.append(f"Final state '{fs}' is not in the states list.")
            
    for state, paths in transitions.items():
        for symbol, targets in paths.items():
            for target in targets:
                if target not in states:
                    errors.append(f"Target state '{target}' in transitions is not in the states list.")
                    
    return errors

def classify_automata(states: List[str], alphabet: List[str], transitions: Dict[str, Dict[str, List[str]]]) -> Tuple[str, str]:
    """
    Classifies the automaton as ε-NFA, NFA, or DFA.
    Returns (Type, Reason)
    """
    has_epsilon = False
    
    for state, paths in transitions.items():
        if EPSILON in paths and len(paths[EPSILON]) > 0:
            has_epsilon = True
            break
            
    if has_epsilon:
        return "ε-NFA", "There exists at least one non-loop epsilon transition."
        
    is_nfa = False
    for state in states:
        paths = transitions.get(state, {})
        for symbol in alphabet:
            targets = paths.get(symbol, [])
            if len(targets) > 1:
                is_nfa = True
                break
            if len(targets) == 0:
                is_nfa = True
                break
        if is_nfa:
            break
            
    if is_nfa:
        return "NFA", "There is at least one state with multiple transitions for the same symbol, or missing transitions for a symbol."
        
    return "DFA", "Every state has exactly one transition for each symbol in the alphabet, and no epsilon transitions exist."

def epsilon_closure(state: str, transitions: Dict[str, Dict[str, List[str]]]) -> Set[str]:
    """
    Computes the epsilon closure of a state using DFS.
    """
    closure = set([state])
    stack = [state]
    
    while stack:
        current = stack.pop()
        eps_targets = transitions.get(current, {}).get(EPSILON, [])
        for target in eps_targets:
            if target not in closure:
                closure.add(target)
                stack.append(target)
                
    return closure

def get_epsilon_closure_set(states: Set[str], transitions: Dict[str, Dict[str, List[str]]]) -> Set[str]:
    """
    Computes the epsilon closure for a set of states.
    """
    closure = set()
    for state in states:
        closure.update(epsilon_closure(state, transitions))
    return closure

def simulate_automata(states: List[str], alphabet: List[str], start_state: str, final_states: List[str], transitions: Dict[str, Dict[str, List[str]]], automata_type: str, input_string: str) -> Dict[str, Any]:
    """
    Simulates the processing of the input string.
    Returns the trace and acceptance result.
    """
    trace = []
    
    if automata_type == "DFA":
        current_state = start_state
        trace.append({"step": 0, "current_states": [current_state], "symbol": input_string[0] if input_string else None})
        
        for i, symbol in enumerate(input_string):
            targets = transitions.get(current_state, {}).get(symbol, [])
            if not targets:
                return {
                    "accepted": False,
                    "trace": trace,
                    "message": f"String '{input_string}' REJECTED. Stuck at state {current_state} with no transition for symbol '{symbol}'."
                }
            current_state = targets[0]
            next_symbol = input_string[i+1] if i+1 < len(input_string) else None
            trace.append({"step": i+1, "current_states": [current_state], "symbol": next_symbol})
            
        accepted = current_state in final_states
        return {
            "accepted": accepted,
            "trace": trace,
            "message": f"String '{input_string}' {'ACCEPTED' if accepted else 'REJECTED'}. Ended in state {current_state}."
        }
        
    elif automata_type in ["NFA", "ε-NFA"]:
        current_states = set([start_state])
        
        if automata_type == "ε-NFA":
            current_states = get_epsilon_closure_set(current_states, transitions)
            
        trace.append({"step": 0, "current_states": sorted(list(current_states)), "symbol": input_string[0] if input_string else None})
        
        for i, symbol in enumerate(input_string):
            next_states = set()
            for state in current_states:
                targets = transitions.get(state, {}).get(symbol, [])
                next_states.update(targets)
                
            if automata_type == "ε-NFA":
                next_states = get_epsilon_closure_set(next_states, transitions)
                
            current_states = next_states
            next_symbol = input_string[i+1] if i+1 < len(input_string) else None
            trace.append({"step": i+1, "current_states": sorted(list(current_states)), "symbol": next_symbol})
            
            if not current_states:
                return {
                    "accepted": False,
                    "trace": trace,
                    "message": f"String '{input_string}' REJECTED. Stuck with no active states at step {i+1}."
                }
                
        accepted = any(s in final_states for s in current_states)
        ended_states = ", ".join(sorted(list(current_states)))
        return {
            "accepted": accepted,
            "trace": trace,
            "message": f"String '{input_string}' {'ACCEPTED' if accepted else 'REJECTED'}. Active states at end: {ended_states}."
        }

    return {"accepted": False, "trace": [], "message": "Unknown automata type."}
