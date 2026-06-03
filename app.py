
import json
import random
import string
import streamlit as st
from pathlib import Path
 
# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaPay Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)
 
# ─── CSS Styling ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
 
/* App background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0c14 100%);
    min-height: 100vh;
}
 
/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 700px;
}
 
/* Header */
.bank-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-bottom: 1.5rem;
}
.bank-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #00d4aa, #00b4d8, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.bank-tagline {
    color: #4a5568;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.25rem;
    font-weight: 300;
}
 
/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: -0.3px;
}
 
/* Balance display */
.balance-card {
    background: linear-gradient(135deg, #00d4aa15, #7c3aed15);
    border: 1px solid #00d4aa30;
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-bottom: 1rem;
}
.balance-label {
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a5568;
    font-weight: 500;
}
.balance-amount {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #00d4aa;
    letter-spacing: -1px;
    margin-top: 0.25rem;
}
.balance-acc {
    font-size: 0.78rem;
    color: #4a5568;
    font-family: monospace;
    margin-top: 0.5rem;
    letter-spacing: 1px;
}
 
/* Info rows */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #a0aec0;
    font-size: 0.9rem;
}
.info-row:last-child { border-bottom: none; }
.info-key {
    color: #4a5568;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}
.info-val {
    color: #e2e8f0;
    font-weight: 400;
}
 
/* Success / error banners */
.success-box {
    background: #00d4aa15;
    border: 1px solid #00d4aa40;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #00d4aa;
    font-size: 0.88rem;
    margin-top: 0.75rem;
}
.error-box {
    background: #f5525215;
    border: 1px solid #f5525240;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #f55252;
    font-size: 0.88rem;
    margin-top: 0.75rem;
}
.warn-box {
    background: #f6c90e15;
    border: 1px solid #f6c90e40;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #f6c90e;
    font-size: 0.88rem;
    margin-top: 0.75rem;
}
 
/* Streamlit widget overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label {
    color: #4a5568 !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 2px #00d4aa20 !important;
}
 
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #00b4d8) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px #00d4aa30 !important;
}
 
/* Selectbox */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
 
/* Divider */
hr { border-color: rgba(255,255,255,0.07) !important; }
 
/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    gap: 2px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    color: #4a5568 !important;
    border-radius: 8px !important;
    text-transform: uppercase !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00d4aa, #00b4d8) !important;
    color: #0a0a0f !important;
}
 
/* Warning/info streamlit */
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)
 
 
# ─── Database Logic ──────────────────────────────────────────────────────────
DATABASE = "novapay_database.json"
 
def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []
 
def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data, indent=2))
 
def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=6)
    num   = random.choices(string.digits, k=4)
    acc   = alpha + num
    random.shuffle(acc)
    return "NP-" + "".join(acc)
 
def find_user(data, accno, pin):
    matches = [u for u in data if u["AccountNo."] == accno and u["pin"] == pin]
    return matches[0] if matches else None
 
 
# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bank-header">
    <div class="bank-logo">◈ NovaPay</div>
    <div class="bank-tagline">Digital Banking · Secure · Fast</div>
