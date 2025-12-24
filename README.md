import time
from collections import deque
import sys

def pezzotti_sliding_window(n_nodes, k=4):
    """
    Sliding Window Solver for Streamed Graphs.
    Optimized for high throughput and minimal memory footprint.
    """
    start_time = time.time()
    errors = 0
    
    # Circular buffer: keeps only the last 6 nodes in memory
    # This allows O(1) memory usage regardless of N
    history_buffer = deque([-1]*6, maxlen=6)
    
    print(f"Starting processing on {n_nodes:,} nodes...")
    print("Mode: Sliding Window (Low-RAM)")
    
    # Available colors (k=4)
    base_phases = {0, 1, 2, 3}
    
    for i in range(n_nodes):
        # --- CONSTRAINT LOGIC ---
        # We look back in the buffer to check relevant neighbors.
        # For this topology, relevant neighbors are at (i-1) and (i-5)
        
        relevant_neighbors = []
        
        if i > 0:
            relevant_neighbors.append(history_buffer[-1]) # i-1
        if i > 5:
            relevant_neighbors.append(history_buffer[-5]) # i-5
            
        # --- SATURATION ---
        possible_phases = set(base_phases)
        
        for neighbor_val in relevant_neighbors:
            if neighbor_val != -1:
                possible_phases.discard(neighbor_val)
        
        # Deterministic Greedy Choice
        if possible_phases:
            choice = min(possible_phases)
        else:
            choice = 0 # Conflict handled
            errors += 1
        
        # Push choice to buffer
        history_buffer.append(choice)
            
        # --- VISUAL FEEDBACK (Every 500k nodes) ---
        if i % 500_000 == 0 and i > 0:
            elapsed = time.time() - start_time
            speed = i / elapsed
            perc = (i / n_nodes) * 100
            
            # Progress Bar
            bar_len = 20
            filled = int(bar_len * i // n_nodes)
            bar = '█' * filled + '-' * (bar_len - filled)
            
            sys.stdout.write(f"\r[{bar}] {perc:.1f}% | Processed: {i:,} | Speed: {speed:,.0f} nodes/s | Err: {errors}")
            sys.stdout.flush()

    duration = time.time() - start_time
    sys.stdout.write(f"\r[{'█'*20}] 100.0% | Processed: {n_nodes:,} | COMPLETED.\n")
    return duration, errors

if __name__ == "__main__":
    # Test with 100 Million Nodes
    n_nodes = 100_000_000
    duration, err = pezzotti_sliding_window(n_nodes)
    
    print(f"\n--- FINAL RESULTS ---")
    print(f"Total Time: {duration:.2f} seconds ({duration/60:.1f} mins)")
    print(f"Constraints Broken: {err}")
