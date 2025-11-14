#!/usr/bin/env python3
"""Replace the render_multi_objective_optimizer function in app.py"""

# Read the new function
with open('dashboard/new_optimizer.py', 'r', encoding='utf-8') as f:
    new_function = f.read()

# Read the original file
with open('dashboard/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 1478-1989 (Python uses 0-based indexing, so 1477-1988)
# Keep everything before line 1478 and after line 1989
before = ''.join(lines[:1477])  # Lines 1-1477
after = ''.join(lines[1989:])    # Lines 1990+

# Combine
new_content = before + '\n' + new_function + '\n\n' + after

# Write back
with open('dashboard/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Function replaced successfully!")
print(f"   - Removed lines 1478-1989 (old function)")
print(f"   - Inserted new clean 3-column layout")
print(f"   - Removed all Multi-Objective Analytics section")
print(f"   - Removed Insights Panel section")
print(f"   - Kept only: Weights, Optimal Region, Comparison Chart, Pareto Frontier")
