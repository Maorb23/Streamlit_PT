import base64
import os
import pathlib

import streamlit as st
from birthday_problem.view import birthday_problem_app
from monty_hall.view import monty_hall_app
from streamlit_pdf_viewer import pdf_viewer


#from streamlit_javascript import st_javascript

#user_agent = st_javascript("navigator.userAgent")
#if user_agent and "mobile" in user_agent.lower():
#    st.warning("📱 You’re viewing this on a **mobile device**. Layout is optimized, but performance and interactivity may vary.")

st.set_page_config(
    page_title="Maor Blumberg | Private Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

def local_css():
    st.markdown("""
    <style>
    :root { --ink:#172033; --muted:#687386; --blue:#2563eb; --line:#e5eaf2; }
    html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    div[data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f7faff 0%, #ffffff 55%, #f4f8ff 100%) !important;
        color: var(--ink);
    }
    div[data-testid="stHeader"] { background: transparent !important; }
    .block-container { max-width: 1180px; padding-top: 2.5rem; padding-bottom: 4rem; }
    section[data-testid="stSidebar"] { background: #f8fafc !important; border-right: 1px solid var(--line); }
    section[data-testid="stSidebar"] .block-container { padding: 1.25rem 1rem; }
    .brand { padding: .5rem .4rem 1.5rem; }
    .brand-name { color: var(--ink); font-size: 1.15rem; font-weight: 750; margin-top: .6rem; }
    .brand-copy { color: var(--muted); font-size: .82rem; line-height: 1.45; }
    h1, h2, h3 { color: var(--ink) !important; letter-spacing: -.025em; }
    .hero { background: radial-gradient(circle at 88% 8%, #dbeafe 0, transparent 32%), #fff; border: 1px solid var(--line); border-radius: 24px; padding: 2.5rem; box-shadow: 0 18px 45px rgba(31,54,94,.08); margin-bottom: 1rem; }
    .hero h1 { font-size: clamp(2.3rem, 5vw, 4.2rem); line-height: 1; margin: 0 0 .8rem; }
    .eyebrow { color: var(--blue); font-size: .78rem; font-weight: 750; letter-spacing: .12em; text-transform: uppercase; }
    .hero-lead { color: var(--muted); font-size: 1.1rem; line-height: 1.65; max-width: 680px; }
    .contact-card { background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 16px; padding: 1rem 1.15rem; }
    .contact-card a { color: #163c83; text-decoration: none; }
    .section-card { background: #fff; border: 1px solid var(--line); border-radius: 18px; padding: 1.3rem 1.4rem; height: 100%; }
    .section-card h3 { margin-top: 0; font-size: 1.05rem; }
    .section-card p { color: var(--muted); line-height: 1.55; margin-bottom: 0; }
    .stButton > button {
        width: 100%;
        background-color: transparent !important;
        color: #4b5563;
        border: 1px solid transparent;
        border-radius: 10px;
        margin-bottom: 8px;
        padding: 9px 12px;
        font-size: .95rem;
        text-align: left;
    }
    .stButton > button:hover {
        background-color: #eaf2ff !important;
        border-color: #cfe0ff;
        color: #163c83 !important;
    }
    .stDownloadButton > button { width: 100%; }

    /* -------- Responsive tweaks for mobile -------- */
    @media screen and (max-width: 768px) {
        .stButton > button {
            font-size: 1rem !important;
            padding: 10px 12px !important;
        }
        .block-container { padding: 1.5rem 1rem 3rem; }
        .hero { padding: 1.5rem; border-radius: 18px; }
        .hero h1 { font-size: 2.5rem; }
        section[data-testid="stSidebar"] {
            width: 100vw !important;
        }
        img {
            max-width: 100% !important;
            height: auto !important;
        }
        iframe {
            width: 100% !important;
        }
        .element-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

BASE_DIR = pathlib.Path(__file__).parent.resolve()

@st.cache_data(show_spinner=False)
def read_asset_base64(filename):
    with open(BASE_DIR / filename, "rb") as asset:
        return base64.b64encode(asset.read()).decode()

sidebar_logo_base64 = read_asset_base64("symbol_no_background.png")

st.sidebar.markdown(f"""
    <div class='brand'>
        <img src='data:image/png;base64,{sidebar_logo_base64}' width='58' style='display:block;'>
        <div class='brand-name'>Maor Blumberg</div>
        <div class='brand-copy'>Statistics · Probability · Machine Learning</div>
    </div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Home'

if st.sidebar.button("🏠 Home"):
    st.session_state.page = 'Home'
if st.sidebar.button("🎥 Videos"):
    st.session_state.page = 'Videos'
if st.sidebar.button("📄 CV"):
    st.session_state.page = 'CV'
if st.sidebar.button("🎂 Birthday Paradox"):
    st.session_state.page = 'Birthday'
if st.sidebar.button("🚪 Monty Hall Paradox"):
    st.session_state.page = "Monty"

page = st.session_state.page

def list_videos(category):
    path = BASE_DIR / 'videos' / category.lower()
    if not path.exists():
        return []
    return [str(f) for f in path.glob("*") if f.suffix.lower() in (".mp4", ".mov", ".webm", ".ogg")]

def render_home():
    st.markdown(
        f"""
        <div class='hero'>
            <div class='eyebrow'>Private tutoring · Visual learning</div>
            <h1>Make the hard stuff<br>click.</h1>
            <p class='hero-lead'>Personalized tutoring in Statistics, Probability, and Machine Learning — with clear explanations, practical examples, and interactive simulations.</p>
            <div class='contact-card'>
                <a href='mailto:maorblumberg@gmail.com'>📧 maorblumberg@gmail.com</a>&nbsp;&nbsp; · &nbsp;&nbsp;
                <a href='https://www.linkedin.com/in/maor-blumberg-9b5a43259/'>LinkedIn</a>&nbsp;&nbsp; · &nbsp;&nbsp;
                <a href='https://github.com/Maorb23'>GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    cards = [("Learn by doing", "Explore the video library and interactive experiments."), ("Build intuition", "Turn formulas into ideas you can explain and use."), ("Go at your pace", "Focused support for assignments, exams, and long-term mastery.")]
    for column, (title, copy) in zip((col1, col2, col3), cards):
        with column:
            st.markdown(f"<div class='section-card'><h3>{title}</h3><p>{copy}</p></div>", unsafe_allow_html=True)

def render_videos():
    st.title("Tutorial videos")
    st.caption("Short, focused explanations for the ideas that matter most.")
    categories = ["Statistics", "Probability", "Machine Learning"]

    all_videos = []
    for cat in categories:
        all_videos.extend(list_videos(cat))
    if all_videos:
        st.subheader("Featured Video")
        st.video(all_videos[0])
    else:
        st.info("No videos found. Place video files in /videos/[category]/ folders.")

    st.markdown("---")
    choice = st.radio("Browse by Category", categories)
    vids = list_videos(choice)
    if vids:
        selected = st.selectbox(f"Choose a video in '{choice}'", [os.path.basename(v) for v in vids])
        st.video(BASE_DIR / "videos" / choice.lower() / selected)
    else:
        st.warning(f"No videos in {choice}.")



# Define your annotations (example positions on page 1)
ANNOTATIONS = [
    {
        "page": 1,
        "x": 220,
        "y": 155,
        "height": 22,
        "width": 65,
        "color": "red",
        "border": "solid",      # you can omit border for a filled rectangle
    },
    {
        "page": 1,
        "x": 220,
        "y": 180,
        "height": 18,
        "width": 120,
        "color": "blue",
        "border": "dotted",
    }
]

def on_annotation_click(annotation):
    # this runs in your Streamlit script, so use st.info() or st.success()
    st.info("👋 Check out my GitHub at https://github.com/Maorb23")

def render_cv_alternative():
    st.title("Curriculum Vitae")
    pdf_path = BASE_DIR / "Maor_Blumberg CV_Updated_ds.pdf"
    if not pdf_path.exists():
        st.error("CV PDF not found.")
        return

    # Simplified annotation structure
    annotations = [
        {
            "page": 0,  # Try 0-indexed if 1-indexed doesn't work
            "x": 220,
            "y": 155,
            "width": 65,
            "height": 22,
            "color": "#ff0000",
            "opacity": 0.3,
            "label": "GitHub Link"
        },
        {
            "page": 0,
            "x": 220,
            "y": 180,
            "width": 120,
            "height": 18,
            "color": "#0000ff",
            "opacity": 0.3,
            "label": "Contact Info"
        }
    ]

    # Create columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Render PDF viewer
        result = pdf_viewer(
            input=pdf_path,
            annotations=annotations,
            width=700,
            height=800
        )
        
        # Handle clicks
        if result:
            st.json(result)  # Debug output
            
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("🔗 Visit GitHub"):
            st.success("Opening GitHub...")
            st.markdown("[GitHub Profile](https://github.com/Maorb23)")
            
        if st.button("📧 Contact Me"):
            st.info("Email: maorblumberg@gmail.com")
        
        st.markdown("---")
        
        # Download button
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            "📄 Download CV",
            data=pdf_bytes,
            file_name="Maor_Blumberg_CV.pdf",
            mime="application/pdf",
        )




# --- Route Pages ---
if page == "Home":
    render_home()
elif page == "Videos":
    render_videos()
elif page == "CV":
    render_cv_alternative()
elif page == "Birthday":
    birthday_problem_app()
elif page == "Monty":
    monty_hall_app()
