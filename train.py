import pandas as pd
import numpy as np
import re
from scipy.special import expit


class AadhaarRiskEngine:
    def __init__(self):
        pass

    # -------------------------------
    # Utility functions
    # -------------------------------
    @staticmethod
    def clean_state(state):
        state = str(state).upper()
        state = state.replace("&", "AND")
        state = re.sub(r"[^A-Z ]", "", state)
        state = re.sub(r"\s+", " ", state)
        state = re.sub(r"^THE\s+", "", state)
        return state.strip()

    @staticmethod
    def parse_date(series):
        return pd.to_datetime(
            series,
            format="mixed",
            dayfirst=True,
            errors="coerce"
        )

    # -------------------------------
    # Load & prepare datasets
    # -------------------------------
    def load_enrolment(self, paths):
        df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)

        df["date"] = self.parse_date(df["date"])
        df["state"] = df["state"].apply(self.clean_state)

        df["total_enrolment"] = (
            df["age_0_5"] +
            df["age_5_17"] +
            df["age_18_greater"]
        )

        df = df.sort_values(["pincode", "date"])
        df["enrol_velocity"] = df.groupby("pincode")["total_enrolment"].diff().fillna(0)

        df["enrol_zscore"] = (
            (df["total_enrolment"] - df["total_enrolment"].mean())
            / df["total_enrolment"].std()
        )

        return df

    def load_demographic(self, paths):
        df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)

        df["date"] = self.parse_date(df["date"])
        df["state"] = df["state"].apply(self.clean_state)

        df["demo_total"] = df["demo_age_5_17"] + df["demo_age_17_"]

        df = df.sort_values(["pincode", "date"])
        df["demo_velocity"] = df.groupby("pincode")["demo_total"].diff().fillna(0)

        df["demo_zscore"] = (
            (df["demo_total"] - df["demo_total"].mean())
            / df["demo_total"].std()
        )

        return df

    def load_biometric(self, paths):
        df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)

        df["date"] = self.parse_date(df["date"])
        df["state"] = df["state"].apply(self.clean_state)

        df["bio_total"] = df["bio_age_5_17"] + df["bio_age_17_"]

        df = df.sort_values(["pincode", "date"])
        df["bio_velocity"] = df.groupby("pincode")["bio_total"].diff().fillna(0)

        df["bio_zscore"] = (
            (df["bio_total"] - df["bio_total"].mean())
            / df["bio_total"].std()
        )

        return df

    # -------------------------------
    # Merge datasets
    # -------------------------------
    def merge_all(self, enrol_df, demo_df, bio_df):
        df = enrol_df.merge(
            demo_df[["date", "pincode", "demo_total", "demo_velocity", "demo_zscore"]],
            on=["date", "pincode"],
            how="left"
        )

        df = df.merge(
            bio_df[["date", "pincode", "bio_total", "bio_velocity", "bio_zscore"]],
            on=["date", "pincode"],
            how="left"
        )

        return df.fillna(0)

    # -------------------------------
    # Risk Engine
    # -------------------------------
    def compute_risk(self, df):
        for col in [
            "enrol_velocity", "demo_velocity", "bio_velocity",
            "enrol_zscore", "demo_zscore", "bio_zscore"
        ]:
            df[col] = df[col].clip(-10, 10)

        df["enrol_risk"] = expit(df["enrol_velocity"] + df["enrol_zscore"])
        df["demo_risk"] = expit(df["demo_velocity"] + df["demo_zscore"])
        df["bio_risk"] = expit(df["bio_velocity"] + df["bio_zscore"])

        df["final_risk_score"] = (
            0.4 * df["bio_risk"] +
            0.35 * df["enrol_risk"] +
            0.25 * df["demo_risk"]
        ) * 100

        df["risk_level"] = df["final_risk_score"].apply(
            lambda x: "HIGH" if x >= 80 else "MEDIUM" if x >= 50 else "LOW"
        )

        df["risk_reason"] = df.apply(self._risk_reason, axis=1)

        return df

    @staticmethod
    def _risk_reason(row):
        reasons = []
        if row["bio_risk"] > 0.7:
            reasons.append("BIOMETRIC SPIKE")
        if row["enrol_risk"] > 0.7:
            reasons.append("ENROLMENT SPIKE")
        if row["demo_risk"] > 0.7:
            reasons.append("DEMOGRAPHIC SPIKE")
        return ", ".join(reasons)
