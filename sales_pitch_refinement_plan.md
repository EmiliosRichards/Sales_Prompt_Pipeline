# Plan to Refine Sales Pitch Rationale Generation (Version 2)

The goal is to improve the quality and specificity of the `match_rationale_features` generated during the sales pitch step. This will be achieved by providing more detailed instructions in the prompt, including positive and negative examples, and by feeding the rationale from the partner matching step as additional context.

## 1. Update the Sales Pitch Generation Prompt

The `prompts/german_sales_pitch_generation_prompt.txt` file will be modified. The key changes will be:

*   **Add Rationale Context:** A new placeholder, `{{PREVIOUS_MATCH_RATIONALE_PLACEHOLDER}}`, will be added to provide the rationale from the partner matching step as context.
*   **Refine Rationale Generation Instructions:** The instructions for generating `match_rationale_features` will be replaced with the following detailed guidance:

    ---
    **1. Identify Key Rationale (in German):**
    Generate an array called `match_rationale_features`.

    Each item must describe specific, clear, and concrete similarities between the Target Company and Matched Golden Partner.

    Acceptable similarities include:
    *   Clearly overlapping customer segments
    *   Similar products, services, or technology fields
    *   Industry-specific regulatory or operational requirements

    **Example of good rationale features:**
    *   `"Gemeinsame Zielgruppe: Pflegeeinrichtungen, Kliniken und Gesundheitseinrichtungen"`
    *   `"Ähnliche Produkte: KI-gestützte Softwarelösungen zur Prozessoptimierung im Gesundheitswesen"`

    **Example of bad rationale (DO NOT produce these):**
    *   `"Beide Unternehmen sind innovativ"` (too general)
    *   `"Sie operieren im gleichen Marktsegment"` (not specific enough)
    ---

*   **Add Placeholder Instruction:** An explicit instruction will be added to ensure the `{programmatic placeholder}` is never altered.

## 2. Update the Sales Pitch Generation Task

The function `generate_sales_pitch` in `src/extractors/llm_tasks/generate_sales_pitch_task.py` will be updated to accept the `match_rationale_features` from the previous step and pass them to the prompt.

*   **Modify Function Signature:** The `generate_sales_pitch` function signature will be updated to accept a new argument: `previous_match_rationale: List[str]`.
*   **Update Prompt Formatting:** The code that formats the prompt will be updated to replace the new `{{PREVIOUS_MATCH_RATIONALE_PLACEHOLDER}}` with the provided rationale.

## 3. Update the Main Pipeline

The main pipeline logic will be updated to pass the `match_rationale_features` from the `match_partner` output to the `generate_sales_pitch` input. `src/processing/pipeline_flow.py` will be investigated and modified to implement this change.

```mermaid
sequenceDiagram
    participant pipeline as Pipeline
    participant match_partner as match_partner()
    participant generate_sales_pitch as generate_sales_pitch()

    pipeline->>match_partner: (target_attributes, ...)
    match_partner-->>pipeline: (partner_match_output, ...)
    note right of match_partner: partner_match_output contains<br/>`match_rationale_features`

    pipeline->>generate_sales_pitch: (target_attributes, matched_partner, **partner_match_output.match_rationale_features**)
    generate_sales_pitch-->>pipeline: (golden_partner_match_output, ...)