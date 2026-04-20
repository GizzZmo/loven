"""Streamlit dashboard for loven – WorldPeace-Lovdata-Kompendium.

Launch with::

    streamlit run app/streamlit_app.py

Or via Docker::

    docker compose up
"""

from __future__ import annotations

import io

import streamlit as st

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="loven – Norwegian Law Explorer",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("🕊️ loven")
    st.caption("WorldPeace-Lovdata-Kompendium")
    st.divider()

    st.subheader("Search Settings")
    query = st.text_input(
        "Search query (Norwegian)",
        value="energi",
        placeholder="e.g. energilov, miljøvern, klimamål",
    )
    limit = st.slider("Max results", min_value=5, max_value=100, value=20, step=5)

    st.divider()
    st.subheader("Peace-Theme Filter")

    from loven.themes import PEACE_THEMES

    selected_themes = st.multiselect(
        "Active peace themes",
        options=PEACE_THEMES,
        default=PEACE_THEMES,
        help="Only laws containing at least one selected theme keyword will appear.",
    )

    use_synonyms = st.checkbox(
        "Expand with synonyms (NLP)",
        value=False,
        help="Include Norwegian synonym variants of each selected theme keyword.",
    )

    st.divider()
    st.subheader("Cache")
    use_cache = st.checkbox("Enable disk cache", value=True)
    if st.button("Clear cache"):
        from loven.cache import DiskCache

        n = DiskCache().clear()
        st.success(f"Cleared {n} cached entries.")

    st.divider()
    st.caption("v0.4.0 · [GitHub](https://github.com/GizzZmo/loven)")

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------

st.title("🕊️ Norwegian Peace-Law Explorer")
st.write(
    "Query the [Lovdata](https://lovdata.no) API for laws related to "
    "energy, water, climate, ethics, and other peace themes."
)

if not query.strip():
    st.info("Enter a search query in the sidebar to get started.")
    st.stop()

# Build effective theme list
if use_synonyms:
    from loven.nlp import expand_themes

    effective_themes: list[str] | None = expand_themes(selected_themes) if selected_themes else None
else:
    effective_themes = selected_themes if selected_themes else None

# Run analysis
with st.spinner(f"Searching Lovdata for **{query}**…"):
    try:
        from loven import LovDataClient, analyze_peace_laws
        from loven.cache import DiskCache

        cache = DiskCache() if use_cache else None
        client = LovDataClient(cache=cache)
        df = analyze_peace_laws(client, query, limit=limit, themes=effective_themes)
    except Exception as exc:
        st.error(f"Search failed: {exc}")
        st.stop()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

if df.empty:
    st.warning("No peace-relevant results found for this query.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Results", len(df))
col2.metric("Max tema_treff", int(df["tema_treff"].max()))
col3.metric("Active themes", len(effective_themes) if effective_themes else len(PEACE_THEMES))

st.divider()

# Tabs: Table | Charts | Export
tab_table, tab_charts, tab_export = st.tabs(["📋 Table", "📊 Charts", "💾 Export"])

# ------------------------------------------------------------------ Table tab
with tab_table:
    display_cols = [c for c in ("tittel", "url", "dato", "dokumenttype", "tema_treff") if c in df.columns]
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        column_config={
            "url": st.column_config.LinkColumn("URL"),
            "tema_treff": st.column_config.NumberColumn("Theme Matches", format="%d"),
        },
    )

# ------------------------------------------------------------------ Charts tab
with tab_charts:
    try:
        import matplotlib.pyplot as plt

        from loven.viz import bar_chart

        st.subheader("Top Peace-Relevant Laws")
        fig = bar_chart(df, top_n=15)
        st.pyplot(fig)
        plt.close(fig)
    except ImportError:
        st.info(
            "Install visualisation extras for charts: `pip install 'loven[viz]'`"
        )
    except Exception as exc:
        st.warning(f"Could not render chart: {exc}")

    try:
        import matplotlib.pyplot as plt

        from loven.viz import word_cloud

        st.subheader("Title Word Cloud")
        fig_wc = word_cloud(df)
        st.pyplot(fig_wc)
        plt.close(fig_wc)
    except ImportError:
        st.info(
            "Install visualisation extras for word clouds: `pip install 'loven[viz]'`"
        )
    except Exception as exc:
        st.warning(f"Could not render word cloud: {exc}")

# ------------------------------------------------------------------ Export tab
with tab_export:
    st.subheader("Download Results")

    col_csv, col_md = st.columns(2)

    with col_csv:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download CSV",
            data=csv_bytes,
            file_name=f"loven_{query[:20].replace(' ', '_')}.csv",
            mime="text/csv",
        )

    with col_md:
        from loven.export import to_markdown

        buf = io.StringIO()
        # Reuse to_markdown logic by writing to a temp buffer
        cols = [c for c in ("tittel", "url", "dato", "dokumenttype", "tema_treff") if c in df.columns]
        subset = df[cols]
        lines = []
        lines.append("| " + " | ".join(subset.columns) + " |")
        lines.append("| " + " | ".join("---" for _ in subset.columns) + " |")
        for _, row in subset.iterrows():
            cells = [str(v).replace("|", "\\|") for v in row]
            lines.append("| " + " | ".join(cells) + " |")
        md_content = "\n".join(lines) + "\n"

        st.download_button(
            label="⬇ Download Markdown",
            data=md_content.encode("utf-8"),
            file_name=f"loven_{query[:20].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    st.caption("Excel export: `pip install openpyxl`, then use `loven export` CLI.")
