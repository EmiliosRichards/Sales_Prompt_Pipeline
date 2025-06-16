import pandas as pd
from typing import List, Dict, Any
import logging
import os
import time

from dotenv import load_dotenv

from src.data_handling.loader import load_and_preprocess_data
from src.llm_clients.gemini_client import GeminiClient
from src.core.logging_config import setup_logging
from src.core.config import AppConfig
from src.data_handling.partner_data_handler import load_golden_partners, summarize_golden_partner
from src.utils.helpers import (
    generate_run_id,
    resolve_path,
    initialize_run_metrics,
    setup_output_directories,
    precompute_input_duplicate_stats,
    initialize_dataframe_columns
)
from src.processing.pipeline_flow import execute_pipeline_flow

load_dotenv()

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_test_pipeline():
    """
    Runs a test of the sales prompt generation pipeline on a small subset of data.
    """
    app_config = AppConfig()
    run_id = generate_run_id()
    
    # Use a dedicated output directory for tests
    run_output_dir, llm_context_dir = setup_output_directories(app_config, f"test_{run_id}", __file__)

    logger.info(f"Test Run ID: {run_id}")
    logger.info(f"Test output directory: {run_output_dir}")

    # Initialize Gemini Client
    try:
        gemini_client = GeminiClient(config=app_config)
        logger.info("GeminiClient initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize GeminiClient: {e}", exc_info=True)
        return

    # Load Golden Partners
    golden_partner_summaries: List[str] = []
    try:
        golden_partner_data_path_abs = resolve_path(app_config.PATH_TO_GOLDEN_PARTNERS_DATA, __file__)
        loaded_partners_raw = load_golden_partners(file_path=golden_partner_data_path_abs)
        if loaded_partners_raw:
            logger.info(f"Loaded {len(loaded_partners_raw)} golden partners.")
            for partner_dict_data in loaded_partners_raw:
                summary_str = summarize_golden_partner(partner_data=partner_dict_data)
                if summary_str and summary_str != "Partner data not available or empty.":
                    golden_partner_summaries.append(summary_str)
            logger.info(f"Generated {len(golden_partner_summaries)} golden partner summaries.")
        else:
            logger.warning("No golden partner data loaded.")
    except Exception as e:
        logger.error(f"Error loading golden partners: {e}", exc_info=True)
        return

    # Load and preprocess a small chunk of the input data
    try:
        input_file_path_abs = resolve_path('data/final_80k.csv', __file__)
        app_config.input_file_profile_name = "final_80k" # Set the correct profile
        app_config.nrows_config = 5 # Set the number of rows to read in the config
        df = load_and_preprocess_data(input_file_path_abs, app_config_instance=app_config)
        if df is not None:
            logger.info(f"Loaded {len(df)} rows for testing.")
        else:
            logger.error("Failed to load data.")
            return
    except Exception as e:
        logger.error(f"Error loading input data: {e}", exc_info=True)
        return

    # Set the correct input profile for the test data
    app_config.input_file_profile_name = "final_80k"

    # Initialize metrics and failure log (dummy for this test)
    run_metrics: Dict[str, Any] = initialize_run_metrics(run_id)
    failure_log_csv_path = os.path.join(run_output_dir, f"test_failed_rows_{run_id}.csv")
    with open(failure_log_csv_path, 'w', newline='', encoding='utf-8') as f:
        failure_writer = None # Dummy writer

        # Execute the pipeline flow
        _, all_match_outputs, _, _, _, _, _, _ = execute_pipeline_flow(
            df=df,
            app_config=app_config,
            gemini_client=gemini_client,
            run_output_dir=run_output_dir,
            llm_context_dir=llm_context_dir,
            run_id=run_id,
            failure_writer=failure_writer,
            run_metrics=run_metrics,
            golden_partner_summaries=golden_partner_summaries,
        )

    # Print the results
    logger.info("\n--- Generated Sales Pitches ---")
    if all_match_outputs:
        for i, result in enumerate(all_match_outputs):
            company_url = result.analyzed_company_url
            sales_line = result.phone_sales_line
            match_name = result.closest_golden_partner_match_name
            rationale = result.match_rationale_features

            print(f"\n--- Result {i+1} ---")
            print(f"Company URL: {company_url}")
            print(f"Closest Match: {match_name}")
            print(f"Rationale: {rationale}")
            print(f"Generated Sales Line: {sales_line}")
    else:
        print("No sales pitches were generated.")
    logger.info("--- End of Test ---")


if __name__ == "__main__":
    run_test_pipeline()