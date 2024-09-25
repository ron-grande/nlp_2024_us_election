# 2024 US Presidential Election NLP Analysis

## Overview
This project is primarily a learning exercise to explore the principles of **data lakes** and apply **Natural Language Processing (NLP)** techniques to analyze media coverage of the **2024 US Presidential Election**. By ingesting full-text articles from the **New York Times API** and **GNews API**, we aim to gain insights into sentiment, key topics, and named entities around significant election events such as debates, primaries, and candidate announcements.

Given the **computational constraints** (running on a **2020 MacBook Air** with an **i7 processor** and **16GB of RAM**), this project focuses on balancing efficiency and sophisticated NLP analysis techniques. The project is not focused on speed, but rather on performing deeper NLP analyses such as **LDA topic modeling** and **sentiment analysis** without overloading resources.

### Why Google Drive for the Data Lake?
We’re using **Google Drive** as our **pseudo data lake** due to its **free storage** and ease of access, making it a simple yet scalable solution for organizing and storing project data. Google Drive allows for clear separation between the raw, cleansed, and transformed datasets, adhering to a **medallion architecture** (Bronze, Silver, Gold layers), even though we’re working within a small-scale environment. Google Drive provides sufficient **cloud storage** to mimic data lake principles while keeping data organized and accessible.

### Data Lake File Structure
The data lake is structured according to the **medallion architecture**:

- **Bronze Layer**: Stores raw data directly ingested from APIs in its original format (JSON).
  - Example: `Datalake/GNews/bronze/20240920/json_election_gnews_20240920.json`
  
- **Silver Layer**: Contains **cleansed** and **error-checked** data, which retains its original format but has undergone basic cleaning using **PySpark**.
  - Example: `Datalake/GNews/silver/20240920/csv_cleaned_election_gnews_20240920.csv`
  
- **Gold Layer**: Houses fully **transformed** data, ready for analysis and visualization, often in formats like **Parquet** for better performance and scalability.
  - Example: `Datalake/GNews/gold/20240920/parq_sentiment_election_gnews_20240920.parquet`

This file structure allows for clear separation of raw, processed, and final data, aligning with data lake best practices, but adapted to work within the Google Drive environment.

## Key Features
- **Sentiment Analysis**: Analyze sentiment toward candidates and topics using models such as **VADER** and **DistilBERT**.
- **Keyword and Topic Extraction**: Use techniques like **RAKE** and **LDA** to identify key phrases and model topics.
- **Named Entity Recognition (NER)**: Identify key political figures, organizations, and locations.
- **Event-Based Data Collection**: Collect articles around election events to analyze how media coverage shifts over time.
- **ETL with PySpark**: Use **PySpark** to efficiently transform large datasets before they are analyzed with DuckDB.
- **Data Storage on Google Drive**: Leverage Google Drive as a pseudo data lake to store and organize data across **Bronze**, **Silver**, and **Gold** layers.

## Tools and Libraries
- **Python** for scripting and analysis.
- **PySpark** for data transformation.
- **VADER**, **DistilBERT**, and **SpaCy** for NLP tasks.
- **DuckDB** for querying and data modeling.
- **Google Data Studio** for reporting and visualization.
- **GNews API** and **New York Times API** for data collection.

## Goals
- Learn the principles of data lakes and apply **NLP** techniques to media data.
- Gain insights into how media covers political figures and election topics.
- Build a scalable, event-based data architecture that supports **in-depth trend analysis** using sophisticated NLP techniques while respecting computational limits.
