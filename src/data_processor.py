# Data processing
from datetime import datetime
import pandas as pd

def filter_date_range(data, start_date, end_date):
    try:
        # Convert date inputs
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            raise ValueError("End date cannot be before start date.")

        # --- Handle both dicts and DataFrames ---
        if isinstance(data, dict):
            # Convert dict → DataFrame
            df = pd.DataFrame.from_dict(data, orient="index")
            df.index.name = "date"

            # Convert index to datetime (skip keys that aren't dates)
            try:
                df.index = pd.to_datetime(df.index, errors="coerce")
                df = df[df.index.notna()]
            except Exception:
                raise ValueError("Could not parse date index from data.")

            # Convert all numeric columns to float where possible
            for col in df.columns:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass

        elif isinstance(data, pd.DataFrame):
            df = data.copy()

        else:
            raise TypeError("Unsupported data type received. Expected dict or DataFrame.")

        # Filter date range
        filtered = df.loc[(df.index >= start) & (df.index <= end)]

        if filtered.empty:
            print(f"No data found between {start_date} and {end_date}.")
        return filtered

    except Exception as e:
        print(f"Error filtering data range: {e}")
        return pd.DataFrame()