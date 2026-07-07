from services.bigquery_service import (
    load_crop_data,
    get_dashboard_stats,
)

print(get_dashboard_stats())

df = load_crop_data()

print(df.head())
print(df.shape)