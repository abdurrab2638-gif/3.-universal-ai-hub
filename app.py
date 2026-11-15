import os
import tempfile
from google import genai
from moviepy import ColorClip, CompositeVideoClip, TextClip
from PIL import Image
from pypdf import PdfReader
import streamlit as st

# 1. Page Setup
st.set_page_config(
    page_title="Universal AI Hub Pro",
    page_icon="🚀",
    layout="centered",
)

# 2. GitHub Icon aur Streamlit Menu Chupane ka Code (Security)
hide_github_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_github_css, unsafe_allow_html=True)

# 3. API & VIP Security Settings
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

YOUR_WHATSAPP = "+92-3401504999"  # Apna WhatsApp number yahan likhein

# Har VIP User ka apna Email aur alag Passcode (taake koi code share na kar sake)
VIP_USERS = {
    "admin@gmail.com": "ADMIN2026",
    "ali@gmail.com": "VIP101",
    "sara@gmail.com": "VIP102",
}

if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False


# 4. AI Response Engine (Text & Image Support ke Saath)
def get_ai_response(prompt_text, image_file=None):
    models_list = [
        "gemini-3.5-flash",
        "gemini-3.8-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-3.8-flash",
    ]
    contents_data = [prompt_text]
    if image_file is not None:
        contents_data.append(image_file)

    for model_name in models_list:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents_data,
            )
            return response.text, model_name
        except Exception:
            continue
    return None, None


