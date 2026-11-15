from google import genai
from pypdf import PdfReader
import streamlit as st

# 1. Website Page Setup
st.set_page_config(
    page_title="Universal AI Hub Pro",
    page_icon="🚀",
    layout="centered",
)

# 2. API Key & Earning Settings
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

YOUR_WHATSAPP = "+92-340-1504999"  # Yahan apna WhatsApp number likhein
VIP_PASSCODE = "PRO2027"  # Ye code aap payment karne wale users ko dein ge

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False


# 3. AI Response Function (4-Model Auto-Fallback)
def get_ai_response(prompt_text):
    models_list = [
        "gemini-3.5-flash",
        "gemini-3.8-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-3.8-flash",
    ]
    for model_name in models_list:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
            )
            return response.text, model_name
        except Exception:
            continue
    return None, None


# 4. Sidebar: Language, Tools & VIP Unlock
st.sidebar.title("🚀 Universal AI Hub")

lang = st.sidebar.selectbox(
    "🌍 Select Language / Zuban:",
    ["English (Global)", "Roman Urdu + English"],
)

tool_choice = st.sidebar.radio(
    "🛠️ Choose AI Tool:",
    [
        "🛡️ Scam & Fraud Detector",
        "📄 CV & Cover Letter Maker",
        "✍️ Email & Application Writer",
        "🎓 Study & Concept Tutor",
        "📚 VIP: PDF Document Reader & Q&A",
        "💼 VIP: Fiverr/Upwork Proposal Writer",
        "🎬 VIP: YouTube & TikTok Script Maker",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("💎 Unlock Unlimited VIP Access")
if not st.session_state.is_vip:
    st.sidebar.write(
        f"Free Uses Left: **{max(0, 3 - st.session_state.usage_count)} / 3**"
    )
    entered_code = st.sidebar.text_input(
        "Enter VIP Passcode:", type="password"
    )
    if st.sidebar.button("Activate VIP 🔓"):
        if entered_code == VIP_PASSCODE:
            st.session_state.is_vip = True
            st.session_state.usage_count = 0
            st.sidebar.success("🎉 VIP Unlocked! Enjoy Unlimited Access.")
            st.rerun()
        else:
            st.sidebar.error("Invalid Code!")
    st.sidebar.info(
        f"💳 **Get VIP Code (Rs. 300/month):**\nSend payment via JazzCash/EasyPaisa & message on WhatsApp: **{YOUR_WHATSAPP}**"
    )
else:
    st.sidebar.success("✅ VIP Member Active (Unlimited)")

# 5. Main Interface
st.title(f"{tool_choice}")

lang_instruction = (
    "Respond strictly in clear, professional English."
    if lang == "English (Global)"
    else "Respond clearly in easy Roman Urdu along with English."
)

is_vip_tool = "VIP:" in tool_choice

if is_vip_tool and not st.session_state.is_vip:
    st.warning(
        "🔒 This is a **VIP Pro Tool**! Enter your VIP Passcode in the left sidebar to unlock it."
    )
elif not st.session_state.is_vip and st.session_state.usage_count >= 3:
    st.error(
        f"⏳ Your 3 free trials are complete! Contact WhatsApp **{YOUR_WHATSAPP}** to get your VIP Passcode for unlimited access."
    )
else:
    # Special Handling for PDF Tool
    if tool_choice == "📚 VIP: PDF Document Reader & Q&A":
        uploaded_pdf = st.file_uploader("Upload your PDF file:", type=["pdf"])
        pdf_question = st.text_input(
            "What do you want to know from this PDF? (e.g., Summarize it in 5 bullet points):"
        )

        if st.button("Analyze PDF ✨"):
            if uploaded_pdf is None:
                st.warning("Please upload a PDF file first!")
            else:
                with st.spinner("Reading PDF and generating answer..."):
                    reader = PdfReader(uploaded_pdf)
                    pdf_text = ""
                    for page in reader.pages[:10]:  # First 10 pages for speed
                        pdf_text += page.extract_text() or ""

                    user_question = (
                        pdf_question
                        if pdf_question.strip() != ""
                        else "Provide a complete, easy-to-understand summary of this document."
                    )
                    final_prompt = f"Analyze this document and answer the user's request. {lang_instruction}\n\nUser Request: {user_question}\n\nDocument Text:\n{pdf_text[:15000]}"

                    result, used_engine = get_ai_response(final_prompt)
                    if result:
                        st.success(f"Completed! (Engine: {used_engine})")
                        st.markdown(result)
                        st.download_button(
                            "📥 Download Summary (.txt)",
                            result,
                            "PDF_Summary.txt",
                        )
                    else:
                        st.error(
                            "Server is busy right now. Please try again in 5 seconds."
                        )
    else:
        user_input = st.text_area(
            "Enter your details, message, or topic below:", height=150
        )

        prompts = {
            "🛡️ Scam & Fraud Detector": f"You are a cybersecurity expert. Analyze this message/link for scams or phishing. Tell if it is SAFE or SCAM, why, and what the user should do. {lang_instruction} Message: {user_input}",
            "📄 CV & Cover Letter Maker": f"You are an expert HR recruiter. Write a high-converting Professional CV Summary and Cover Letter based on these details. {lang_instruction} Details: {user_input}",
            "✍️ Email & Application Writer": f"You are a professional communication specialist. Write a formal, clear, and effective email or application for this purpose. {lang_instruction} Purpose: {user_input}",
            "🎓 Study & Concept Tutor": f"You are an expert teacher. Explain this topic step-by-step with simple real-world examples. {lang_instruction} Topic: {user_input}",
            "💼 VIP: Fiverr/Upwork Proposal Writer": f"You are a top-rated freelancer. Write a winning, client-focused Fiverr/Upwork job proposal that gets replies. {lang_instruction} Job Details: {user_input}",
            "🎬 VIP: YouTube & TikTok Script Maker": f"You are a viral content creator. Write an engaging video script with a strong hook, main points, and call-to-action. {lang_instruction} Video Topic: {user_input}",
        }

        if st.button("Generate Now ✨"):
            if user_input.strip() == "":
                st.warning("Please enter something in the box first!")
            else:
                with st.spinner("AI is working on your request..."):
                    result, used_engine = get_ai_response(prompts[tool_choice])
                    if result:
                        if not st.session_state.is_vip:
                            st.session_state.usage_count += 1
                        st.success(f"Completed! (Engine: {used_engine})")
                        st.markdown(result)
                        st.download_button(
                            label="📥 Download Result (.txt)",
                            data=result,
                            file_name="AI_Pro_Result.txt",
                            mime="text/plain",
                        )
                    else:
                        st.error(
                            "Server is busy right now. Please try again in 5 seconds."
                        )
