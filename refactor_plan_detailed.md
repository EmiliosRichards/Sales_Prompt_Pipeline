# Detailed Refactoring Plan: Splitting Sales Insight Generation

This document provides a granular breakdown of the plan to refactor the sales insight generation process. Tasks with a difficulty rating of 4 or higher are expanded into sub-tasks.

---

### Task 1: Create New LLM Task Modules (Overall Difficulty: 7/10)

This is the most significant part of the refactor, involving the creation of two new modules to handle the separated LLM calls.

**Sub-task 1.1: Create the Partner Matching Task File**
*   **Action:** Create a new file: `src/extractors/llm_tasks/match_partner_task.py`.
*   **Details:** This file will contain the logic for the first new LLM call, which is solely focused on matching.
*   **Anticipated Challenge:** Ensuring the new file has the correct boilerplate, imports (`json`, `logging`, `GeminiClient`, schemas, etc.), and function signature to integrate smoothly.
*   **Assessment:** I will start by creating the file with a placeholder function and necessary imports, ensuring the basic structure is sound before adding complex logic.

**Sub-taks 1.2: Define the Matching-Only Schema**
*   **Action:** In `src/core/schemas.py`, add a new Pydantic schema named `PartnerMatchOnlyOutput`.
*   **Details:** This schema will be simple, primarily designed to validate the JSON output from the matching LLM call. It will likely contain `matched_partner_name: str` and `match_score: str`.
*   **Anticipated Challenge:** The LLM might occasionally return malformed JSON. The Pydantic schema provides a robust way to validate the structure.
*   **Assessment:** The schema definition is straightforward and serves as a contract for the LLM's output.

**Sub-task 1.3: Implement the `match_partner` Function**
*   **Action:** Inside `match_partner_task.py`, implement the `match_partner` function.
*   **Details:** This function will accept the target company's attributes and the list of all golden partner summaries. It will load the new `german_partner_matching_prompt.txt`, format it, call the Gemini client, and parse the response into the `PartnerMatchOnlyOutput` schema.
*   **Anticipated Challenge:** The logic must correctly handle the "No suitable match found" case returned by the LLM, as defined in our improved prompt.
*   **Assessment:** The function's success will be determined by its ability to reliably return a validated `PartnerMatchOnlyOutput` object or handle the "no match" scenario without errors.

**Sub-task 1.4: Create the Sales Pitch Generation Task File**
*   **Action:** Create the second new file: `src/extractors/llm_tasks/generate_sales_pitch_task.py`.
*   **Details:** This file will handle the second LLM call, which generates the creative sales pitch.
*   **Anticipated Challenge:** Similar to the first file, setting up the correct initial structure is key.
*   **Assessment:** I will create the file with a placeholder function to begin.

**Sub-task 1.5: Implement the `generate_sales_pitch` Function**
*   **Action:** Inside `generate_sales_pitch_task.py`, implement the `generate_sales_pitch` function.
*   **Details:** This function will be more focused. It will receive the target company's attributes and the full data of the *single, pre-selected* matched partner. It will then use the new `german_sales_pitch_generation_prompt.txt` to generate the final, detailed `GoldenPartnerMatchOutput`.
*   **Anticipated Challenge:** The prompt formatting will be simpler as it only deals with one partner, but ensuring all necessary data points (like `avg_leads_per_day`) are correctly passed and used is critical.
*   **Assessment:** The function must successfully produce a validated `GoldenPartnerMatchOutput` object.

---

### Task 2: Update Pipeline Flow (Overall Difficulty: 6/10)

This task involves re-wiring the main pipeline to use the new two-step LLM process.

**Sub-task 2.1: Modify Imports and Function Calls in `pipeline_flow.py`**
*   **Action:** Open `src/processing/pipeline_flow.py`. Remove the import for `generate_sales_insights` and add imports for the new `match_partner` and `generate_sales_pitch` functions.
*   **Anticipated Challenge:** The `execute_pipeline_flow` function signature will change. It will no longer need `golden_partners_raw` as a direct parameter for the LLM call, but it will need access to it for data retrieval. I will adjust the plan to keep `golden_partners_raw` available within the scope of this function.
*   **Assessment:** The code should be syntactically correct after changing the imports and function calls.

**Sub-task 2.2: Integrate the New Two-Step Logic**
*   **Action:** In the main loop of `execute_pipeline_flow`, replace the single call to `generate_sales_insights` with the new sequence.
*   **Details:**
    1.  Call `match_partner`, passing in the target attributes and all partner summaries.
    2.  Check the result. If `matched_partner_name` is "No suitable match found", log this information and create a partial `GoldenPartnerMatchOutput` object indicating the failure, then `continue` to the next row.
    3.  If a match is found, search the `golden_partners_raw` list to get the full data for the matched partner.
    4.  Call `generate_sales_pitch`, passing the target attributes and the single matched partner's full data.
*   **Anticipated Challenge:** The logic for retrieving the full partner data after the match must be efficient and handle the possibility of the name not being found (though this is unlikely if the LLM is working correctly).
*   **Assessment:** The data flow must be seamless, with the output of the first call correctly informing the input of the second, and edge cases (like no match) handled gracefully.

**Sub-task 2.3: Final Cleanup**
*   **Action:** Once the new pipeline flow is fully implemented and validated, delete the old `src/extractors/llm_tasks/generate_insights_task.py` file.
*   **Anticipated Challenge:** None. This is a simple file deletion.
*   **Assessment:** This final step ensures that no legacy code is left behind, completing the refactor.

---
I will now await your instructions.