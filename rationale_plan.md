# Plan to Add Rationale to Matching Call (Version 2)

The goal is to enhance the partner matching process by including a "rationale" for why a partner was selected. This will be achieved by modifying the system instruction, the prompt sent to the LLM, and updating the data structure that handles the response.

## 1. Update the Partner Matching Prompt

The `prompts/german_partner_matching_prompt.txt` file will be modified. The key changes will be:

*   **Add a new instruction:** A step will be added to the prompt, requiring the LLM to identify and list the key reasons for the match in German, with examples.
*   **Update the JSON format:** The example JSON structure in the prompt will be updated to include the new `match_rationale_features` field with more specific examples.

```diff
--- a/prompts/german_partner_matching_prompt.txt
+++ b/prompts/german_partner_matching_prompt.txt
@@ -8,11 +8,18 @@
  8 | 3.  **No Match Condition.** If NO partner shares a reasonably similar industry or target audience, you MUST return "No suitable match found" for the `matched_partner_name` and a `match_score` of "Low". Do not force a match.
  9 | 
+10 | 4.  **Identify Key Rationale (in German).** Based on the shared attributes, provide a list of 2-4 key reasons for the match in the `match_rationale_features` field. These should be concise, clear, and in German. Examples: "Gemeinsame Zielgruppe: ...", "Ähnliche Produkte/Services: ...", "Überschneidende Marktsegmente: ..."
+11 |
 10 | **JSON Response Format:**
 11 | {
 12 |   "match_score": "High",
-13 |   "matched_partner_name": "Partner Name"
+13 |   "matched_partner_name": "Partner Name",
+14 |   "match_rationale_features": [
+15 |     "Gemeinsame Zielgruppe im Gesundheitsbereich, speziell Einrichtungen mit hohem Bedarf an technologiebasierten Lösungen.",
+16 |     "Ähnliche technologische Ausrichtung: Software und assistive Technologien zur Verbesserung der Patientenversorgung und Mobilität."
+17 |   ]
 14 | }
 15 | 
 16 | --------TARGET COMPANY ATTRIBUTES JSON------------
```

## 2. Update the System Instruction

To ensure the LLM includes the new field, the system instruction in `src/extractors/llm_tasks/match_partner_task.py` will be updated.

*   **File to Modify:** `src/extractors/llm_tasks/match_partner_task.py`
*   **Change:** Modify the `system_instruction_text` to explicitly mention that the response must include `match_rationale_features`.

```python
# src/extractors/llm_tasks/match_partner_task.py

system_instruction_text = (
    "You are a partner matching assistant. Your entire response MUST be a single, "
    "valid JSON formatted string. Do NOT include any explanations, markdown formatting (like ```json), "
    "or any other text outside of this JSON string. The JSON object must strictly conform to the "
    "PartnerMatchOnlyOutput schema, including the match_score, matched_partner_name, and match_rationale_features fields."
)
```

## 3. Update the Data Schema

To handle the new data from the LLM, the `src/core/schemas.py` file will be updated. Specifically, the `match_rationale_features` field will be added to the `PartnerMatchOnlyOutput` Pydantic model.

*   **File to Modify:** `src/core/schemas.py`
*   **Class to Modify:** `PartnerMatchOnlyOutput`
*   **Change:** Add `match_rationale_features: Optional[List[str]] = Field(default_factory=list, description="List of key shared features or reasons provided by the LLM for the match.")`

```mermaid
classDiagram
    class PartnerMatchOnlyOutput {
        +match_score: Optional[str]
        +matched_partner_name: Optional[str]
        +match_rationale_features: Optional[List[str]]
    }
---

## Difficulty Assessment

Here is a breakdown of the difficulty for each step in the plan, rated on a scale of 1 to 10.

*   **1. Update the Partner Matching Prompt:**
    *   **Rating: 2/10**
    *   **Justification:** This is a straightforward text edit. The primary task is to carefully craft the new instructions for the LLM to ensure clarity and effectiveness, but it doesn't involve any complex code logic.

*   **2. Update the System Instruction:**
    *   **Rating: 1/10**
    *   **Justification:** This is a minor change to a string variable within a Python file. The risk is very low, and the effort required is minimal.

*   **3. Update the Data Schema:**
    *   **Rating: 2/10**
    *   **Justification:** This involves adding a single field to a Pydantic model. It's a simple code change, but it's critical for ensuring the new data is correctly parsed and validated. The existing framework handles the heavy lifting.