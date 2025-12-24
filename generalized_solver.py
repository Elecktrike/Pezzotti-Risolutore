import time
from collections import deque
import sys

def generalized_pezzotti_solver(n_nodes, offsets):
    """
    Generalized Sliding Window Solver (Debug Version).
    Uses standard print to guarantee visibility on all consoles.
    """
    max_lookback = max(offsets)
    history_buffer = deque([-1] * (max_lookback + 1), maxlen=max_lookback + 1)
    
    start_time = time.time()
    errors = 0
    
    print(f"--- GENERALIZED SOLVER CONFIGURATION ---")
    print(f"Target Nodes: {n_nodes:,}")
    print(f"Constraints (Offsets): {offsets}")
    print(f"Window Size (RAM usage): {max_lookback + 1} integers")
    print(f"----------------------------------------")
    print("Processing started... please wait.")
    
    base_phases = {0, 1, 2, 3, 4, 5, 6, 7} 
    
    for i in range(n_nodes):
        relevant_neighbors = []
        for offset in offsets:
            if i >= offset:
                relevant_neighbors.append(history_buffer[-offset])
        
        possible_phases = set(base_phases)
        for neighbor_val in relevant_neighbors:
            if neighbor_val != -1:
                possible_phases.discard(neighbor_val)
        
        if possible_phases:
            choice = min(possible_phases)
        else:
            choice = 0
            errors += 1
        
        history_buffer.append(choice)
            
        # LOGGING MODIFICATO: Usa print normale ogni 500k nodi
        if i % 500_000 == 0 and i > 0:
            elapsed = time.time() - start_time
            if elapsed > 0:
                speed = i / elapsed
                print(f" -> Processed: {i:,} | Speed: {speed:,.0f} nodes/s | Err: {errors}")

    total_time = time.time() - start_time
    print(f"----------------------------------------")
    print(f"DONE! Processed {n_nodes:,} nodes.")
    print(f"Total Time: {total_time:.4f} seconds")
    print(f"Average Speed: {n_nodes/total_time:,.0f} nodes/s")
    print(f"Total Errors: {errors}")
    return total_time, errors

if __name__ == "__main__":
    # Test con Fibonacci
    complex_offsets = [1, 2, 3, 5, 8, 13, 21] 
    print("Launching Solver...")
    generalized_pezzotti_solver(10_000_000, complex_offsets)
    input("Press Enter to exit...") 
