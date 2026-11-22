"""
ReviewSense AI — Configuration & Constants
Central configuration, prompt engineering templates (V3 methodology),
and demo baseline datasets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
HISTORY_FILE = DATA_DIR / "history.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Default API configuration
DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DEFAULT_API_KEY = os.getenv("LLM_API_KEY", "")


def get_backend_llm_config():
    """
    Reload and return backend LLM configurations from the server's .env file.
    Ensures API credentials remain strictly on the backend.
    """
    load_dotenv(BASE_DIR / ".env", override=True)
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").strip()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    return base_url, model, api_key

# Application metadata
APP_TITLE = "ReviewSense AI"
APP_SUBTITLE = "Product Review Intelligence & Priority-Aware Insights"
APP_VERSION = "1.0.0 (V3 Final Methodology)"

# V3 Analysis Prompt Template (Exact specification)
V3_PROMPT_TEMPLATE = """You are an expert product review analyst. Analyze the customer reviews to produce an accurate, evidence-based, concise analysis that helps a product team understand customer satisfaction and decide which product issues should be addressed first.

Follow these instructions:

### 1. Overall Sentiment
Determine the overall sentiment as Positive, Negative, or Mixed. Explain the conclusion briefly using the reviews.

### 2. Aspect Identification
Identify distinct product aspects discussed in the reviews. Merge closely related mentions under the same aspect. Do not introduce unsupported aspects.

### 3. Aspect-Level Analysis
For every aspect, report:
- Overall aspect sentiment: Positive, Negative, Neutral, or Mixed.
- Total number of distinct reviews mentioning the aspect.
- Number of reviews expressing positive feedback.
- Number of reviews expressing negative feedback.
- One or two short, exact supporting quotations.

Count each review only once per aspect and sentiment category. If a review expresses both positive and negative opinions about the same aspect, it may count in both sentiment categories but only once in the total reviews mentioning that aspect.

### 4. Recurring Issues
Identify aspects receiving negative feedback in multiple reviews. Clearly distinguish recurring negative concerns from concerns mentioned in only one review. Do not repeat the entire aspect analysis here; provide only a concise recurrence summary.

### 5. Product Strengths
Identify the strongest positively received aspects. Rank them based on the number of reviews expressing positive feedback. Avoid repeating all supporting quotations or explanations already provided in the aspect-level analysis.

### 6. Improvement Prioritization
Generate practical product improvement suggestions based only on negative customer feedback.

Apply these priority rules consistently:
- High Priority: Negative feedback about the aspect appears in 2 or more distinct reviews.
- Medium Priority: Negative feedback about the aspect appears in exactly 1 distinct review.
- Do not assign Low Priority to an aspect unless an improvement is genuinely supported by the reviews.
- Do not increase priority based on assumptions about severity, technical difficulty, cost, or business impact that are not stated in the reviews.
- If multiple aspects have the same priority, order them by the number of negative reviews.

### 7. Avoid Redundancy
Do not repeat the same analysis, evidence, or explanation in multiple sections. Keep the result concise while preserving all important findings.

## OUTPUT FORMAT
Return only valid JSON without Markdown code fences.

Use this structure:
{
  "overall_sentiment": {
    "classification": "",
    "explanation": ""
  },
  "aspect_analysis": [
    {
      "aspect": "",
      "sentiment": "",
      "total_reviews_mentioning": 0,
      "positive_reviews": 0,
      "negative_reviews": 0,
      "supporting_quotes": []
    }
  ],
  "recurring_negative_concerns": {
    "multiple_review_issues": [],
    "single_review_issues": []
  },
  "product_strengths": [],
  "prioritized_improvements": [
    {
      "priority": "",
      "aspect": "",
      "negative_review_count": 0,
      "reason": "",
      "suggestion": ""
    }
  ]
}

## RULES
- Use only information explicitly supported by the reviews.
- Do not invent review counts, quotations, product features, or customer experiences.
- Supporting quotes must be copied exactly from the original reviews.
- Review counts must be based on distinct reviews, not repeated mentions.
- Sentiment must reflect the actual opinions expressed.
- Mixed sentiment must be used when both positive and negative opinions exist for the same aspect.
- Clearly distinguish an aspect being mentioned from an aspect receiving negative feedback.
- Improvement priorities must follow the defined rules rather than subjective assumptions.
- If the reviews do not provide sufficient evidence for a conclusion, state this clearly.

