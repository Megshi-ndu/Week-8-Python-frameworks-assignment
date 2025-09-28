# Week-8-Python-frameworks-assignment

CORD-19 Data Explorer
A Streamlit web application for exploring and analyzing the CORD-19 COVID-19 research dataset. This interactive tool provides insights into research trends, publication patterns, and content analysis of scientific papers related to COVID-19.

https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white
https://img.shields.io/badge/Matplotlib-%2523ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black

📋 Table of Contents
Features

Installation

Usage

Dataset

Project Structure

Configuration

Technical Details

Troubleshooting

Contributing

License

✨ Features
📊 Data Analysis
Dataset Overview: Basic statistics including total papers, columns, and unique journals

Missing Data Analysis: Identify and handle missing values in the dataset

Interactive Filtering: Filter data by year range and customize visualization parameters

📈 Visualizations
Publications Timeline: Track COVID-19 research publications over time

Journal Analysis: Identify top journals publishing COVID-19 research

Word Frequency Analysis: Most common words in paper titles with interactive charts

Word Cloud: Visual representation of frequently used terms in research titles

Source Distribution: Analysis of paper sources and origins

🔧 Interactive Components
Sidebar Controls: Adjust year ranges and display settings

Dynamic Charts: Responsive visualizations that update in real-time

Data Sampling: Interactive data preview with adjustable sample sizes

Error Handling: Robust error handling for various data scenarios

🚀 Installation
Prerequisites
Python 3.7 or higher
pip (Python package installer)

Step-by-Step Setup

1. Clone or download the project files

git clone <repository-url>
cd cord-19-explorer

2. Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install required packages

pip install -r requirements.txt

If you don't have a requirements.txt file, install dependencies manually:

pip install streamlit pandas numpy matplotlib seaborn wordcloud

4. Download the CORD-19 dataset

Visit the CORD-19 dataset page

Download the metadata.csv file

Place it in the same directory as the Python script

📁 Project Structure

text

cord-19-explorer/
│
├── app.py                 # Main Streamlit application
├── metadata.csv           # CORD-19 dataset (to be downloaded)
├── requirements.txt       # Python dependencies
└── README.md             # This file

🎯 Usage
Start the application

In terminal (powershell), type : PS C:\Users\PC\Desktop\Python\PYTHON ASSIGNMENTS\Week 8 assignment\Week-8-Python-frameworks-assignment> streamlit run main.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.100.17:8501

bash
streamlit run app.py
Access the web interface

Open your web browser

Navigate to http://localhost:8501

Explore the data

Use the sidebar to adjust settings

Interact with various sections and visualizations

Filter data by year range and other parameters

Application Sections

Dataset Overview: Basic statistics and data preview

Publications Over Time: Timeline analysis of research output

Top Journals: Leading publishers in COVID-19 research

Word Frequency: Analysis of common terms in paper titles

Word Cloud: Visual word frequency representation

Source Distribution: Analysis of data sources

Sample Data: Interactive data exploration

📊 Dataset

The application uses the CORD-19 (COVID-19 Open Research Dataset) metadata file which includes:

Paper Titles: Research paper titles

Authors: Author information

Publication Dates: When papers were published

Journal Information: Where papers were published

Abstracts: Paper summaries (when available)

DOIs and IDs: Unique identifiers

Source Information: Data source origins

***Expected Columns

title, authors, journal, publish_time

doi, pmcid, pubmed_id, abstract

source_x, url, sha, and various ID fields

⚙️ Configuration

Sidebar Settings

Year Range Slider: Filter publications by publication year

Top N Journals: Control how many top journals to display

Sample Size: Adjust the number of rows shown in data preview

***Customization Options

The code can be easily modified to:

Add new visualizations

Change color schemes

Include additional data analysis features

Modify text processing parameters

🔧 Technical Details

Key Functions

handle_missing(): Robust missing data handling with column-specific replacements

load_and_process_data(): Cached data loading with error handling

Dynamic Visualization: Real-time chart updates based on user input

***Data Processing Pipeline

Data Loading: CSV file ingestion with memory optimization

Missing Value Handling: Intelligent filling of NaN values

Date Processing: Proper datetime conversion and validation

Text Analysis: Title processing for word frequency and cloud generation

*Visualization: Matplotlib and Seaborn-based chart generation

***Dependencies

python
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
wordcloud>=1.8.0

🐛 Troubleshooting
Common Issues

**File Not Found Error

**Error: Could not find metadata.csv file

Solution: Ensure metadata.csv is in the same directory as the script

**Memory Issues with Large Datasets

Solution: The code includes low_memory=False and can handle large files

** Module Import Errors

pip install --upgrade streamlit pandas matplotlib seaborn wordcloud

**Date Parsing Errors

Solution: The application includes robust datetime error handling

**Column Not Found Warnings

Solution: The code includes fallback mechanisms for missing columns

**Performance Tips

For very large datasets, consider using a subset of the data

Close other memory-intensive applications when running the tool

Use the sampling features to preview data without loading everything


Development Setup

Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

📄 License

This project is intended for educational and research purposes. The CORD-19 dataset is provided by the Allen Institute for AI under specific terms of use. Please refer to the official CORD-19 dataset page for licensing details.

🙏 Acknowledgments


CORD-19 Dataset: Allen Institute for AI and collaborating organizations

Streamlit: For the excellent web application framework

Python Community: For the robust data science ecosystem

📞 Support
If you encounter any issues or have questions:

Check the troubleshooting section above

Review the Streamlit documentation

Examine the error messages for specific details

Consider reducing the dataset size for testing

