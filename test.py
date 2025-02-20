from src.reframe.core import Reframe
import json

# Load API key from secrets file
with open("secrets.json") as f:
    secrets = json.load(f)
    api_key = secrets["OPENAI_API_KEY_SR"]  # Use the specific API key

# Initialize Reframe
reframe = Reframe(api_key=api_key)

# Test drug content classification
test_text = "this is for testing"
result = reframe.classify_drug_content(test_text)
print(f"Drug classification result: {result}")

# Test stigma analysis
stigma_result = reframe.analyze_stigma(test_text)
print(f"Stigma analysis result: {stigma_result}")

# Test style analysis
style_result = reframe.retrive_style_instruction(test_text)
print(f"Style analysis result: {style_result}")

# Test text rewriting with sample explanation and style
sample_explanation = "Labeling: Contains stigmatizing labels"
sample_style = {"tone": "neutral", "lexical_diversity": "moderate"}
rewrite_result = reframe.rewrite_text(test_text, sample_explanation, sample_style)
print(f"Rewrite result: {rewrite_result}")