import tempfile
from google import genai
from moviepy import ColorClip, CompositeVideoClip, TextClip
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(page_title="Universal AI Hub", page_icon="🚀")
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
    "abdurrab2638@gmail.com": "ADMIN2026",
    "..@gmail.com": "VIP101",
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


def make_video(lines):
    clips = []
    for l in lines[:5]:
        txt_str = l.strip()[:100]
        if not txt_str:
            continue
        bg = ColorClip(size=(720, 1280), color=(20, 25, 45), duration=3)
        tc = TextClip(
            text=txt_str,
            font_size=40,
            color="white",
            size=(600, None),
            method="caption",
        )
        tc = tc.with_position("center").with_duration(3)
        clips.append(CompositeVideoClip([bg, tc]))
    if not clips:
        return None
    vid = CompositeVideoClip([c.with_start(i * 3) for i, c in enumerate(clips)])
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    vid.write_videofile(
        f.name, fps=24, codec="libx264", audio=False, logger=None
    )
    return f.name


if st.session_state.email == "":
    st.title("🚀 Universal AI Hub Pro")
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

st.title("🚀 Universal AI Hub Pro")
c_u, c_l = st.columns([3, 1])
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
            "🛡️ Scam Detector",
            "🖼️ Image Analyzer",
            "📄 CV & Cover Letter",
            "✍️ Email Writer",
            "🎓 Study Tutor",
            "📚 VIP: PDF Reader",
            "🎬 VIP: Video Maker",
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
    if tool == "🖼️ Image Analyzer":
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

    elif tool == "🎬 VIP: Video Maker":
        vt = st.text_input("Video Topic:")
        if st.button("Create Video 🎥") and vt.strip():
            with st.spinner("Making MP4..."):
                p = f"Write 5 short lines (max 8 words each, no numbers) about: {vt}. {l_inst}"
                res = ask_ai(p)
                if res:
                    vp = make_video(res.split("\n"))
                    if vp:
                        st.video(vp)
                        with open(vp, "rb") as vf:
                            st.download_button(
                                "📥 Download MP4", vf, "Video.mp4"
                            )

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
