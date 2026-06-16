import streamlit as st
import os
import plotly.express as px

def load_css(file_name="assets/style.css"):
    """Fungsi untuk memuat custom CSS struktural ke dalam aplikasi Streamlit."""
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def apply_theme():
    """Mengaplikasikan tema dinamis (Kini ditangani otomatis oleh Streamlit Native Theme)."""
    pass

def render_sidebar_theme_toggle():
    """Merender toggle tema (Kini dihapus karena menggunakan pengaturan tema bawaan OS)."""
    pass

def format_currency(value: float) -> str:
    """Format angka menjadi format Rupiah (Rp X.XXX.XXX) dibulatkan ke atas."""
    import math
    # Bulatkan ke atas (ceil)
    rounded_val = math.ceil(value)
    # Format dengan koma untuk ribuan lalu ganti koma menjadi titik
    indonesian_format = f"{rounded_val:,}".replace(",", ".")
    return f"Rp {indonesian_format}"

def render_page_header(title: str, subtitle: str):
    """Menampilkan Header Halaman yang lega dan konsisten."""
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_empty_state(title: str, description: str, icon: str = "📭"):
    """Menampilkan komponen Empty State."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_feature_card(title: str, description: str, icon: str = "✨"):
    """Menampilkan Feature Card di halaman Landing/Overview."""
    st.markdown(f"""
    <div class="feature-card">
        <div class="icon-wrap">{icon}</div>
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, subtitle: str = "", icon: str = ""):
    """Menampilkan KPI Card spesifik metrik analitik."""
    display_sub = subtitle if subtitle else "&nbsp;"
    sub_html = f'<p class="kpi-subtitle">{display_sub}</p>'
    icon_html = f'<div class="kpi-icon">{icon}</div>' if icon else ""
    
    st.markdown(f"""
    <div class="custom-kpi-card">
        <div class="kpi-header">
            <p class="kpi-title">{title}</p>
            {icon_html}
        </div>
        <h3 class="kpi-value">{value}</h3>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(label: str, status: str) -> str:
    """Mengembalikan string HTML untuk Risk Badge berdasarkan status warna."""
    lvl = status.lower()
    if "high" in lvl:
        badge_class = "badge-danger"
    elif "medium" in lvl:
        badge_class = "badge-warning"
    elif "low" in lvl:
        badge_class = "badge-success"
    else:
        badge_class = "badge-info"
        
    return f'<span class="badge {badge_class}">{label}</span>'

def render_insight_box(title: str, text: str, icon: str = "💡"):
    """Menampilkan Insight Box bergaya Executive Summary."""
    st.markdown(f"""
<div class="insight-box">
<div class="insight-box-title">{icon} {title}</div>
<div class="insight-box-text">

{text}

</div>
</div>
""", unsafe_allow_html=True)


# ================= PLOTLY HELPERS (TRANSPARAN & RAPI) =================

def _apply_plotly_layout(fig):
    """Template konsisten untuk margin dan interaktivitas. Warna diatur oleh Streamlit Theme."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        hovermode="x unified"
    )
    return fig

def create_line_chart(df, x_col, y_col, line_color="#06B6D4"):
    fig = px.line(df, x=x_col, y=y_col, markers=True)
    fig = _apply_plotly_layout(fig)
    fig.update_layout(xaxis_title="", yaxis_title="")
    fig.update_traces(
        line_color=line_color, 
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    )
    return fig

def create_bar_chart(df, x_col, y_col, orientation='v', color_seq=None):
    if color_seq is None:
        color_seq = ["#06B6D4"]
        
    if orientation == 'h':
        fig = px.bar(df, x=y_col, y=x_col, orientation='h', color_discrete_sequence=color_seq)
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        hovertemp = '<b>%{y}</b><br>%{x}<extra></extra>'
    else:
        fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=color_seq)
        hovertemp = '<b>%{x}</b><br>%{y}<extra></extra>'
        
    fig = _apply_plotly_layout(fig)
    fig.update_layout(xaxis_title="", yaxis_title="")
    
    if orientation == 'h':
        fig.update_layout(hovermode="y unified")
        
    fig.update_traces(hovertemplate=hovertemp)
    return fig

def create_donut_chart(df, names_col, values_col):
    fig = px.pie(df, names=names_col, values=values_col, hole=0.6, 
                 color_discrete_sequence=px.colors.sequential.Teal_r)
    fig = _apply_plotly_layout(fig)
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), hovermode=False)
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label'
    )
    return fig