</div>
""", unsafe_allow_html=True)
 
 
# ─── Navigation Tabs ─────────────────────────────────────────────────────────
tabs = st.tabs(["Create Account", "Deposit", "Withdraw", "My Details", "Update", "Delete"])
 
data = load_data()
 
 
# ════════════════════════════════════════════════
# TAB 1 — Create Account
# ════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="card"><div class="card-title">👤 Open a New Account</div>', unsafe_allow_html=True)
 
    name  = st.text_input("Full Name", placeholder="e.g. Aarav Sharma", key="c_name")
    age   = st.number_input("Age", min_value=0, max_value=120, step=1, key="c_age")
    email = st.text_input("Email Address", placeholder="you@example.com", key="c_email")
    pin   = st.text_input("4-Digit PIN", max_chars=4, type="password", placeholder="••••", key="c_pin")
 
    if st.button("Open Account", key="btn_create"):
        if not name or not email or not pin:
            st.markdown('<div class="error-box">⚠ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif age < 12:
            st.markdown('<div class="error-box">⚠ Minimum age to open an account is 12 years.</div>', unsafe_allow_html=True)
        elif not pin.isdigit() or len(pin) != 4:
            st.markdown('<div class="error-box">⚠ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
        else:
            acc_no = generate_account_no()
            new_user = {
                "name": name,
                "age": int(age),
                "email": email,
                "AccountNo.": acc_no,
                "pin": int(pin),
                "balance": 0
            }
            data.append(new_user)
            save_data(data)
            st.markdown(f"""
            <div class="success-box">
                ✅ Account created successfully!<br>
                <span style="font-family:monospace;font-size:1rem;color:#00d4aa;font-weight:700;">{acc_no}</span>
                <br><span style="font-size:0.8rem;color:#4a5568;">Save your Account Number — you'll need it to log in.</span>
            </div>""", unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════
# TAB 2 — Deposit
# ════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="card"><div class="card-title">💳 Deposit Money</div>', unsafe_allow_html=True)
 
    d_acc    = st.text_input("Account Number", placeholder="NP-XXXXXXXX", key="d_acc")
    d_pin    = st.text_input("PIN", max_chars=4, type="password", placeholder="••••", key="d_pin")
    d_amount = st.number_input("Amount (₹)", min_value=1, step=100, key="d_amt")
 
    if st.button("Deposit", key="btn_deposit"):
        if not d_acc or not d_pin:
            st.markdown('<div class="error-box">⚠ Enter account number and PIN.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, d_acc.strip(), int(d_pin) if d_pin.isdigit() else -1)
            if not user:
                st.markdown('<div class="error-box">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                user["balance"] += int(d_amount)
                save_data(data)
                st.markdown(f'<div class="success-box">✅ ₹{int(d_amount):,} deposited. New balance: <strong>₹{user["balance"]:,}</strong></div>', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════
# TAB 3 — Withdraw
# ════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="card"><div class="card-title">🏧 Withdraw Money</div>', unsafe_allow_html=True)
 
    w_acc    = st.text_input("Account Number", placeholder="NP-XXXXXXXX", key="w_acc")
    w_pin    = st.text_input("PIN", max_chars=4, type="password", placeholder="••••", key="w_pin")
    w_amount = st.number_input("Amount (₹)", min_value=1, step=100, key="w_amt")
 
    if st.button("Withdraw", key="btn_withdraw"):
        if not w_acc or not w_pin:
            st.markdown('<div class="error-box">⚠ Enter account number and PIN.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, w_acc.strip(), int(w_pin) if w_pin.isdigit() else -1)
            if not user:
                st.markdown('<div class="error-box">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            elif int(w_amount) > user["balance"]:
                st.markdown(f'<div class="warn-box">⚠ Insufficient balance. Available: ₹{user["balance"]:,}</div>', unsafe_allow_html=True)
            else:
                user["balance"] -= int(w_amount)
                save_data(data)
                st.markdown(f'<div class="success-box">✅ ₹{int(w_amount):,} withdrawn. Remaining balance: <strong>₹{user["balance"]:,}</strong></div>', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════
# TAB 4 — Show Details
# ════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="card"><div class="card-title">📋 Account Details</div>', unsafe_allow_html=True)
 
    s_acc = st.text_input("Account Number", placeholder="NP-XXXXXXXX", key="s_acc")
    s_pin = st.text_input("PIN", max_chars=4, type="password", placeholder="••••", key="s_pin")
 
    if st.button("View Details", key="btn_show"):
        if not s_acc or not s_pin:
            st.markdown('<div class="error-box">⚠ Enter account number and PIN.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, s_acc.strip(), int(s_pin) if s_pin.isdigit() else -1)
            if not user:
                st.markdown('<div class="error-box">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="balance-card">
                    <div class="balance-label">Available Balance</div>
                    <div class="balance-amount">₹{user['balance']:,}</div>
                    <div class="balance-acc">{user['AccountNo.']}</div>
                </div>
                <div class="info-row"><span class="info-key">Name</span><span class="info-val">{user['name']}</span></div>
                <div class="info-row"><span class="info-key">Age</span><span class="info-val">{user['age']} yrs</span></div>
                <div class="info-row"><span class="info-key">Email</span><span class="info-val">{user['email']}</span></div>
                <div class="info-row"><span class="info-key">Account No.</span><span class="info-val" style="font-family:monospace">{user['AccountNo.']}</span></div>
                """, unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════
