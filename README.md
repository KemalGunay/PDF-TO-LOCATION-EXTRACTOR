

# PDF Location Extractor  

🌍 **Extract and Map Locations from PDF Documents**  

This project is a Python-based application built with **Streamlit** to extract geographical entities (cities and countries) from PDF documents and map their coordinates on an interactive world map.  

![PDF Location Extractor Screenshot](/images/picture1.png)  
![PDF Location Extractor Screenshot](/images/picture2.png)
*Example visualization of extracted locations*  


---

## 🚀 Features  

- **PDF Parsing**: Reads text from uploaded PDF files using `PyPDF2`.  
- **NLP Entity Extraction**: Identifies location entities (GPE, LOC) using **spaCy**'s NLP pipeline.  
- **Location Matching**: Validates extracted locations against a world cities dataset.  
- **Geocoding**: Fetches precise latitude and longitude for matched locations using `Geopy`.  
- **Interactive Mapping**: Visualizes the geocoded locations on an interactive map with Streamlit.  
- **Secure API Requests**: Custom SSL handling ensures reliable performance for geocoding.  

---

## 🛠️ Tech Stack  

- **Languages**: Python  
- **Libraries**:  
  - PDF Parsing: `PyPDF2`  
  - Natural Language Processing: `spaCy`  
  - Geocoding: `Geopy`  
  - Data Processing: `Pandas`, `Numpy`  
  - Web App Framework: `Streamlit`  

---

## 🖥️ Installation  

Follow the steps below to run the project on your local machine:  

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/yourusername/pdf-location-extractor.git  
   cd pdf-location-extractor  
   ```  

2. **Create and activate a virtual environment:**  
   ```bash
   python -m venv env  
   source env/bin/activate  # For macOS/Linux
   env\Scripts\activate     # For Windows  
   ```  

3. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt  
   ```  

4. **Download the `en_core_web_sm` spaCy model:**  
   ```bash
   python -m spacy download en_core_web_sm  
   ```  

5. **Add the world cities dataset:**  
   - Download a `worldcities.xlsx` file in the repository  
   - Save it in the root directory of the project.  

---

## ▶️ Usage  

1. Run the Streamlit application:  
   ```bash
   streamlit run text-to-location.py
   ```  

2. Upload one or more PDF files through the interface.  

3. Select the checkbox to view extracted text (optional).  

4. View matched locations, their coordinates, and the interactive map.  

---

## 📂 Project Structure  

```
pdf-location-extractor/  
│  
├── text-to-location.py # Main Streamlit app   
├── worldcities.xlsx    # Dataset for city-country mapping  
└── README.md           # Project documentation  
```  

---

## 💡 Potential Use Cases  

- Extracting and mapping locations from research reports, legal contracts, or other documents.  
- Automating geographical insights for journalists or businesses.  
- Exploring location-based trends in unstructured text.  

---

## 🤝 Contributions  

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit an issue for discussion.  

---

## 📜 License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## 📬 Contact  

If you have any questions or suggestions, feel free to reach out:  

- **Name**: Kemal Gunay  
- **Email**: kemalgnay@gmail.com 
- **Website**: [gunaykemal.com](https://gunaykemal.com)  

---

Let me know if you'd like to customize this further or add anything!