Reviews to analyze:
{reviews_input}
"""

# Benchmark headphone reviews from Prompt Experiments E1–E3
DEMO_HEADPHONE_REVIEWS = [
    "The sound quality is excellent, but the battery barely lasts four hours.",
    "Great sound and comfortable to wear. The battery life could be better.",
    "The headphones look premium, but they are too expensive.",
    "Sound is clear, though the ear cups become uncomfortable after long use.",
]

# Precomputed Demo Result for Benchmark Headphone Reviews
DEMO_HEADPHONE_RESULT = {
    "overall_sentiment": {
        "classification": "Mixed",
        "explanation": "Customers consistently praise sound quality and aesthetic appeal, but significant dissatisfaction exists regarding battery life, comfort during extended use, and high pricing."
    },
    "aspect_analysis": [
        {
            "aspect": "Sound Quality",
            "sentiment": "Positive",
            "total_reviews_mentioning": 3,
            "positive_reviews": 3,
            "negative_reviews": 0,
            "supporting_quotes": [
                "The sound quality is excellent, but the battery barely lasts four hours.",
                "Great sound and comfortable to wear."
            ]
        },
        {
            "aspect": "Battery Life",
            "sentiment": "Negative",
            "total_reviews_mentioning": 2,
            "positive_reviews": 0,
            "negative_reviews": 2,
            "supporting_quotes": [
                "The sound quality is excellent, but the battery barely lasts four hours.",
                "The battery life could be better."
            ]
        },
        {
            "aspect": "Comfort",
            "sentiment": "Mixed",
            "total_reviews_mentioning": 2,
            "positive_reviews": 1,
            "negative_reviews": 1,
            "supporting_quotes": [
                "Great sound and comfortable to wear.",
                "though the ear cups become uncomfortable after long use."
            ]
        },
        {
            "aspect": "Design & Appearance",
            "sentiment": "Positive",
            "total_reviews_mentioning": 1,
            "positive_reviews": 1,
            "negative_reviews": 0,
            "supporting_quotes": [
                "The headphones look premium, but they are too expensive."
            ]
        },
        {
            "aspect": "Price",
            "sentiment": "Negative",
            "total_reviews_mentioning": 1,
            "positive_reviews": 0,
            "negative_reviews": 1,
            "supporting_quotes": [
                "The headphones look premium, but they are too expensive."
            ]
        }
    ],
    "recurring_negative_concerns": {
        "multiple_review_issues": [
            "Battery Life: Negative feedback in 2 distinct reviews (short 4-hour lifespan and general inadequacy)."
        ],
        "single_review_issues": [
            "Comfort: Ear cups cause discomfort after prolonged listening (1 review).",
            "Price: Product perceived as too expensive for value provided (1 review)."
        ]
    },
    "product_strengths": [
        {
            "aspect": "Sound Quality",
            "positive_review_count": 3,
            "reason": "Consistently praised for excellent clarity across 3 distinct reviews."
        },
        {
            "aspect": "Comfort",
            "positive_review_count": 1,
            "reason": "Noted as comfortable to wear during initial use."
        },
        {
            "aspect": "Design & Appearance",
            "positive_review_count": 1,
            "reason": "Recognized for premium visual aesthetics."
        }
    ],
    "prioritized_improvements": [
        {
            "priority": "High",
            "aspect": "Battery Life",
            "negative_review_count": 2,
            "reason": "Negative feedback appears in 2 distinct reviews, meeting the High Priority criterion.",
            "suggestion": "Increase battery cell capacity and optimize chipset efficiency to extend playback duration beyond 4 hours."
        },
        {
            "priority": "Medium",
            "aspect": "Comfort",
            "negative_review_count": 1,
            "reason": "Negative feedback appears in 1 review regarding ear cup pressure during prolonged wear.",
            "suggestion": "Upgrade ear cup padding to ergonomic memory foam and optimize headband clamping force."
        },
        {
            "priority": "Medium",
            "aspect": "Price",
            "negative_review_count": 1,
            "reason": "Negative feedback appears in 1 review perceiving the current price point as excessive.",
            "suggestion": "Review pricing tiers or bundle complimentary accessories to improve perceived market value."
        }
    ]
}