# TAB 5 — Update Details
# ════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="card"><div class="card-title">✏️ Update Account</div>', unsafe_allow_html=True)
 
    u_acc = st.text_input("Account Number", placeholder="NP-XXXXXXXX", key="u_acc")
    u_pin = st.text_input("Current PIN", max_chars=4, type="password", placeholder="••••", key="u_pin")
 
    st.markdown('<hr style="margin:1rem 0">', unsafe_allow_html=True)
    st.markdown('<div style="color:#4a5568;font-size:0.75rem;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:0.75rem;">Leave blank to keep current value</div>', unsafe_allow_html=True)
 
    u_name  = st.text_input("New Name", placeholder="Leave blank to skip", key="u_name")
    u_email = st.text_input("New Email", placeholder="Leave blank to skip", key="u_email")
    u_newpin = st.text_input("New PIN", max_chars=4, type="password", placeholder="Leave blank to skip", key="u_newpin")
 
    if st.button("Save Changes", key="btn_update"):
        if not u_acc or not u_pin:
            st.markdown('<div class="error-box">⚠ Enter account number and current PIN.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, u_acc.strip(), int(u_pin) if u_pin.isdigit() else -1)
            if not user:
                st.markdown('<div class="error-box">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                if u_name.strip():  user["name"]  = u_name.strip()
                if u_email.strip(): user["email"] = u_email.strip()
                if u_newpin.strip():
                    if u_newpin.isdigit() and len(u_newpin) == 4:
                        user["pin"] = int(u_newpin)
                    else:
                        st.markdown('<div class="error-box">⚠ New PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
                        st.stop()
                save_data(data)
                st.markdown('<div class="success-box">✅ Account details updated successfully.</div>', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════
# TAB 6 — Delete Account
# ════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="card"><div class="card-title">🗑️ Close Account</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#f55252;font-size:0.8rem;margin-bottom:1rem;background:#f5525210;padding:0.75rem 1rem;border-radius:8px;border:1px solid #f5525230;">⚠ This action is permanent and cannot be undone.</div>', unsafe_allow_html=True)
 
    del_acc = st.text_input("Account Number", placeholder="NP-XXXXXXXX", key="del_acc")
    del_pin = st.text_input("PIN", max_chars=4, type="password", placeholder="••••", key="del_pin")
    confirm = st.checkbox("I understand this will permanently delete my account", key="del_confirm")
 
    if st.button("Delete Account", key="btn_delete"):
        if not del_acc or not del_pin:
            st.markdown('<div class="error-box">⚠ Enter account number and PIN.</div>', unsafe_allow_html=True)
        elif not confirm:
            st.markdown('<div class="warn-box">⚠ Please check the confirmation box above.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, del_acc.strip(), int(del_pin) if del_pin.isdigit() else -1)
            if not user:
                st.markdown('<div class="error-box">⚠ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                data.remove(user)
                save_data(data)
                st.markdown('<div class="success-box">✅ Account has been permanently closed.</div>', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
 
# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-bottom:1rem;color:#1a202c;font-size:0.75rem;letter-spacing:1px;">
    ◈ NOVAPAY · SECURE BANKING SYSTEM
</div>
""", unsafe_allow_html=True)
