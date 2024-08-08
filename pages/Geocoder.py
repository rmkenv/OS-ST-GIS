import streamlit as st
from geopy.geocoders import Nominatim
import pandas as pd

# Function to geocode an address
def geocode_address(address):
    geolocator = Nominatim(user_agent="streamlit_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Streamlit app
st.title("Batch Geocoding App")
st.write("Upload a CSV file with columns for street, city, and zip to get the geocoded latitude and longitude.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)
    
    # Check if necessary columns are present
    if all(col in df.columns for col in ['street', 'city', 'zip']):
        st.write("CSV file uploaded successfully. Here is a preview:")
        st.dataframe(df.head())
        
        if st.button("Geocode"):
            # Create new columns for latitude and longitude
            df['latitude'] = None
            df['longitude'] = None
            
            # Geocode each address
            for i, row in df.iterrows():
                address = f"{row['street']}, {row['city']}, {row['zip']}"
                lat, lon = geocode_address(address)
                df.at[i, 'latitude'] = lat
                df.at[i, 'longitude'] = lon
            
            st.success("Geocoding completed.")
            st.write("Here is a preview of the geocoded data:")
            st.dataframe(df.head())
            
            # Option to download the geocoded data
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download geocoded CSV",
                data=csv,
                file_name="geocoded_addresses.csv",
                mime="text/csv"
            )
    else:
        st.error("CSV file must contain 'street', 'city', and 'zip' columns.")
