import json

# Load the data from the input.json file
with open('input.json') as f:
    data = json.load(f)

# Extract the 'A__Axis__Rotary_Speed' values
a_axis_rotary_speeds = [d['A__Axis__Rotary_Speed'] for d in data]

# Find the maximum 'A__Axis__Rotary_Speed'
max_a_axis_rotary_speed = max(a_axis_rotary_speeds)

# Write the maximum 'A__Axis__Rotary_Speed' to the output.json file
with open('output.json', 'w') as f:
    json.dump({'max_A__Axis__Rotary_Speed': max_a_axis_rotary_speed}, f)