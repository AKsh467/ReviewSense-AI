# ReviewSense AI — Working Prototype

> **Prompt-Engineered Product Review Intelligence Platform**  
> Developed as part of the Prompt Engineering Mini-Project (`V1 → V2 → V3` methodology).

---

## 1. Overview

**ReviewSense AI** transforms unstructured customer product reviews into actionable, evidence-based product intelligence. Rather than relying on simple keyword counters or superficial sentiment classifiers, ReviewSense AI implements the **Prompt V3 Analysis Methodology** via a single, carefully calibrated LLM prompt per analysis.

The application automatically identifies:
1. **Overall Sentiment Classification** with synthesis explanation.
2. **Aspect-Level Granularity:** Distinct product aspects with separate positive and negative mention counts.
3. **Problem Recurrence Analysis:** Explicit separation between recurring negative concerns (2+ reviews) and isolated issues (1 review).
4. **Verbatim Quotation Evidence:** Direct citation of original review snippets for every finding.
5. **Priority-Aware Recommendations:** Actionable product improvements assigned strictly by review recurrence frequency (`High Priority`: $\ge 2$ reviews; `Medium Priority`: $1$ review).

---

## 2. Technology Stack

- **Application Framework:** [Streamlit](https://streamlit.io/) (v1.38+)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/) (v2.2+)
- **Interactive Visualizations:** [Plotly](https://plotly.com/) (v5.24+)
- **LLM Integration:** [OpenAI Python SDK](https://github.com/openai/openai-python) (OpenAI-compatible chat completion API)
- **Configuration & Environment:** [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 3. Project Structure

All files for the working prototype reside inside `06_Prototype/`:

```
ReviewSense AI/06_Prototype/
├── .env.example              # Environment variables template
├── .env                      # Local environment configuration (API keys, endpoints)
├── requirements.txt          # Python dependencies
├── README.md                 # Complete system documentation
├── app.py                    # Main Streamlit application and page router
├── config.py                 # Central configurations, Prompt V3 template, demo data
├── llm_analyzer.py           # Review normalization, LLM execution, JSON extraction & schema validation
├── history_manager.py        # Local persistent history management (JSON storage)
├── ui_components.py          # Modern SaaS CSS styles, Plotly chart builders, KPI widgets
├── test_prototype.py         # Automated test suite (14 comprehensive test cases)
├── data/
│   └── history.json          # Persistent local analysis history storage
└── sample_data/
    ├── sample_headphones.csv # Benchmark 4-review headphone dataset from prompt experiments
    ├── smartwatch_reviews.csv# 12 diverse smartwatch reviews for thorough testing
    ├── sample_reviews.txt    # Plain text format review inputs
    └── test_edge_cases.csv   # Edge case test file (missing values, blank rows, custom headers)
```

---

## 4. Setup and Installation

### Prerequisites
- Python 3.10+ (Tested with Python 3.14)
- Windows PowerShell (or command prompt / bash)

### Quick Setup

1. Open PowerShell and navigate into `06_Prototype`:
   ```powershell
   cd "C:\Users\aunin\OneDrive\Desktop\ReviewSense AI\06_Prototype"
   ```

2. Activate the existing virtual environment (or create a new one):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(If creating fresh: `py -m venv .venv` followed by `pip install -r requirements.txt`)*

3. Verify packages are installed:
   ```powershell
   python -m pip list
   ```

---

## 5. API Configuration (Backend-Only)

ReviewSense AI manages all API configurations strictly on the **backend**. The frontend contains no API key inputs, ensuring credentials are never exposed to end users, in network responses, or in downloadable exports.

Configure the server's `.env` file located at `ReviewSense AI/06_Prototype/.env`:
```env
# OpenAI-compatible API base URL
LLM_BASE_URL=https://api.openai.com/v1

# Target model identifier
LLM_MODEL=gpt-4o-mini

# Server API key
LLM_API_KEY=your_api_key_here
```

Compatible providers include:
- **Groq (Free & Fast):** `LLM_BASE_URL=https://api.groq.com/openai/v1`, `LLM_MODEL=llama-3.3-70b-versatile`
- **OpenAI:** `LLM_BASE_URL=https://api.openai.com/v1`, `LLM_MODEL=gpt-4o-mini`
- **Google Gemini (OpenAI Endpoint):** `LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/`, `LLM_MODEL=gemini-1.5-flash`

*(Changes in `.env` are picked up dynamically on the next analysis run without restarting the server).*

---

## 6. Running the Application

Launch the Streamlit web application:
```powershell
streamlit run app.py
```

The application will start locally and provide a URL (typically `http://localhost:8501`).

---

## 7. Application Features & Pages

The application features a clean sidebar navigation with 6 functional pages:

| Page | Description |
| :--- | :--- |
| **1. Overview** | High-level executive dashboard showing 4 KPI cards (Total Reviews, Overall Sentiment, Aspects, Negative Issues), interactive Positive vs. Negative feedback chart, mention frequency, sentiment donut, and key analytical takeaways. |
| **2. Analyze Reviews** | Dual input methods: direct text paste (with instant line/review counter) or CSV file upload (with preview, auto-detected review column, and custom column selector). Triggers the single-prompt V3 analysis engine. |
| **3. Sentiment Analysis** | Detailed aspect-level cards displaying total mentions, positive vs. negative review counts, sentiment badges, and verbatim supporting quotations. Filterable by sentiment and searchable by aspect name. |
| **4. Customer Pain Points** | Strict separation of negative feedback into **Recurring Concerns** ($\ge 2$ reviews) and **Single-Review Concerns** ($1$ review) with attached evidence quotes. |
| **5. Recommendations** | Decision-oriented table/cards prioritizing product improvements based strictly on negative feedback frequency (High Priority for $\ge 2$ reviews; Medium for $1$ review) with actionable product suggestions. |
| **6. Analysis History** | Persistent local analysis history. Reload any previous analysis run, delete entries, or export analysis JSON, executive Markdown summary, or raw reviews. |

---

## 8. Demo Mode (Benchmark Data)

To test the application immediately without configuring an API key or consuming tokens:
1. Click **`⚡ Load Demo Mode (Instant)`** in the sidebar, or
2. From the empty state on the Overview page, click **`⚡ Load Demo Headphone Dataset`**.

This instantly loads the verified, precomputed results for the exact 4 headphone reviews used in Prompt Experiments E1–E3.
Demo mode is clearly flagged with a distinct `[DEMO DATA - PRECOMPUTED]` banner.

---

## 9. Running the Automated Test Suite

ReviewSense AI includes a complete automated test suite covering all 10 project test requirements plus schema validation and history persistence:
```powershell
python test_prototype.py -v
```

**Test Coverage:**
- Normal product reviews
- Mixed sentiment reviews
- Reviews with repeated aspects
- Reviews containing only positive feedback
- Reviews containing only negative feedback
- Very short reviews
- Empty input & missing data handling
- Invalid / corrupt CSV handling
- CSV with missing values and whitespace
- Robust JSON extraction from markdown code fences
- V3 Priority rules enforcement (High $\ge 2$, Medium $= 1$)
- Local Analysis History CRUD operations
- Benchmark demo dataset integrity
- Sample dataset file verification
