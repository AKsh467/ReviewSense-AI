"""
ReviewSense AI — Full Working Prototype
AI-Powered Product Review Analyzer using Prompt Engineering V3 Methodology.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

# Local modules
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
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
    execute_v3_analysis,
    generate_markdown_summary,
    normalize_text_reviews,
    process_csv_file,
)
from ui_components import (
    apply_theme,
    create_aspect_frequency_bar,
    create_pos_neg_grouped_bar,
    create_sentiment_distribution_donut,
    get_priority_badge_html,
    get_sentiment_badge_html,
)

# ---------------------------------------------------------
# Page Configuration & State Initialization
# ---------------------------------------------------------

st.set_page_config(
    page_title=f"{APP_TITLE} — Product Review Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Overview"

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "dataset_title" not in st.session_state:
    st.session_state["dataset_title"] = ""

if "input_reviews" not in st.session_state:
    st.session_state["input_reviews"] = []

if "is_demo_mode" not in st.session_state:
    st.session_state["is_demo_mode"] = False

if "pasted_text_input" not in st.session_state:
    st.session_state["pasted_text_input"] = ""

# Apply theme CSS based on dark_mode state
apply_theme(st.session_state["dark_mode"])


# ---------------------------------------------------------
# Sidebar Navigation & Controls
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 0.25rem 0 0.75rem 0;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 2rem;">🧠</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800;">{APP_TITLE}</h2>
                    <p style="margin: 0; font-size: 0.78rem; font-weight: 600; opacity: 0.8;">{APP_SUBTITLE}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Theme Toggle: Dark Mode vs Light Mode
    st.toggle("🌙 Dark Mode", key="dark_mode")
    is_dark = st.session_state.get("dark_mode", False)

    st.markdown("<hr style='margin: 0.75rem 0;'>", unsafe_allow_html=True)

    # Active Analysis Status Pill
    if st.session_state["analysis_result"]:
        is_demo = st.session_state.get("is_demo_mode", False)
        status_label = "⚡ DEMO (Precomputed)" if is_demo else "🟢 ACTIVE DATASET"
        rev_count = len(st.session_state.get("input_reviews", []))
        dataset_name = st.session_state.get("dataset_title", "Custom Analysis")
        
        pill_bg = "#172554" if is_dark and not is_demo else ("#451A03" if is_dark and is_demo else ("#EFF6FF" if not is_demo else "#FEF3C7"))
        pill_border = "#3B82F6" if not is_demo else "#F59E0B"
        pill_text = "#93C5FD" if is_dark and not is_demo else ("#FDE68A" if is_dark and is_demo else ("#1D4ED8" if not is_demo else "#92400E"))
        pill_title = "#F8FAFC" if is_dark else "#0F172A"

        st.markdown(
            f"""
            <div style="background-color: {pill_bg}; border: 1.5px solid {pill_border};
                        border-radius: 8px; padding: 0.65rem 0.85rem; margin-bottom: 1rem;">
                <div style="font-size: 0.75rem; font-weight: 800; color: {pill_text};">
                    {status_label}
                </div>
                <div style="font-size: 0.9rem; font-weight: 700; color: {pill_title}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {dataset_name}
                </div>
                <div style="font-size: 0.8rem; font-weight: 500; opacity: 0.85;">
                    {rev_count} reviews analyzed
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Navigation Menu
    nav_options = [
        "Overview",
        "Analyze Reviews",
        "Sentiment Analysis",
        "Customer Pain Points",
        "Recommendations",
        "Analysis History"
    ]

    selected_page = st.radio(
        "Navigation",
        options=nav_options,
        index=nav_options.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_options else 0,
        label_visibility="collapsed"
    )

    if selected_page != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page
        st.rerun()

    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

    # Quick Demo Trigger
    if st.button("⚡ Load Demo Mode (Instant)", use_container_width=True, type="secondary"):
        st.session_state["analysis_result"] = DEMO_HEADPHONE_RESULT
        st.session_state["dataset_title"] = "Benchmark Headphone Reviews (Demo)"
        st.session_state["input_reviews"] = DEMO_HEADPHONE_REVIEWS
        st.session_state["is_demo_mode"] = True
        st.session_state["current_page"] = "Overview"
        save_history_entry(
            source_name="Benchmark Headphone Reviews",
            review_count=len(DEMO_HEADPHONE_REVIEWS),
            reviews=DEMO_HEADPHONE_REVIEWS,
            result=DEMO_HEADPHONE_RESULT,
            model_name="Precomputed Demo Baseline",
            is_demo=True
        )
        st.rerun()

    # Clear current session
    if st.session_state["analysis_result"] is not None:
        if st.button("🗑️ Clear Active Analysis", use_container_width=True):
            st.session_state["analysis_result"] = None
            st.session_state["dataset_title"] = ""
            st.session_state["input_reviews"] = []
            st.session_state["is_demo_mode"] = False
            st.rerun()

    st.markdown(
        f"""
        <div style="margin-top: 2rem; font-size: 0.75rem; opacity: 0.7; text-align: center; font-weight: 500;">
            {APP_VERSION}<br>Prompt Engineering Mini-Project
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Helper: Empty State Renderer
# ---------------------------------------------------------

def render_empty_state_prompt(title: str = "No Analysis Loaded Yet"):
    st.markdown(
        f"""
        <div class="empty-state">
            <span style="font-size: 3rem;">📊</span>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-text">
                To view insights, please input customer reviews on the <b>Analyze Reviews</b> page
                or load the precomputed demo dataset to explore the dashboard instantly.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔍 Go to Analyze Reviews", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Analyze Reviews"
            st.rerun()
    with col2:
        if st.button("⚡ Load Demo Headphone Dataset", use_container_width=True):
            st.session_state["analysis_result"] = DEMO_HEADPHONE_RESULT
            st.session_state["dataset_title"] = "Benchmark Headphone Reviews (Demo)"
            st.session_state["input_reviews"] = DEMO_HEADPHONE_REVIEWS
            st.session_state["is_demo_mode"] = True
            st.session_state["current_page"] = "Overview"
            save_history_entry(
                source_name="Benchmark Headphone Reviews",
                review_count=len(DEMO_HEADPHONE_REVIEWS),
                reviews=DEMO_HEADPHONE_REVIEWS,
                result=DEMO_HEADPHONE_RESULT,
                model_name="Precomputed Demo Baseline",
                is_demo=True
            )
            st.rerun()
    with col3:
        st.empty()


# ---------------------------------------------------------
# PAGE 1: OVERVIEW DASHBOARD
# ---------------------------------------------------------

def render_overview_page():
    result = st.session_state.get("analysis_result")
    if not result:
        st.title("Product Review Intelligence — Overview")
        st.write("Transform raw customer feedback into structured, evidence-backed product priorities.")
        render_empty_state_prompt("Ready to Analyze Customer Feedback")
        return

    is_dark = st.session_state.get("dark_mode", False)
    is_demo = st.session_state.get("is_demo_mode", False)
    if is_demo:
        st.markdown(
            """
            <div class="demo-banner">
                <span style="font-size: 1.1rem; margin-right: 0.4rem;">⚡</span>
                <span><b>DEMO MODE (PRECOMPUTED BENCHMARK):</b> Displaying verified analysis for the 4 benchmark headphone reviews from Prompt Experiments E1–E3. No API tokens consumed.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    dataset_title = st.session_state.get("dataset_title", "Customer Reviews")
    st.markdown(f"<h1 style='margin-bottom: 0.25rem;'>Product Intelligence Overview</h1>", unsafe_allow_html=True)
    st.caption(f"Active Dataset: **{dataset_title}** • Single-Prompt V3 Methodology")

    overall = result.get("overall_sentiment", {})
    sentiment_class = overall.get("classification", "Mixed")
    aspects = result.get("aspect_analysis", [])
    concerns = result.get("recurring_negative_concerns", {})
    strengths = result.get("product_strengths", [])
    improvements = result.get("prioritized_improvements", [])

    total_reviews = len(st.session_state.get("input_reviews", []))
    if total_reviews == 0 and aspects:
        total_reviews = max([a.get("total_reviews_mentioning", 0) for a in aspects] + [1])

    total_negative_mentions = sum(a.get("negative_reviews", 0) for a in aspects)
    recurring_count = len(concerns.get("multiple_review_issues", []))

    # --- KPI Cards Row ---
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Total Reviews Analyzed</div>
                <div class="kpi-value">{total_reviews}</div>
                <div class="kpi-subtitle">Distinct customer inputs</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k2:
        badge_html = get_sentiment_badge_html(sentiment_class)
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Overall Sentiment</div>
                <div class="kpi-value" style="font-size: 1.35rem; padding-top: 0.35rem;">{badge_html}</div>
                <div class="kpi-subtitle">V3 synthesis of all reviews</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Aspects Identified</div>
                <div class="kpi-value">{len(aspects)}</div>
                <div class="kpi-subtitle">Distinct feature categories</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-title">Negative Feedback Issues</div>
                <div class="kpi-value">{total_negative_mentions} <span style="font-size: 0.9rem; font-weight: 700; color: #DC2626;">({recurring_count} recurring)</span></div>
                <div class="kpi-subtitle">Negative customer mentions</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # --- Visualizations & Highlights ---
    chart_col, cards_col = st.columns([1.5, 1])

    with chart_col:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        fig_pos_neg = create_pos_neg_grouped_bar(aspects, dark_mode=is_dark)
        st.plotly_chart(fig_pos_neg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cards_col:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; font-size:1.15rem;'>🎯 Key Analytical Takeaways</h4>", unsafe_allow_html=True)

        # 1. Top Strength
        top_strength = strengths[0] if strengths else None
        if top_strength:
            str_bg = "#064E3B" if is_dark else "#F0FDF4"
            str_border = "#059669" if is_dark else "#86EFAC"
            str_lbl = "#6EE7B7" if is_dark else "#166534"
            str_head = "#F8FAFC" if is_dark else "#0F172A"
            str_desc = "#E2E8F0" if is_dark else "#1E293B"

            st.markdown(
                f"""
                <div style="margin-bottom: 0.9rem; padding: 0.75rem 0.9rem; background-color: {str_bg}; border-radius: 8px; border: 1.5px solid {str_border};">
                    <div style="font-size: 0.75rem; font-weight: 800; color: {str_lbl}; text-transform: uppercase;">🌟 Strongest Product Strength</div>
                    <div style="font-size: 1rem; font-weight: 700; color: {str_head};">{top_strength.get('aspect', 'Key Strength')}</div>
                    <div style="font-size: 0.85rem; color: {str_desc}; margin-top: 0.15rem;">{top_strength.get('reason', '')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 2. Most Recurring Concern
        multi_issues = concerns.get("multiple_review_issues", [])
        top_recurring = multi_issues[0] if multi_issues else "No recurring negative issues identified."
        rec_bg = "#450A0A" if is_dark else "#FEF2F2"
        rec_border = "#DC2626" if is_dark else "#FCA5A5"
        rec_lbl = "#FCA5A5" if is_dark else "#991B1B"
        rec_text = "#F8FAFC" if is_dark else "#0F172A"

        st.markdown(
            f"""
            <div style="margin-bottom: 0.9rem; padding: 0.75rem 0.9rem; background-color: {rec_bg}; border-radius: 8px; border: 1.5px solid {rec_border};">
                <div style="font-size: 0.75rem; font-weight: 800; color: {rec_lbl}; text-transform: uppercase;">🚨 Recurring Customer Concern</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: {rec_text};">{top_recurring}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 3. Top Improvement
        top_improvement = improvements[0] if improvements else None
        if top_improvement:
            priority_badge = get_priority_badge_html(top_improvement.get("priority", "High"))
            imp_bg = "#451A03" if is_dark else "#FFFBEB"
            imp_border = "#D97706" if is_dark else "#FCD34D"
            imp_lbl = "#FDE68A" if is_dark else "#92400E"
            imp_head = "#F8FAFC" if is_dark else "#0F172A"
            imp_desc = "#E2E8F0" if is_dark else "#1E293B"

            st.markdown(
                f"""
                <div style="padding: 0.75rem 0.9rem; background-color: {imp_bg}; border-radius: 8px; border: 1.5px solid {imp_border};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                        <span style="font-size: 0.75rem; font-weight: 800; color: {imp_lbl}; text-transform: uppercase;">💡 Top Recommended Action</span>
                        {priority_badge}
                    </div>
                    <div style="font-size: 0.98rem; font-weight: 700; color: {imp_head};">{top_improvement.get('aspect', 'Improvement')}</div>
                    <div style="font-size: 0.85rem; color: {imp_desc}; margin-top: 0.15rem;">{top_improvement.get('suggestion', '')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --- Secondary Row of Charts ---
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        fig_freq = create_aspect_frequency_bar(aspects, dark_mode=is_dark)
        st.plotly_chart(fig_freq, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        fig_donut = create_sentiment_distribution_donut(aspects, dark_mode=is_dark)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Overall Analysis Summary ---
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0;'>📝 Overall Sentiment Synthesis</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 0.95rem; line-height: 1.6;'>{overall.get('explanation', 'No detailed sentiment explanation provided.')}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 2: ANALYZE REVIEWS
# ---------------------------------------------------------

def render_analyze_page():
    st.title("Analyze Customer Reviews")
    st.write("Input raw customer reviews via direct paste or CSV file upload to run the V3 analysis engine.")

    # Input method selection tabs
    tab_paste, tab_csv = st.tabs(["📝 Paste Reviews", "📁 Upload CSV File"])

    extracted_reviews: List[str] = []
    source_label = "Pasted Reviews"

    with tab_paste:
        st.markdown("<p style='font-size:0.92rem; font-weight:500;'>Enter reviews below. Each review must be on a new line.</p>", unsafe_allow_html=True)

        p_col1, p_col2 = st.columns([1, 4])
        with p_col1:
            if st.button("📋 Load Sample Reviews"):
                st.session_state["pasted_text_input"] = "\n".join(DEMO_HEADPHONE_REVIEWS)
                st.rerun()

        text_val = st.text_area(
            "Customer Reviews",
            value=st.session_state.get("pasted_text_input", ""),
            height=240,
            placeholder="Paste reviews here, one per line:\nExample: The sound quality is great, but battery dies too quickly.\nExample: Very lightweight and comfortable headphones...",
            label_visibility="collapsed"
        )
        st.session_state["pasted_text_input"] = text_val

        detected_from_text = normalize_text_reviews(text_val)
        if detected_from_text:
            st.info(f"✨ **{len(detected_from_text)} distinct reviews detected** from pasted text.")
            extracted_reviews = detected_from_text
            source_label = f"Pasted Text ({len(detected_from_text)} reviews)"

    with tab_csv:
        st.markdown("<p style='font-size:0.92rem; font-weight:500;'>Upload a CSV file containing customer feedback or reviews.</p>", unsafe_allow_html=True)
        uploaded_csv = st.file_uploader("Upload CSV", type=["csv"], help="Accepts CSV files with UTF-8 or Latin1 encoding.")

        if uploaded_csv is not None:
            try:
                uploaded_csv.seek(0)
                temp_df = pd.read_csv(uploaded_csv)
                cols = list(temp_df.columns)
                
                default_ix = 0
                for i, col in enumerate(cols):
                    if str(col).lower() in ["review", "reviews", "review_text", "customer_review", "feedback", "comment", "text"]:
                        default_ix = i
                        break

                selected_col = st.selectbox(
                    "Select column containing review text:",
                    options=cols,
                    index=default_ix,
                    help="ReviewSense AI auto-selects the most likely column, but you can select any column."
                )

                uploaded_csv.seek(0)
                csv_reviews, df_preview, _, chosen_col = process_csv_file(uploaded_csv, preferred_column=selected_col)

                st.caption(f"Previewing dataset: {len(df_preview)} rows • {len(df_preview.columns)} columns • Target column: **{chosen_col}**")
                st.dataframe(df_preview.head(5), use_container_width=True)

                if csv_reviews:
                    st.success(f"✅ Extracted **{len(csv_reviews)} valid non-empty reviews** from column `{chosen_col}`.")
                    extracted_reviews = csv_reviews
                    source_label = f"CSV: {uploaded_csv.name} ({len(csv_reviews)} reviews)"
                else:
                    st.warning("No valid reviews found in the selected column.")

            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Pre-packaged Sample Data files helper
    with st.expander("📂 Explore Ready-to-Test Datasets in this Prototype", expanded=False):
        st.markdown(
            """
            This prototype comes with pre-packaged datasets ready for testing in `06_Prototype/sample_data/`:
            - **sample_headphones.csv**: The 4 headphone reviews from the prompt engineering experiments.
            - **smartwatch_reviews.csv**: 12 diverse reviews covering display, battery, fitness tracking, straps, and app sync.
            - **test_edge_cases.csv**: Edge cases with missing values, blank rows, and alternative column names.
            """
        )
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            if st.button("Load 12-Review Smartwatch Dataset"):
                smartwatch_path = SAMPLE_DATA_DIR / "smartwatch_reviews.csv"
                if smartwatch_path.exists():
                    with open(smartwatch_path, "r", encoding="utf-8") as f:
                        sw_reviews, _, _, _ = process_csv_file(f, preferred_column="customer_review")
                        st.session_state["pasted_text_input"] = "\n".join(sw_reviews)
                        st.rerun()
        with s_col2:
            if st.button("Load 4-Review Benchmark Headphone Dataset"):
                st.session_state["pasted_text_input"] = "\n".join(DEMO_HEADPHONE_REVIEWS)
                st.rerun()

    # Execution Action Bar
    st.subheader("Run Analysis")
    act_col1, act_col2 = st.columns([2, 1])

    with act_col1:
        if extracted_reviews:
            st.markdown(f"**Target Dataset:** `{source_label}` (**{len(extracted_reviews)} reviews** ready)")
        else:
            st.markdown("<span style='opacity: 0.7; font-weight: 500;'>Please paste reviews or upload a CSV file above.</span>", unsafe_allow_html=True)

    with act_col2:
        analyze_button = st.button(
            "🚀 Analyze Reviews (Prompt V3)",
            type="primary",
            use_container_width=True,
            disabled=len(extracted_reviews) == 0
        )

    if analyze_button:
        # Load credentials strictly from backend server environment (.env)
        base_url, model, api_key = get_backend_llm_config()

        if not extracted_reviews:
            st.error("No reviews found. Please paste reviews or upload a CSV file.")
        elif len(extracted_reviews) > 500:
            st.error("This prototype supports up to 500 reviews per batch to maintain responsive LLM performance.")
        elif not api_key:
            st.error(
                "⚠️ **Backend Service Not Configured:**\n\n"
                "The application administrator must configure `LLM_API_KEY` in the server's `.env` file before live review analysis can be performed.\n\n"
                "*(You can still explore all application features by clicking **Load Demo Mode (Instant)** in the sidebar!)*"
            )
        else:
            with st.spinner(f"Analyzing {len(extracted_reviews)} reviews using Prompt V3..."):
                try:
                    result = execute_v3_analysis(
                        reviews=extracted_reviews,
                        api_key=api_key,
                        base_url=base_url,
                        model_name=model
                    )

                    st.session_state["analysis_result"] = result
                    st.session_state["dataset_title"] = source_label
                    st.session_state["input_reviews"] = extracted_reviews
                    st.session_state["is_demo_mode"] = False

                    save_history_entry(
                        source_name=source_label,
                        review_count=len(extracted_reviews),
                        reviews=extracted_reviews,
                        result=result,
                        model_name=model,
                        is_demo=False
                    )

                    # Automatically open the Overview Dashboard immediately
                    st.session_state["current_page"] = "Overview"
                    st.rerun()

                except Exception as exc:
                    st.error(f"❌ **Analysis Failed:** {exc}")


# ---------------------------------------------------------
# PAGE 3: SENTIMENT ANALYSIS
# ---------------------------------------------------------

def render_sentiment_page():
    result = st.session_state.get("analysis_result")
    if not result:
        st.title("Sentiment Analysis")
        render_empty_state_prompt("No Sentiment Data to Display")
        return

    is_dark = st.session_state.get("dark_mode", False)
    st.title("Sentiment Analysis & Aspect Breakdown")
    st.caption("Deep-dive into overall customer perception and individual product aspect sentiments.")

    overall = result.get("overall_sentiment", {})
    sentiment_class = overall.get("classification", "Mixed")
    aspects = result.get("aspect_analysis", [])

    # Overall Sentiment Banner
    st.markdown(
        f"""
        <div class="saas-card" style="border-left: 5px solid #2563EB !important;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;">
                <h3 style="margin: 0;">Overall Sentiment: {sentiment_class}</h3>
                {get_sentiment_badge_html(sentiment_class)}
            </div>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.6;">
                {overall.get('explanation', 'No explanation provided.')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Visualizations
    col_chart1, col_chart2 = st.columns([1.3, 1])
    with col_chart1:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(create_pos_neg_grouped_bar(aspects, dark_mode=is_dark), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_chart2:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.plotly_chart(create_sentiment_distribution_donut(aspects, dark_mode=is_dark), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Aspect Cards Section
    st.subheader(f"Aspect-Level Analysis ({len(aspects)} Aspects Identified)")
    
    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        sentiment_filter = st.selectbox("Filter by Sentiment:", ["All", "Positive", "Negative", "Mixed", "Neutral"])
    with search_col:
        search_query = st.text_input("Search aspect name:", placeholder="e.g. Sound, Battery, Display...")

    filtered_aspects = aspects
    if sentiment_filter != "All":
        filtered_aspects = [a for a in filtered_aspects if str(a.get("sentiment", "")).lower() == sentiment_filter.lower()]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_aspects = [a for a in filtered_aspects if q in str(a.get("aspect", "")).lower()]

    if not filtered_aspects:
        st.info("No aspects match the selected filter criteria.")
    else:
        for item in filtered_aspects:
            asp_name = item.get("aspect", "Aspect")
            sentiment = item.get("sentiment", "Neutral")
            total_m = item.get("total_reviews_mentioning", 0)
            pos_m = item.get("positive_reviews", 0)
            neg_m = item.get("negative_reviews", 0)
            quotes = item.get("supporting_quotes", [])

            st.markdown(
                f"""
                <div class="saas-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span style="font-size: 1.2rem; font-weight: 800;">{asp_name}</span>
                        {get_sentiment_badge_html(sentiment)}
                    </div>
                    <div style="display: flex; gap: 1.5rem; margin-bottom: 0.85rem; font-size: 0.9rem;">
                        <span><b>Total Mentions:</b> {total_m}</span>
                        <span style="color: #10B981; font-weight: 700;">Positive: {pos_m}</span>
                        <span style="color: #EF4444; font-weight: 700;">Negative: {neg_m}</span>
                    </div>
                """,
                unsafe_allow_html=True
            )

            if quotes:
                st.markdown("<div style='font-size: 0.82rem; font-weight: 700; opacity: 0.8; margin-top: 0.5rem;'>Supporting Quotes from Reviews:</div>", unsafe_allow_html=True)
                for q in quotes:
                    st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)
            else:
                st.caption("No direct supporting quotes attached.")

            st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE 4: CUSTOMER PAIN POINTS
# ---------------------------------------------------------

def render_pain_points_page():
    result = st.session_state.get("analysis_result")
    if not result:
        st.title("Customer Pain Points")
        render_empty_state_prompt("No Pain Points Data Available")
        return

    st.title("Customer Pain Points & Problem Frequency")
    st.write("Identifies negative customer feedback, clearly separating recurring issues (multiple reviews) from single-review concerns.")

    concerns = result.get("recurring_negative_concerns", {})
    multi_issues = concerns.get("multiple_review_issues", [])
    single_issues = concerns.get("single_review_issues", [])
    aspects = result.get("aspect_analysis", [])

    quotes_by_aspect = {
        a.get("aspect", "").lower(): a.get("supporting_quotes", [])
        for a in aspects
    }

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <h3 style="margin: 0; color: #DC2626; font-size: 1.2rem;">🚨 Recurring Concerns</h3>
                <span class="badge badge-negative">{len(multi_issues)} Issues (2+ Reviews)</span>
            </div>
            <p style="font-size: 0.88rem; opacity: 0.85;">Issues mentioned negatively across multiple distinct customer reviews. Highest risk to user satisfaction.</p>
            """,
            unsafe_allow_html=True
        )

        if multi_issues:
            for issue in multi_issues:
                matched_quotes = []
                for asp_name, q_list in quotes_by_aspect.items():
                    if asp_name in issue.lower():
                        matched_quotes = q_list
                        break

                st.markdown(
                    f"""
                    <div class="saas-card" style="border-left: 4px solid #EF4444 !important;">
                        <div style="font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem;">
                            {issue}
                        </div>
                    """,
                    unsafe_allow_html=True
                )
                if matched_quotes:
                    st.markdown("<div style='font-size: 0.78rem; opacity: 0.8; font-weight: 700;'>Verified Evidence Quotations:</div>", unsafe_allow_html=True)
                    for q in matched_quotes[:2]:
                        st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No recurring negative concerns detected across multiple reviews.")

    with p_col2:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <h3 style="margin: 0; color: #D97706; font-size: 1.2rem;">⚠️ Single-Review Concerns</h3>
                <span class="badge badge-mixed">{len(single_issues)} Issues (1 Review)</span>
            </div>
            <p style="font-size: 0.88rem; opacity: 0.85;">Issues mentioned negatively in exactly one review. Worth monitoring for potential recurrence.</p>
            """,
            unsafe_allow_html=True
        )

        if single_issues:
            for issue in single_issues:
                matched_quotes = []
                for asp_name, q_list in quotes_by_aspect.items():
                    if asp_name in issue.lower():
                        matched_quotes = q_list
                        break

                st.markdown(
                    f"""
                    <div class="saas-card" style="border-left: 4px solid #F59E0B !important;">
                        <div style="font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem;">
                            {issue}
                        </div>
                    """,
                    unsafe_allow_html=True
                )
                if matched_quotes:
                    st.markdown("<div style='font-size: 0.78rem; opacity: 0.8; font-weight: 700;'>Verified Evidence Quotation:</div>", unsafe_allow_html=True)
                    for q in matched_quotes[:1]:
                        st.markdown(f"<div class='quote-box'>“{q}”</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No isolated single-review concerns reported.")


# ---------------------------------------------------------
# PAGE 5: RECOMMENDATIONS
# ---------------------------------------------------------

def render_recommendations_page():
    result = st.session_state.get("analysis_result")
    if not result:
        st.title("Product Recommendations")
        render_empty_state_prompt("No Recommendations to Display")
        return

    is_dark = st.session_state.get("dark_mode", False)
    st.title("Prioritized Product Improvement Recommendations")
    st.write("Actionable suggestions derived strictly from customer negative feedback, ranked according to Prompt V3 rules.")

    improvements = result.get("prioritized_improvements", [])

    if not improvements:
        st.info("No negative feedback was identified that warranted improvements.")
        return

    r_col1, r_col2 = st.columns([1, 3])
    with r_col1:
        priority_filter = st.selectbox("Filter by Priority:", ["All Priorities", "High", "Medium", "Low"])

    filtered_improvements = improvements
    if priority_filter != "All Priorities":
        filtered_improvements = [i for i in filtered_improvements if str(i.get("priority", "")).lower() == priority_filter.lower()]

    st.markdown(f"<div style='font-size: 0.9rem; opacity: 0.85; margin-bottom: 1rem; font-weight:600;'>Showing <b>{len(filtered_improvements)}</b> prioritized recommendations:</div>", unsafe_allow_html=True)

    action_box_bg = "#0B1120" if is_dark else "#F8FAFC"
    action_box_border = "#334155" if is_dark else "#CBD5E1"

    for item in filtered_improvements:
        priority = item.get("priority", "Medium")
        aspect = item.get("aspect", "Aspect")
        neg_count = item.get("negative_review_count", 1)
        reason = item.get("reason", "")
        suggestion = item.get("suggestion", "")

        border_color = "#EF4444" if priority.lower() == "high" else ("#F59E0B" if priority.lower() == "medium" else "#3B82F6")

        st.markdown(
            f"""
            <div class="saas-card" style="border-left: 5px solid {border_color} !important;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <div>
                        <span style="font-size: 1.25rem; font-weight: 800;">{aspect}</span>
                        <span style="margin-left: 0.5rem; font-size: 0.85rem; opacity: 0.75; font-weight: 700;">({neg_count} Negative Review{'s' if neg_count != 1 else ''})</span>
                    </div>
                    {get_priority_badge_html(priority)}
                </div>
                <div style="margin-bottom: 0.6rem;">
                    <span style="font-size: 0.78rem; font-weight: 800; opacity: 0.8; text-transform: uppercase;">Prioritization Rationale:</span>
                    <p style="margin: 0.2rem 0 0.5rem 0; font-size: 0.95rem; line-height: 1.5;">{reason}</p>
                </div>
                <div style="background-color: {action_box_bg}; border-radius: 8px; padding: 0.85rem 1rem; border: 1.5px solid {action_box_border};">
                    <span style="font-size: 0.78rem; font-weight: 800; color: #3B82F6; text-transform: uppercase;">💡 Recommended Action:</span>
                    <p style="margin: 0.25rem 0 0 0; font-size: 0.95rem; font-weight: 700; line-height: 1.5;">{suggestion}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# PAGE 6: ANALYSIS HISTORY & EXPORT
# ---------------------------------------------------------

def render_history_page():
    st.title("Analysis History & Data Management")
    st.write("Review previously analyzed datasets, reload historical runs, or manage saved records.")

    history_records = get_all_history()

    active_result = st.session_state.get("analysis_result")
    if active_result:
        st.subheader("📥 Export Active Analysis")
        dataset_name = st.session_state.get("dataset_title", "reviewsense_analysis")
        safe_filename = "".join(c for c in dataset_name if c.isalnum() or c in ("-", "_")).strip() or "analysis"
        
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        with exp_col1:
            json_str = json.dumps(active_result, indent=2, ensure_ascii=False)
            st.download_button(
                "📥 Download Analysis JSON",
                data=json_str,
                file_name=f"{safe_filename}_v3.json",
                mime="application/json",
                use_container_width=True
            )
        with exp_col2:
            summary_md = generate_markdown_summary(
                active_result,
                dataset_name,
                len(st.session_state.get("input_reviews", []))
            )
            st.download_button(
                "📄 Download Executive Summary (MD)",
                data=summary_md,
                file_name=f"{safe_filename}_summary.md",
                mime="text/markdown",
                use_container_width=True
            )
        with exp_col3:
            raw_revs = "\n".join(st.session_state.get("input_reviews", []))
            st.download_button(
                "📋 Download Input Reviews (TXT)",
                data=raw_revs,
                file_name=f"{safe_filename}_reviews.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader(f"Saved Analyses ({len(history_records)} Records)")

    if not history_records:
        st.info("No saved analysis records found in local storage.")
        return

    if st.button("🗑️ Clear Entire History", type="secondary"):
        clear_all_history()
        st.success("Analysis history has been cleared.")
        st.rerun()

    for entry in history_records:
        entry_id = entry.get("id")
        title = entry.get("title", "Untitled")
        time_str = entry.get("display_time", "")
        rev_count = entry.get("review_count", 0)
        sentiment = entry.get("overall_sentiment", "Unknown")
        is_demo = entry.get("is_demo", False)
        model_name = entry.get("model_name", "")

        demo_tag = "<span class='badge badge-mixed' style='margin-left:0.5rem;'>DEMO</span>" if is_demo else ""

        st.markdown(
            f"""
            <div class="saas-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.15rem; font-weight: 800;">{title}</span>
                        {demo_tag}
                        <div style="font-size: 0.85rem; opacity: 0.8; font-weight: 500; margin-top: 0.25rem;">
                            Analyzed: {time_str} • Model: {model_name} • Reviews: {rev_count}
                        </div>
                    </div>
                    <div>
                        {get_sentiment_badge_html(sentiment)}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        h_col1, h_col2, h_col3 = st.columns([1, 1, 4])
        with h_col1:
            if st.button("📂 Reload Analysis", key=f"load_{entry_id}", use_container_width=True):
                st.session_state["analysis_result"] = entry.get("result")
                st.session_state["dataset_title"] = title
                st.session_state["input_reviews"] = entry.get("reviews", [])
                st.session_state["is_demo_mode"] = is_demo
                st.session_state["current_page"] = "Overview"
                st.rerun()
        with h_col2:
            if st.button("🗑️ Delete Record", key=f"del_{entry_id}", use_container_width=True):
                delete_history_entry(entry_id)
                st.rerun()
        with h_col3:
            st.empty()


# ---------------------------------------------------------
# Main Page Router
# ---------------------------------------------------------

current = st.session_state.get("current_page", "Overview")

if current == "Overview":
    render_overview_page()
elif current == "Analyze Reviews":
    render_analyze_page()
elif current == "Sentiment Analysis":
    render_sentiment_page()
elif current == "Customer Pain Points":
    render_pain_points_page()
elif current == "Recommendations":
    render_recommendations_page()
elif current == "Analysis History":
    render_history_page()
else:
    render_overview_page()
