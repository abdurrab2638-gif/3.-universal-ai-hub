import os
from google import genai
import streamlit as st

# 1. Website Page Setup
st.set_page_config(
    page_title="Universal AI Hub",
    page_icon="🚀",
    layout="centered",
)

# 2. API Key Setup (Laptop aur Internet dono par chalne wala safe system)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = "YAHAN_APNI_ASAL_API_KEY_PASTE_KAREIN"

client = genai.Client(api_key=API_KEY)


# 3. AI Response Function (4-Model Auto-Fallback ke saath)
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


# 4. Sidebar Menu (Universal Tools Selection)
st.sidebar.title("🚀 Universal AI Tools")
st.sidebar.write("Apni pasand ka AI tool chunein:")
tool_choice = st.sidebar.radio(
    "Select Tool:",
    [
        "🛡️ Scam & Fraud Detector",
        "📄 CV & Cover Letter Maker",
        "✍️ Email & Application Writer",
        "🎓 Easy Study & Concept Tutor",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tip: Har jawab ko neeche diye gaye button se download bhi kiya ja sakta hai."
)

# 5. Main Screen Interface
st.title(f"{tool_choice}")

if tool_choice == "🛡️ Scam & Fraud Detector":
    st.write(
        "Koi bhi mashkook message, email, ya link paste karein aur check karein ke ye Safe hai ya Fraud."
    )
    user_input = st.text_area("Message yahan paste karein:", height=150)
    final_prompt = f"""
    Tum ek expert cybersecurity aur scam detector AI ho. Neeche diye gaye message ko check karo aur aasan Roman Urdu aur English mein batao:
    1. Kya ye message SAFE hai ya SCAM/FRAUD?
    2. Wajah kya hai?
    3. User ko ab kya karna chahiye?
    Message: {user_input}
    """

elif tool_choice == "📄 CV & Cover Letter Maker":
    st.write(
        "Apni details likhein aur aik professional Job CV summary aur Cover Letter tayyar karein."
    )
    user_input = st.text_area(
        "Apna naam, taleem (education), skills, aur kis job ke liye apply kar rahe hain likhein:",
        height=150,
    )
    final_prompt = f"""
    Tum ek professional HR aur Career Expert ho. Neeche di gayi details ki bunyad par English mein aik zabardast Professional CV Summary aur aik impressive Cover Letter likho:
    Details: {user_input}
    """

elif tool_choice == "✍️ Email & Application Writer":
    st.write(
        "School, college, office, ya freelancing client ke liye fori professional email ya darkhwast likhwayein."
    )
    user_input = st.text_area(
        "Kis maqsad ke liye email ya application likhni hai? (Mukhtasir details likhein):",
        height=150,
    )
    final_prompt = f"""
    Tum ek expert communication writer ho. Neeche diye gaye maqsad ke liye aik professional, saaf aur asar-dar Email / Application likho:
    Maqsad: {user_input}
    """

elif tool_choice == "🎓 Easy Study & Concept Tutor":
    st.write(
        "Koi bhi mushkil sawal, coding concept, ya topic likhein—AI aasan misalon ke saath samjhayega."
    )
    user_input = st.text_area(
        "Apna sawal ya topic yahan likhein:", height=150
    )
    final_prompt = f"""
    Tum ek behtareen ustaad (Teacher) ho. Neeche diye gaye topic ko aasan Roman Urdu aur English mein step-by-step aur rozmarra ki misalon ke saath samjhao:
    Topic: {user_input}
    """

# 6. Action Button & Result
if st.button("Generate Karein ✨"):
    if user_input.strip() == "":
        st.warning("Pehle neeche wale box mein kuch likhein!")
    else:
        with st.spinner("AI aapke liye kaam kar raha hai..."):
            result, used_engine = get_ai_response(final_prompt)
            if result:
                st.success(f"Kaam Mukammal! (Engine: {used_engine})")
                st.markdown(result)
                st.download_button(
                    label="📥 Jawab Download Karein (.txt)",
                    data=result,
                    file_name="Universal_AI_Result.txt",
                    mime="text/plain",
                )
            else:
                st.error(
                    "⚠️ Is waqt server busy hai, 5 second baad dobara try karein."
                )
