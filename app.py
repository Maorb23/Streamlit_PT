import streamlit as st
import os
import base64

# --- Page Configuration and Theme ---
st.set_page_config(page_title="Private Tutor Site", layout="wide")

# Custom CSS for business-elegant theme
def local_css():
    st.markdown("""
    <style>
      /* Full page background color */
      div[data-testid="stAppViewContainer"] {
          background-color: #fffafa !important;
      }
      /* Fallback if needed */
      body, .main {
          background-color: #fffafa !important;
      }

      /* Sidebar background */
      section[data-testid="stSidebar"] {
          background-color: #f5f5f0 !important;
      }
      section[data-testid="stSidebar"] > div {
          background-color: #f5f5f0 !important;
      }
      section[data-testid="stSidebar"] form {
          background-color: transparent !important;
      }

      /* Button styling */
      .stButton > button {
          width: 100%;
          text-align: left;
          background-color: #a9a9a9 !important;
          color: white;
          border-radius: 8px;
          margin-bottom: 8px;
          padding: 10px 15px;
          font-size: 1.1rem;
      }
      .stButton > button:hover { background-color: #0059b3 !important; 
                color: #778899 !important; }
      .stButton > button:focus,
      .stButton > button:active {
          outline: none !important;
          box-shadow: none !important;
          background-color: #a9a9a9 !important;
      }
    </style>
    """, unsafe_allow_html=True)



local_css()
with open("symbol_no_background.png", "rb") as f:
    sidebar_logo_base64 = base64.b64encode(f.read()).decode()


st.sidebar.markdown(f"""
    <div style='position: absolute; top: 0; left: 0; padding: 0; margin: 0; z-index: 999;'>
        <img src='data:image/png;base64,{sidebar_logo_base64}' width='60' style='display:block; margin:0; padding:0;'>
    </div>
    <div style='height: 80px;'></div> <!-- spacer to push content below the logo -->
""", unsafe_allow_html=True)


# Initialize page state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Emoji buttons
if st.sidebar.button("🏠 Home", key="home_btn",type = "tertiary"):
    st.session_state.page = 'Home'
if st.sidebar.button("🎥 Videos", key="videos_btn"):
    st.session_state.page = 'Videos'
if st.sidebar.button("📄 CV", key="cv_btn"):
    st.session_state.page = 'CV'

#add_selectbox = st.sidebar.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone")
#)

# Using "with" notation
#with st.sidebar:
#    add_radio = st.radio(
#        "Choose a shipping method",
#        ("Standard (5-15 days)", "Express (2-5 days)")
#    )

page = st.session_state.page

# --- Helper: Load Videos ---
def list_videos(category):
    path = os.path.join('videos', category.lower())
    if not os.path.exists(path):
        return []
    return [os.path.join(path, f) for f in os.listdir(path)
            if f.lower().endswith(('.mp4', '.mov', '.webm', '.ogg'))]

# --- Page: Home ---
def render_home():
    st.markdown(
        """
        <div style='background-color:#ffffff; padding:30px; border-radius:12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width:900px; margin:auto;'>
            <div style='display:flex; align-items:center;'>
                <div style='flex-shrink:0;'>
                    <img src='data:image/jpeg;base64,""" + base64.b64encode(open("Headshot.jpeg", "rb").read()).decode() + """'  
                         width='180' style='border-radius:12px; margin-top:50px; margin-right:30px;  box-shadow: 2px 2px 8px rgba(0,0,0,0.1);' />
                </div>
                <div>
                    <h1 style='margin-bottom:5px; margin-left:5px; color:#004080;'>Maor Blumberg</h1>
                    <p style='line-height: 1.6; font-size: 36px;'>
                        <strong>📧 &nbsp;</strong><a href='mailto:maorblumberg@gmail.com'>maorblumberg@gmail.com</a><br>
                        <strong>📞 &nbsp;</strong><a href='tel:+972543276073'>+972 543276073</a><br>
                        <strong>🔗 &nbsp;</strong><a href='https://www.linkedin.com/in/maor-blumberg-9b5a43259/' target='_blank'>LinkedIn</a><br>
                        <strong>💻 &nbsp;</strong><a href='https://github.com/Maorb23' target='_blank'>Github</a>
                <div style='text-align:center; margin-top:30px; font-size:18px; color:#333;'>
            Welcome! Use the sidebar to explore topics and access my CV.<br>
            I specialize in personalized learning for Statistics, Probability and Machine Learning.
        </div>
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )
    # st.write("---")
    # st.markdown(
    #     """
    #     <div style='text-align:center; margin-top:30px; font-size:18px; color:#333;'>
    #         Welcome! Use the sidebar to explore topics and access my CV.<br>
    #         I specialize in personalized learning for Statistics, ML, and Data Science.
    #     </div>
    #     """, unsafe_allow_html=True
    # )


# --- Page: Videos ---
def render_videos():
    st.title("Tutorial Videos")
    categories = ["Statistics", "Probability", "Machine Learning"]

    # Featured Video Selection
    all_videos = []
    for cat in categories:
        all_videos.extend(list_videos(cat))
    if all_videos:
        st.subheader("Featured Video")
        featured_names = [os.path.basename(v) for v in all_videos]
        #choice_feat = st.selectbox("Select featured video:", featured_names)
        vid_path = next(v for v in all_videos if os.path.basename(v) == featured_names[0])
        st.video(vid_path)
    else:
        st.info("No videos found. Upload or add video files under the /videos folder.")

    st.markdown("---")
    st.subheader("Browse by Category")
    choice = st.radio("Select a category:", categories)
    vids = list_videos(choice)
    if vids:
        vid_names = [os.path.basename(v) for v in vids]
        selected = st.selectbox(f"Choose a video in '{choice}':", vid_names)
        vid_path = os.path.join("videos", choice.lower(), selected)
        st.video(vid_path)
    else:
        st.warning(
            f"No videos found in '{choice}'. Place your .mp4/.mov/.webm files in videos/{choice.lower()}."
        )

# --- Page: CV ---
def render_cv():
    st.title("Curriculum Vitae")
    # Inline PDF embed
    pdf_path = 'Maor_Blumberg CV_Updated_ds.pdf'
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" ' \
                        'width="100%" height="800px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        st.download_button(
            label="Download CV as PDF",
            data=open(pdf_path, 'rb'),
            file_name="CV.pdf",
            mime='application/pdf'
        )
    else:
        st.error("cv.pdf not found in the root directory.")

# --- Render Pages ---
if page == "Home":
    render_home()
elif page == "Videos":
    render_videos()
else:
    render_cv()
