import tempfile
from google import genai
from moviepy import ColorClip, CompositeVideoClip, TextClip
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(
    page_title="Universal AI Hub Pro", page_icon="🚀", layout="centered"
)

# Footer aur Deploy button chupayein
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

# ==========================================
# APNI PAYMENT & WHATSAPP DETAILS YAHAN LIKHEIN
# ==========================================
YOUR_WHATSAPP = "923401504999"  # Bina '+' ke likhein (e.g., 923001234567)
ACCOUNT_TITLE = "ABDUR RAB"  # Apna Account Title likhein
EASYPAISA_NO = "0340-1504999"
JAZZCASH_NO = "0340-1504999"
MEEZAN_BANK = "2697-0115726042 (Meezan Bank)"
VIP_PRICE = "Rs. 300 / Month"

# Har VIP Customer ka Email aur uska Personal Code
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
    st.write("Apne Email se login karein aur AI Tools istemal karein:")
    email_input = st.text_input("Enter your Email Address:")
    vip_code_input = st.text_input(
        "VIP Passcode (Agar aapke paas code hai toh yahan likhein):",
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

# 2. Top Status Bar & Direct VIP Unlock Box (Bilkul Samne Screen Par)
st.title("🚀 Universal AI Hub Pro")

col_user, col_logout = st.columns()
with col_user:
    if st.session_state.is_vip:
        st.success(f"💎 VIP Active: **{st.session_state.user_email}**")
    else:
        st.info(
            f"👤 **{st.session_state.user_email}** | Free Trials Left: **{max(0, 3 - st.session_state.usage_count)} / 3**"
        )
with col_logout:
    if st.button("Logout 🚪"):
        st.session_state.user_email = ""
        st.session_state.is_vip = False
        st.rerun()

# Agar user abhi VIP nahi hai toh samne VIP Unlock aur Wallets ka Box dikhayein
if not st.session_state.is_vip:
    with st.expander(
        "💎 Unlock Unlimited VIP Access & Payment Wallets (Click Here)",
        expanded=True,
    ):
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.subheader("🔑 Enter VIP Code")
            quick_code = st.text_input(
                "Apna VIP Passcode yahan dalein:",
                type="password",
                key="main_vip_box",
            )
            if st.button("Activate VIP Now 🔓"):
                if (
                    st.session_state.user_email in VIP_USERS
                    and VIP_USERS[st.session_state.user_email] == quick_code
                ):
                    st.session_state.is_vip = True
                    st.success("🎉 VIP Unlocked! Enjoy Unlimited Access.")
                    st.rerun()
                else:
                    st.error(
                        "❌ Galat Code! Apne email ke liye code hasil karne ke liye neeche payment karein."
                    )

        with v_col2:
            st.subheader(f"💳 Payment Wallets ({VIP_PRICE})")
            st.markdown(f"""
            **Account Title:** `{ACCOUNT_TITLE}`  
            🟢 **EasyPaisa:** `{EASYPAISA_NO}`  
            🔴 **JazzCash:** `{JAZZCASH_NO}`  
            🏦 **Meezan Bank:** `{MEEZAN_BANK}`  
            """)
            whatsapp_msg = f"Assalam-o-Alaikum! Maine {VIP_PRICE} payment kar di hai. Mera Email: {st.session_state.user_email} hai, please mujhe VIP Code de dein."
            wa_link = f"https://wa.me{YOUR_WHATSAPP}?text={whatsapp_msg.replace(' ', '%20')}"
            st.link_button("📲 Send Screenshot on WhatsApp", wa_link)

st.markdown("---")

# 3. Main Tool & Language Selector
c1, c2 = st.columns(2)
with c1:
    tool_choice = st.selectbox(
        "🛠️ Select AI Tool:",
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

st.subheader(f"{tool_choice}")
lang_instruction = (
    "Respond strictly in clear English."
    if lang == "English (Global)"
    else "Respond in easy Roman Urdu and English."
)
is_vip_tool = "VIP:" in tool_choice

if is_vip_tool and not st.session_state.is_vip:
    st.warning(
        "🔒 Ye **VIP Tool** hai! Upar diye gaye **Payment Wallets** par payment karke apna VIP code hasil karein aur box mein daal kar unlock karein."
    )
elif not st.session_state.is_vip and st.session_state.usage_count >= 3:
    st.error(
        "⏳ Aapke 3 free trials mukammal ho gaye hain! Upar **Payment Wallets** ke zariye VIP code hasil karein."
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
