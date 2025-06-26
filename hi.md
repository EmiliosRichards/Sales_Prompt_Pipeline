# This file serves as a template for the .env file.
# Copy this file to .env and fill in your actual values.
# Lines starting with # are comments.

# === General Project Configuration ===
# Path to the input data file (Excel or CSV). Relative to the project root.
INPUT_EXCEL_FILE_PATH="data/deduped_urls_26-05-2025.xlsx"

# Specifies a range of rows (1-based inclusive) or a number of rows to process from the input file.
# Examples: "10-20" (rows 10-20), "20" (first 20), "10-" (row 10 to end), "-20" (first 20), "" or "0" (all rows).
ROW_PROCESSING_RANGE=""

# Base directory for all output files. Relative to the project root. Will be created if it doesn't exist.
OUTPUT_BASE_DIR="output_data"

# Template for the main summary Excel report file name. {run_id} will be replaced.
OUTPUT_EXCEL_FILE_NAME_TEMPLATE="Pipeline_Summary_Report_{run_id}.xlsx"

# Specifies which input column mapping profile to use from AppConfig.INPUT_COLUMN_PROFILES.
# See src/core/config.py for profile definitions (e.g., "default", "lean_formatted", "ManauvKlaus").
INPUT_FILE_PROFILE_NAME="default"

# Number of consecutive empty rows to detect as end-of-data when ROW_PROCESSING_RANGE is open-ended.
CONSECUTIVE_EMPTY_ROWS_TO_STOP="3"

# === Filename Configuration for Output Files ===
# Max length for the sanitized company name part of output filenames.
FILENAME_COMPANY_NAME_MAX_LEN="25"
# Max length for the sanitized URL domain part of output filenames.
FILENAME_URL_DOMAIN_MAX_LEN="8"
# Max length for the URL hash part of output filenames.
FILENAME_URL_HASH_MAX_LEN="8"

# === Logging Configuration ===
# Log level for the main log file (e.g., DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL="INFO"
# Log level for the console output (e.g., DEBUG, INFO, WARNING, ERROR)
CONSOLE_LOG_LEVEL="WARNING"

# === LLM Configuration (Google Gemini) ===
# REQUIRED: Your API key for the Google Gemini service.
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

# Gemini model to use (e.g., "gemini-1.5-pro-latest", "gemini-1.5-flash-latest").
LLM_MODEL_NAME="gemini-2.5-flash-preview-05-20"
LLM_MODEL_NAME_SALES_INSIGHTS="gemini-2.5-pro-preview-06-05"
# Temperature for general-purpose LLM calls.
LLM_TEMPERATURE_DEFAULT="0.3"

# Temperature for precise data extraction tasks (lower is better).
LLM_TEMPERATURE_EXTRACTION="0.2"

# Temperature for creative tasks like sales pitch generation (higher allows more creativity).
LLM_TEMPERATURE_CREATIVE="0.5"

# Optional: Specific temperature for summarization tasks. If blank, uses LLM_TEMPERATURE_DEFAULT.
LLM_TEMPERATURE_SUMMARY=""

LLM_MAX_TOKENS="3000"
LLM_TOP_K=""
LLM_TOP_P=""

# === Extraction Profiles and Prompt Paths (relative to project root) ===
# Active extraction profile: "minimal", "minimal_plus_summary", "enriched_direct" (future).
EXTRACTION_PROFILE="minimal"

# Prompt for generating homepage context (company name, summary, industry).
PROMPT_PATH_HOMEPAGE_CONTEXT="prompts/summarization_prompt.txt"

# Prompt for general summarization tasks (if used separately).
PROMPT_PATH_SUMMARIZATION="prompts/summarization_prompt.txt"

# Prompt for website text summarization.
PROMPT_PATH_WEBSITE_SUMMARIZER="prompts/website_summarizer_prompt.txt"

# Maximum characters of website text to feed into the summarization LLM.
LLM_MAX_INPUT_CHARS_FOR_SUMMARY="40000"

# Number of top-priority pages the scraper should collect text from for summarization.
SCRAPER_PAGES_FOR_SUMMARY_COUNT="3"
# === Web Scraper Configuration ===
# A comma-separated list of User-Agent strings to be rotated for scraper requests.
SCRAPER_USER_AGENTS="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36,Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36,Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

# A JSON string of default headers to be sent with every scraper request.
SCRAPER_DEFAULT_HEADERS='{"Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Referer": "https://www.google.com/"}'
SCRAPER_PAGE_TIMEOUT_MS="30000"
SCRAPER_NAVIGATION_TIMEOUT_MS="60000"
SCRAPER_MAX_RETRIES="2"
SCRAPER_RETRY_DELAY_SECONDS="5"
SCRAPER_NETWORKIDLE_TIMEOUT_MS="3000" # Default 3s, 0 to disable.
MAX_DEPTH_INTERNAL_LINKS="1"

