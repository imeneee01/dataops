import pandas as pd
from pathlib import Path
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.clean_data import clean_customers

# Utiliser des chemins absolus pour le Docker
data_dir = Path("/app/data")
input_files = [
    str(data_dir / "raw" / "customers_dirty.csv"),
    str(data_dir / "raw" / "customers_dirty2.csv"),
    str(data_dir / "raw" / "customers_dirty3.csv")
]

output_dir = data_dir / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

report_dir = data_dir / "reports"
report_dir.mkdir(parents=True, exist_ok=True)

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
