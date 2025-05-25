import streamlit as st
import os
import base64
import pathlib
from birthday_problem.view import birthday_problem_app
from monty_hall.view import monty_hall_app
from streamlit_pdf_viewer import pdf_viewer


#from streamlit_javascript import st_javascript

#user_agent = st_javascript("navigator.userAgent")
#if user_agent and "mobile" in user_agent.lower():
#    st.warning("📱 You’re viewing this on a **mobile device**. Layout is optimized, but performance and interactivity may vary.")

st.set_page_config(page_title="Private Tutor Site", layout="wide")


def local_css():
    st.markdown("""
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #fffafa !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #f5f5f0 !important;
    }
    .stButton > button {
        width: 100%;
        background-color: #a9a9a9 !important;
        color: white;
        border-radius: 8px;
        margin-bottom: 8px;
        padding: 10px 15px;
        font-size: 1.1rem;
    }
    .stButton > button:hover {
        background-color: #0059b3 !important;
        color: #778899 !important;
    }

    /* -------- Responsive tweaks for mobile -------- */
    @media screen and (max-width: 768px) {
        .stButton > button {
            font-size: 1.3rem !important;
            padding: 12px 18px !important;
        }
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

with open("symbol_no_background.png", "rb") as f:
    sidebar_logo_base64 = base64.b64encode(f.read()).decode()

st.sidebar.markdown(f"""
    <div style='position: absolute; top: 0; left: 0; z-index: 999;'>
        <img src='data:image/png;base64,{sidebar_logo_base64}' width='60' style='display:block; margin:0; padding:0;'>
    </div>
    <div style='height: 80px;'></div>
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
        <div style='background-color:#ffffff; padding:30px; border-radius:12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width:900px; margin:auto;'>
            <div style='display:flex; flex-wrap:wrap; align-items:center;'>
                <img src='data:image/jpeg;base64,{base64.b64encode(open("Headshot.jpeg", "rb").read()).decode()}'  
                     width='180' style='border-radius:12px; margin-top:30px; margin-right:30px;' />
                <div>
                    <h1 style='margin-bottom:5px; margin-left:5px; color:#004080;'>Maor Blumberg</h1>
                    <p style='line-height: 1.6; font-size: 28px;'>
                        <strong>📧</strong> <a href='mailto:maorblumberg@gmail.com'>maorblumberg@gmail.com</a><br>
                        <strong>📞</strong> <a href='tel:+972543276073'>+972 543276073</a><br>
                        <strong>🔗</strong> <a href='https://www.linkedin.com/in/maor-blumberg-9b5a43259/'>LinkedIn</a><br>
                        <strong>💻</strong> <a href='https://github.com/Maorb23'>GitHub</a>
                    </p>
                    <div style='margin-top:30px; font-size:18px; color:#333;'>
                        Welcome! Use the sidebar to explore topics and access my CV.<br>
                        I specialize in personalized learning for Statistics, Probability and Machine Learning.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def render_videos():
    st.title("Tutorial Videos")
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
