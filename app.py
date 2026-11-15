import tempfile
from google import genai
from moviepy import ColorClip, CompositeVideoClip, TextClip
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(
    page_title="Universal AI Hub Pro", page_icon="🚀", layout="centered"
)
st.markdown(
    "<style>footer {visibility: hidden;} .stDeployButton {display:none;}</style>",
    unsafe_allow_html=True,
)

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# APNI DETAILS YAHAN LIKHEIN
YOUR_WHATSAPP = "923401504999"
ACCOUNT_TITLE = "ABDUR RAB"
EASYPAISA_NO = "0340-1504999"
JAZZCASH_NO = "0340-1504999"
MEEZAN_BANK = "26970115726042"
VIP_PRICE = "Rs. 300 / Month"

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


if st.session_state.user_email == "":
    st.title("🚀 Welcome to Universal AI Hub Pro")
    email_input = st.text_input("Enter your Email Address:")
    vip_code_input = st.text_input(
        "VIP Passcode (Optional):", type="password"
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

st.title("🚀 Universal AI Hub Pro")
col_u, col_l = st.columns()
with col_u:
    if st.session_state.is_vip:
        st.success(f"💎 VIP Active: **{st.session_state.user_email}**")
    else:
        st.info(
            f"👤 **{st.session_state.user_email}** | Free Left: **{max(0, 3 - st.session_state.usage_count)} / 3**"
        )
with col_l:
    if st.button("Logout 🚪"):
        st.session_state.user_email = ""
        st.session_state.is_vip = False
        st.rerun()

if not st.session_state.is_vip:
    with st.expander(
        "💎 Unlock VIP Access & Payment Wallets (Click Here)", expanded=True
    ):
        v1, v2 = st.columns(2)
        with v1:
            st.subheader("🔑 Enter VIP Code")
            q_code = st.text_input(
                "VIP Passcode:", type="password", key="vip_box"
            )
            if st.button("Activate VIP 🔓"):
                if (
                    st.session_state.user_email in VIP_USERS
                    and VIP_USERS[st.session_state.user_email] == q_code
                ):
                    st.session_state.is_vip = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Code!")
        with v2:
            st.subheader(f"💳 Wallets ({VIP_PRICE})")
            st.write(f"**Title:** {ACCOUNT_TITLE}")
            st.write(f"🟢 **EasyPaisa:** {EASYPAISA_NO}")
            st.write(f"🔴 **JazzCash:** {JAZZCASH_NO}")
            st.write(f"🏦 **Meezan:** {MEEZAN_BANK}")
            msg = f"Assalam-o-Alaikum! Maine {VIP_PRICE} payment kar di hai. Mera Email: {st.session_state.user_email}"
            st.link_button(
                "📲 Send Screenshot on WhatsApp",
                f"https://wa.me{YOUR_WHATSAPP}?text={msg.replace(' ', '%20')}",
            )

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    tool_choice = st.selectbox(
        "🛠️ Select Tool:",
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
        "🌍 Language:", ["English (Global)", "Roman Urdu + English"]
    )

st.subheader(tool_choice)
lang_inst = (
    "Respond strictly in clear English."
    if lang == "English (Global)"
    else "Respond in easy Roman Urdu and English."
)
is_vip = "VIP:" in tool_choice

if is_vip and not st.session_state.is_vip:
    st.warning("🔒 VIP Tool! Upar Payment Wallets se VIP code hasil karein.")
elif not st.session_state.is_vip and st.session_state.usage_count >= 3:
    st.error("⏳ Free trials khatam! Upar Wallets se VIP code hasil karein.")
else:
    if tool_choice == "🖼️ AI Image Vision & Analyzer":
        up_img = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
        img_q = st.text_input("Question about image:")
        if up_img:
            st.image(up_img, width=300)
        if st.button("Analyze Image 🔍"):
            if not up_img:
                st.warning("Upload image first!")
            else:
                with st.spinner("Analyzing..."):
                    q = (
                        img_q
                        if img_q.strip()
                        else "Describe this image in detail."
                    )
                    res, eng = get_ai_response(
                        f"{q} {lang_inst}", image_file=Image.open(up_img)
                    )
                    if res:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.markdown(res)
                        st.download_button(
                            "📥 Download", res, "Image_Result.txt"
                        )

    elif tool_choice == "🎬 VIP: AI Video Maker (.mp4)":
        v_topic = st.text_input("Video Topic:")
        if st.button("Create Video 🎥"):
            if not v_topic.strip():
                st.warning("Enter topic!")
            else:
                with st.spinner("Creating MP4 video..."):
                    res, eng = get_ai_response(
                        f"Write 5 short lines (max 10 words each, one per line, no numbers) for a video about: {v_topic}. {lang_inst}"
                    )
                    if res:
                        v_path = create_ai_video(res.strip().split("\n"))
                        if v_path:
                            st.video(v_path)
                            with open(v_path, "rb") as vf:
                                st.download_button(
                                    "📥 Download MP4",
                                    vf,
                                    "AI_Video.mp4",
                                    "video/mp4",
                                )

    elif tool_choice == "📚 VIP: PDF Document Reader":
        up_pdf = st.file_uploader("Upload PDF:", type=["pdf"])
        pdf_q = st.text_input("Question or Summary:")
        if st.button("Analyze PDF ✨"):
            if not up_pdf:
                st.warning("Upload PDF!")
            er. {lang_inst} Details: {u_in}",
            "✍️ Email & Application Writer": f"Write a formal email or application. {lang_inst} Purpose: {u_in}",
            "🎓 Study & Concept Tutor": f"Explain this topic simply. {lang_inst} Topic: {u_in}",
        }
        if st.button("Generate ✨"):
            if not u_in.strip():
                st.warning("Enter text first!")
            else:
                with st.spinner("Generating..."):
                    res, eng = get_ai_response(prompts[tool_choice])
                    if res:
                                         if res:
                     if not st.session_state.is_vip:
                         st.session_state.usage_count += 1
                     st.markdown(res)
                     st.download_button("📥 Download", res, "Result.txt")



        else:
        u_in = st.text_area("Enter text or topic:", height=150)
        prompts = {
            "🛡️ Scam & Fraud Detector": f"Check if SAFE or SCAM and explain why. {lang_inst} Message: {u_in}",
            "📄 CV & Cover Letter Maker": f"Write a CV Summary and Cover Letter. {lang_inst} Details: {u_in}",
            "✍️ Email & Application Writer": f"Write a formal email or application. {lang_inst} Purpose: {u_in}",
            "🎓 Study & Concept Tutor": f"Explain this topic simply. {lang_inst} Topic: {u_in}",
        }
        if st.button("Generate ✨"):
            if not u_in.strip():
                st.warning("Enter text first!")
            else:
                with st.spinner("Generating..."):
                    res, eng = get_ai_response(prompts[tool_choice])
                    if res:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.markdown(res)
                        st.download_button("📥 Download", res, "Result.txt")


