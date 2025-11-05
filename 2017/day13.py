"""Day 13 solution."""
import copy
import numbers
from pathlib import Path
import sys
import re


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

from dataclasses import dataclass

@dataclass
class Layer:
    depth: int
    pos: int
    direction: int
    



def print_layers(picosecond: int, layers: dict[int, Layer], packet_layer: int) -> None:
    """
    Visualize the firewall with the packet position.

    Args:
        picosecond (int): Current simulation time.
        layers (dict[int, Layer]): {layer_index: Layer(depth, pos, direction)}
        packet_layer (int): The current layer where the packet is (0 = top row).
    """
    if not layers:
        print(f"\nPicosecond {picosecond}: (no layers)")
        return

    max_layer = max(layers)
    max_depth = max(L.depth for L in layers.values())

    print(f"\nPicosecond {picosecond}:")
    # Header
    for i in range(max_layer + 1):
        print(f"{i:>3}", end=" ")
    print()

    # Grid
    for row in range(max_depth):
        for col in range(max_layer + 1):
            if col not in layers:
                cell = "..."
            else:
                L = layers[col]
                if row >= L.depth:
                    cell = "   "
                else:
                    # If the packet is at this layer and top row (row == 0)
                    if col == packet_layer and row == 0:
                        # Use parentheses for the packet
                        if L.pos == row:
                            cell = "(S)"   # packet and scanner in same cell
                        else:
                            cell = "( )"   # packet only
                    else:
                        cell = "[S]" if L.pos == row else "[ ]"
            print(cell, end=" ")
        print()


def run_firewall(layers: dict[int, Layer], delay: int = 0, visualize: bool = False) -> int:
    """
    Simulate the packet moving through the firewall with an optional delay.
    Returns the total severity of getting caught.

    Args:
        layers (dict[int, Layer]): Mapping {layer_index: Layer(depth, pos, direction)}.
        delay (int): How many picoseconds the packet waits before entering.
        visualize (bool): If True, prints each firewall state.

    Returns:
        int: Total severity.
    """
    # Deep copy to avoid mutating the original state between runs
    
    firewall = copy.deepcopy(layers)

    picosecond = 0
    severity = 0
    max_layer = max(firewall)

   


    # Advance scanners by 'delay' before the packet starts
    for _ in range(delay):
        for L in firewall.values():
            if L.depth <= 1:
                continue
            if L.direction == 1 and L.pos == L.depth - 1:
                L.direction = -1
            elif L.direction == -1 and L.pos == 0:
                L.direction = 1
            L.pos += L.direction

    # Main simulation loop
    while picosecond <= max_layer:
        packet_layer = picosecond
        if visualize:
            print_layers(picosecond, firewall, packet_layer)
        # Check if caught
        if packet_layer in firewall and firewall[packet_layer].pos == 0:
            depth = firewall[packet_layer].depth
            severity += packet_layer * depth

        # Move scanners
        for L in firewall.values():
            if L.depth <= 1:
                continue
            if L.direction == 1 and L.pos == L.depth - 1:
                L.direction = -1
            elif L.direction == -1 and L.pos == 0:
                L.direction = 1
            L.pos += L.direction

        # Optional visualization


        picosecond += 1

    return severity

def passes_undetected_math(layers: dict[int, Layer], delay: int) -> bool:
    for L, layer in layers.items():
        D = layer.depth
        if D == 1:
            # scanner never moves and is always at top
            return False
        period = 2 * (D - 1)
        if (delay + L) % period == 0:
            return False
    return True



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day13.txt')

    layers = {}
    for line in lines:
        key, value = line.split(":", 1)
        k = int(key.strip())
        d = int(value.strip())
        layers[k] = Layer(d, 0, 1)

    layers2 = copy.deepcopy(layers)

    picosecond = 0
    severity = 0
    max_layer = max(layers)  # rightmost layer index

    while picosecond <= max_layer:                      # include the last layer
        packet_layer = picosecond
       # print_layers(picosecond, layers, packet_layer)
        # 1) Caught check BEFORE moving scanners
        if packet_layer in layers and layers[packet_layer].pos == 0:
            depth = layers[packet_layer].depth
            severity += packet_layer * depth
        #    print(f"Caught at layer {packet_layer}, severity += {packet_layer * depth}")

        # 2) Move all scanners (bounce at 0 and depth-1)
        for col, L in layers.items():
            if L.depth <= 1:
                L.pos = 0
                L.direction = +1
                continue
    
            # bounce logic
            if L.direction == 1 and L.pos == L.depth - 1:
                L.direction = -1
            elif L.direction == -1 and L.pos == 0:
                L.direction = 1
    
            L.pos += L.direction

        # 3) Optional visualization
       # print_layers(picosecond, layers, packet_layer)

        # 4) Advance time
        picosecond += 1

    
    print("Day 13 a = ", severity)



  #  print(run_firewall(layers2,0,False))

    
    for i in range(100000000):
    ##    if (i % 100000 == 0): print("i = ", i)
        if passes_undetected_math(layers,i) == True:
            print("Day 13 b = ",i)
            break


    


if __name__ == "__main__":
    main()
