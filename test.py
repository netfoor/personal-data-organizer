import pandas as pd

csv_path = r'C:\artifacts\catalog.csv'
column_name = 'extension'

try: 
    df = pd.read_csv(csv_path)
    extensions = df[column_name].unique()
    print(list(extensions))
except FileNotFoundError:
    print(f"File not found: {csv_path}")
except KeyError:
    print(f"Column '{column_name}' not found in the CSV file.")