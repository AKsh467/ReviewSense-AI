"""
ReviewSense AI — LLM Integration & Review Processing Engine
Handles review normalization, single-prompt V3 execution via OpenAI-compatible API,
robust JSON extraction, and strict schema validation.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from openai import OpenAI
from config import V3_PROMPT_TEMPLATE


# ---------------------------------------------------------
# Review Normalization Utilities
# ---------------------------------------------------------

def normalize_text_reviews(raw_text: str) -> List[str]:
    """
    Parse multi-line pasted text into a clean list of individual reviews.
    Strips leading bullets, numbers, and whitespace.
    """
    if not raw_text or not raw_text.strip():
        return []
    
    cleaned_reviews = []
    for line in raw_text.splitlines():
        trimmed = line.strip()
        if not trimmed:
            continue
        # Remove common bullet markers or numbered list prefixes like "1.", "1)", "-", "•", "*"
        trimmed = re.sub(r"^(?:[\d]+[\.\)]|[-•*])\s*", "", trimmed).strip()
        if trimmed:
            cleaned_reviews.append(trimmed)
            
    return cleaned_reviews


def process_csv_file(
    file_obj,
    preferred_column: Optional[str] = None
) -> Tuple[List[str], pd.DataFrame, List[str], str]:
    """
    Process an uploaded CSV file, extract columns, and return clean reviews.
    
    Returns:
        tuple: (reviews_list, dataframe_preview, column_names_list, chosen_column_name)
    """
    try:
        # Support various encodings
        try:
            df = pd.read_csv(file_obj)
        except UnicodeDecodeError:
            file_obj.seek(0)
            df = pd.read_csv(file_obj, encoding="latin1")
    except Exception as exc:
        raise ValueError(f"Unable to parse CSV file: {exc}")

    if df.empty:
        raise ValueError("The uploaded CSV file is empty and contains no records.")

    columns = [str(c) for c in df.columns]
    
    # Identify target review column
    chosen_col = None
    if preferred_column and preferred_column in df.columns:
        chosen_col = preferred_column
    else:
        # Detect common review-related column names
        candidates = [
            "review", "reviews", "review_text", "customer_review",
            "feedback", "comment", "comments", "text", "body", "content"
        ]
        col_lookup = {c.strip().lower(): c for c in df.columns}
        for cand in candidates:
            if cand in col_lookup:
                chosen_col = col_lookup[cand]
                break
        
        if not chosen_col:
            chosen_col = df.columns[0]

    # Extract non-empty, non-null reviews
    raw_series = df[chosen_col].dropna().astype(str)
    reviews = []
    for item in raw_series:
        cleaned = item.strip()
        # Filter out NaN strings or empty records
        if cleaned and cleaned.lower() not in {"nan", "null", "none"}:
            reviews.append(cleaned)

    return reviews, df, columns, chosen_col


# ---------------------------------------------------------
# JSON Extraction & Schema Validation
# ---------------------------------------------------------

def clean_and_parse_json(raw_response: str) -> Dict[str, Any]:
    """
    Strictly extract and parse JSON from the model's raw string response.
    Handles accidental markdown code fences, leading notes, and trailing comments.
    """
    if not raw_response or not raw_response.strip():
        raise ValueError("The language model returned an empty response.")

    text = raw_response.strip()

    # Strip code block fences ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # Attempt direct parse
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Fallback: extract the outermost JSON object using regex
    match = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as err:
            raise ValueError(f"Malformed JSON in model output: {err}")

    raise ValueError("The model response did not contain a valid JSON object matching the V3 schema.")


def validate_v3_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize the parsed JSON against the V3 schema requirements.
    Ensures safe access without crashing the UI, while strictly maintaining
    the prompt's analytical structure.
    """
    validated = {}

    # 1. Overall sentiment
    overall = data.get("overall_sentiment")
    if not isinstance(overall, dict):
        validated["overall_sentiment"] = {
            "classification": "Mixed",
            "explanation": "Analysis completed, but overall sentiment was not structured as an object."
        }
    else:
        validated["overall_sentiment"] = {
            "classification": str(overall.get("classification", "Mixed")).capitalize(),
            "explanation": str(overall.get("explanation", "No detailed explanation provided.")).strip()
        }

    # 2. Aspect analysis
    raw_aspects = data.get("aspect_analysis", [])
    valid_aspects = []
    if isinstance(raw_aspects, list):
        for item in raw_aspects:
            if not isinstance(item, dict):
                continue
            aspect_name = str(item.get("aspect", "Unknown Aspect")).strip()
            sentiment = str(item.get("sentiment", "Neutral")).capitalize()
            
            # Safe int parsing
            try:
                total_mentions = int(item.get("total_reviews_mentioning", 0))
            except (ValueError, TypeError):
                total_mentions = 0

            try:
                pos_count = int(item.get("positive_reviews", 0))
            except (ValueError, TypeError):
                pos_count = 0

            try:
                neg_count = int(item.get("negative_reviews", 0))
            except (ValueError, TypeError):
                neg_count = 0

            quotes = item.get("supporting_quotes", [])
            if not isinstance(quotes, list):
                quotes = [str(quotes)] if quotes else []
            quotes = [str(q).strip() for q in quotes if str(q).strip()]

            valid_aspects.append({
                "aspect": aspect_name,
                "sentiment": sentiment,
                "total_reviews_mentioning": total_mentions,
                "positive_reviews": pos_count,
                "negative_reviews": neg_count,
                "supporting_quotes": quotes
            })
    validated["aspect_analysis"] = valid_aspects

    # 3. Recurring negative concerns
    concerns = data.get("recurring_negative_concerns")
    if not isinstance(concerns, dict):
        concerns = {}
    
    multi_issues = concerns.get("multiple_review_issues", [])
    if not isinstance(multi_issues, list):
        multi_issues = [str(multi_issues)] if multi_issues else []
        
    single_issues = concerns.get("single_review_issues", [])
    if not isinstance(single_issues, list):
        single_issues = [str(single_issues)] if single_issues else []

    validated["recurring_negative_concerns"] = {
        "multiple_review_issues": [str(i).strip() for i in multi_issues if str(i).strip()],
        "single_review_issues": [str(i).strip() for i in single_issues if str(i).strip()]
    }

    # 4. Product strengths
    raw_strengths = data.get("product_strengths", [])
    valid_strengths = []
    if isinstance(raw_strengths, list):
        for s in raw_strengths:
            if isinstance(s, dict):
                valid_strengths.append({
                    "aspect": str(s.get("aspect", "Strength")).strip(),
                    "positive_review_count": s.get("positive_review_count", 1),
                    "reason": str(s.get("reason", "")).strip()
                })
            elif isinstance(s, str) and s.strip():
                valid_strengths.append({
                    "aspect": s.strip(),
                    "positive_review_count": "—",
                    "reason": "Identified as a key product strength in the reviews."
                })
    validated["product_strengths"] = valid_strengths

    # 5. Prioritized improvements
    raw_improvements = data.get("prioritized_improvements", [])
    valid_improvements = []
    if isinstance(raw_improvements, list):
        for imp in raw_improvements:
            if not isinstance(imp, dict):
                continue
            priority = str(imp.get("priority", "Medium")).strip().capitalize()
            aspect = str(imp.get("aspect", "General")).strip()
            
            try:
                neg_count = int(imp.get("negative_review_count", 1))
            except (ValueError, TypeError):
                neg_count = 1

            reason = str(imp.get("reason", "")).strip()
            suggestion = str(imp.get("suggestion", "")).strip()

            valid_improvements.append({
                "priority": priority,
                "aspect": aspect,
                "negative_review_count": neg_count,
                "reason": reason,
                "suggestion": suggestion
            })

    # Ensure prioritized order: High first, then Medium, then Low; ties broken by negative_review_count desc
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    valid_improvements.sort(
        key=lambda x: (
            priority_order.get(x["priority"], 3),
            -x["negative_review_count"]
        )
    )
    validated["prioritized_improvements"] = valid_improvements

    return validated


