import os
import tempfile
import time
from google import genai
from google.genai import types
from gtts import gTTS
from moviepy import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip, TextClip
import numpy as np
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(page_title="Universal AI Studio Pro", page_icon="🚀")
st.markdown(
    "<style>footer{visibility:hidden}.stDeployButton{display:none}</style>",
    unsafe_allow_html=True,
)

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# APNI DETAILS YAHAN LIKHEIN
WA_NO = "923401504999"
TITLE = "ABDUR RAB"
EP_NO = "0340-1504999"
JC_NO = "0340-1504999"
BANK = "2697-0115726042"
PRICE = "Rs. 300/Month"

VIP_USERS = {
    "abdurrab2638@gmail.om": "ADMIN2026",
    "@gmail.com": "VIP101",
}

for k, v in [("email", ""), ("count", 0), ("vip", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


def ask_ai(prompt, img=None):
    models = ["gemini-3.5-flash", "gemini-3.8-flash-lite", "gemini-3.8-flash"]
    data = [prompt, img] if img else [prompt]
    for m in models:
        try:
            r = client.models.generate_content(model=m, contents=data)
            return r.text
        except Exception:
            continue
    return None


def build_pro_video(
    lines, user_images, aspect_ratio, quality, add_voice, lang_code
):
    # Video Size & Quality Setup
    if "TikTok" in aspect_ratio:
        w, h = (
            (1080, 1920)
            if "1080p" in quality
            else ((720, 1280) if "720p" in quality else (480, 854))
        )
    else:
        w, h = (
            (1920, 1080)
            if "1080p" in quality
            else ((1280, 720) if "720p" in quality else (854, 480))
        )

    clips = []
    full_script = ""
    current_time = 0

    for i, line in enumerate(lines[:5]):
        txt_str = line.strip()[:110]
        if not txt_str:
            continue
        full_script += txt_str + ". "
        dur = 4

        # Agar user ne images upload ki hain toh unhein background mein lagayein
        if user_images and len(user_images) > 0:
            pil_im = Image.open(user_images[i % len(user_images)]).convert(
                "RGB"
            )
            pil_im = pil_im.resize((w, h))
            bg = ImageClip(np.array(pil_im)).with_duration(dur)
        else:
            colors = [(15, 23, 42), (30, 27, 75), (20, 40, 60), (45, 20, 50)]
            bg = ColorClip(
                size=(w, h), color=colors[i % len(colors)], duration=dur
            )

        font_sz = int(w * 0.045)
        tc = TextClip(
            text=txt_str,
            font_size=font_sz,
            color="white",
            bg_color="black",
            size=(int(w * 0.85), None),
            method="caption",
        )
        tc = tc.with_position(("center", int(h * 0.72))).with_duration(dur)

        scene = CompositeVideoClip([bg, tc]).with_start(current_time)
        clips.append(scene)
        current_time += dur

    if not clips:
        return None

    final_vid = CompositeVideoClip(clips)

    # AI Voice-Over Add Karna
    audio_path = None
    if add_voice and full_script.strip():
        try:
            tts = gTTS(text=full_script, lang=lang_code, slow=False)
            af = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(af.name)
            audio_path = af.name
            aclip = AudioFileClip(audio_path)
            if aclip.duration > final_vid.duration:
                final_vid = final_vid.with_duration(aclip.duration)
            final_vid = final_vid.with_audio(aclip)
        except Exception:
            pass

    out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    final_vid.write_videofile(
        out_file.name,
        fps=24,
        codec="libx264",
        audio_codec="aac" if audio_path else None,
        logger=None,
    )
    return out_file.name


if st.session_state.email == "":
    st.title("🚀 Universal AI Studio Pro")
    em = st.text_input("Enter Email:")
    cd = st.text_input("VIP Code (Optional):", type="password")
    if st.button("Login / Start ✨"):
        em = em.strip().lower()
        if "@" not in em or "." not in em:
            st.error("Valid email likhein!")
        else:
            st.session_state.email = em
            if em in VIP_USERS and VIP_USERS[em] == cd:
                st.session_state.vip = True
            st.rerun()
    st.stop()

st.title("🚀 Universal AI Studio Pro")
c_u, c_l = st.columns()
with c_u:
    if st.session_state.vip:
        st.success(f"💎 VIP: {st.session_state.email}")
    else:
        left = max(0, 3 - st.session_state.count)
        st.info(f"👤 {st.session_state.email} | Free Left: {left}/3")
with c_l:
    if st.button("Logout"):
        st.session_state.email = ""
        st.session_state.vip = False
        st.rerun()

if not st.session_state.vip:
    with st.expander("💎 Unlock VIP & Payment Wallets", expanded=True):
        w1, w2 = st.columns(2)
        with w1:
            qc = st.text_input("Enter VIP Code:", type="password")
            if st.button("Activate VIP 🔓"):
                em = st.session_state.email
                if em in VIP_USERS and VIP_USERS[em] == qc:
                    st.session_state.vip = True
                    st.rerun()
                else:
                    st.error("Invalid Code!")
        with w2:
            st.write(f"**Title:** {TITLE}")
            st.write(f"🟢 **EasyPaisa:** {EP_NO}")
            st.write(f"🔴 **JazzCash:** {JC_NO}")
            st.write(f"🏦 **Meezan:** {BANK}")
            msg = f"Paid {PRICE} for Email: {st.session_state.email}"
            url = f"https://wa.me{WA_NO}?text={msg.replace(' ', '%20')}"
            st.link_button("📲 Send Screenshot", url)

st.markdown("---")
t1, t2 = st.columns(2)
with t1:
    tool = st.selectbox(
        "🛠️ Select Tool:",
        [
            "🎬 VIP: Pro AI Video Studio",
            "🛡️ Scam Detector",
            "🖼️ Image Analyzer",
            "📄 CV & Cover Letter",
            "✍️ Email Writer",
            "🎓 Study Tutor",
            "📚 VIP: PDF Reader",
        ],
    )
with t2:
    lang = st.selectbox("🌍 Language:", ["English", "Roman Urdu + English"])

st.subheader(tool)
l_inst = (
    "Reply in clear English."
    if lang == "English"
    else "Reply in easy Roman Urdu and English."
)

if "VIP:" in tool and not st.session_state.vip:
    st.warning("🔒 VIP Tool! Upar Wallets se VIP code hasil karein.")
elif not st.session_state.vip and st.session_state.count >= 3:
    st.error("⏳ Free limit khatam! Upar Wallets se VIP code lein.")
else:
    if tool == "🎬 VIP: Pro AI Video Studio":
        st.write(
            "YouTube ya TikTok ke liye Voice-Over, Custom Images, Title aur Description ke saath full video banayein!"
        )
        v_topic = st.text_input("1. Video Topic / Idea likhein:")

        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            v_size = st.selectbox(
                "2. Video Size:",
                ["TikTok / Shorts (9:16)", "YouTube Video (16:9)"],
            )
        with vc2:
            v_qual = st.selectbox(
                "3. Video Quality:",
                ["720p HD", "1080p Full HD", "480p Fast"],
            )
        with vc3:
            v_voice = st.selectbox(
                "4. AI Voice-Over:", ["Yes (English Voice)", "No Voice"]
            )

        up_imgs = st.file_uploader(
            "5. Apni Tasveerein Upload Karein (Optional - Max 5 Images):",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
        )

        if st.button("🎬 Generate Complete Video & SEO ✨"):
            if not v_topic.strip():
                st.warning("Pehle Video Topic likhein!")
            else:
                with st.spinner(
                    "AI Video, Voice-Over, Title aur Description tayyar kar raha hai..."
                ):
                    # Step A: Pehle Google Veo Model Try Karein (Agar API key par Veo enabled ho)
                    veo_done = False
                    try:
                        op = client.models.generate_videos(
                            model="veo-2.0-generate-001",
                            prompt=v_topic,
                            config=types.GenerateVideosConfig(
                                aspect_ratio="9:16"
                                if "TikTok" in v_size
                                else "16:9"
                            ),
                        )
                        while not op.done:
                            time.sleep(5)
                            op = client.operations.get(op)
                        if op.response and op.response.generated_videos:
                            vid_obj = op.response.generated_videos
                            client.files.download(file=vid_obj.video)
                            vf_path = tempfile.NamedTemporaryFile(
                                delete=False, suffix=".mp4"
                            ).name
                            vid_obj.video.save(vf_path)
                            st.success("🎉 Cinematic Veo AI Video Tayyar Hai!")
                            st.video(vf_path)
                            with open(vf_path, "rb") as f:
                                st.download_button(
                                    "📥 Download Veo MP4",
                                    f,
                                    "Veo_AI_Video.mp4",
                                    "video/mp4",
                                )
                            veo_done = True
                    except Exception:
                        veo_done = False

                    # Step B: Script + Title + Description + Tags Generate Karein
                    seo_prompt = f"""
                    Create a video package for topic: {v_topic}. {l_inst}
                    Format strictly like this:
                    SCRIPT:
                    res = ask_ai(seo_prompt)
if res:
parts = res.split("SEO:")
script_part = (
parts.replace("SCRIPT:", "").strip()
)
seo_part = parts[1].strip() if len(parts) > 1 else ""
# Agar Veo free tier par available nahi tha toh Custom Image + Voice Studio video banayein
if not veo_done:
add_v = "Yes" in v_voice
vp = build_pro_video(
script_part.split("\n"),
up_imgs,
v_size,
v_qual,
add_v,
"en",
)
if vp:
st.success(
f"🎉 Aapki {v_size} ({v_qual}) Video Tayyar Hai!"
)
st.video(vp)
with open(vp, "rb") as vf:
st.download_button(
"📥 Download MP4 Video",
vf,
"AI_Studio_Video.mp4",
"video/mp4",
)
if seo_part:
st.subheader("📝 Viral Title, Description & Tags")
st.markdown(seo_part)
st.download_button(
"📥 Download Title & Description",
seo_part,
"Video_SEO.txt",
)
elif tool == "🖼️ Image Analyzer":
img = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
iq = st.text_input("Question:")
if img:
st.image(img, width=250)
if st.button("Analyze 🔍") and img:
with st.spinner("Working..."):
q = iq if iq.strip() else "Describe this image."
res = ask_ai(f"{q} {l_inst}", Image.open(img))
if res:
st.session_state.count += 1
st.markdown(res)
st.download_button("📥 Download", res, "Image.txt")
elif tool == "📚 VIP: PDF Reader":
pdf = st.file_uploader("Upload PDF:", type=["pdf"])
pq = st.text_input("Question:")
if st.button("Read PDF ✨") and pdf:
with st.spinner("Reading..."):
rdr = PdfReader(pdf)
txt = "".join([p.extract_text() or "" for p in rdr.pages[:8]])
q = pq if pq.strip() else "Summarize this PDF."
res = ask_ai(f"{q} {l_inst}\n\n{txt[:12000]}")
if res:
st.markdown(res)
st.download_button("📥 Download", res, "PDF.txt")
else:
uin = st.text_area("Enter text:", height=130)
if st.button("Generate ✨") and uin.strip():
with st.spinner("Generating..."):
p = f"Task: {tool}. {l_inst} Input: {uin}"
res = ask_ai(p)
if res:
st.session_state.count += 1
st.markdown(res)
st.download_button("📥 Download", res, "Result.txt")
