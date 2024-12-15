import re
import PyPDF2
import spacy
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
import streamlit as st

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# Function to extract place names using spaCy
def extract_place_names(text):
    doc = nlp(text)
    places = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    return list(set(places))  # Return unique place names

# Function to get coordinates for a place name
def get_coordinates(place_name, country=None):
    geolocator = Nominatim(user_agent="place_locator")
    try:
        location = geolocator.geocode(f"{place_name}, {country}" if country else place_name)
        if location:
            return location.latitude, location.longitude
        else:
            st.warning(f"Could not find coordinates for: {place_name}")
    except GeopyError as e:
        st.error(f"Geopy error for {place_name}: {e}")
    return None

# Streamlit app
def main():
    st.title("Place Name Extractor and Geolocator")

    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

    country = st.text_input("Specify a country to narrow results (optional)")

    if uploaded_file is not None:
        st.write("Extracting text from the PDF...")
        text = extract_text_from_pdf(uploaded_file)

        st.write("Extracting place names...")
        place_names = extract_place_names(text)

        st.write(f"Extracted places: {place_names}")

        st.write("Finding coordinates for the places...")
        place_coordinates = {}
        for place in place_names:
            coordinates = get_coordinates(place, country)
            if coordinates:
                place_coordinates[place] = coordinates

        st.write("\nPlace coordinates:")
        for place, coords in place_coordinates.items():
            st.write(f"{place}: {coords}")

if __name__ == "__main__":
    main()
