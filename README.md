# ReviewSense AI

**AI-powered product review analysis using prompt engineering.**

ReviewSense AI is a product review analyzer designed to transform unstructured customer feedback into meaningful insights. It uses prompt engineering and large language models (LLMs) to identify customer sentiment, extract product-related aspects, uncover recurring concerns, highlight product strengths, and generate actionable improvement suggestions.

The project explores how iterative prompt refinement can improve the quality, consistency, and structure of AI-generated review analysis.

---

## Problem Statement

Customer reviews contain valuable information about product quality, customer satisfaction, and areas that need improvement. However, manually analyzing large volumes of reviews to identify recurring patterns and customer concerns can be time-consuming.

ReviewSense AI aims to simplify this process by automatically analyzing customer feedback and organizing it into structured insights that are easier to understand and act upon.

---

## Features

- **Overall Sentiment Analysis** — Determines the overall sentiment expressed across customer reviews.
- **Aspect-Based Analysis** — Identifies product aspects mentioned in reviews, such as quality, comfort, performance, price, or durability.
- **Aspect-Level Sentiment** — Analyzes the sentiment associated with individual product aspects.
- **Review Frequency Analysis** — Tracks how frequently different aspects and concerns appear across reviews.
- **Customer Pain Points** — Highlights recurring negative feedback and individual customer concerns.
- **Product Strengths** — Identifies aspects receiving positive customer feedback.
- **Actionable Recommendations** — Generates suggestions for product improvement based on customer feedback.
- **Structured Output** — Organizes analysis into structured data for easier interpretation and visualization.
- **Analysis History** — Supports maintaining analysis records within the prototype.

---

## Prompt Engineering Approach

Prompt engineering is a central part of this project. The analysis prompt is developed through iterative experimentation to improve the quality of the generated insights.

The prompt development process follows three iterations:

| Version | Approach |
|---|---|
| V1 – Baseline | Initial prompt for identifying overall sentiment, themes, and improvement suggestions. |
| V2 – Improved | Introduces structured analysis, review counts, recurring concerns, and prioritization. |
| V3 – Refined | Improves consistency, evidence-based analysis, counting rules, and recommendation prioritization. |

Each iteration is evaluated to identify strengths, weaknesses, and opportunities for improvement.

The final prototype is designed to use a single analysis prompt rather than a multi-prompt chain.

---

## Project Structure

```text
ReviewSense AI/
│
├── 01_Prompt_Experiments/
│   ├── Experiment 1 – V1 Baseline/
│   ├── Experiment 2 – V2 Improved/
│   └── Experiment 3 – V3 Final/
│
├── 06_Prototype/
│   ├── app.py
│   ├── config.py
│   ├── llm_analyzer.py
│   ├── history_manager.py
│   ├── ui_components.py
│   ├── requirements.txt
│   ├── README.md
│   ├── .env.example
│   ├── data/
│   ├── sample_data/
│   └── .streamlit/
│
└── README.md
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web application interface |
| Pandas | Data handling and review processing |
| LLM API | AI-powered review analysis |
| JSON | Structured analysis output |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AKsh467/ReviewSense-AI.git
```

### 2. Navigate to the prototype directory

```bash
cd ReviewSense-AI/06_Prototype
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create your local environment configuration using the provided `.env.example` file.

Add the required API credentials and configuration values.

**Never commit API keys, passwords, or private credentials to GitHub.**

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Sample Data

Sample review datasets are included in the prototype for testing and demonstration purposes.

The project is designed to analyze reviews from different product categories rather than being restricted to a single product type.

---

## Project Status

**Status: Prototype / Active Development**

ReviewSense AI is currently being developed as a prompt engineering mini-project. Prompt experimentation, prototype development, testing, and evaluation are ongoing.

Features and implementation details may evolve as the project progresses.

---

## Future Scope

- Improved sentiment and aspect extraction accuracy.
- Better handling of ambiguous and mixed-sentiment reviews.
- Analysis of larger review datasets.
- Enhanced interactive visualizations.
- More comprehensive evaluation of prompt performance.
- Additional export and reporting capabilities.

---

## Repository

GitHub: [AKsh467/ReviewSense-AI](https://github.com/AKsh467/ReviewSense-AI)

---

*Built as a Prompt Engineering Mini Project.*