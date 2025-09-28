import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re
from collections import Counter
from wordcloud import WordCloud

# Set Streamlit page configuration
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")
st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")


# Add some basic info
st.markdown("---")
st.write("This app analyzes the CORD-19 dataset to explore COVID-19 research trends.")

# Your handle_missing function - FIXED datetime handling
def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles NaN values in metadata_df with column-specific replacements.
    """
    replacements = {
        "title": "No Title",
        "doi": "No DOI",
        "pmcid": "No PMCID",
        "pubmed_id": "No PubMed ID",
        "abstract": "No Abstract",
        "publish_time": "1900-01-01",   # Use a default date
        "authors": "Unknown Authors",
        "journal": "Unknown Journal",
        "who_covidence_id": "No Covidence ID",
        "arxiv_id": "No ArXiv ID",
        "pdf_json_files": "No PDF JSON",
        "pmc_json_files": "No PMC JSON",
        "url": "No URL",
        "sha": "No SHA",
        "mag_id": 0,  
        "s2_id": 0    
    }

    # Apply replacements - FIXED: Handle datetime conversion separately
    for col, value in replacements.items():
        if col in df.columns:
            if col == "publish_time":
                # Convert to string first, then to datetime with error handling
                df[col] = df[col].astype(str)
                df[col] = pd.to_datetime(df[col], errors='coerce').fillna(pd.to_datetime(value))
            else:
                df[col] = df[col].fillna(value)

    return df

# Load and process data - FIXED: Added better error handling
@st.cache_data
def load_and_process_data():
    """Load and process the data using your original code"""
    
    try:
        # Load data with more robust error handling
        st.write("Loading data...")
        metadata_df = pd.read_csv("metadata.csv", nrows = 3000)  # Removed nrows for full dataset

        metadata_df.to_csv("metadata_sample.csv", index=False)  # Save a sample for reference
        
        # Show basic info
        st.write(f"Dataset shape: {metadata_df.shape}")
        
        # Handle missing data using your function
        metadata_df = handle_missing(metadata_df)
        
        # Ensure publish_time is properly formatted as datetime
        if 'publish_time' in metadata_df.columns:
            metadata_df['publish_time'] = pd.to_datetime(metadata_df['publish_time'], errors='coerce')
        
        return metadata_df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame as fallback

# Load the data with better error handling
try:
    metadata_df = load_and_process_data()
    if metadata_df.empty:
        st.error("No data loaded. Please check if metadata.csv exists.")
        st.stop()
    else:
        st.success(f"Data loaded successfully! Shape: {metadata_df.shape}")
        
except FileNotFoundError:
    st.error("Could not find metadata.csv file. Please make sure it's in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Unexpected error: {e}")
    st.stop()

# Add interactive widgets - MOVED after data loading to avoid errors
st.sidebar.header("Settings")

# FIXED: Get actual year range from data to avoid hardcoding
if 'publish_time' in metadata_df.columns and not metadata_df['publish_time'].isna().all():
    min_year = int(metadata_df['publish_time'].dt.year.min())
    max_year = int(metadata_df['publish_time'].dt.year.max())
    # Handle cases where year might be invalid
    if pd.isna(min_year) or min_year < 1900:
        min_year = 2015
    if pd.isna(max_year) or max_year > 2030:
        max_year = 2023
else:
    min_year = 2015
    max_year = 2023

year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))
top_n_journals = st.sidebar.selectbox("Top N journals to show", [5, 10, 15, 20], index=1)

# Section 1: Basic Data Overview - FIXED: Added checks for column existence
st.header("📊 Dataset Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Papers", f"{len(metadata_df):,}")

with col2:
    st.metric("Total Columns", len(metadata_df.columns))

with col3:
    if 'journal' in metadata_df.columns:
        unique_journals = metadata_df['journal'].nunique()
        st.metric("Unique Journals", f"{unique_journals:,}")
    else:
        st.metric("Unique Journals", "N/A")

# Show first few rows
if st.checkbox("Show first 5 rows of data"):
    st.dataframe(metadata_df.head())

# Show missing data info - FIXED: Handle case where no missing data
if st.checkbox("Show missing data information"):
    missing_data = metadata_df.isnull().sum()
    if missing_data.sum() > 0:
        st.write("Missing data per column:")
        st.dataframe(missing_data[missing_data > 0])
    else:
        st.write("No missing data found!")

# Section 2: Publications Over Time - FIXED: Added proper datetime handling
st.header("📈 Publications Over Time")

if 'publish_time' in metadata_df.columns:
    # Ensure we have valid datetime data
    valid_dates = metadata_df['publish_time'].notna()
    
    if valid_dates.any():
        # Extract year from valid dates
        metadata_df['year'] = metadata_df.loc[valid_dates, 'publish_time'].dt.year
        
        # Count papers by publication year
        publication_year_counts = metadata_df['year'].value_counts().sort_index()
        
        # Filter by year range
        filtered_counts = publication_year_counts[
            (publication_year_counts.index >= year_range[0]) & 
            (publication_year_counts.index <= year_range[1])
        ]
        
        if len(filtered_counts) > 0:
            # Plot 
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(filtered_counts.index, filtered_counts.values, marker='o', linewidth=2, markersize=8)
            ax.set_title("Number of COVID-19 Publications Over Time")
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Publications")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Show the data
            st.write("Publications by year:")
            year_data = pd.DataFrame({
                'Year': filtered_counts.index,
                'Count': filtered_counts.values
            })
            st.dataframe(year_data)
        else:
            st.warning("No data available for the selected year range.")
    else:
        st.warning("No valid date data available for analysis.")
else:
    st.warning("Publication time column not found in dataset.")

# Section 3: Top Journals - FIXED: Added column existence check
st.header("📰 Top Journals")

if 'journal' in metadata_df.columns:
    # Identify top journals, excluding placeholder values
    journal_counts = metadata_df['journal'].value_counts()
    # Filter out placeholder values like "Unknown Journal"
    valid_journals = journal_counts[journal_counts.index != "Unknown Journal"]
    
    if len(valid_journals) > 0:
        top_journals = valid_journals.head(top_n_journals)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        top_journals.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title(f"Top {top_n_journals} Journals Publishing COVID-19 Research")
        ax.set_xlabel("Journal")
        ax.set_ylabel("Number of Publications")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show journal data
        st.write("Top journals data:")
        journal_data = pd.DataFrame({
            'Journal': top_journals.index,
            'Papers': top_journals.values
        })
        st.dataframe(journal_data)
    else:
        st.warning("No valid journal data available.")
else:
    st.warning("Journal column not found in dataset.")

# Section 4: Word Analysis - FIXED: Added better text processing
st.header("🔤 Most Frequent Words in Titles")

if 'title' in metadata_df.columns:
    # Combine all titles and clean text
    all_titles = ' '.join(metadata_df['title'].astype(str).tolist()).lower()
    
    # Remove common stop words and short words
    stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'on', 'with', 'by', 
                  'an', 'at', 'from', 'as', 'is', 'are', 'this', 'that', 'these', 
                  'those', 'be', 'was', 'were', 'has', 'have', 'had', 'but', 'or',
                  'not', 'no', 'yes', 'covid', '19', 'sars', 'cov', '2', 'coronavirus'}
    
    words = re.findall(r'\b[a-z]{3,}\b', all_titles)  # Only words with 3+ letters
    filtered_words = [word for word in words if word not in stop_words]
    
    if filtered_words:
        word_counts = Counter(filtered_words)
        most_common_words = word_counts.most_common(20)
        
        # Show top words
        st.write("Most frequent words in titles (excluding common words):")
        word_df = pd.DataFrame(most_common_words, columns=['Word', 'Count'])
        st.dataframe(word_df)
        
        # Word frequency bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        words_to_plot = word_df.head(10)  # Top 10 for better readability
        ax.bar(words_to_plot['Word'], words_to_plot['Count'], color='lightgreen')
        ax.set_title("Top 10 Most Frequent Words in Titles")
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("No valid words found for analysis.")
else:
    st.warning("Title column not found in dataset.")

# Section 5: Word Cloud - FIXED: Added proper error handling
st.header("☁️ Word Cloud")

if 'title' in metadata_df.columns and 'all_titles' in locals():
    try:
        if filtered_words:  # Use the filtered words from previous section
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                colormap='viridis',
                max_words=100
            ).generate_from_frequencies(dict(word_counts))
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title("Word Cloud of Paper Titles")
            st.pyplot(fig)
        else:
            st.warning("Not enough words to generate word cloud.")
    except Exception as e:
        st.error(f"Could not generate word cloud: {e}")
else:
    st.warning("Title data not available for word cloud.")

# Section 6: Source Distribution - FIXED: Better column detection
st.header("📊 Papers by Source")

# Try different possible column names for source
source_columns = [col for col in metadata_df.columns if 'source' in col.lower()]
    
if source_columns:
    source_col = source_columns[0]  # Use the first source column found
    # Count papers by source 
    source_counts = metadata_df[source_col].value_counts()
    
    if len(source_counts) > 0:
        # Plot 
        fig, ax = plt.subplots(figsize=(10, 6))
        source_counts.plot(kind="bar", color="lightcoral", edgecolor="black", ax=ax)
        ax.set_title(f"Distribution of Paper Count by Source ({source_col})")
        ax.set_xlabel("Source")
        ax.set_ylabel("Number of Papers")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show source data
        st.write("Papers by source:")
        source_data = pd.DataFrame({
            'Source': source_counts.index,
            'Count': source_counts.values
        })
        st.dataframe(source_data)
    else:
        st.warning("No source data available.")
else:
    st.write("No source column found in the dataset")

# Section 7: Sample Data - FIXED: Better column selection
st.header("📋 Sample Data")
sample_size = st.slider("Number of rows to display", 5, 50, 10)

# Show sample of the actual data
st.write(f"Showing {sample_size} sample records:")

# Select informative columns that likely exist
possible_columns = ['title', 'journal', 'authors', 'publish_time', 'doi', 'abstract']
available_columns = [col for col in possible_columns if col in metadata_df.columns]

if available_columns:
    st.dataframe(metadata_df[available_columns].head(sample_size))
else:
    st.warning("No common columns found to display.")

# Footer
st.markdown("---")
st.write("Data source: CORD-19 COVID-19 Research Dataset")