# ---------------------------------------------------------
# LLM Execution Pipeline
# ---------------------------------------------------------

def execute_v3_analysis(
    reviews: List[str],
    api_key: str,
    base_url: str,
    model_name: str
) -> Dict[str, Any]:
    """
    Executes the single-prompt V3 analysis on the provided reviews list.
    Calls OpenAI-compatible API and returns validated structured JSON.
    """
    if not reviews:
        raise ValueError("No reviews provided for analysis.")

    if not api_key or not api_key.strip():
        raise ValueError(
            "API Key is missing. Please configure LLM_API_KEY in your .env file "
            "or input it in the sidebar settings."
        )

    # Format reviews with numbering for explicit citation
    numbered_reviews = "\n".join(f"{i+1}. {r}" for i, r in enumerate(reviews))
    prompt = V3_PROMPT_TEMPLATE.replace("{reviews_input}", numbered_reviews)

    # Initialize client
    client = OpenAI(
        api_key=api_key.strip(),
        base_url=base_url.strip() if base_url else "https://api.openai.com/v1"
    )

    # Execute chat completion
    try:
        response = client.chat.completions.create(
            model=model_name.strip(),
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional product review analysis system that returns strictly valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
    except Exception as exc:
        # Some endpoints do not support response_format={"type": "json_object"}
        # Attempt fallback without the response_format constraint
        if "response_format" in str(exc).lower() or "unsupported" in str(exc).lower():
            try:
                response = client.chat.completions.create(
                    model=model_name.strip(),
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional product review analysis system that returns strictly valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1
                )
            except Exception as inner_exc:
                raise RuntimeError(f"LLM API request failed: {inner_exc}") from inner_exc
        else:
            raise RuntimeError(f"LLM API request failed: {exc}") from exc

    raw_content = response.choices[0].message.content or ""
    parsed_json = clean_and_parse_json(raw_content)
    validated_output = validate_v3_schema(parsed_json)

    return validated_output


# ---------------------------------------------------------
# Markdown Executive Summary Generator
# ---------------------------------------------------------

def generate_markdown_summary(result: Dict[str, Any], title: str, total_reviews: int) -> str:
    """Generate a formatted markdown executive summary suitable for export."""
    overall = result.get("overall_sentiment", {})
    aspects = result.get("aspect_analysis", [])
    concerns = result.get("recurring_negative_concerns", {})
    strengths = result.get("product_strengths", [])
    improvements = result.get("prioritized_improvements", [])

    lines = [
        f"# ReviewSense AI — Analysis Summary Report",
        f"**Dataset / Source:** {title}",
        f"**Total Reviews Analyzed:** {total_reviews}",
        f"**Overall Sentiment:** {overall.get('classification', 'N/A')}",
        "",
        "## Overall Sentiment Overview",
        overall.get("explanation", "No explanation provided."),
        "",
        "---",
        "## Key Product Aspects Analyzed",
        "| Aspect | Sentiment | Total Mentions | Positive Reviews | Negative Reviews |",
        "| :--- | :--- | :---: | :---: | :---: |",
    ]

    for asp in aspects:
        lines.append(
            f"| {asp.get('aspect')} | {asp.get('sentiment')} | "
            f"{asp.get('total_reviews_mentioning')} | {asp.get('positive_reviews')} | "
            f"{asp.get('negative_reviews')} |"
        )

    lines.extend([
        "",
        "---",
        "## Recurring Customer Pain Points (Multiple Reviews)",
    ])
    multi = concerns.get("multiple_review_issues", [])
    if multi:
        for m in multi:
            lines.append(f"- **[RECURRING]** {m}")
    else:
        lines.append("- *No recurring issues identified.*")

    lines.extend([
        "",
        "## Single-Review Concerns (1 Review)",
    ])
    single = concerns.get("single_review_issues", [])
    if single:
        for s in single:
            lines.append(f"- {s}")
    else:
        lines.append("- *No single-review concerns reported.*")

    lines.extend([
        "",
        "---",
        "## Top Product Strengths",
    ])
    for st in strengths:
        lines.append(f"- **{st.get('aspect')}** ({st.get('positive_review_count', '—')} positive mentions): {st.get('reason')}")

    lines.extend([
        "",
        "---",
        "## Prioritized Product Improvements",
    ])
    for imp in improvements:
        lines.append(
            f"### [{imp.get('priority').upper()} PRIORITY] {imp.get('aspect')} ({imp.get('negative_review_count')} Negative Reviews)\n"
            f"- **Rationale:** {imp.get('reason')}\n"
            f"- **Recommended Action:** {imp.get('suggestion')}\n"
        )

    lines.append("\n*Generated by ReviewSense AI — Prompt Engineering V3 Methodology*")
    return "\n".join(lines)
