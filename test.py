import streamlit as st
import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
import spacy
import ssl
import certifi
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim


# Custom SSL context to resolve certificate verification issues
def create_ssl_context():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return ssl_context


# Function to find coordinates with improved error handling
def findGeocode(city, country, admin_name=None):
    try:
        # Create a custom SSL context
        ssl_context = create_ssl_context()

        # Initialize geolocator with custom SSL context
        geolocator = Nominatim(
            user_agent="pdf_location_extractor",
            ssl_context=ssl_context
        )

        # Construct search query with additional context if available
        if admin_name and pd.notna(admin_name):
            search_query = f"{city}, {admin_name}, {country}"
        else:
            search_query = f"{city}, {country}"

        # Attempt to geocode with a timeout
        location = geolocator.geocode(search_query, timeout=10)
        return location

    except (GeocoderTimedOut, GeocoderUnavailable, ssl.SSLError) as e:
        st.warning(f"Geocoding error for {search_query}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error geocoding {search_query}: {str(e)}")
        return None


# Streamlit application
st.title("PDF Location Extractor")
st.write("Upload PDFs to extract location entities and map their coordinates.")

# File uploader
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    text = ""
    for uploaded_file in uploaded_files:
        # Read the uploaded PDF
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    # Display extracted text if user wants to see it
    if st.checkbox("Show extracted text"):
        st.write(text)

    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract location entities
    st.write("### Extracting Location Entities")
    places = []

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            places.append(ent.text)

    # Filter unique locations
    places = list(set(places))

    # Load world cities data
    st.write("### Checking Extracted Places with World Cities Data")
    world_cities = pd.read_excel("/Users/kemalgunay/Desktop/VERI_BILIMI/PDF-TO-LOCATION/worldcities.xlsx")

    # Ensure consistent column names and types
    world_cities = world_cities.copy()

    # Fill NaN values for admin_name if not present
    if 'admin_name' not in world_cities.columns:
        world_cities['admin_name'] = np.nan

    # Normalize city names for matching
    world_cities['city_lower'] = world_cities['city'].str.lower()

    # Match extracted places with world cities
    matched_places_list = []

    for place in places:
        # Find matches, case-insensitive
        city_matches = world_cities[world_cities['city_lower'] == place.lower()]

        if not city_matches.empty:
            for _, match in city_matches.iterrows():
                # Create a dictionary with location details
                matched_place = {
                    'city': match['city'],
                    'country': match['country'],
                    'admin_name': match.get('admin_name', np.nan),
                    'context': f"{match['city']}, {match.get('admin_name', 'N/A')}, {match['country']}"
                }
                matched_places_list.append(matched_place)

    # Convert to DataFrame
    if matched_places_list:
        matched_places_df = pd.DataFrame(matched_places_list)

        st.write("Matched Places:")
        st.dataframe(matched_places_df[['city', 'country', 'admin_name']])

        # Fetch coordinates for matched places
        st.write("### Fetching Coordinates")
        coordinates_data = []

        for _, row in matched_places_df.iterrows():
            loc = findGeocode(row['city'], row['country'], row['admin_name'])

            # Prepare coordinate data
            coord_entry = row.to_dict()
            if loc:
                coord_entry['lat'] = loc.latitude
                coord_entry['lon'] = loc.longitude
            else:
                coord_entry['lat'] = np.nan
                coord_entry['lon'] = np.nan

            coordinates_data.append(coord_entry)

        # Create DataFrame of matches with coordinates
        matched_coords_df = pd.DataFrame(coordinates_data)

        # Drop rows with missing coordinates
        matched_coords_df_clean = matched_coords_df.dropna(subset=['lat', 'lon'])

        st.write("Places with Coordinates:")
        st.dataframe(matched_coords_df[['city', 'country', 'admin_name', 'lat', 'lon']])

        # Map the locations
        st.write("### Map of Locations")
        if not matched_coords_df_clean.empty:
            st.map(matched_coords_df_clean)
        else:
            st.write("No valid coordinates to display on the map.")
    else:
        st.write("No matching places found in the world cities dataset.")