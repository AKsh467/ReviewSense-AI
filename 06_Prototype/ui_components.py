"""
ReviewSense AI — UI Component Library & Visual Theme
Defines modern SaaS aesthetics for both Light and Dark modes, clean custom CSS,
Plotly visualization helpers, and reusable dashboard card widgets.
Guarantees full readability, matching background/text pairs, and no color clashes.
"""

from typing import Any, Dict, List
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------
# High-Contrast Light Mode CSS
# ---------------------------------------------------------

LIGHT_THEME_CSS = """
<style>
/* CSS Variables & Base Layout Light */
:root, [data-testid="stApp"], .stApp {
    --primary-color: #2563EB !important;
    --background-color: #F8FAFC !important;
    --secondary-background-color: #FFFFFF !important;
    --text-color: #0F172A !important;
    color-scheme: light !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

header[data-testid="stHeader"] {
    background-color: #F8FAFC !important;
}

[data-testid="stDeployButton"] {
    display: none !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

p, span, label, div, li {
    color: #1E293B;
}

[data-testid="stMarkdownContainer"] > p {
    color: #1E293B !important;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* Sidebar Light */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 2px solid #E2E8F0 !important;
}

[data-testid="stSidebar"] * {
    color: #0F172A !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-weight: 600 !important;
    color: #0F172A !important;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background-color: #F1F5F9 !important;
}

/* Tabs Light */
button[data-baseweb="tab"] {
    color: #64748B !important;
    background-color: transparent !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563EB !important;
    border-bottom-color: #2563EB !important;
    font-weight: 700 !important;
}

/* Textarea & Inputs Light Mode */
.stTextArea textarea,
.stTextArea div[data-baseweb="textarea"],
.stTextInput input,
.stTextInput div[data-baseweb="input"],
[data-testid="stTextArea"] textarea,
[data-testid="stTextAreaRootElement"],
[data-baseweb="textarea"],
[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
}

.stTextArea textarea:focus,
[data-baseweb="textarea"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
}

/* Alert Boxes Light Mode */
[data-testid="stAlert"],
.stAlert,
[data-testid="stAlertContainer"] {
    background-color: #EFF6FF !important;
    border: 1.5px solid #BFDBFE !important;
    border-radius: 8px !important;
}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlertContainer"] *,
.stAlert p,
.stAlert span,
.stAlert strong {
    color: #1E3A8A !important;
    -webkit-text-fill-color: #1E3A8A !important;
    font-weight: 500 !important;
}

/* SaaS Cards Light */
.saas-card {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 1.35rem 1.6rem !important;
    margin-bottom: 1.25rem !important;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
}

.saas-card h1, .saas-card h2, .saas-card h3, .saas-card h4 {
    color: #0F172A !important;
    margin-top: 0 !important;
}

.saas-card p, .saas-card span, .saas-card div {
    color: #1E293B !important;
}

/* KPI Cards Light */
.kpi-container {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 1.15rem 1.25rem !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
    text-align: left !important;
}

.kpi-title {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #475569 !important;
    margin-bottom: 0.4rem !important;
}

.kpi-value {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    line-height: 1.2 !important;
}

.kpi-subtitle {
    font-size: 0.82rem !important;
    color: #64748B !important;
    margin-top: 0.4rem !important;
    font-weight: 500 !important;
}

/* Badges Light */
.badge {
    display: inline-block !important;
    padding: 0.3rem 0.75rem !important;
    border-radius: 9999px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    line-height: 1 !important;
}

.badge-positive {
    background-color: #DCFCE7 !important;
    color: #14532D !important;
    border: 1.5px solid #86EFAC !important;
}

.badge-negative {
    background-color: #FEE2E2 !important;
    color: #7F1D1D !important;
    border: 1.5px solid #FCA5A5 !important;
}

.badge-mixed {
    background-color: #FEF3C7 !important;
    color: #78350F !important;
    border: 1.5px solid #FCD34D !important;
}

.badge-neutral {
    background-color: #E2E8F0 !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
}

/* Priority Badges Light */
.badge-priority-high {
    background-color: #FEE2E2 !important;
    color: #991B1B !important;
    border: 1.5px solid #EF4444 !important;
    font-weight: 800 !important;
}

.badge-priority-medium {
    background-color: #FEF3C7 !important;
    color: #92400E !important;
    border: 1.5px solid #F59E0B !important;
    font-weight: 800 !important;
}

.badge-priority-low {
    background-color: #E0F2FE !important;
    color: #0369A1 !important;
    border: 1.5px solid #0284C7 !important;
    font-weight: 800 !important;
}

/* Supporting Quote Blocks Light */
.quote-box {
    background-color: #F1F5F9 !important;
    border-left: 4px solid #2563EB !important;
    padding: 0.75rem 1rem !important;
    margin: 0.5rem 0 !important;
    border-radius: 0 8px 8px 0 !important;
    font-size: 0.92rem !important;
    font-style: italic !important;
    color: #0F172A !important;
    line-height: 1.5 !important;
}

/* Demo Banner Light */
.demo-banner {
    background-color: #EFF6FF !important;
    border: 1.5px solid #3B82F6 !important;
    border-radius: 8px !important;
    padding: 0.85rem 1.1rem !important;
    color: #1E3A8A !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    margin-bottom: 1.25rem !important;
}

.demo-banner b {
    color: #1D4ED8 !important;
}

/* Empty State Light */
.empty-state {
    text-align: center !important;
    padding: 3rem 2rem !important;
    background-color: #FFFFFF !important;
    border: 2px dashed #94A3B8 !important;
    border-radius: 14px !important;
    margin: 2rem 0 !important;
}

.empty-state-title {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin-top: 0.75rem !important;
}

.empty-state-text {
    font-size: 0.95rem !important;
    color: #475569 !important;
    max-width: 520px !important;
    margin: 0.6rem auto 1.5rem auto !important;
    line-height: 1.5 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
}

button[kind="primary"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3) !important;
}

button[kind="primary"]:hover {
    background-color: #1D4ED8 !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

button[kind="secondary"]:hover {
    background-color: #F1F5F9 !important;
    border-color: #94A3B8 !important;
}

hr {
    border: 0 !important;
    height: 1px !important;
    background: #CBD5E1 !important;
    margin: 1.5rem 0 !important;
}
</style>
"""


