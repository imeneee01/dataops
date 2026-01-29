import pandas as pd
import re
from pathlib import Path

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
CLEAN_DIR = Path("data/processed")


def load_all_clean_data():
    files = list(CLEAN_DIR.glob("*clean*.csv"))
    assert len(files) > 0, "No clean files found in data/processed"
    return files

def test_full_name_not_missing():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        missing_names = df["full_name"].isna() | (df["full_name"] == "")
        assert not missing_names.any(), f"{file.name} → full_name missing"


def test_emails_are_valid():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        invalid = ~df["email"].str.match(EMAIL_REGEX)
        assert not invalid.any(), \
            f"{file.name} → invalid emails detected"
        
def test_signup_date_is_valid():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        dates = pd.to_datetime(df["signup_date"], errors="coerce")
        assert dates.notna().all(), \
            f"{file.name} → invalid signup_date"


def test_age_is_reasonable():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        assert ((df["age"] >= 16) & (df["age"] <= 100)).all(), \
            f"{file.name} → age out of range"


def test_purchase_amount_non_negative():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        assert (df["last_purchase_amount"] >= 0).all(), \
            f"{file.name} → negative purchase amount"

def test_loyalty_tier_values():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        assert "UNKNOWN" not in df["loyalty_tier"].values, \
            f"{file.name} → 'UNKNOWN' found in loyalty_tier"

def test_no_duplicate_emails():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        duplicates = df["email"].duplicated()
        assert not duplicates.any(), \
            f"{file.name} → duplicate emails found"

def test_no_missing_values():
    for file in load_all_clean_data():
        df = pd.read_csv(file)
        missing = df.isna().any().any() 
        assert not missing, f"{file.name} → missing values detected"

   
