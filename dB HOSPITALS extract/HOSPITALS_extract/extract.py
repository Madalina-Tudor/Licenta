import geopandas as gpd
import pandas as pd
from unidecode import unidecode

# Load the shapefile
# Update the shapefile path
shapefile_path = "C:/Users/madal/OneDrive/Desktop/licent/.SERVICII/dB HOSPITALS extract/hotosm_rou_health_facilities_points_shp/hotosm_rou_health_facilities_points_shp.shp"
gdf = gpd.read_file(shapefile_path)

# Extract latitude and longitude from geometry
gdf['longitude'] = gdf.geometry.x
gdf['latitude'] = gdf.geometry.y

# Drop the original geometry column
gdf = gdf.drop(columns=['geometry'])

# Function to correct text encoding
def correct_encoding(text):
    return unidecode(text)

# Apply encoding correction to all object columns
for col in gdf.select_dtypes(include=['object']).columns:
    gdf[col] = gdf[col].apply(lambda x: correct_encoding(x) if isinstance(x, str) else x)

# Save to CSV with UTF-8 encoding
csv_output_path = "C:/Users/madal/OneDrive/Desktop/licent/.SERVICII/dB HOSPITALS extract/hospitals_corrected1.csv"
gdf.to_csv(csv_output_path, index=False, encoding='utf-8')

print(f"CSV file saved to {csv_output_path}")

# Filter the data to only include hospitals from Brasov
gdf_brasov = gdf[(gdf['addr_city'] == 'Brasov') & (gdf['healthcare'].isin(['hospital', 'pharmacy']))]

# Save to CSV with UTF-8 encoding
csv_output_path_brasov = "C:/Users/madal/OneDrive/Desktop/licent/.SERVICII/dB HOSPITALS extract/hospitals_brasov.csv"
gdf_brasov.to_csv(csv_output_path_brasov, index=False, encoding='utf-8')

print(f"CSV file saved to {csv_output_path_brasov}")