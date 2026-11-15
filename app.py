import tempfile
from google import genai
from moviepy import ColorClip, CompositeVideoClip, TextClip
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(
    page_title="Universal AI Hub Pro", page_icon="🚀", layout="centered"
)

# Sirf footer aur deploy button chupayein (Menu ko chupane se sidebar gayab ho jata hai)
st.markdown(
    """
<style>
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""",
    unsafe_allow_html=True,
)

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)
YOUR_WHATSAPP = "+92-3401504999"  # Yahan apna WhatsApp number likhein

VIP_USERS = {
    "admin@gmail.com": "ADMIN2026",
    "ali@gmail.com": "VIP101",
}

if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False


def get_ai_response(prompt_text, image_file=None):
    models_list = [
        "gemini-3.5-flash",
        "gemini-3.8-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-3.8-flash",
    ]
    contents_data = (
        [prompt_text, image_file] if image_file is not None else [prompt_text]
    )
    for model_name in models_list:
        try:
            response = client.models.generate_content(
                model=model_name, contents=contents_data
            )
            return response.text, model_name
        except Exception:
            continue
    return None, None


def create_ai_video(script_lines):
    clips = []
    for line in script_lines[:5]:
        clean_line = line.strip()[:120]
        if not clean_line:
            continue
        bg = ColorClip(size=(720, 1280), color=(20, 25, 45), duration=3)
        txt = (
            TextClip(
                text=clean_line,
                font_size=42,
                color="white",
                size=(620, None),
                method="caption",
            )
            .with_position("center")
            .with_duration(3)
        )
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


# 1. Email Login Screen
if st.session_state.user_email == "":
    st.title("🚀 Welcome to Universal AI Hub Pro")
    st.write("Apne Email se login karein aur saare AI Tools istemal karein:")
    email_input = st.text_input("Enter your Email Address:")
    vip_code_input = st.text_input(
        "VIP Passcode (Optional - Free users khali chhor dein):",
        type="password",
    )
    if st.button("Login / Start Free ✨"):
        clean_email = email_input.strip().lower()
        if "@" not in clean_email or "." not in clean_email:
            st.error("Please enter a valid email!")
        else:
            st.session_state.user_email = clean_email
            if (
                clean_email in VIP_USERS
                and VIP_USERS[clean_email] == vip_code_input
            ):
                st.session_state.is_vip = True
            st.rerun()
    st.stop()

# 2. Top Header Bar (Har mobile aur laptop par saaf nazar aayega)
st.title("🚀 Universal AI Hub Pro")
col1, col2 = st.columns([3, 1])
with col1:
    if st.session_state.is_vip:
        st.success(f"💎 VIP Active: {st.session_state.user_email}")
    else:
        st.info(
            f"👤 {st.session_state.user_email} | Free Uses Left: {max(0, 3 - st.session_state.usage_count)} / 3"
        )
with col2:
    if st.button("Logout 🚪"):
        st.session_state.user_email = ""
        st.session_state.is_vip = False
        st.rerun()

# 3. Main Page Tool & Language Selector (Ab koi cheez nahi chupegi!)
c1, c2 = st.columns(2)
with c1:
    tool_choice = st.selectbox(
        "🛠️ Select AI Tool (Yahan se Tool Chunein):",
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
with c2:
    lang = st.selectbox(
        "🌍 Select Language:",
        ["English (Global)", "Roman Urdu + English"],
    )

st.markdown("---")
st.subheader(f"{tool_choice}")

lang_instruction = (
    "Respond strictly in clear English."
    if lang == "English (Global)"
    else "Respond in easy Roman Urdu and English."
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
    if tool_choice == "🖼️ AI Image Vision & Analyzer":
        uploaded_img = st.file_uploader(
            "Upload Image:", type=["png", "jpg", "jpeg"]
        )
        img_q = st.text_input("Question about this image:")
        if uploaded_img:
            st.image(uploaded_img, width=300)
        if st.button("Analyze Image 🔍"):
            if not uploaded_img:
                st.warning("Upload an image first!")
            else:
                with st.spinner("Analyzing..."):
                    pil_img = Image.open(uploaded_img)
                    q = (
                        img_q
                        if img_q.strip()
                        else "Describe this image in detail."
                    )
                    res, eng = get_ai_response(
                        f"{q} {lang_instruction}", image_file=pil_img
                    )
                    if res:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.markdown(res)
                        st.download_button(
                            "📥 Download", res, "Image_Result.txt"
                        )

    elif tool_choice == "🎬 VIP: AI Video Maker (.mp4)":
        video_topic = st.text_input("Video Topic:")
        if st.button("Create Video 🎥"):
            if not video_topic.strip():
                st.warning("Enter topic!")
            else:
                with st.spinner("Creating MP4 video..."):
                    prompt = f"Write 5 short lines (max 10 words each, one per line, no numbers) for a video about: {video_topic}. {lang_instruction}"
                    res, eng = get_ai_response(prompt)
                    if res:
                        video_path = create_ai_video(res.strip().split("\n"))
                        if video_path:
                            st.video(video_path)
                            with open(video_path, "rb") as vf:
                                st.download_button(
                                    "📥 Download MP4",
                                    vf,
                                    "AI_Video.mp4",
                                    "video/mp4",
                                )

    elif tool_choice == "📚 VIP: PDF Document Reader":
        uploaded_pdf = st.file_uploader("Upload PDF:", type=["pdf"])
        pdf_q = st.text_input("Question or Summary:")
        if st.button("Analyze PDF ✨"):
            if not uploaded_pdf:
                st.warning("Upload PDF!")
            else:
                with st.spinner("Reading PDF..."):
                    reader = PdfReader(uploaded_pdf)
                    text = "".join(
                        [p.extract_text() or "" for p in reader.pages[:10]]
                    )
                    q = pdf_q if pdf_q.strip() else "Summarize this document."
                    res, eng = get_ai_response(
                        f"{q} {lang_instruction}\n\n{text[:15000]}"
                    )
                    if res:
                        st.markdown(res)
                        st.download_button(
                            "📥 Download", res, "PDF_Summary.txt"
                        )

    else:
        user_input = st.text_area("Enter text or topic:", height=150)
        prompts = {
            "🛡️ Scam & Fraud Detector": f"Check if SAFE or SCAM and explain why. {lang_instruction} Message: {user_input}",
            "📄 CV & Cover Letter Maker": f"Write a CV Summary and Cover Letter. {lang_instruction} Details: {user_input}",
            "✍️ Email & Application Writer": f"Write a formal email or application. {lang_instruction} Purpose: {user_input}",
            "🎓 Study & Concept Tutor": f"Explain this topic simply. {lang_instruction} Topic: {user_input}",
        }
        if st.button("Generate ✨"):
            if not user_input.strip():
                st.warning("Enter text first!")
            else:
                with st.spinner("Generating..."):
                    res, eng = get_ai_response(prompts[tool_choice])
                    if res:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.markdown(res)
                        st.download_button("📥 Download", res, "Result.txt")
