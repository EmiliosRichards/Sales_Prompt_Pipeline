# Scraper Enhancement Plan (V2)

This document outlines the revised plan to upgrade the existing scraper (`src/scraper/`) with key features from the `base_scraper` reference implementation. The goal is to improve scraper success rates and efficiency while minimizing risk and preserving existing functionality.

### 1. Session Management: Fresh Sessions Confirmed

This plan **maintains the current behavior of using a fresh, isolated browser session for each top-level website scrape.** The new features (cookie handling, proxies) will operate *within* this fresh session. This ensures there is no data leakage between different company scrapes and fulfills the requirement for stateless runs.

### 2. Create New, Isolated Modules

To avoid disrupting the existing scraper, the new functionality will be added in separate, dedicated files within the current `src/scraper/` directory.

*   **New File:** `src/scraper/interaction_handler.py`
    *   **Content:** This file will contain the `InteractionHandler` class from `base_scraper`. Its purpose is to programmatically find and click cookie consent banners.
*   **New File:** `src/scraper/proxy_manager.py`
    *   **Content:** This file will contain the `ProxyManager` class from `base_scraper`. It will manage a list of proxies, handle rotation, and perform health checks.
*   **New File (Added):** `src/scraper/caching.py`
    *   **Content:** This file will contain the caching functions from `base_scraper`. It will handle saving successful scrape results to disk and loading them to avoid re-scraping.

### 3. Unify Configuration

All new settings will be integrated into the main application's configuration system.

*   **File to Modify:** `src/core/config.py`
    *   **Action:** Add new attributes to the `AppConfig` class for the interaction handler, proxy manager, and **caching** (e.g., `PROXY_ENABLED`, `INTERACTION_SELECTORS`, `CACHING_ENABLED`, `CACHE_DIR`).
*   **Files to Modify:** `.env` and `.env.example`
    *   **Action:** Add the corresponding environment variables to these files so they can be easily configured.

### 4. Integrate Features into Existing Logic

The new modules will be carefully integrated into the current scraper's workflow.

*   **File to Modify:** `src/scraper/scraper_logic.py`
    *   **Action:** The `scrape_website` function will be updated with the following logic:
        1.  **Caching Check:** Before any scraping, check if a valid result for the URL exists in the cache. If so, return the cached data immediately.
        2.  **Proxy Initialization:** Initialize the `ProxyManager` and get a proxy for the Playwright browser, if enabled.
        3.  **Scraping Execution:** Perform the scrape as usual.
        4.  **Caching Save:** If the scrape is successful, save the results to the cache before returning them.
*   **File to Modify:** `src/scraper/page_handler.py`
    *   **Action:** The `fetch_page_content` function will be modified. After a page successfully loads, it will call the new `InteractionHandler` to handle any cookie banners before proceeding to extract the page content.