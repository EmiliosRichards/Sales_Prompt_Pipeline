# Prospect Analyzer Guide

This document provides an overview of the inputs, outputs, and potential failure points of the "Intelligent Prospect Analyzer & Sales Insights Generator" pipeline.

## 1. Input

The pipeline requires a single CSV or Excel file as input. This file should contain the company URLs that need to be analyzed.

*   **Input File Path**: Configured via `INPUT_EXCEL_FILE_PATH` in the `.env` file.
*   **Required Column**: The file must contain a column named `Homepage` which holds the URLs.
*   **Optional Column**: A `Firma Vollname` column can be provided for the company name.

## 2. Outputs

The primary output is a single CSV report, along with logs and intermediate artifacts for debugging. All outputs are saved in a unique directory for each run: `output_data/{run_id}/`.

*   **`ProspectAnalysisReport_{run_id}.csv`**: This is the main report. It contains the full, flattened output of the analysis for each successfully processed prospect. The columns correspond to the `GoldenPartnerMatchOutput` schema and include the initial summary, all extracted attributes, and the final sales insights.
*   **LLM/Scraper Artifacts**: For debugging purposes, the pipeline saves the raw text scraped from websites and the raw inputs and outputs from each of the three LLM calls. These are stored in subdirectories within the run folder.
*   **Log File**: A `pipeline_run_{run_id}.log` file captures detailed logs of the entire process.

## 3. Failure Reasons & Outcome Explanations

The new three-stage LLM process introduces new potential points of failure. The final report and logs will indicate why a prospect might have failed.

*   **`ScrapingFailed_{status}`**: The pipeline was unable to successfully scrape the company's website. The `{status}` provides more detail (e.g., `Error_Network`, `Error_AccessDenied`).
*   **`LLM_Summary_Failed`**: The first LLM call (Summarization) failed. This could be due to an API error from the LLM provider or an issue parsing the model's response.
*   **`LLM_AttributeExtraction_Failed`**: The second LLM call (Detailed Attribute Extraction) failed, likely due to an API or response parsing error.
*   **`LLM_Comparison_Failed`**: The third LLM call (Comparison to Golden Partners & Sales Line Generation) failed.
*   **`GoldenPartners_Load_Failed`**: The `golden_partners.csv` file could not be loaded, which is essential for the third LLM call.