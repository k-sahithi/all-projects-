# CrowdGuard Registration Form using Streamlit
import streamlit as st
import pandas as pd
import qrcode
import time
import re
import os

# --------------- Page Configuration ---------------
st.set_page_config(page_title="CrowdGuard Registration", page_icon="🏟️", layout="centered")
st.title("🏟️ CrowdGuard Registration Form")
st.markdown("### 📝 Please fill in your details below")

# --------------- CSV Configuration ---------------
csv_path = "registered_users.csv"
expected_columns = ["Name", "Phone", "Email"]

def ensure_csv_structure(path, columns):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        pd.DataFrame(columns=columns).to_csv(path, index=False)
    else:
        try:
            df = pd.read_csv(path)
            if list(df.columns) != columns:
                pd.DataFrame(columns=columns).to_csv(path, index=False)
        except Exception:
            pd.DataFrame(columns=columns).to_csv(path, index=False)

ensure_csv_structure(csv_path, expected_columns)

# --------------- Load Data ---------------
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path, dtype=str)
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame(columns=expected_columns)

# --------------- Registration Form ---------------
with st.form("registration_form", clear_on_submit=False):
    name = st.text_input("👤 Full Name (letters and spaces only)").strip()
    phone = st.text_input("📱 Mobile Number (10 digits only)", max_chars=10, placeholder="Enter 10-digit number").strip()
    email = st.text_input("📧 Email Address", placeholder="Enter your real email").strip()
    submitted = st.form_submit_button("🚀 Register")

    if submitted:
        name_valid = bool(re.match(r"^[A-Za-z\s]+$", name))
        phone_valid = phone.isdigit() and len(phone) == 10
        email_valid = bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

        if not name or not phone or not email:
            st.warning("⚠️ Please fill in all fields.")
        elif not name_valid:
            st.error("❌ Name must contain only letters and spaces.")
        elif not phone_valid:
            st.error("❌ Mobile number must be exactly 10 digits.")
        elif not email_valid:
            st.error("❌ Please enter a valid email address (correct format needed).")
        else:
            try:
                existing = load_data(csv_path)
                formatted_phone = f"+91{phone}"
                if formatted_phone in existing["Phone"].values:
                    st.warning("⚠️ This number is already registered.")
                else:
                    new_entry = pd.DataFrame({
                        "Name": [name],
                        "Phone": [formatted_phone],
                        "Email": [email]
                    })
                    updated = pd.concat([existing, new_entry], ignore_index=True)
                    updated.to_csv(csv_path, index=False)
                    with st.spinner("Submitting..."):
                        time.sleep(1.5)
                    st.success("🎉 You're successfully registered!")
                    st.info(f"📧 Registered email: {email}")
                    st.info(f"📱 Registered phone: {formatted_phone}")
            except Exception as e:
                st.error(f"❌ Error saving registration: {e}")

# --------------- QR Code Section ---------------
st.markdown("---")
st.subheader("📲 Register via QR Code")

# ⭐ Update your Ngrok URL here
NGROK_URL = "https://your-ngrok-link.ngrok-free.app"

# Generate QR Code
qr = qrcode.make(NGROK_URL)
qr_path = "registration_qr.png"
qr.save(qr_path)
st.image(qr_path, caption="📷 Scan this QR Code to Open Registration", use_column_width=True)

# Also show clickable link
st.markdown(f"🔗 [Click here to open registration form]({NGROK_URL})", unsafe_allow_html=True)

# --------------- Footer ---------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Made with ❤️ by CrowdGuard Team</p>", unsafe_allow_html=True)
