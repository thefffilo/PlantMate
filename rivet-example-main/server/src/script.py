import json

def find_max():
    # Load the data from the file
    with open('input.json', 'r') as file:
        data = json.load(file)
    
    # Check if the variable exists in the data
    if 'A__Axis__Rotary_Speed' in data:
        # Find the maximum of the variable
        max_value = max(data['A__Axis__Rotary_Speed'])
        
        # Write the output to a file
        with open('output.json', 'w') as outfile:
            json.dump({'max_A__Axis__Rotary_Speed': max_value}, outfile)
    else:
        print("Variable 'A__Axis__Rotary_Speed' not found in the data.")

# Call the function
find_max()