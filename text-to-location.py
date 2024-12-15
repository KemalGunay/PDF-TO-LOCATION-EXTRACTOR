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
def findGeocode(city, country):
    try:
        # Create a custom SSL context
        ssl_context = create_ssl_context()

        # Initialize geolocator with custom SSL context
        geolocator = Nominatim(
            user_agent="pdf_location_extractor",
            ssl_context=ssl_context
        )

        # Attempt to geocode with a timeout
        location = geolocator.geocode(f"{city}, {country}", timeout=10)
        return location

    except (GeocoderTimedOut, GeocoderUnavailable, ssl.SSLError) as e:
        st.warning(f"Geocoding error for {city}, {country}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error geocoding {city}, {country}: {str(e)}")
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

    # Match extracted places with world cities (city and country)
    matched_places = world_cities[world_cities["city"].isin(places)][['city', 'country']]
    matched_places.drop_duplicates(inplace=True)

    st.write("Matched Places:")
    st.dataframe(matched_places)

    # Fetch coordinates for matched places
    st.write("### Fetching Coordinates")
    longitude = []
    latitude = []

    for index, row in matched_places.iterrows():
        loc = findGeocode(row['city'], row['country'])
        if loc:
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)

    # Add coordinates to the DataFrame
    matched_places["lat"] = latitude
    matched_places["lon"] = longitude

    # Drop rows with missing coordinates
    matched_places_with_coords = matched_places.dropna(subset=["lat", "lon"])

    st.write("Places with Coordinates:")
    st.dataframe(matched_places)

    # Map the locations
    st.write("### Map of Locations")
    if not matched_places_with_coords.empty:
        st.map(matched_places_with_coords)
    else:
        st.write("No valid coordinates to display on the map.")