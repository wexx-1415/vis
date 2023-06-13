import pandas as pd

# Create a sample DataFrame
data = {'Region': ['Africa', 'Africa', 'Asia', 'Asia', 'Europe'],
        'Country': ['Ethiopia', 'Kenya', 'China', 'Japan', 'France'],
        'value': [1, 2, 3, 4, 5]}
df = pd.DataFrame(data)

# Group the data by Region
grouped = df.groupby('Region')

# Define a function to convert the grouped data into the desired JSON format
def grouped_to_json(grouped):
    result = []
    for name, group in grouped:
        group_dict = {}
        group_dict['name'] = name
        group_dict['value'] = group['value'].sum()
        group_dict['children'] = group.to_dict('records')
        result.append(group_dict)
    return result

# Convert the grouped data into the desired JSON format
result = grouped_to_json(grouped)

# Print the resulting JSON
print(result)