# ---------------------------------------------------------
# High-Contrast Dark Mode CSS
# ---------------------------------------------------------

DARK_THEME_CSS = """
<style>
/* CSS Variables & Base Layout Dark */
:root, [data-testid="stApp"], .stApp {
    --primary-color: #3B82F6 !important;
    --background-color: #0B1120 !important;
    --secondary-background-color: #1E293B !important;
    --text-color: #F8FAFC !important;
    color-scheme: dark !important;
    background-color: #0B1120 !important;
    color: #F8FAFC !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

header[data-testid="stHeader"] {
    background-color: #0B1120 !important;
}

[data-testid="stDeployButton"] {
    display: none !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
}

p, span, label, div, li {
    color: #E2E8F0;
}

[data-testid="stMarkdownContainer"] > p {
    color: #E2E8F0 !important;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* Sidebar Dark */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1.5px solid #1F2937 !important;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-weight: 600 !important;
    color: #F8FAFC !important;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background-color: #1F2937 !important;
}

/* Tabs Dark */
button[data-baseweb="tab"] {
    color: #94A3B8 !important;
    background-color: transparent !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #60A5FA !important;
    border-bottom-color: #3B82F6 !important;
    font-weight: 700 !important;
}

button[data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
}

/* Textarea & Inputs Dark Mode */
.stTextArea textarea,
.stTextArea div[data-baseweb="textarea"],
.stTextInput input,
.stTextInput div[data-baseweb="input"],
[data-testid="stTextArea"] textarea,
[data-testid="stTextAreaRootElement"],
[data-baseweb="textarea"],
[data-baseweb="base-input"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    border: 1.5px solid #475569 !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
}

.stTextArea textarea:focus,
[data-baseweb="textarea"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

/* Alert Boxes Dark Mode */
[data-testid="stAlert"],
.stAlert,
[data-testid="stAlertContainer"] {
    background-color: #172554 !important;
    border: 1.5px solid #3B82F6 !important;
    border-radius: 8px !important;
}

[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlertContainer"] *,
.stAlert p,
.stAlert span,
.stAlert strong {
    color: #DBEAFE !important;
    -webkit-text-fill-color: #DBEAFE !important;
    font-weight: 500 !important;
}

/* SaaS Cards Dark */
.saas-card {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 1.35rem 1.6rem !important;
    margin-bottom: 1.25rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4) !important;
}

.saas-card h1, .saas-card h2, .saas-card h3, .saas-card h4 {
    color: #F8FAFC !important;
    margin-top: 0 !important;
}

.saas-card p, .saas-card span, .saas-card div {
    color: #E2E8F0 !important;
}

/* KPI Cards Dark */
.kpi-container {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    padding: 1.15rem 1.25rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
    text-align: left !important;
}

.kpi-title {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #94A3B8 !important;
    margin-bottom: 0.4rem !important;
}

.kpi-value {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
    line-height: 1.2 !important;
}

.kpi-subtitle {
    font-size: 0.82rem !important;
    color: #94A3B8 !important;
    margin-top: 0.4rem !important;
    font-weight: 500 !important;
}

/* Badges Dark */
.badge {
    display: inline-block !important;
    padding: 0.3rem 0.75rem !important;
    border-radius: 9999px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    line-height: 1 !important;
}

.badge-positive {
    background-color: #064E3B !important;
    color: #6EE7B7 !important;
    border: 1.5px solid #059669 !important;
}

.badge-negative {
    background-color: #450A0A !important;
    color: #FCA5A5 !important;
    border: 1.5px solid #DC2626 !important;
}

.badge-mixed {
    background-color: #451A03 !important;
    color: #FCD34D !important;
    border: 1.5px solid #D97706 !important;
}

.badge-neutral {
    background-color: #334155 !important;
    color: #F1F5F9 !important;
    border: 1.5px solid #475569 !important;
}

/* Priority Badges Dark */
.badge-priority-high {
    background-color: #7F1D1D !important;
    color: #FEE2E2 !important;
    border: 1.5px solid #EF4444 !important;
    font-weight: 800 !important;
}

.badge-priority-medium {
    background-color: #78350F !important;
    color: #FEF3C7 !important;
    border: 1.5px solid #F59E0B !important;
    font-weight: 800 !important;
}

.badge-priority-low {
    background-color: #0C4A6E !important;
    color: #E0F2FE !important;
    border: 1.5px solid #0284C7 !important;
    font-weight: 800 !important;
}

/* Supporting Quote Blocks Dark */
.quote-box {
    background-color: #0F172A !important;
    border-left: 4px solid #3B82F6 !important;
    padding: 0.75rem 1rem !important;
    margin: 0.5rem 0 !important;
    border-radius: 0 8px 8px 0 !important;
    font-size: 0.92rem !important;
    font-style: italic !important;
    color: #E2E8F0 !important;
    line-height: 1.5 !important;
}

/* Demo Banner Dark */
.demo-banner {
    background-color: #172554 !important;
    border: 1.5px solid #3B82F6 !important;
    border-radius: 8px !important;
    padding: 0.85rem 1.1rem !important;
    color: #93C5FD !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    margin-bottom: 1.25rem !important;
}

.demo-banner b {
    color: #BFDBFE !important;
}

/* Empty State Dark */
.empty-state {
    text-align: center !important;
    padding: 3rem 2rem !important;
    background-color: #1E293B !important;
    border: 2px dashed #475569 !important;
    border-radius: 14px !important;
    margin: 2rem 0 !important;
}

.empty-state-title {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    margin-top: 0.75rem !important;
}

.empty-state-text {
    font-size: 0.95rem !important;
    color: #94A3B8 !important;
    max-width: 520px !important;
    margin: 0.6rem auto 1.5rem auto !important;
    line-height: 1.5 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    background-color: #1E293B !important;
}

button[kind="primary"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(37, 99, 235, 0.4) !important;
}

button[kind="primary"]:hover {
    background-color: #3B82F6 !important;
}

button[kind="secondary"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1.5px solid #475569 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

button[kind="secondary"]:hover {
    background-color: #334155 !important;
    border-color: #64748B !important;
}

hr {
    border: 0 !important;
    height: 1px !important;
    background: #334155 !important;
    margin: 1.5rem 0 !important;
}
</style>
"""


