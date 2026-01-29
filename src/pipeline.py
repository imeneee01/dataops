import pandas as pd
from pathlib import Path
from clean_data import clean_customers
import json

input_files = [
    "data/raw/customers_dirty.csv",
    "data/raw/customers_dirty2.csv",
    "data/raw/customers_dirty3.csv"
]

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

report_dir = Path("data/reports")
report_dir.mkdir(exist_ok=True)

for file_path in input_files:
    
    df = pd.read_csv(file_path)
    
    df_clean, report = clean_customers(df)

    input_name = Path(file_path).stem
    output_file = output_dir / (input_name.replace("dirty", "clean") + ".csv")
    report_file = report_dir / (input_name.replace("dirty", "report") + ".json")
    
    df_clean.to_csv(output_file, index=False)

    with open(report_file, "w") as f:
        f.write(f"Fichier nettoye : {output_file.name}\n")
        f.write(f"Lignes initiales : {report['rows_input']}\n")
        f.write(f"Lignes supprimees : {report['rows_dropped']}\n")
        f.write(f"Emails invalides : {report['invalid_emails']}\n")
        f.write(f"Doublons supprimes : {report['duplicates_removed']}\n")
    
    
    print(f"{output_file.name} → {report['rows_input']} lignes initiales, "
          f"{report['rows_dropped']} lignes supprimées, "
          f"{report['invalid_emails']} emails invalides, "
          f"{report['duplicates_removed']} doublons supprimés")
