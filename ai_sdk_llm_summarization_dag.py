# ai_sdk_llm_summarization_dag.py
import pendulum
from typing import Literal, Any

from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

# Import the airflow-ai-sdk
import airflow_ai_sdk as ai_sdk

# Define the Pydantic model for the structured output
class ProductFeedbackSummary(ai_sdk.BaseModel):
    """Structure to hold the summarized feedback."""
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]
    feature_requests: list[str]

# Define the DAG
@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=['ai-sdk', 'example', 'gemini'],
)
def ai_sdk_gemini_summarization_example():
    """
    Example DAG demonstrating @task.llm for text summarization
    using airflow-ai-sdk with Google Gemini.
    """

    @task
    def get_product_feedback() -> list[str]:
        """
        Provides sample product feedback.
        In a real DAG, this could fetch data from an API, database, etc.
        """
        return [
            "The new dashboard UI in Airflow is fantastic! Much easier to navigate.",
            "I'm having trouble connecting my custom executor. The documentation is unclear.",
            "Airflow is great, but I wish it had better native support for GPU scheduling.",
            "The latest update broke my CI/CD pipeline, please fix the scheduler bug.",
            "This feedback doesn't mention Airflow.", # This one should be skipped
        ]

    @task.llm(
        # Specify the connection ID for Google Generative AI - REMOVED
        # conn_id="google_genai_default", 
        # Specify the Gemini model you want to use
        # Common options include 'gemini-pro', 'gemini-1.0-pro', 'gemini-1.5-flash-latest'
        model="gemini-1.5-flash-latest",
        result_type=ProductFeedbackSummary, # The Pydantic model to structure the output
        system_prompt="""
        You are a helpful assistant that summarizes product feedback about Apache Airflow.
        Determine the sentiment (positive, negative, or neutral) and extract any specific feature requests mentioned.
        """
    )
    def summarize_product_feedback(feedback: str | None = None) -> ProductFeedbackSummary:
        """
        Summarizes a single piece of product feedback using a Gemini LLM.
        Skips feedback if it doesn't mention "Airflow".
        """
        # Simple preprocessing/filtering logic
        if feedback is None or "Airflow" not in feedback:
            print(f"Skipping feedback: {feedback}")
            raise AirflowSkipException("Feedback does not mention Airflow")

        print(f"Summarizing feedback: {feedback}")
        # The feedback string is automatically passed as the main prompt argument to the LLM
        return feedback

    @task(trigger_rule="all_done")
    def print_summaries(summaries: list[dict[str, Any]]):
        """Prints the summarized feedback."""
        print("Received Summaries:")
        for summary_dict in summaries:
            if summary_dict: # Check if the task wasn't skipped
                try:
                    # Re-create the Pydantic model instance for easier access/printing
                    summary_obj = ProductFeedbackSummary(**summary_dict)
                    print("-" * 20)
                    print(f"Summary: {summary_obj.summary}")
                    print(f"Sentiment: {summary_obj.sentiment}")
                    print(f"Feature Requests: {summary_obj.feature_requests}")
                except Exception as e:
                    print("-" * 20)
                    print(f"Error processing summary: {summary_dict}")
                    print(f"Error: {e}")
            else:
                print("-" * 20)
                print("Skipped feedback summary.")

    # Define the task flow
    feedback_list = get_product_feedback()
    # Use .expand() to run the LLM task for each item in the feedback list
    summarized_feedback = summarize_product_feedback.expand(feedback=feedback_list)
    print_summaries(summarized_feedback)

# Instantiate the DAG
ai_sdk_gemini_summarization_example()