def apply_theme(dark_mode: bool = False):
    """Inject either Light or Dark mode SaaS CSS based on user toggle."""
    if dark_mode:
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Badges & Renderers
# ---------------------------------------------------------

def get_sentiment_badge_html(sentiment: str) -> str:
    """Generate an HTML sentiment badge with guaranteed contrast."""
    norm = str(sentiment).lower().strip()
    if "pos" in norm:
        cls_name = "badge-positive"
    elif "neg" in norm:
        cls_name = "badge-negative"
    elif "mix" in norm:
        cls_name = "badge-mixed"
    else:
        cls_name = "badge-neutral"
    return f'<span class="badge {cls_name}">{sentiment}</span>'


def get_priority_badge_html(priority: str) -> str:
    """Generate an HTML priority badge with strong visible borders."""
    norm = str(priority).lower().strip()
    if "high" in norm:
        cls_name = "badge-priority-high"
    elif "med" in norm:
        cls_name = "badge-priority-medium"
    else:
        cls_name = "badge-priority-low"
    return f'<span class="badge {cls_name}">{priority} PRIORITY</span>'


# ---------------------------------------------------------
# Plotly Visualization Builders with Dual-Mode Support
# ---------------------------------------------------------

def create_pos_neg_grouped_bar(aspects: List[Dict[str, Any]], dark_mode: bool = False) -> go.Figure:
    """
    Creates an interactive grouped bar chart comparing Positive vs. Negative
    mentions across identified product aspects.
    """
    if not aspects:
        fig = go.Figure()
        fig.update_layout(title="No aspect data available")
        return fig

    aspect_names = [a.get("aspect", "") for a in aspects]
    positive_counts = [a.get("positive_reviews", 0) for a in aspects]
    negative_counts = [a.get("negative_reviews", 0) for a in aspects]

    bg_color = "#1E293B" if dark_mode else "#FFFFFF"
    text_color = "#F8FAFC" if dark_mode else "#0F172A"
    muted_color = "#94A3B8" if dark_mode else "#475569"
    grid_color = "#334155" if dark_mode else "#E2E8F0"
    zeroline_color = "#475569" if dark_mode else "#CBD5E1"

    fig = go.Figure()

    # Positive Bars (Emerald)
    fig.add_trace(go.Bar(
        x=aspect_names,
        y=positive_counts,
        name="Positive Reviews",
        marker_color="#10B981",
        marker_line=dict(color="#059669", width=1.5),
        hovertemplate="<b>%{x}</b><br>Positive Reviews: %{y}<extra></extra>"
    ))

    # Negative Bars (Crimson)
    fig.add_trace(go.Bar(
        x=aspect_names,
        y=negative_counts,
        name="Negative Reviews",
        marker_color="#EF4444",
        marker_line=dict(color="#DC2626", width=1.5),
        hovertemplate="<b>%{x}</b><br>Negative Reviews: %{y}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="Positive vs. Negative Feedback by Product Aspect",
            font=dict(size=16, color=text_color, family="Inter, sans-serif")
        ),
        barmode="group",
        bargap=0.28,
        bargroupgap=0.12,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        margin=dict(l=40, r=20, t=55, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, color=text_color)
        ),
        xaxis=dict(
            title="",
            tickfont=dict(size=12, color=text_color),
            showgrid=False
        ),
        yaxis=dict(
            title="Distinct Review Count",
            title_font=dict(size=12, color=muted_color),
            tickfont=dict(size=11, color=muted_color),
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor=zeroline_color
        )
    )

    return fig