# 5. Simple MP4 Video Generator Function
def create_ai_video(script_lines):
    clips = []
    for line in script_lines[:5]:  # Max 5 slides (15 seconds video)
        clean_line = line.strip()[:120]
        if not clean_line:
            continue
        bg = ColorClip(size=(720, 1280), color=(20, 25, 45), duration=3)
        txt = TextClip(
            text=clean_line,
            font_size=42,
            color="white",
            size=(620, None),
            method="caption",
        ).with_position("center").with_duration(3)
        clips.append(CompositeVideoClip([bg, txt]))

    if not clips:
        return None

    final_video = CompositeVideoClip(
        [clip.with_start(i * 3) for i, clip in enumerate(clips)]
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    final_video.write_videofile(
        temp_file.name, fps=24, codec="libx264", audio=False, logger=None
    )
    return temp_file.name


# 6. Email Login Screen (Pehle Login Zaroori Hai)
if st.session_state.user_email == "":
    st.title("🚀 Welcome to Universal AI Hub Pro")
    st.write("Apne Email se login karein aur AI Tools istemal karein:")
    email_input = st.text_input("Enter your Email Address:")
    vip_code_input = st.text_input(
        "VIP Passcode (Optional - Free users khali chhor dein):",
        type="password",
    )

    if st.button("Login / Start Free ✨"):
        clean_email = email_input.strip().lower()
        if "@" not in clean_email or "." not in clean_email:
            st.error("Please enter a valid email address!")
        else:
            st.session_state.user_email = clean_email
            if (
                clean_email in VIP_USERS
                and VIP_USERS[clean_email] == vip_code_input
            ):
                st.session_state.is_vip = True
            st.rerun()
    st.stop()

# 7. Logged-In Sidebar
st.sidebar.title("🚀 Universal AI Hub")
st.sidebar.write(f"👤 Logged in: **{st.session_state.user_email}**")

if st.session_state.is_vip:
    st.sidebar.success("💎 VIP Member (Unlimited Access)")
else:
    st.sidebar.warning(
        f"Free Uses Left: **{max(0, 3 - st.session_state.usage_count)} / 3**"
    )
    st.sidebar.info(
        f"VIP Code kharidne ke liye apna Email WhatsApp karein: **{YOUR_WHATSAPP}**"
    )

if st.sidebar.button("Logout 🚪"):
    st.session_state.user_email = ""
    st.session_state.is_vip = False
    st.rerun()

st.sidebar.markdown("---")
lang = st.sidebar.selectbox(
    "🌍 Language:", ["English (Global)", "Roman Urdu + English"]
)

tool_choice = st.sidebar.radio(
    "🛠️ Choose Tool:",
    [
        "🛡️ Scam & Fraud Detector",
        "🖼️ AI Image Vision & Analyzer",
        "📄 CV & Cover Letter Maker",
        "✍️ Email & Application Writer",
        "🎓 Study & Concept Tutor",
        "📚 VIP: PDF Document Reader",
        "🎬 VIP: AI Video Maker (.mp4)",
    ],
)

# 8. Main Workspace
st.title(f"{tool_choice}")
lang_instruction = (
    "Respond strictly in clear English."
    if lang == "English (Global)"
    else "Respond clearly in easy Roman Urdu and English."
)

is_vip_tool = "VIP:" in tool_choice

if is_vip_tool and not st.session_state.is_vip:
    st.warning(
        f"🔒 Ye VIP Tool hai! Apna Email ({st.session_state.user_email}) WhatsApp **{YOUR_WHATSAPP}** par bhej kar apna personal VIP code hasil karein."
    )
elif not st.session_state.is_vip and st.session_state.usage_count >= 3:
    st.error(
        f"⏳ Aapke 3 free trials khatam ho gaye hain! Unlimited access ke liye WhatsApp **{YOUR_WHATSAPP}** par rabta karein."
    )
else:
    # TOOL: Image Analyzer
    if tool_choice == "🖼️ AI Image Vision & Analyzer":
        uploaded_img = st.file_uploader(
            "Koi bhi Image / Photo / Notes upload karein:",
            type=["png", "jpg", "jpeg"],
        )
        img_question = st.text_input(
            "Is tasveer ke baray mein kya jaanna chahte hain?"
        )
        if uploaded_img:
            st.image(uploaded_img, width=300)
        if st.button("Analyze Image 🔍"):
            if not uploaded_img:
                st.warning("Pehle koi tasveer upload karein!")
            else:
                with st.spinner("AI tasveer dekh kar samajh raha hai..."):
                    pil_img = Image.open(uploaded_img)
                    q = (
                        img_question
                        if img_question.strip()
                        else "Describe this image in detail and extract any text written in it."
                    )
                    res, eng = get_ai_response(
                        f"{q} {lang_instruction}", image_file=pil_img
                    )
                    if res:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.success(f"Done! ({eng})")
                        st.markdown(res)
                        st.download_button(
                            "📥 Download Result", res, "Image_Analysis.txt"
                        )

    # TOOL: AI Video Maker (.mp4)
    elif tool_choice == "🎬 VIP: AI Video Maker (.mp4)":
        video_topic = st.text_input(
            "Kis topic par short video banani hai? (e.g., 3 Tips for Success):"
        )
        if st.button("Create & Render Video 🎥"):
            if not video_topic.strip():
                st.warning("Topic likhein!")
            else:
                with st.spinner(
                    "AI script likh raha hai aur MP4 video bana raha hai (15-20 sec)..."
                ):
                    prompt = f"Write exactly 5 short, powerful punchlines (max 12 words each, one per line, no numbering) for a viral short video about: {video_topic}. {lang_instruction}"
                    res, eng = get_ai_response(prompt)
                    if res:
                        lines = res.strip().split("\n")
                        video_path = create_ai_video(lines)
                        if video_path:
                            st.success("🎉 Aapki Video Tayyar Hai!")
                            st.video(video_path)
                            with open(video_path, "rb") as v_file:
                                st.download_button(
                                    label="📥 Download MP4 Video",
                                    data=v_file,
                                    file_name="AI_Short_Video.mp4",
                                    mime="video/mp4",
                                )

    # TOOL: PDF Reader
    elif tool_choice == "📚 VIP: PDF Document Reader":
        uploaded_pdf = st.file_uploader("Upload PDF file:", type=["pdf"])
        pdf_q = st.text_input("PDF se kya poochna ya summarize karna hai?")
        if st.button("Analyze PDF ✨"):
            if not uploaded_pdf:
                st.warning("Upload a PDF first!")
            else:
                with st.spinner("Reading PDF..."):
                    reader = PdfReader(uploaded_pdf)
                    text = "".join(
                        [p.extract_text() or "" for p in reader.pages[:10]]
                    )
                    q = (
                        pdf_q
                        if pdf_q.strip()
                        else "Summarize this document clearly."
                    )
                    res, eng = get_ai_response(
                        f"{q} {lang_instruction}\n\nText:\n{text[:15000]}"
                    )
                    if res:
                        st.success(f"Done! ({eng})")
                        st.markdown(res)
                        st.download_button(
                            "📥 Download Summary", res, "PDF_Summary.txt"
                        )

    # OTHER TEXT TOOLS
    else:
        user_input = st.text_area("Enter your text or topic:", height=150)
        prompts = {
            "🛡️ Scam & Fraud Detector": f"Check if this message/link is SAFE or SCAM, explain why, and advise the user. {lang_instruction} Message: {user_input}",
