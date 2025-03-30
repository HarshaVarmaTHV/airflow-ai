# Airflow AI SDK Gemini Example

This project contains an example Apache Airflow DAG demonstrating the use of the `airflow-ai-sdk` to interact with Google's Gemini models.

## DAG: `ai_sdk_gemini_summarization_example`

This DAG performs the following steps:

1.  **`get_product_feedback`**: Simulates fetching sample product feedback as a list of strings.
2.  **`summarize_product_feedback`**: Uses the `@task.llm` decorator from `airflow-ai-sdk` to:
    *   Call the `gemini-1.5-flash-latest` model for each piece of feedback.
    *   Use a system prompt to instruct the model to summarize the feedback, determine sentiment (positive, negative, neutral), and extract feature requests.
    *   Structure the output using a Pydantic model (`ProductFeedbackSummary`).
    *   Skips feedback that doesn't mention "Airflow".
3.  **`print_summaries`**: Prints the structured results from the Gemini model or indicates if a piece of feedback was skipped. Runs even if upstream tasks are skipped (`trigger_rule="all_done"`).

## Setup

### Prerequisites

*   An Apache Airflow environment (like Google Cloud Composer).
*   A Google Cloud Project.
*   A Gemini API Key obtained from [Google AI Studio](https://aistudio.google.com/).

### Installation

1.  **Upload DAG:** Place the `ai_sdk_llm_summarization_dag.py` file into the `dags` folder of your Airflow environment.
2.  **Install Dependencies:** Add the packages listed in `requirements.txt` to your Airflow environment's Python packages:
    *   `airflow-ai-sdk`
    *   `google-generativeai`
3.  **Configure API Key:** Set the following environment variable in your Airflow environment (e.g., via Cloud Composer Environment Variables):
    *   **Name:** `GEMINI_API_KEY`
    *   **Value:** `YOUR_GEMINI_API_KEY` (Replace with your actual key)

## Usage

Once the DAG is uploaded, dependencies installed, and the environment variable is set, the DAG `ai_sdk_gemini_summarization_example` should appear in the Airflow UI (or start running if scheduled). You can monitor its execution and check the logs for the `print_summaries` task to see the output from the Gemini model. 