def create_aspect_frequency_bar(aspects: List[Dict[str, Any]], dark_mode: bool = False) -> go.Figure:
    """
    Creates a horizontal bar chart showing total review mention frequency
    for each product aspect, ranked from most discussed to least.
    """
    if not aspects:
        fig = go.Figure()
        fig.update_layout(title="No aspect data available")
        return fig

    sorted_aspects = sorted(aspects, key=lambda x: x.get("total_reviews_mentioning", 0))
    aspect_names = [a.get("aspect", "") for a in sorted_aspects]
    totals = [a.get("total_reviews_mentioning", 0) for a in sorted_aspects]

    bg_color = "#1E293B" if dark_mode else "#FFFFFF"
    text_color = "#F8FAFC" if dark_mode else "#0F172A"
    muted_color = "#94A3B8" if dark_mode else "#475569"
    grid_color = "#334155" if dark_mode else "#E2E8F0"

    fig = go.Figure(go.Bar(
        x=totals,
        y=aspect_names,
        orientation="h",
        marker=dict(
            color="#2563EB" if not dark_mode else "#3B82F6",
            line=dict(color="#1D4ED8", width=1.5)
        ),
        text=totals,
        textposition="outside",
        textfont=dict(color=text_color, size=12),
        hovertemplate="<b>%{y}</b><br>Total Reviews Mentioning: %{x}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="Aspect Mention Frequency (Total Reviews)",
            font=dict(size=16, color=text_color, family="Inter, sans-serif")
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        margin=dict(l=40, r=40, t=55, b=40),
        xaxis=dict(
            title="Total Distinct Reviews",
            title_font=dict(size=12, color=muted_color),
            tickfont=dict(size=11, color=muted_color),
            gridcolor=grid_color
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=text_color),
            showgrid=False
        )
    )

    return fig


