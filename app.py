
import streamlit as st
import sqlite3
from datetime import datetime

# اتصال به دیتابیس
conn = sqlite3.connect("user_responses.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS responses
             (timestamp TEXT, question TEXT, answer TEXT)''')
conn.commit()

# سوال روز
question = "امروز چه چیز کوچکی از آینده‌ات را در عمل دیدی؟"

st.title("🧠 سیستم بازتاب روزانه")
st.markdown("### ❓ سوال روز:")
st.markdown(f"**{question}**")

answer = st.text_area("✍️ پاسخ خود را اینجا بنویسید:", height=150)

if st.button("ذخیره پاسخ"):
    if answer.strip() != "":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO responses (timestamp, question, answer) VALUES (?, ?, ?)",
                  (timestamp, question, answer))
        conn.commit()
        st.success("✅ پاسخ شما ذخیره شد.")
    else:
        st.warning("⚠️ لطفاً قبل از ذخیره، پاسخ را وارد کنید.")

if st.checkbox("📂 نمایش پاسخ‌های قبلی"):
    c.execute("SELECT timestamp, answer FROM responses ORDER BY timestamp DESC")
    data = c.fetchall()
    for row in data:
        st.markdown(f"🕒 `{row[0]}`")
        st.markdown(f"📝 {row[1]}")
        st.markdown("---")

conn.close()
