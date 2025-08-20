import json
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric
from deepeval.metrics.ragas import RagasMetric

import deepeval
import subprocess


# Inisialisasi metrik
arm = AnswerRelevancyMetric(strict_mode=True)
fm = FaithfulnessMetric()
prec = ContextualPrecisionMetric()
recall = ContextualRecallMetric()
ragas = RagasMetric(threshold=0.5, model="gpt-3.5-turbo")


# Load test cases
with open("test_cases.json", "r") as f:
    cases = json.load(f)

test_cases = []

for case in cases:
    input_text = case["input"]
    expected_output = case.get("expected_output", "")

    result = subprocess.run(
        ["node", "cliEvaluators.js", input_text],
        capture_output=True, text=True
    )

    actual_output = result.stdout.strip()
    print(f"\n❓ Prompt: {input_text}\n📤 Output: {actual_output}\n")

    test_cases.append(
        LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            expected_output=expected_output
        )
    )

# Jalankan evaluasi
deepeval.evaluate(
    test_cases,
    metrics = [ragas]
)
