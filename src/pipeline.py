import pandas as pd
from pathlib import Path
from clean_data import clean_customers

input_files = [
    "data/raw/customers_dirty.csv",
    "data/raw/customers_dirty2.csv",
    "data/raw/customers_dirty3.csv"
]

output_dir = Path("data/processed")


for file_path in input_files:
    
    df = pd.read_csv(file_path)
    
    df_clean = clean_customers(df)
    
    input_name = Path(file_path).stem
    output_file = output_dir / (input_name.replace("dirty", "clean") + ".csv")

    df_clean.to_csv(output_file, index=False)
    
