import pandas as pd
import numpy as np
from src.clean_data import clean_customers

def test_full_name_cleaning():
    df = pd.DataFrame({
        "full_name": ["Alice", None],
        "email": ["a@test.com", "b@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02"],
        "country": ["FR", "USA"],
        "age": [25, 30],
        "last_purchase_amount": [10, 20],
        "loyalty_tier": ["BRONZE", "SILVER"]
    })
    df_clean, _ = clean_customers(df)
    assert df_clean["full_name"].notna().all()
    assert not (df_clean["full_name"] == "").any()

def test_email_cleaning():
    df = pd.DataFrame({
        "full_name": ["A", "B"],
        "email": ["invalid", "good@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02"],
        "country": ["FR", "FR"],
        "age": [20, 30],
        "last_purchase_amount": [0, 10],
        "loyalty_tier": ["BRONZE", "BRONZE"]
    })
    df_clean, _ = clean_customers(df)
    assert "invalid" not in df_clean["email"].values
    assert "good@test.com" in df_clean["email"].values


def test_signup_date_cleaning():
    df = pd.DataFrame({
        "full_name": ["A", "B"],
        "email": ["a@test.com", "b@test.com"],
        "signup_date": ["invalid_date", "2023-01-02"],
        "country": ["FR", "FR"],
        "age": [25, 30],
        "last_purchase_amount": [10, 20],
        "loyalty_tier": ["BRONZE", "GOLD"]
    })
    df_clean, _ = clean_customers(df)
    assert pd.api.types.is_datetime64_any_dtype(df_clean["signup_date"])
    assert df_clean["signup_date"].isna().sum() == 0

def test_age_clipping():
    df = pd.DataFrame({
        "full_name": ["A", "B"],
        "email": ["a@test.com", "b@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02"],
        "country": ["FR", "FR"],
        "age": [10, 150],
        "last_purchase_amount": [0, 10],
        "loyalty_tier": ["BRONZE", "BRONZE"]
    })
    df_clean, _ = clean_customers(df)
    assert df_clean["age"].min() >= 16
    assert df_clean["age"].max() <= 100

def test_purchase_amount_fix():
    df = pd.DataFrame({
        "full_name": ["A", "B"],
        "email": ["a@test.com", "b@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02"],
        "country": ["FR", "FR"],
        "age": [25, 30],
        "last_purchase_amount": [-50, np.nan],
        "loyalty_tier": ["BRONZE", "BRONZE"]
    })
    df_clean, _ = clean_customers(df)
    assert (df_clean["last_purchase_amount"] >= 0).all()
    assert df_clean["last_purchase_amount"].isna().sum() == 0

def test_loyalty_tier_unknown_to_bronze():
    df = pd.DataFrame({
        "full_name": ["A", "B"],
        "email": ["a@test.com", "b@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02"],
        "country": ["FR", "FR"],
        "age": [25, 30],
        "last_purchase_amount": [10, 20],
        "loyalty_tier": ["UNKNOWN", "GOLD"]
    })
    df_clean, _ = clean_customers(df)
    assert "UNKNOWN" not in df_clean["loyalty_tier"].values
    assert "BRONZE" in df_clean["loyalty_tier"].values

def test_duplicates_removed():
    df = pd.DataFrame({
        "full_name": ["A", "A"],
        "email": ["a@test.com", "a@test.com"],
        "signup_date": ["2023-01-01", "2023-01-01"],
        "country": ["FR", "FR"],
        "age": [25, 25],
        "last_purchase_amount": [10, 10],
        "loyalty_tier": ["BRONZE", "BRONZE"]
    })
    df_clean, _ = clean_customers(df)
    assert df_clean["email"].nunique() == 1

def test_no_duplicate_emails():
    df = pd.DataFrame({
        "full_name": ["A", "B", "C"],
        "email": ["a@test.com", "b@test.com", "a@test.com"],
        "signup_date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "country": ["FR", "FR", "FR"],
        "age": [25, 30, 40],
        "last_purchase_amount": [10, 20, 30],
        "loyalty_tier": ["BRONZE", "SILVER", "GOLD"]
    })
    df_clean, _ = clean_customers(df)
    assert df_clean["email"].duplicated().sum() == 0

def test_no_missing_values_after_cleaning():
    df = pd.DataFrame({
        "full_name": ["A", None, "C"],
        "email": ["a@test.com", "b@test.com", None],
        "signup_date": ["2023-01-01", None, "2023-01-03"],
        "country": ["FR", "FR", "USA"],
        "age": [25, 30, 40],
        "last_purchase_amount": [10, 20, np.nan],
        "loyalty_tier": ["BRONZE", "UNKNOWN", "GOLD"]
    })
    df_clean, _ = clean_customers(df)
    assert df_clean.isna().sum().sum() == 0

