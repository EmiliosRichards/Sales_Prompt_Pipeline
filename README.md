# Intelligent Prospect Analyzer & Sales Insights Generator

## Project Overview

The Intelligent Prospect Analyzer & Sales Insights Generator is a Python-based application that analyzes company websites for B2B sales prospecting. It automates the process of gathering intelligence on prospective companies, extracting key information from their websites, and generating actionable sales insights. It leverages web scraping and a multi-stage Large Language Model (LLM) process to provide a comprehensive analysis.

This document provides a general overview. For detailed setup, configuration, and advanced usage, please refer to [USAGE.md](./USAGE.md).

## High-Level Workflow

The pipeline follows a three-stage LLM process:

1.  **Data Ingestion**: Ingests a list of company URLs.
2.  **Web Scraping**: Scrapes the company websites for relevant information.
3.  **LLM Call 1: Summarization**: The scraped content is summarized to create a concise overview.
4.  **LLM Call 2: Detailed Attribute Extraction**: Key attributes are extracted from the scraped content based on a defined schema.
5.  **LLM Call 3: Comparison to Golden Partners & Sales Line Generation**: The extracted attributes are compared against a "Golden Partners" profile to generate tailored sales pitches and insights.
6.  **Reporting**: The final analysis is compiled into a CSV report.

## Key Features & Technologies

*   **Multi-Stage LLM Analysis**: Utilizes a three-stage LLM process for summarization, attribute extraction, and sales insight generation.
*   **Automated Web Scraping**: Gathers up-to-date information directly from company websites.
*   **Company Attribute Extraction**: Identifies key company characteristics from unstructured text.
*   **Sales Pitch Generation**: Creates tailored sales lines by comparing prospects to an ideal partner profile.
*   **CSV Reporting**: Outputs structured data for easy integration with other sales tools.

**Technologies Used:**

*   **Python 3.8+** (recommended)
*   **Pandas**: For data manipulation and Excel/CSV file handling.
*   **Playwright**: For robust web scraping.
*   **Beautiful Soup (bs4)**: For HTML parsing.
*   **Google Gemini API**: For LLM-based extraction and reasoning.
*   **python-dotenv**: For managing environment variables.
*   **Pydantic**: For data validation and settings management.

## Directory Structure Overview

(This section may require minor updates based on actual output file generation)
```
Contact_Pipeline/
├── .env.example           # Example environment variable configuration
├── main_pipeline.py       # Main script to run the entire pipeline
├── README.md              # This file
├── USAGE.md               # Detailed usage and configuration guide
├── requirements.txt       # Python package dependencies
├── data/                  # Default directory for input data files
│   └── test_input_urls.csv  # Example input for prospect URLs
│   └── golden_partners.csv  # Example input for Golden Partners
├── prompts/               # Directory for LLM prompt templates
│   └── attribute_extractor_prompt.txt
│   └── comparison_sales_line_prompt.txt
│   └── website_summarizer_prompt.txt
│   └── ... (other prompts)
├── src/                   # Source code
│   ├── core/
│   │   ├── config.py
│   │   └── ...
│   └── ...
└── output_data/           # Default directory for pipeline outputs (created on run)
    └── [RunID]/           # Outputs for a specific pipeline run
        └── ProspectAnalysisReport_{run_id}.csv # Main prospect analysis output
```

## Setup Instructions

Follow these steps to set up and run the pipeline:

1.  **Clone the Repository (Conceptual)**:
    Ensure you have all the project files in a local directory.

2.  **Set up a Python Virtual Environment**:
    Python 3.8+ is recommended.
    ```bash
    python -m venv venv
    ```
    Activate it:
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers**:
    ```bash
    playwright install
    ```

5.  **Set up the `.env` File**:
    *   Copy the example file:
        *   Windows: `copy .env.example .env`
        *   macOS/Linux: `cp .env.example .env`
    *   Open `.env` and fill in required values, especially:
        *   `GEMINI_API_KEY`: Your Google Gemini API key.
        *   `INPUT_EXCEL_FILE_PATH`: Path to your input file of prospect URLs (e.g., `data/test_input_urls.csv`).
        *   `PATH_TO_GOLDEN_PARTNERS_CSV`: Path to your Golden Partners CSV file (e.g., `data/golden_partners.csv`), if using this feature.
    *   Review other variables in [`.env.example`](./.env.example) and [USAGE.md](./USAGE.md) to customize behavior (e.g., `EXTRACTION_PROFILE`, prompt paths, logging levels).

## Basic Usage

To run the pipeline, simply execute the main script. Ensure your `.env` file is configured with the necessary API keys and paths.
```bash
python main_pipeline.py
```
The script will process the input URLs and generate a `ProspectAnalysisReport_{run_id}.csv` in the `output_data/` directory.

## Advanced Usage & Configuration

For more detailed information on:
*   All environment variables and their effects.
*   Input data format specifications for prospect lists and Golden Partners.
*   Detailed explanation of pipeline outputs and report structures.
*   Configuring extraction profiles and LLM prompts.
*   Troubleshooting common issues.

Please refer to the [**USAGE.md**](./USAGE.md) file.