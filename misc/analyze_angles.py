#!/usr/bin/env python3
import re

# Read the animation file
with open('create_animations.py', 'r') as f:
    content = f.read()

# Find all angle patterns
angles = re.findall(r'"([0-9]+\.[0-9]+_[0-9]+\.[0-9]+_[0-9]+\.[0-9]+)"', content)
unique_angles = sorted(set(angles))

print('All unique angles used in animations:')
for angle in unique_angles:
    print(angle)

print(f'\nTotal unique angles: {len(unique_angles)}')

# Also check grind positions from app.py
with open('app.py', 'r') as f:
    app_content = f.read()

# Find grind position angles
grind_angles = re.findall(r'"angle": \(([^)]+)\)', app_content)
print(f'\nGrind position angles:')
for angle in grind_angles:
    print(angle)

# Parse the angles to see what ranges we actually use
x_angles = set()
y_angles = set()
z_angles = set()

for angle_str in unique_angles:
    parts = angle_str.split('_')
    if len(parts) == 3:
        x_angles.add(float(parts[0]))
        y_angles.add(float(parts[1]))
        z_angles.add(float(parts[2]))

print(f'\nX angle range: {min(x_angles)} to {max(x_angles)} (unique values: {sorted(x_angles)})')
print(f'Y angle range: {min(y_angles)} to {max(y_angles)} (unique values: {sorted(y_angles)})')
print(f'Z angle range: {min(z_angles)} to {max(z_angles)} (unique values: {sorted(z_angles)})')