def create_sentiment_distribution_donut(aspects: List[Dict[str, Any]], dark_mode: bool = False) -> go.Figure:
    """
    Creates a clean donut chart displaying the breakdown of aspect sentiments.
    """
    if not aspects:
        fig = go.Figure()
        fig.update_layout(title="No data")
        return fig

    counts: Dict[str, int] = {}
    for a in aspects:
        sent = str(a.get("sentiment", "Neutral")).capitalize()
        counts[sent] = counts.get(sent, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())

    color_map = {
        "Positive": "#10B981",
        "Negative": "#EF4444",
        "Mixed": "#F59E0B",
        "Neutral": "#64748B"
    }
    colors = [color_map.get(lbl, "#94A3B8") for lbl in labels]

    bg_color = "#1E293B" if dark_mode else "#FFFFFF"
    text_color = "#F8FAFC" if dark_mode else "#0F172A"

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=bg_color, width=2)),
        textinfo="label+value",
        textfont=dict(color=text_color, size=12),
        hovertemplate="<b>%{label}</b><br>Aspects: %{value} (%{percent})<extra></extra>"
    )])

    fig.update_layout(
        title=dict(
            text="Aspect Sentiment Distribution",
            font=dict(size=16, color=text_color, family="Inter, sans-serif")
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        margin=dict(l=20, r=20, t=55, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color=text_color)
        )
    )

    return fig
