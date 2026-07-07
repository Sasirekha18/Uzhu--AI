from services.bigquery_service import get_crop_data


def analyze_farm(
    state,
    district,
    crop,
    season,
    farm_size,
    budget,
    water,
):

    df = get_crop_data()

    farm = df[
        (df["State"] == state) &
        (df["District"] == district) &
        (df["Crop"] == crop)
    ]

    if farm.empty:

        return {
            "status": "warning",
            "message": "No historical data found.",
            "history": None,
        }

    return {

        "status": "success",

        "message": "Historical data analyzed successfully.",

        "history": {

            "production": farm["Production"].mean(),
            "yield": farm["Yield"].mean(),
            "area": farm["Area"].mean(),

        }

    }