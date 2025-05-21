import streamlit as st
import os
import base64
import pathlib
from birthday_problem.view import birthday_problem_app  # <-- Import the birthday view

# --- Page Configuration ---
st.set_page_config(page_title="Private Tutor Site", layout="wide")

# --- Custom CSS ---
def local_css():
    st.markdown("""
    <style>
      div[data-testid="stAppViewContainer"] { background-color: #fffafa !important; }
      section[data-testid="stSidebar"] { background-color: #f5f5f0 !important; }
      .stButton > button {
          width: 100%;
          background-color: #a9a9a9 !important;
          color: white;
          border-radius: 8px;
          margin-bottom: 8px;
          padding: 10px 15px;
          font-size: 1.1rem;
      }
      .stButton > button:hover { background-color: #0059b3 !important; color: #778899 !important; }
    </style>
    """, unsafe_allow_html=True)

local_css()

BASE_DIR = pathlib.Path(__file__).parent.resolve()

# --- Load logo ---
with open("symbol_no_background.png", "rb") as f:
    sidebar_logo_base64 = base64.b64encode(f.read()).decode()

st.sidebar.markdown(f"""
    <div style='position: absolute; top: 0; left: 0; z-index: 999;'>
        <img src='data:image/png;base64,{sidebar_logo_base64}' width='60' style='display:block; margin:0; padding:0;'>
    </div>
    <div style='height: 80px;'></div>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# --- Sidebar Navigation ---
if st.sidebar.button("🏠 Home"):
    st.session_state.page = 'Home'
if st.sidebar.button("🎥 Videos"):
    st.session_state.page = 'Videos'
if st.sidebar.button("📄 CV"):
    st.session_state.page = 'CV'
if st.sidebar.button("🎂 Birthday Problem"):
    st.session_state.page = 'Birthday'

page = st.session_state.page

# --- Helper ---
def list_videos(category):
    path = BASE_DIR / 'videos' / category.lower()
    if not path.exists():
        return []
    return [str(f) for f in path.glob("*") if f.suffix.lower() in (".mp4", ".mov", ".webm", ".ogg")]

# --- Pages ---
def render_home():
    st.markdown(
        f"""
        <div style='background-color:#ffffff; padding:30px; border-radius:12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width:900px; margin:auto;'>
            <div style='display:flex; align-items:center;'>
                <img src='data:image/jpeg;base64,{base64.b64encode(open("Headshot.jpeg", "rb").read()).decode()}'  
                     width='180' style='border-radius:12px; margin-top:50px; margin-right:30px;' />
                <div>
                    <h1 style='margin-bottom:5px; margin-left:5px; color:#004080;'>Maor Blumberg</h1>
                    <p style='line-height: 1.6; font-size: 36px;'>
                        <strong>📧</strong> <a href='mailto:maorblumberg@gmail.com'>maorblumberg@gmail.com</a><br>
                        <strong>📞</strong> <a href='tel:+972543276073'>+972 543276073</a><br>
                        <strong>🔗</strong> <a href='https://www.linkedin.com/in/maor-blumberg-9b5a43259/'>LinkedIn</a><br>
                        <strong>💻</strong> <a href='https://github.com/Maorb23'>GitHub</a>
                    </p>
                    <div style='text-align:center; margin-top:30px; font-size:18px; color:#333;'>
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
        vid_path = all_videos[0]
        st.video(vid_path)
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

def render_cv():
    st.title("Curriculum Vitae")
    pdf_path = BASE_DIR / "Maor_Blumberg CV_Updated_ds.pdf"
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
        st.download_button("Download CV", data=open(pdf_path, "rb"), file_name="CV.pdf", mime="application/pdf")
    else:
        st.error("CV PDF not found.")

# --- Route Pages ---
if page == "Home":
    render_home()
elif page == "Videos":
    render_videos()
elif page == "CV":
    render_cv()
elif page == "Birthday":
    birthday_problem_app()
