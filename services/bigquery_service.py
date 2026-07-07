from google.cloud import bigquery
import pandas as pd
import streamlit as st

PROJECT_ID = "uzhu-ai-2026"
DATASET_ID = "uzhu_ai"
TABLE_ID = "crop_production"

client = bigquery.Client(project=PROJECT_ID)


@st.cache_data
def get_dashboard_stats():

    query = f"""
    SELECT
        COUNT(DISTINCT State) AS states,
        COUNT(DISTINCT District) AS districts,
        COUNT(DISTINCT Crop) AS crops,
        COUNT(*) AS records
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    df = client.query(query).to_dataframe()

    return {
        "states": int(df.iloc[0]["states"]),
        "districts": int(df.iloc[0]["districts"]),
        "crops": int(df.iloc[0]["crops"]),
        "records": int(df.iloc[0]["records"]),
    }


@st.cache_data
def get_crop_data():

    query = f"""
    SELECT
        State,
        District,
        Crop,
        Crop_Year,
        Season,
        Area,
        Production,
        Yield
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    return client.query(query).to_dataframe()


@st.cache_data
def get_state_list():

    query = f"""
    SELECT DISTINCT State
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY State
    """

    return client.query(query).to_dataframe()["State"].tolist()


@st.cache_data
def get_crop_list():

    query = f"""
    SELECT DISTINCT Crop
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY Crop
    """

    return client.query(query).to_dataframe()["Crop"].tolist()


@st.cache_data
def get_year_list():

    query = f"""
    SELECT DISTINCT Crop_Year
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY Crop_Year
    """

    return client.query(query).to_dataframe()["Crop_Year"].tolist()

@st.cache_data
def get_states():

    query = f"""
    SELECT DISTINCT State
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY State
    """

    return client.query(query).to_dataframe()["State"].tolist()

@st.cache_data
def get_districts(state):

    query = f"""
    SELECT DISTINCT District
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE State=@state
    ORDER BY District
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "state",
                "STRING",
                state
            )
        ]
    )

    return (
        client.query(
            query,
            job_config=job_config
        )
        .to_dataframe()["District"]
        .tolist()
    )

@st.cache_data
def get_crops():

    query = f"""
    SELECT DISTINCT Crop
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY Crop
    """

    return client.query(query).to_dataframe()["Crop"].tolist()

@st.cache_data
def get_seasons():

    query = f"""
    SELECT DISTINCT Season
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY Season
    """

    return client.query(query).to_dataframe()["Season"].tolist()

@st.cache_data
def get_years():

    query = f"""
    SELECT DISTINCT Crop_Year
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    ORDER BY Crop_Year
    """

    return client.query(query).to_dataframe()["Crop_Year"].tolist()

@st.cache_data
def get_crop_data_filtered(state, crop):

    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    WHERE State=@state
    AND Crop=@crop
    ORDER BY Crop_Year
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "state",
                "STRING",
                state
            ),
            bigquery.ScalarQueryParameter(
                "crop",
                "STRING",
                crop
            )
        ]
    )

    return client.query(
        query,
        job_config=job_config
    ).to_dataframe()