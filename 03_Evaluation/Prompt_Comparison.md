# Prompt Evaluation and Comparison

## Purpose

This document records the comparison of the three prompt versions developed during the Prompt Engineering experimentation phase of ReviewSense AI. The objective was to improve the quality, structure, consistency, and relevance of product review analysis through iterative prompt refinement.

## Prompt Version 1 – Baseline

The baseline prompt provided basic instructions to analyse product reviews, identify overall sentiment, summarize key themes, provide supporting quotes, and suggest product improvements.

**Limitations observed:**
- Analysis was relatively general.
- Product aspects were not analysed in sufficient detail.
- Output structure was less specific.

## Prompt Version 2 – Improved

The second prompt introduced more detailed instructions for analysing product reviews. It focused on identifying distinct product aspects, classifying sentiments, counting review mentions, identifying recurring themes, and separating positive and negative feedback.

**Improvements introduced:**
- More structured aspect-wise sentiment analysis.
- Review mention counts for individual aspects.
- Separate identification of recurring themes, product strengths, and customer pain points.
- Clearer rules to reduce unsupported information.

## Prompt Version 3 – Final Refined

The third prompt further refined the analysis by introducing stricter evidence-based instructions and a consistent JSON output format.

**Improvements introduced:**
- Structured overall sentiment analysis.
- Detailed aspect-wise analysis with sentiment and review counts.
- Identification of recurring negative concerns based on distinct reviews.
- Separation of product strengths and improvement suggestions.
- Frequency-based prioritization of concerns.
- Strict instructions to avoid inventing information or unsupported conclusions.

## Comparative Summary

| Evaluation Aspect | V1 – Baseline | V2 – Improved | V3 – Final |
|---|---|---|---|
| Overall sentiment | Basic | Detailed | Structured |
| Aspect identification | Limited | Improved | Refined |
| Review mention counts | Not defined | Introduced | Clearly defined |
| Recurring concerns | Basic themes | Improved identification | Frequency-based |
| Product strengths | Basic | Separate category | Evidence-based |
| Improvement suggestions | General | More specific | Prioritized |
| Output structure | Basic | Organized | Structured JSON |
| Evidence-based analysis | Basic instruction | Improved rules | Strict evidence-based rules |

## Final Selection

Prompt Version 3 was selected for the final ReviewSense AI application because it provides the most structured and detailed analysis among the three versions. Its instructions improve the identification of product aspects, recurring concerns, strengths, and improvement suggestions while emphasizing evidence from the provided reviews.

The final refined prompt was used in the deployed prototype to generate structured product review insights.