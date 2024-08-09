import streamlit as st

# Configure the main page
st.set_page_config(
    page_title="Geospatial Tools",
    page_icon="🌍",
    layout="wide",
)

# Sidebar content
st.sidebar.markdown("# Main Page")
st.sidebar.info(
    """
    GitHub repository: [Streamlit Opensource GIS](https://github.com/rmkenv/OS-ST-GIS/)
    """
)
st.sidebar.markdown("# Contact")
st.sidebar.info(
    """
    - [Ryan Kmetz](https://ryankmetz.com/)
    - [LinkedIn](https://www.linkedin.com/in/ryankmetz/)
    """
)

# Main page content
st.markdown("## About")
st.write(
    """
    Welcome to the Open Source Web GIS tool. This tool is designed to help users visualize and interact with geospatial and tabular data in a seamless and intuitive way. Below is a description of the available pages and their functionalities:

    ### Vector Data Visualization 🌍
    **Purpose**: The Vector Data Visualization page allows users to upload, select, and explore various vector data formats such as CSV, XLSX, ZIP, and GEOJSON. This page is ideal for visualizing geospatial data points, lines, and polygons on an interactive map.

    **Key Features**:
    - **Upload Files**: Users can upload their own files in supported formats (CSV, XLSX, ZIP, GEOJSON).
    - **Select Pre-uploaded Files**: Users can choose from a set of pre-uploaded files available via a dropdown menu.
    - **Add URLs**: Enter WFS (Web Feature Service) or ArcREST URLs to load data directly from web services.
    - **View Interactive Map**: The map updates automatically to display data from the selected or uploaded files.
    - **Data Table**: The data associated with the map is displayed in a table below the map for easy viewing and analysis.

    ### Data Manipulation 📊
    **Purpose**: The Data Manipulation page provides users with tools to perform detailed analysis and manipulation of their data. This page is perfect for users who need to filter, transform, and export data for further analysis.

    **Key Features**:
    - **Upload and Select Files**: Similar to the Vector Data Visualization page, users can upload their own files or select from pre-uploaded options.
    - **Advanced Filtering**: Users can apply complex filters to the data to isolate specific subsets based on custom criteria.
    - **Interactive Map and Data Table**: The map and data table are dynamically linked, allowing users to see the impact of their filters in real-time.
    - **Download Filtered Data**: After manipulating the data, users can download the filtered dataset as a CSV file.

    ### CRS Transformer 🌐
    **Purpose**: The CRS Transformer page allows users to view the Coordinate Reference System (CRS) of their geospatial data, transform it to a new CRS, and download the transformed data as a GeoJSON file. This is particularly useful when working with geospatial data in different projections.

    **Key Features**:
    - **View Current CRS**: Users can upload or select a file to view its current CRS.
    - **Transform CRS**: Input a new CRS (e.g., EPSG:4326) to transform the data into the desired projection.
    - **Download Transformed Data**: After transformation, users can download the data as a GeoJSON file.

    ### Batch Geocoding 📍
    **Purpose**: The Batch Geocoding page allows users to upload a CSV file containing address information and automatically geocode these addresses to obtain latitude and longitude coordinates.

    **Key Features**:
    - **Upload CSV File**: Users can upload a CSV file with columns for street, city, and zip.
    - **Geocode Addresses**: The application geocodes each address to obtain latitude and longitude coordinates.
    - **View Geocoded Data**: The geocoded data, including latitude and longitude, is displayed in a table.
    - **Download Geocoded Data**: Users can download the geocoded dataset as a CSV file.

    ### How to Use
    1. **Uploading Files**: Navigate to the desired page and use the file uploader to add your data files. Supported formats include CSV, XLSX, ZIP, and GEOJSON.
    2. **Selecting Pre-uploaded Files**: If you prefer, select from the list of available pre-uploaded files using the dropdown menu.
    3. **Adding URLs**: Enter WFS or ArcREST URLs to load data directly from web services.
    4. **Viewing the Map**: The interactive map will automatically update to display the data from your selected or uploaded files.
    5. **Filtering Data**: Use the sidebar options to filter the data based on specific columns and values. This feature helps in focusing on the data points that matter most to you.
    6. **Geocoding Addresses**: Upload a CSV file with columns for street, city, and zip, then click the "Geocode" button to obtain latitude and longitude coordinates.
    7. **Transforming CRS**: Navigate to the CRS Transformer page, view the current CRS of your data, and input a new CRS to transform your data into a new projection. Download the transformed data as a GeoJSON file.
    8. **Downloading Data**: Once you are satisfied with your data visualization, filtering, geocoding, or CRS transformation, use the download button to export the data as a CSV or GeoJSON file.
    9. **Exploring the Data Table**: Scroll down to view the data table associated with the map or geocoded addresses. This table provides a detailed view of your data and can be used for further analysis.

    This application is built to be user-friendly and versatile, catering to both novice and advanced users who need to work with geospatial and tabular data. We hope you find it useful for your data exploration and analysis needs!

    **Shoutout**: This project was inspired by the great work done on [Streamlit Geospatial Tools](https://github.com/hossamhassan77/streamlit-geospatial-tools). Be sure to check it out for more awesome geospatial applications!

    ### 💻 Used Technology:
    - Streamlit
    - Pandas
    - Geopandas
    - Folium
    - Geopy
    """
)
