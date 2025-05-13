
import streamlit as st
import sqlite3
from datetime import datetime

# لیست سوالات روزانه
questions = [
    "امروز چه چیز کوچکی از آینده‌ات را در عمل دیدی؟",
    "کدام تصمیم امروزت به رسالت زندگی‌ات نزدیک بود؟",
    "کجا نیاز به اصلاح، مکث یا بازنگری داشتی؟"
]

# ایجاد Session State برای ردیابی شماره سوال
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

# سوال فعلی بر اساس ایندکس
q_index = st.session_state.q_index
question = questions[q_index]

# نمایش سوال
st.title("🧠 سیستم بازتاب چندسؤاله روزانه")
st.markdown(f"### ❓ سوال {q_index+1} از {len(questions)}:")
st.markdown(f"**{question}**")

# باکس پاسخ
answer = st.text_area("✍️ پاسخ خود را بنویس:", height=150)

# دکمه ذخیره پاسخ
if st.button("✅ ذخیره پاسخ"):
    if answer.strip():
        conn = sqlite3.connect("user_responses.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS responses 
                     (timestamp TEXT, question TEXT, answer TEXT)''')
        c.execute("INSERT INTO responses VALUES (?, ?, ?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), question, answer))
        conn.commit()
        conn.close()
        st.success("✅ پاسخ شما ذخیره شد.")
    else:
        st.warning("⚠️ لطفاً پاسخ را وارد کنید.")

# دکمه سوال بعدی
if st.button("➡️ سوال بعدی"):
    if st.session_state.q_index < len(questions) - 1:
        st.session_state.q_index += 1
    else:
        st.info("🎉 همه سوالات امروز را پاسخ داده‌ای!")

# دکمه سوال قبلی
if st.session_state.q_index > 0:
    if st.button("⬅️ سوال قبلی"):
        st.session_state.q_index -= 1
