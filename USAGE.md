# Intelligent Prospect Analyzer & Sales Insights Generator - Usage Guide

This document provides detailed instructions for setting up, configuring, and running the Intelligent Prospect Analyzer & Sales Insights Generator.

## Table of Contents

- [Intelligent Prospect Analyzer \& Sales Insights Generator - Usage Guide](#intelligent-prospect-analyzer--sales-insights-generator---usage-guide)
  - [Table of Contents](#table-of-contents)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Detailed Setup](#2-detailed-setup)
    - [Python Version](#python-version)
    - [Virtual Environment](#virtual-environment)
    - [Install Dependencies](#install-dependencies)
    - [Playwright Browser Installation](#playwright-browser-installation)
    - [Environment Variables (`.env` file)](#environment-variables-env-file)
  - [3. Input Data Format](#3-input-data-format)
    - [Prospect Input File (`INPUT_EXCEL_FILE_PATH`)](#prospect-input-file-input_excel_file_path)
    - [Golden Partners CSV File (`PATH_TO_GOLDEN_PARTNERS_CSV`)](#golden-partners-csv-file-path_to_golden_partners_csv)
  - [4. Running the Pipeline (`main_pipeline.py`)](#4-running-the-pipeline-main_pipelinepy)
    - [Command](#command)
    - [Operation](#operation)
    - [Outputs](#outputs)
    - [Output Directory Structure](#output-directory-structure)
  - [5. Configuration Details](#5-configuration-details)
    - [Primary Configuration: `.env` File](#primary-configuration-env-file)
    - [Core Configuration Class: `src/core/config.py`](#core-configuration-class-srccoreconfigpy)
    - [Key Configuration Variables Explained](#key-configuration-variables-explained)
      - [Core File Paths](#core-file-paths)
      - [LLM and Prompt Configuration](#llm-and-prompt-configuration)
      - [Web Scraper Settings](#web-scraper-settings)
  - [6. Troubleshooting](#6-troubleshooting)

## 1. Prerequisites

*   **Python**: Version 3.8 or higher is recommended.
*   **Access to Google Gemini API**: A valid API key is required for LLM-based components.
*   **Internet Connection**: For web scraping and accessing the Gemini API.

## 2. Detailed Setup

### Python Version

Ensure you have Python 3.8+ installed. You can check your Python version by running:
```bash
python --version
```

### Virtual Environment

It is strongly recommended to use a Python virtual environment.
*   **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
*   **Activate the virtual environment**:
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

### Install Dependencies

All required Python packages are listed in [`requirements.txt`](./requirements.txt). Install them using pip:
```bash
pip install -r requirements.txt
```

### Playwright Browser Installation

Playwright uses browser binaries for web automation. Install these:
```bash
playwright install
```

### Environment Variables (`.env` file)

The application uses a `.env` file to manage configurations.
1.  **Create the `.env` file**:
    Copy [`.env.example`](./.env.example) to `.env` in the project root:
    ```bash
    # On Windows
    copy .env.example .env
    # On macOS/Linux
    cp .env.example .env
    ```
2.  **Edit the `.env` file**:
    Open `.env` and fill in the values. Minimally, you must set:
    *   `GEMINI_API_KEY`: Your Google Gemini API key.
    *   `INPUT_EXCEL_FILE_PATH`: Path to your input file of prospect company URLs (e.g., `data/test_input_urls.csv`).
    *   `PATH_TO_GOLDEN_PARTNERS_CSV`: Path to your Golden Partners CSV file (e.g., `data/golden_partners.csv`), if using this feature.
    Review all variables in [`.env.example`](./.env.example) and the [Key Configuration Variables Explained](#key-configuration-variables-explained) section.

## 3. Input Data Format

### Prospect Input File (`INPUT_EXCEL_FILE_PATH`)

The primary input for the pipeline is a CSV or Excel file containing a list of company website URLs. The file path is specified by `INPUT_EXCEL_FILE_PATH` in the `.env` file.

The file should contain a header row, and the column containing the URLs should be named `Homepage` (or mapped correctly in the input profile in `config.py`). An optional `Firma Vollname` column can be included to provide the company name, otherwise it will be inferred.

**Example `test_input_urls.csv`:**
```csv
Firma Vollname,Homepage
Example AG,https://www.example.com
Test GmbH,http://test-site.org
```

### Golden Partners CSV File (`PATH_TO_GOLDEN_PARTNERS_CSV`)

If using the Golden Partner comparison feature, provide a CSV file specified by `PATH_TO_GOLDEN_PARTNERS_CSV`.
The expected column structure for this file is:

*   **`id`**: Unique identifier for the golden partner.
*   **`name`**: Name of the golden partner.
*   **`url`**: Website URL of the golden partner.
*   **`description`**: A brief description of the golden partner.
*   **`industry`**: The industry of the golden partner.
*   **`target_audience`**: Description of their typical customer.
*   **`usp`**: Unique Selling Proposition(s).
*   **`services_products`**: Key services or products offered.
*   Other columns may be present but the ones listed above are primarily used by the `summarize_golden_partner` function and potentially by the comparison prompt.

**Example `data/golden_partners.csv` (Updated Structure):**
```csv
id,name,url,description,industry,target_audience,usp,services_products
1,Alpha Solutions,http://alpha.com,"Leader in AI-driven analytics, known for innovative solutions and strong customer support.",Tech,Enterprises,"Proprietary AI algorithms, Fast deployment","AI Analytics Platform, Custom AI Models"
2,Beta Services,http://beta.com,"Provides comprehensive cloud services with a focus on scalability and security.",Cloud Services,SMEs,"High uptime guarantee, Pay-as-you-go","Cloud Hosting, Managed Kubernetes, Backup Solutions"
3,Gamma Consulting,http://gamma.org,"Strategic business consulting for digital transformation.",Consulting,Large Corporations,"Proven methodologies, Experienced consultants","Strategy Workshops, Process Optimization, Tech Implementation"
```
The content of this file, especially `description`, `industry`, `usp`, and `services_products`, is crucial for effective comparison by the LLM using the `PROMPT_PATH_COMPARISON_SALES_LINE` prompt.

## 4. Running the Pipeline (`main_pipeline.py`)

The [`main_pipeline.py`](./main_pipeline.py) script is the entry point.

### Command
Navigate to the project root directory (with venv activated) and run:
```bash
python main_pipeline.py
```

### Operation
When executed, `main_pipeline.py` orchestrates the three-stage LLM pipeline for each URL provided in the input file:

1.  **Initialization**: Loads configuration from `.env`, sets up logging, and generates a unique `RunID` for the session.
2.  **Data Ingestion & Scraping**: For each URL, the pipeline scrapes the website to gather text content.
3.  **LLM Stage 1: Summarization**: The scraped text is passed to the first LLM call, which uses the `PROMPT_PATH_WEBSITE_SUMMARIZER` prompt to generate a concise summary of the company's business.
4.  **LLM Stage 2: Attribute Extraction**: The summary and original text are passed to the second LLM call, which uses the `PROMPT_PATH_ATTRIBUTE_EXTRACTOR` prompt to extract a detailed list of attributes (e.g., industry, target audience, technologies used).
5.  **LLM Stage 3: Comparison & Sales Insight**: The extracted attributes are passed to the third LLM call, along with a summary of "Golden Partners" (loaded from `PATH_TO_GOLDEN_PARTNERS_CSV`). This stage uses the `PROMPT_PATH_COMPARISON_SALES_LINE` prompt to generate a comparative analysis and a tailored sales pitch.
6.  **Reporting**: The final output, containing the data from all stages, is written to the `ProspectAnalysisReport_{run_id}.csv` file.

### Outputs
The primary output of the pipeline is the **Prospect Analysis Report**, a CSV file named `ProspectAnalysisReport_{run_id}.csv` located in the `output_data/[RunID]/` directory.

This report contains the flattened data from the `GoldenPartnerMatchOutput` schema (`src/core/schemas.py`). Each row corresponds to a successfully processed prospect URL and includes columns for:
*   The original input data (URL, Company Name).
*   The summary generated in LLM Stage 1.
*   All attributes extracted in LLM Stage 2 (e.g., `company_summary`, `primary_industry`, `target_audience`, `technologies_used`, etc.).
*   The comparative analysis and sales line generated in LLM Stage 3.

Other outputs include logs and intermediate files (scraper content, raw LLM outputs) which are useful for debugging.

### Output Directory Structure
(Illustrative, may vary slightly based on configuration and run specifics)
```
output_data/
└── [RunID]/  (e.g., 20240520_113000)
    ├── ProspectAnalysisReport_20240520_113000.csv # Main analysis output
    ├── pipeline_run_20240520_113000.log
    ├── run_metrics.md
    ├── failed_rows_20240520_113000.csv
    ├── row_attrition_report_20240520_113000.csv
    ├── scraped_content/
    │   └── cleaned_pages_text/
    │       └── CompanyName__domain_hash_cleaned.txt
    ├── llm_context/
    │   ├── CANONICAL_example_com_attribute_extractor_prompt.txt
    │   ├── CANONICAL_example_com_attribute_extractor_raw_output.json
    │   └── ...
    └── ... (other reports or intermediate files)
```

## 5. Configuration Details

### Primary Configuration: `.env` File
Create and edit `.env` from [`.env.example`](./.env.example) for primary configuration.

### Core Configuration Class: `src/core/config.py`
The [`src/core/config.py`](./src/core/config.py) defines `AppConfig` for loading and managing settings.

### Key Configuration Variables Explained
This section highlights the most important variables in the `.env` file. Deprecated variables have been removed.

#### Core File Paths
*   **`INPUT_EXCEL_FILE_PATH`** (Required): Path to the input CSV/Excel file containing prospect URLs.
*   **`PATH_TO_GOLDEN_PARTNERS_CSV`** (Required): Path to the CSV file defining your "Golden Partners" for comparison.
*   **`OUTPUT_BASE_DIR`**: The directory where run-specific output folders will be created. Default: `output_data`.

#### LLM and Prompt Configuration
*   **`GEMINI_API_KEY`** (Required): Your API key for the Google Gemini service.
*   **`LLM_MODEL_NAME`**: The specific Gemini model to use (e.g., `gemini-1.5-pro-latest`).
*   **`PROMPT_PATH_WEBSITE_SUMMARIZER`**: Path to the text file containing the prompt for LLM Stage 1 (Summarization).
*   **`PROMPT_PATH_ATTRIBUTE_EXTRACTOR`**: Path to the prompt for LLM Stage 2 (Attribute Extraction).
*   **`PROMPT_PATH_COMPARISON_SALES_LINE`**: Path to the prompt for LLM Stage 3 (Comparison and Sales Line Generation).
*   **`LLM_MAX_INPUT_CHARS_FOR_SUMMARY`**: The maximum number of characters from the scraped website text to feed into the summarization LLM. This prevents exceeding token limits for very large websites.
*   **`LLM_TEMPERATURE`**, **`LLM_MAX_TOKENS`**, **`LLM_TOP_K`**, **`LLM_TOP_P`**: Standard LLM parameters to control the creativity, length, and sampling of the model's responses.

#### Web Scraper Settings
*   **`SCRAPER_MAX_PAGES_PER_DOMAIN`**: The maximum number of pages the scraper will visit on a single domain to prevent excessively long scraping times.
*   **`SCRAPER_PAGE_TIMEOUT_MS`**: Timeout in milliseconds for waiting for a page to load.
*   **`RESPECT_ROBOTS_TXT`**: Whether the scraper should obey the rules defined in a website's `robots.txt` file. Default: `True`.
*   **`TARGET_LINK_KEYWORDS`**: A comma-separated list of keywords used to prioritize which links to follow (e.g., `about,services,products,contact`).

## 6. Troubleshooting

*   **`GEMINI_API_KEY` errors**: Ensure key is correct in `.env`, file is loaded, and key is active.
*   **Playwright browser issues**: Run `playwright install` in your venv.
*   **`FileNotFoundError` for input files**: Verify `INPUT_EXCEL_FILE_PATH` and `PATH_TO_GOLDEN_PARTNERS_CSV` in `.env` are correct and relative to project root. Ensure the files exist.
*   **Scraping issues (blocks, CAPTCHAs)**: Adjust timeouts. Check `RESPECT_ROBOTS_TXT`.
*   **LLM issues (poor extraction, nonsensical output)**:
    *   Check/Refine LLM prompts (`PROMPT_PATH_ATTRIBUTE_EXTRACTOR`, etc.).
    *   Adjust `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`.
    *   Ensure `LLM_MODEL_NAME` is appropriate.
    *   Verify quality of scraped text being fed to LLM.
*   **`ModuleNotFoundError`**: Ensure venv is active and `pip install -r requirements.txt` was successful.
*   **Scraper not finding relevant content**:
    *   Adjust `TARGET_LINK_KEYWORDS`, `SCRAPER_CRITICAL_PRIORITY_KEYWORDS`, `SCRAPER_HIGH_PRIORITY_KEYWORDS`.
    *   Tune `SCRAPER_MIN_SCORE_TO_QUEUE`, `SCRAPER_MAX_PAGES_PER_DOMAIN`.
    *   Check `PAGE_TYPE_KEYWORDS_*` if used for content targeting.
*   **Path too long errors (Windows)**: Reduce `FILENAME_COMPANY_NAME_MAX_LEN`, etc. Ensure project root path isn't too long.
*   **Issues with Golden Partner Comparison**:
    *   Verify `PATH_TO_GOLDEN_PARTNERS_CSV` is correct and file format matches prompt expectations.
    *   Check `PROMPT_PATH_COMPARISON_SALES_LINE` for clarity and effectiveness.
    *   Adjust `MAX_GOLDEN_PARTNERS_IN_PROMPT`.

For other issues, consult the run log file (`output_data/[RunID]/pipeline_run_{RunID}.log`) and `run_metrics.md`.