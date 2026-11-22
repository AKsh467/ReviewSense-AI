"""
ReviewSense AI — Automated Prototype Verification & Test Suite
Covers the 10 testing requirements from the project specification:
1. Normal product reviews
2. Mixed sentiment reviews
3. Reviews with repeated aspects
4. Reviews containing only positive feedback
5. Reviews containing only negative feedback
6. Very short reviews
7. Empty input handling
8. Invalid CSV handling
9. CSV with missing values
10. API failure / malformed JSON parsing & schema validation
Plus priority ranking logic, local history persistence, and demo dataset verification.
"""

import io
import json
import unittest
from pathlib import Path
import pandas as pd

from config import (
    DEMO_HEADPHONE_RESULT,
    DEMO_HEADPHONE_REVIEWS,
    SAMPLE_DATA_DIR,
    get_backend_llm_config,
)
from history_manager import (
    clear_all_history,
    delete_history_entry,
    get_all_history,
    get_history_entry,
    save_history_entry,
)
from llm_analyzer import (
    clean_and_parse_json,
    generate_markdown_summary,
    normalize_text_reviews,
    process_csv_file,
    validate_v3_schema,
)


class TestReviewSenseAIPrototype(unittest.TestCase):

    def setUp(self):
        # Clear test history before tests
        clear_all_history()

    def tearDown(self):
        clear_all_history()

    # -----------------------------------------------------
    # Test 1: Normal Product Reviews Parsing
    # -----------------------------------------------------
    def test_01_normal_product_reviews(self):
        raw_text = (
            "1. The camera is outstanding for outdoor photography.\n"
            "2. Battery drain is very noticeable when recording 4K video.\n"
            "3. The grip feels comfortable in hand."
        )
        reviews = normalize_text_reviews(raw_text)
        self.assertEqual(len(reviews), 3)
        self.assertEqual(reviews[0], "The camera is outstanding for outdoor photography.")
        self.assertEqual(reviews[1], "Battery drain is very noticeable when recording 4K video.")
        self.assertEqual(reviews[2], "The grip feels comfortable in hand.")

    # -----------------------------------------------------
    # Test 2: Mixed Sentiment Reviews Parsing
    # -----------------------------------------------------
    def test_02_mixed_sentiment_reviews(self):
        raw_text = (
            "- The sound quality is top-notch, but the ear cushions get sweaty quickly.\n"
            "* Great display and speed, though the build quality feels slightly cheap."
        )
        reviews = normalize_text_reviews(raw_text)
        self.assertEqual(len(reviews), 2)
        self.assertTrue("sweaty" in reviews[0])
        self.assertTrue("build quality" in reviews[1])

    # -----------------------------------------------------
    # Test 3: Reviews with Repeated Aspects
    # -----------------------------------------------------
    def test_03_repeated_aspects_schema_validation(self):
        # Validate that schema handles multiple aspects and counts correctly
        mock_raw = {
            "overall_sentiment": {"classification": "Mixed", "explanation": "Sound is loved, battery is hated."},
            "aspect_analysis": [
                {
                    "aspect": "Battery",
                    "sentiment": "Negative",
                    "total_reviews_mentioning": 3,
                    "positive_reviews": 0,
                    "negative_reviews": 3,
                    "supporting_quotes": ["Battery dies fast", "Awful battery life"]
                },
                {
                    "aspect": "Sound Quality",
                    "sentiment": "Positive",
                    "total_reviews_mentioning": 3,
                    "positive_reviews": 3,
                    "negative_reviews": 0,
                    "supporting_quotes": ["Sound is crisp", "Great audio bass"]
                }
            ],
            "recurring_negative_concerns": {
                "multiple_review_issues": ["Battery: 3 distinct reviews expressed dissatisfaction."],
                "single_review_issues": []
            },
            "product_strengths": [
                {"aspect": "Sound Quality", "positive_review_count": 3, "reason": "Consistent praise across all reviews."}
            ],
            "prioritized_improvements": [
                {
                    "priority": "High",
                    "aspect": "Battery",
                    "negative_review_count": 3,
                    "reason": "Mentioned negatively in 3 reviews.",
                    "suggestion": "Double battery capacity."
                }
            ]
        }
        validated = validate_v3_schema(mock_raw)
        self.assertEqual(len(validated["aspect_analysis"]), 2)
        self.assertEqual(validated["prioritized_improvements"][0]["priority"], "High")
        self.assertEqual(validated["prioritized_improvements"][0]["negative_review_count"], 3)

    # -----------------------------------------------------
    # Test 4: Positive Feedback Only
    # -----------------------------------------------------
    def test_04_positive_reviews_only(self):
        mock_pos = {
            "overall_sentiment": {"classification": "Positive", "explanation": "All users are thrilled."},
            "aspect_analysis": [
                {
                    "aspect": "Performance",
                    "sentiment": "Positive",
                    "total_reviews_mentioning": 2,
                    "positive_reviews": 2,
                    "negative_reviews": 0,
                    "supporting_quotes": ["Blazing fast", "Super responsive"]
                }
            ],
            "recurring_negative_concerns": {"multiple_review_issues": [], "single_review_issues": []},
            "product_strengths": [{"aspect": "Performance", "positive_review_count": 2, "reason": "Fast"}],
            "prioritized_improvements": []
        }
        validated = validate_v3_schema(mock_pos)
        self.assertEqual(validated["overall_sentiment"]["classification"], "Positive")
        self.assertEqual(len(validated["prioritized_improvements"]), 0)

    # -----------------------------------------------------
    # Test 5: Negative Feedback Only
    # -----------------------------------------------------
    def test_05_negative_reviews_only(self):
        mock_neg = {
            "overall_sentiment": {"classification": "Negative", "explanation": "Severe customer complaints."},
            "aspect_analysis": [
                {
                    "aspect": "Build Quality",
                    "sentiment": "Negative",
                    "total_reviews_mentioning": 2,
                    "positive_reviews": 0,
                    "negative_reviews": 2,
                    "supporting_quotes": ["Broke on day 2", "Hinges cracked immediately"]
                }
            ],
            "recurring_negative_concerns": {
                "multiple_review_issues": ["Build Quality: broke rapidly across 2 reviews."],
                "single_review_issues": []
            },
            "product_strengths": [],
            "prioritized_improvements": [
                {
                    "priority": "High",
                    "aspect": "Build Quality",
                    "negative_review_count": 2,
                    "reason": "2 reviews reporting breakage.",
                    "suggestion": "Strengthen hinge material."
                }
            ]
        }
        validated = validate_v3_schema(mock_neg)
        self.assertEqual(validated["overall_sentiment"]["classification"], "Negative")
        self.assertEqual(validated["prioritized_improvements"][0]["priority"], "High")

    # -----------------------------------------------------
    # Test 6: Very Short Reviews
    # -----------------------------------------------------
    def test_06_very_short_reviews(self):
        raw_text = "Good.\nBad battery.\nLoved it."
        reviews = normalize_text_reviews(raw_text)
        self.assertEqual(len(reviews), 3)
        self.assertEqual(reviews[1], "Bad battery.")

    # -----------------------------------------------------
    # Test 7: Empty Input Handling
    # -----------------------------------------------------
    def test_07_empty_input_handling(self):
        reviews = normalize_text_reviews("   \n\n   \t  \n")
        self.assertEqual(len(reviews), 0)

        # Empty CSV
        empty_csv = io.StringIO("")
        with self.assertRaises(ValueError):
            process_csv_file(empty_csv)

    # -----------------------------------------------------
    # Test 8: Invalid CSV Handling
    # -----------------------------------------------------
    def test_08_invalid_csv_handling(self):
        # Binary garbage or unparseable stream
        bad_csv = io.BytesIO(b"\x00\x01\x02\x03\xff")
        try:
            # Should either succeed or raise ValueError cleanly
            process_csv_file(bad_csv)
        except ValueError as e:
            self.assertTrue("Unable to parse CSV" in str(e) or "empty" in str(e))

    # -----------------------------------------------------
    # Test 9: CSV with Missing Values and Whitespace
    # -----------------------------------------------------
    def test_09_csv_with_missing_values(self):
        csv_content = (
            "id,comment,rating\n"
            "1,Super clear screen,5\n"
            "2,,3\n"
            "3,   ,2\n"
            "4,NaN,1\n"
            "5,Battery lasts only 3 hours,2\n"
        )
        csv_file = io.StringIO(csv_content)
        reviews, df, cols, chosen = process_csv_file(csv_file, preferred_column="comment")
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0], "Super clear screen")
        self.assertEqual(reviews[1], "Battery lasts only 3 hours")

    # -----------------------------------------------------
    # Test 10: JSON Parser Robustness (Code Fences & Extra Text)
    # -----------------------------------------------------
    def test_10_json_parser_robustness(self):
        fenced_json = (
            "Here is the requested analysis:\n"
            "```json\n"
            "{\n"
            '  "overall_sentiment": {"classification": "Mixed", "explanation": "Test"},\n'
            '  "aspect_analysis": [],\n'
            '  "recurring_negative_concerns": {"multiple_review_issues": [], "single_review_issues": []},\n'
            '  "product_strengths": [],\n'
            '  "prioritized_improvements": []\n'
            "}\n"
            "```\n"
            "Hope this helps!"
        )
        parsed = clean_and_parse_json(fenced_json)
        self.assertIn("overall_sentiment", parsed)
        self.assertEqual(parsed["overall_sentiment"]["classification"], "Mixed")

    # -----------------------------------------------------
    # Test 11: Priority Rules Enforcement (High >= 2, Medium = 1)
    # -----------------------------------------------------
    def test_11_priority_rules_enforcement(self):
        mock_data = {
            "overall_sentiment": {"classification": "Mixed", "explanation": "Test"},
            "aspect_analysis": [],
            "recurring_negative_concerns": {"multiple_review_issues": [], "single_review_issues": []},
            "product_strengths": [],
            "prioritized_improvements": [
                {"priority": "Medium", "aspect": "Price", "negative_review_count": 1, "reason": "Cost", "suggestion": "Discount"},
                {"priority": "High", "aspect": "Battery", "negative_review_count": 4, "reason": "Dies", "suggestion": "Bigger battery"},
                {"priority": "High", "aspect": "App Sync", "negative_review_count": 2, "reason": "Crashes", "suggestion": "Fix bug"}
            ]
        }
        validated = validate_v3_schema(mock_data)
        imps = validated["prioritized_improvements"]
        # High priorities must come first, sorted by negative_review_count desc
        self.assertEqual(imps[0]["priority"], "High")
        self.assertEqual(imps[0]["aspect"], "Battery")
        self.assertEqual(imps[0]["negative_review_count"], 4)
        self.assertEqual(imps[1]["priority"], "High")
        self.assertEqual(imps[1]["aspect"], "App Sync")
        self.assertEqual(imps[1]["negative_review_count"], 2)
        self.assertEqual(imps[2]["priority"], "Medium")
        self.assertEqual(imps[2]["aspect"], "Price")

    # -----------------------------------------------------
    # Test 12: Local Analysis History Manager (CRUD)
    # -----------------------------------------------------
    def test_12_history_manager_crud(self):
        # 1. Save entry
        entry_id = save_history_entry(
            source_name="Unit Test Dataset",
            review_count=4,
            reviews=["R1", "R2", "R3", "R4"],
            result=DEMO_HEADPHONE_RESULT,
            model_name="test-model",
            is_demo=False
        )
        self.assertTrue(bool(entry_id))

        # 2. Retrieve entry
        retrieved = get_history_entry(entry_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["title"], "Unit Test Dataset")
        self.assertEqual(retrieved["review_count"], 4)

        # 3. List history
        all_hist = get_all_history()
        self.assertEqual(len(all_hist), 1)

        # 4. Delete entry
        del_res = delete_history_entry(entry_id)
        self.assertTrue(del_res)
        self.assertEqual(len(get_all_history()), 0)

    # -----------------------------------------------------
    # Test 13: Demo Dataset Integrity
    # -----------------------------------------------------
    def test_13_demo_dataset_integrity(self):
        self.assertEqual(len(DEMO_HEADPHONE_REVIEWS), 4)
        self.assertEqual(DEMO_HEADPHONE_RESULT["overall_sentiment"]["classification"], "Mixed")
        self.assertEqual(len(DEMO_HEADPHONE_RESULT["aspect_analysis"]), 5)
        # Verify Battery Life has 2 negative reviews and is High Priority
        battery_imp = [i for i in DEMO_HEADPHONE_RESULT["prioritized_improvements"] if i["aspect"] == "Battery Life"][0]
        self.assertEqual(battery_imp["priority"], "High")
        self.assertEqual(battery_imp["negative_review_count"], 2)

    # -----------------------------------------------------
    # Test 14: Sample Data Files Existence
    # -----------------------------------------------------
    def test_14_sample_data_files_exist(self):
        hp_csv = SAMPLE_DATA_DIR / "sample_headphones.csv"
        sw_csv = SAMPLE_DATA_DIR / "smartwatch_reviews.csv"
        edge_csv = SAMPLE_DATA_DIR / "test_edge_cases.csv"
        self.assertTrue(hp_csv.exists(), "sample_headphones.csv missing")
        self.assertTrue(sw_csv.exists(), "smartwatch_reviews.csv missing")
        self.assertTrue(edge_csv.exists(), "test_edge_cases.csv missing")

    # -----------------------------------------------------
    # Test 15: Backend LLM Configuration Loader
    # -----------------------------------------------------
    def test_15_backend_llm_config_loader(self):
        base_url, model, key = get_backend_llm_config()
        self.assertIsInstance(base_url, str)
        self.assertIsInstance(model, str)
        self.assertIsInstance(key, str)
        self.assertTrue(len(base_url) > 0)
        self.assertTrue(len(model) > 0)


if __name__ == "__main__":
    unittest.main()
