import streamlit as st
import time

def run_with_loading(pipeline_function):
    """
    Wraps a pipeline function with loading UI
    """

    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        "Loading data...",
        "Building features...",
        "Training model...",
        "Generating predictions...",
        "Computing ingredient demand...",
        "Calculating order plan..."
    ]

    results = None

    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))

        time.sleep(0.3)

        # Run actual pipeline only once (on final step)
        if i == len(steps) - 1:
            results = pipeline_function()

    status_text.text("✅ Done!")
    return results