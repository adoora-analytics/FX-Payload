# FX Rate ETL Pipeline (Portfolio Learning Project)

An incrementally developed FX rates ETL pipeline built in Python as part of a data engineering learning portfolio.
The project focuses on core ETL fundamentals, clean project structure, and disciplined version control rather than one-off scripts. 
This repository reflects realistic pipeline evolution, with progress tracked through daily Git commits.

## Project Goal
The goal of this project is to practice and demonstrate:
1. Designing a clear Extract - Transform - Load (ETL) pipeline.
2. Working with real-world API data.
3. Normalizing nested JSON into structured records.
4. Separating concerns across pipeline stages.
5. Using Git properly to track incremental progress.

## Pipeline Overview
- Extract:
Fetches latest FX rates from a public API.
- Transform:
Converts nested API responses into row-level, analytics-ready records.
- Load:
Writes cleaned data to structured output formats.
- Main:
A lightweight entry point coordinates the pipeline without embedding business logic.

## Project Structure 
fx-payload/
├── src/
│   ├── config.py        # Configuration and paths
│   ├── extract.py       # API ingestion logic
│   ├── transform.py    # Data normalization logic
│   ├── load.py          # Data persistence logic
│   └── main.py          # Pipeline entry point
├── data/
│   ├── raw/             # Raw API payloads (git ignored)
│   └── processed/       # Cleaned outputs (git ignored)
├── notes/               # Optional learning notes
├── requirements.txt
├── .gitignore
└── README.md
