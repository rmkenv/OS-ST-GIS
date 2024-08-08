import json
import requests
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import tempfile

class GeoDataVisualizer:
    def __init__(self):
        self.map = folium.Map(location=[39.0458, -76.6413], zoom_start=7)  # Centered on Maryland
        self.marker_cluster = MarkerCluster().add_to(self.map)
        self.uploaded_files = []
        self.selected_files = []
        self.data_frames = []
        self.latitude_column = None
        self.longitude_column = None
        self.github_files = {}
        self.temp_dir = tempfile.TemporaryDirectory()
        self._setup_page()

    def _setup_page(self):
        st.set_page_config(page_title="Data Visualization", layout="wide", page_icon="🛰️")
        st.sidebar.markdown("# Vector Data Visualization 🛰️")
        with st.sidebar.expander("User Instructions"):
            st.markdown("""
            ### Instructions:
            1. **Upload Files**: Use the uploader to add your own files in CSV, XLSX, ZIP, or GEOJSON formats.
            2. **Select Files**: Alternatively, select from pre-uploaded files using the dropdown menu.
            3. **View Map**: The map will automatically update to display the data from the selected or uploaded files.
            4. **Data Table**: The data associated with the map will be displayed below the map.
            """)
        self._get_files()
        if self.uploaded_files or self.selected_files:
            self._load_data()
            self._save_data()
            self._display_layout()

    def _get_files(self):
        uploaded_files = st.file_uploader("Upload one or more files", type=["csv", "xlsx", "zip", "geojson"], accept_multiple_files=True)
        if uploaded_files:
            self.uploaded_files = uploaded_files
        st.write("Or")
        file_options = self._fetch_github_files()
        if file_options:
            selected_files = st.multiselect("Choose one or more options", list(file_options.keys()))
            self.selected_files = [file_options[file_name] for file_name in selected_files]

    def _fetch_github_files(self):
        url = "https://api.github.com/repos/MEADecarb/st-gis/contents/data"
        response = requests.get(url)
        if response.status_code == 200:
            self.github_files = {file_info['name']: file_info['download_url'] for file_info in response.json() if file_info['name'].endswith(('.csv', '.geojson', '.xlsx', '.zip'))}
            return self.github_files
        else:
            return {}

    def _load_data(self):
        all_files = self.uploaded_files + self.selected_files
        if all_files:
            for file in all_files:
                if isinstance(file, str):
                    self._load_data_from_url(file)
                else:
                    self._load_data_from_file(file)
            self._fit_map_to_all_bounds()
            folium.LayerControl().add_to(self.map)
            folium_static(self.map, width=1000)
            self._display_all_data()

    def _load_data_from_url(self, url):
        extension = url.split(".")[-1]
        layer_name = url.split('/')[-1].split('.')[0]
        if extension == "geojson":
            data_frame = gpd.read_file(url)
            self.data_frames.append(data_frame)
            json_data_frame = json.loads(data_frame.to_json())
            self._add_geojson_layer(json_data_frame, layer_name)
        elif extension in {"csv", "xlsx"}:
            data_frame = self._load_tabular_data(url, extension)
            self.data_frames.append(data_frame)
            self._add_markers(data_frame)
        else:
            st.write("Unsupported URL format or unable to load data.")

    def _load_data_from_file(self, uploaded_file):
        extension = uploaded_file.name.split(".")[-1]
        if extension in {"csv", "xlsx"}:
            data_frame = self._load_tabular_data(uploaded_file, extension)
            self.data_frames.append(data_frame)
            self._add_markers(data_frame)
        else:
            data_frame = gpd.read_file(uploaded_file)
            self.data_frames.append(data_frame)
            layer_name = uploaded_file.name.split(".")[0]
            json_data_frame = json.loads(data_frame.to_json())
            self._add_geojson_layer(json_data_frame, layer_name)

    def _load_tabular_data(self, file, extension):
        if extension == "csv":
            data_frame = pd.read_csv(file)
        else:
            data_frame = pd.read_excel(file, engine="openpyxl")

        self.latitude_column, self.longitude_column = self._select_lat_long_columns(data_frame)

        data_frame = gpd.GeoDataFrame(
            data_frame,
            geometry=gpd.points_from_xy(
                data_frame[self.longitude_column],
                data_frame[self.latitude_column],
            ),
            crs="wgs84",
        ).dropna(subset=[self.longitude_column, self.latitude_column])

        return data_frame

    def _select_lat_long_columns(self, data_frame):
        col1, col2 = st.columns(2)

        with col1:
            lat_index = self._get_column_index(data_frame, "lat|latitude")
            latitude_column = st.selectbox(
                "Choose latitude column:", data_frame.columns, index=lat_index
            )
        with col2:
            lng_index = self._get_column_index(data_frame, "lng|long|longitude")
            longitude_column = st.selectbox(
                "Choose longitude column:", data_frame.columns, index=lng_index
            )

        return latitude_column, longitude_column

    def _get_column_index(self, data_frame, pattern):
        column_guess = data_frame.columns.str.contains(pattern, case=False)
        if column_guess.any():
            return data_frame.columns.get_loc(data_frame.columns[column_guess][0])
        return 0

    def _add_geojson_layer(self, json_data_frame, layer_name):
        if "features" in json_data_frame and json_data_frame["features"]:
            property_keys = list(json_data_frame["features"][0]["properties"].keys())
            folium.GeoJson(
                json_data_frame,
                name=layer_name,
                zoom_on_click=True,
                highlight_function=lambda feature: {"fillColor": "dark gray"},
                popup=folium.GeoJsonPopup(
                    fields=property_keys,
                    aliases=property_keys,
                    localize=True,
                    style="max-height: 200px; overflow-y: auto;",
                ),
            ).add_to(self.map)
        else:
            folium.GeoJson(json_data_frame, name=layer_name, zoom_on_click=True).add_to(self.map)

    def _fit_map_to_bounds(self, bounds):
        self.map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    def _fit_map_to_all_bounds(self):
        if self.data_frames:
            combined_bounds = None
            for data_frame in self.data_frames:
                if combined_bounds is None:
                    combined_bounds = data_frame.total_bounds
                else:
                    combined_bounds[0] = min(combined_bounds[0], data_frame.total_bounds[0])
                    combined_bounds[1] = min(combined_bounds[1], data_frame.total_bounds[1])
                    combined_bounds[2] = max(combined_bounds[2], data_frame.total_bounds[2])
                    combined_bounds[3] = max(combined_bounds[3], data_frame.total_bounds[3])
            self._fit_map_to_bounds(combined_bounds)

    def _add_markers(self, data_frame):
        for _, row in data_frame.iterrows():
            popup_html = self.create_popup_html(row[:-1])
            folium.Marker(
                location=[row[self.latitude_column], row[self.longitude_column]],
                popup=folium.Popup(popup_html, max_width=300),
            ).add_to(self.marker_cluster)

    def _display_data(self, data_frame):
        st.dataframe(data_frame.drop(columns="geometry"))

    def _display_all_data(self):
        for data_frame in self.data_frames:
            self._display_data(data_frame)

    def create_popup_html(self, properties):
        html = "<div style='max-height: 200px; overflow-y: auto;'>"
        for key, value in properties.items():
            html += f"<b>{key}</b>: {value}<br>"
        html += "</div>"
        return html

    def _save_data(self):
        combined_data = pd.concat(self.data_frames, ignore_index=True)
        save_path = f"{self.temp_dir.name}/combined_data.csv"
        combined_data.to_csv(save_path, index=False)

    def _display_layout(self):
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("## Map")
            folium_static(self.map, width=1000)

        with col2:
            st.markdown("## Data Table")
            if not self.data_frames:
                st.write("No data available")
            else:
                st.dataframe(self.data_frame.drop(columns="geometry"))
                st.download_button(
                    label="Download data as CSV",
                    data=self.data_frame.to_csv().encode("utf-8"),
                    file_name="Streamlit_df.csv",
                    mime="text/csv",
                )

if __name__ == "__main__":
    GeoDataVisualizer()
