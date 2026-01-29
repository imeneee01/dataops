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
    report = {}

    report["rows_input"] = len(df)

    # full_name
    report["empty_full_name"] = (df["full_name"] == " ").sum()
    df["full_name"] = df["full_name"].replace(" ", np.nan)

    # email
    invalid_email_mask = ~df["email"].str.match(EMAIL_REGEX, na=False)
    report["invalid_emails"] = invalid_email_mask.sum()
    df.loc[invalid_email_mask, "email"] = np.nan

    # signup_date
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    report["invalid_signup_dates"] = df["signup_date"].isna().sum()
    median_date = df["signup_date"].median()
    df["signup_date"] = df["signup_date"].fillna(median_date).dt.normalize()

    # country
    df["country"] = df["country"].astype(str).str.upper().replace(COUNTRY_STANDARD)

    # age
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    report["age_clipped_min"] = (df["age"] < 16).sum()
    report["age_clipped_max"] = (df["age"] > 100).sum()
    df.loc[df["age"] < 16, "age"] = 16
    df.loc[df["age"] > 100, "age"] = 100
    df["age"] = df["age"].astype("Int64")

    # last_purchase_amount
    df["last_purchase_amount"] = pd.to_numeric(df["last_purchase_amount"], errors="coerce")
    report["negative_purchase_fixed"] = (df["last_purchase_amount"] < 0).sum()
    df.loc[df["last_purchase_amount"] < 0, "last_purchase_amount"] = 0
    df["last_purchase_amount"] = df["last_purchase_amount"].fillna(0.0)

    # loyalty_tier
    report["unknown_loyalty"] = (df["loyalty_tier"] == "UNKNOWN").sum()
    df["loyalty_tier"] = df["loyalty_tier"].astype(str).replace("UNKNOWN", "BRONZE")

    # duplicates
    report["duplicates_removed"] = df.duplicated(subset=["email"]).sum()
    df = df.drop_duplicates(subset=["email"])

    # dropna final
    before_dropna = len(df)
    df = df.dropna()
    report["rows_dropped_na"] = before_dropna - len(df)

    report["rows_output"] = len(df)
    report["rows_dropped"] = report["rows_input"] - report["rows_output"]

    return df, report