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
        ssl_context = create_ssl_context()
        geolocator = Nominatim(
            user_agent="pdf_location_extractor",
            ssl_context=ssl_context
        )
        location = geolocator.geocode(f"{city}, {country}", timeout=10)
        return location
    except (GeocoderTimedOut, GeocoderUnavailable, ssl.SSLError) as e:
        st.warning(f"Geocoding error for {city}, {country}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error geocoding {city}, {country}: {str(e)}")
        return None


def main():
    st.title("PDF Location Extractor")
    st.write("Upload PDFs to extract location entities and map their coordinates.")

    # File uploader
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        # Load SpaCy model
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("SpaCy model not found. Please download it using 'python -m spacy download en_core_web_sm'")
            return

        # Extract text from PDFs
        text = ""
        for uploaded_file in uploaded_files:
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()

        # Display extracted text option
        if st.checkbox("Show extracted text"):
            st.write(text)

        # Process text with SpaCy
        doc = nlp(text)

        # Extract location entities
        st.write("### Extracting Location Entities")
        places = list(set([ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]))

        # Load world cities data (consider using a more flexible data loading method)
        try:
            world_cities = pd.read_excel("worldcities.xlsx")  # Use relative path
        except FileNotFoundError:
            st.error("World cities data file not found. Please ensure 'worldcities.xlsx' is in the project directory.")
            return

        # Match extracted places with world cities
        matched_places = world_cities[world_cities["city"].isin(places)][['city', 'country']].drop_duplicates()

        st.write("Matched Places:")
        st.dataframe(matched_places)

        # Fetch coordinates
        st.write("### Fetching Coordinates")
        coords_data = []
        for _, row in matched_places.iterrows():
            loc = findGeocode(row['city'], row['country'])
            if loc:
                coords_data.append({
                    'city': row['city'],
                    'country': row['country'],
                    'lat': loc.latitude,
                    'lon': loc.longitude
                })

        # Create DataFrame with coordinates
        matched_places_with_coords = pd.DataFrame(coords_data)

        st.write("Places with Coordinates:")
        st.dataframe(matched_places_with_coords)

        # Map the locations
        st.write("### Map of Locations")
        if not matched_places_with_coords.empty:
            st.map(matched_places_with_coords)
        else:
            st.write("No valid coordinates to display on the map.")


if __name__ == "__main__":
    main()