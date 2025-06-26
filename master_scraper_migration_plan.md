# Master Scraper Migration Plan

This document outlines the steps required to replace the existing scraper logic in the main pipeline with the new, more advanced `base_scraper`.

## 1. Project Structure Consolidation

The first step is to merge the `base_scraper` directory into the main `src` directory to create a unified and simplified project structure.

*   **Action:** Move the contents of `base_scraper/src/` into `src/scraper/`.
*   **Action:** Delete the now-empty `base_scraper` directory.
*   **Rationale:** This will place all scraper-related modules (`config.py`, `scraper.py`, `interaction_handler.py`, etc.) into a single, cohesive `scraper` package within the main application source.

## 2. Configuration Unification

We need to merge the two separate configuration systems into a single, authoritative `AppConfig`.

*   **Action:** Modify `src/core/config.py` to include all the configurable parameters from the new scraper (caching, proxy settings, interaction handling).
*   **Action:** Update the `.env` and `.env.example` files to include the new configuration variables for the scraper, such as `PROXY_ENABLED`, `INTERACTION_SELECTORS`, and `CACHING_ENABLED`.
*   **Rationale:** This creates a single point of configuration for the entire pipeline, making it easier to manage and deploy.

## 3. Pipeline Integration

This is the core of the migration, where we will rewire the main pipeline to use the new scraper.

*   **Action:** Modify `src/processing/pipeline_flow.py`.
    *   Remove the call to the old `scrape_website` function.
    *   Add a call to the new, more robust `scrape_website` function from the `scraper` package.
*   **Action:** Modify `main_pipeline.py`.
    *   Update the main function to pass the new scraper configurations to the pipeline flow.
*   **Rationale:** This step directly replaces the old, problematic scraper with the new, feature-rich one.

## 4. Data Flow Adaptation

Finally, we must ensure that the data produced by the new scraper is compatible with the rest of the pipeline.

*   **Action:** Analyze the data structure returned by the new `scrape_website` function.
*   **Action:** Create an adapter function or modify the existing data handling logic to transform the new scraper's output into the format expected by the downstream processes (e.g., the LLM analysis tasks).
*   **Rationale:** This ensures that the new scraper integrates seamlessly without breaking the existing data processing workflow.