# Keywords to identify relevant internal links. Comma-separated.
TARGET_LINK_KEYWORDS="about,company,services,products,solutions,team,mission"
# Keywords for top-priority pages (e.g., "Impressum", "Kontakt"). Comma-separated.
SCRAPER_CRITICAL_PRIORITY_KEYWORDS="about-us,company-profile"
# Keywords for high-priority pages (e.g., "Legal", "Privacy"). Comma-separated.
SCRAPER_HIGH_PRIORITY_KEYWORDS="services,products,solutions"
# Max path segments for a priority keyword to retain its highest score tier.
SCRAPER_MAX_KEYWORD_PATH_SEGMENTS="3"
# URL path patterns to hard-exclude from scraping. Comma-separated.
SCRAPER_EXCLUDE_LINK_PATH_PATTERNS="/media/,/blog/,/wp-content/,/video/,/hilfe-video/"
# Max pages to scrape per domain (0 for no limit).
SCRAPER_MAX_PAGES_PER_DOMAIN="20"
# Minimum score a link needs to be added to the scrape queue.
SCRAPER_MIN_SCORE_TO_QUEUE="40"
# Score threshold for a page to bypass SCRAPER_MAX_PAGES_PER_DOMAIN.
SCRAPER_SCORE_THRESHOLD_FOR_LIMIT_BYPASS="80"
# Max additional high-priority pages to scrape after SCRAPER_MAX_PAGES_PER_DOMAIN is hit.
SCRAPER_MAX_HIGH_PRIORITY_PAGES_AFTER_LIMIT="5"

# Whether the scraper should respect robots.txt (True/False).
RESPECT_ROBOTS_TXT="True"
# User-agent string for checking robots.txt.
ROBOTS_TXT_USER_AGENT="*"

# === URL Handling ===
# TLDs to try appending to domain-like inputs lacking a TLD. Comma-separated.
URL_PROBING_TLDS="de,com,at,ch"
# Enable DNS error fallback strategies (True/False).
ENABLE_DNS_ERROR_FALLBACKS="True"

# === Page Type Classification Keywords (for scraper link scoring and content analysis) ===
# Keywords to identify 'about' or 'company profile' pages. Comma-separated.
PAGE_TYPE_KEYWORDS_ABOUT="about,about-us,company,profile,mission,vision,team,management,history,karriere,careers"
# Keywords to identify 'product' or 'service' pages. Comma-separated.
PAGE_TYPE_KEYWORDS_PRODUCT_SERVICE="products,services,solutions,offerings,platform,features,technologie,technology,portfolio,leistungen"

PROMPT_PATH_ATTRIBUTE_EXTRACTOR="prompts/attribute_extractor_prompt.txt"
# Path to the Golden Partners CSV file
PATH_TO_GOLDEN_PARTNERS_CSV="data/golden_partners.csv"
# Maximum number of Golden Partner summaries to include in the prompt for LLM Call 3.
MAX_GOLDEN_PARTNERS_IN_PROMPT="50"
SALES_PROMPT_LANGUAGE="de"

# === German Language Prompt Paths (relative to project root) ===
# These are optional. If left blank, the default paths from the AppConfig class will be used.
PROMPT_PATH_GERMAN_PARTNER_MATCHING=""
PROMPT_PATH_GERMAN_SALES_PITCH_GENERATION=""
# === Advanced Scraper Features ===

# --- Caching Settings ---
# Enable or disable the file-based cache for scraping results.
CACHING_ENABLED=True
# The directory where cache files will be stored.
CACHE_DIR=cache

# --- Proxy Management ---
# Enable or disable the use of proxies for IP rotation.
PROXY_ENABLED=False
# Provide a comma-separated list of your proxy URLs.
# Example: PROXY_LIST="http://user:pass@proxy1.com:8080,http://user:pass@proxy2.com:8080"
PROXY_LIST=
# Choose the proxy rotation strategy: 'random', 'sequential', or 'rotate_on_failure'.
PROXY_ROTATION_STRATEGY=random
# Enable or disable automatic health checks for proxies.
PROXY_HEALTH_CHECK_ENABLED=True
# Set the cooldown period in seconds for a failing proxy before it's retried.
PROXY_COOLDOWN_SECONDS=300

# --- Interaction Handling ---
# Enable or disable the automatic handling of modals (cookie banners, pop-ups).
INTERACTION_HANDLER_ENABLED=True
# Comma-separated list of CSS selectors for elements to click.
INTERACTION_SELECTORS="button[id*='accept'],button[id*='agree'],button[id*='consent'],button[id*='cookie']"
# Comma-separated list of text queries to find on clickable elements.
INTERACTION_TEXT_QUERIES="Accept all,Agree,Consent,I agree"
# Timeout in seconds for the interaction handler loop.
INTERACTION_HANDLER_TIMEOUT_SECONDS=5

# --- CAPTCHA Solving ---
# Enable or disable third-party CAPTCHA solving.
CAPTCHA_SOLVER_ENABLED=False
# Specify the CAPTCHA solving service provider (e.g., '2captcha').
CAPTCHA_PROVIDER=2captcha
# Your API key for the chosen CAPTCHA solving service.
CAPTCHA_API_KEY=