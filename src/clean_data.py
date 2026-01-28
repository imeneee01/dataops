import pandas as pd
import numpy as np

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

COUNTRY_STANDARD = {
    "FRANCE": "FR",
    "FRA": "FR",
    "USA": "US"
}

def clean_customers(input_df):

    df = input_df.copy()

    # full_name
    df["full_name"] = df["full_name"].replace(" ", np.nan)

    # email
    df.loc[
        ~df["email"].str.contains("@", na=False),
        "email"
    ] = df["email"].str.replace(
        "example.com", "@example.com", regex=False
    )
    df["email"] = df["email"].where(
        df["email"].str.match(EMAIL_REGEX, na=False)
    )

    # signup_date
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    median_date = df["signup_date"].median()
    df["signup_date"] = df["signup_date"].fillna(median_date).dt.normalize()

    # country
    df["country"] = df["country"].astype(str).str.upper().replace(COUNTRY_STANDARD)

    # age
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[df["age"] < 16, "age"] = 16
    df.loc[df["age"] > 100, "age"] = 100
    df["age"] = df["age"].astype("Int64")

    # last_purchase_amount
    df["last_purchase_amount"] = pd.to_numeric(df["last_purchase_amount"], errors="coerce")
    df.loc[df["last_purchase_amount"] < 0, "last_purchase_amount"] = 0
    df["last_purchase_amount"] = df["last_purchase_amount"].fillna(0.0)

    # loyalty_tier
    df["loyalty_tier"] = df["loyalty_tier"].astype(str).replace("UNKNOWN", "BRONZE")

    df = df.drop_duplicates(subset=["email"])
    df = df.dropna()
    
    return df
