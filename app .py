import json
import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Student Dropout Risk Predictor", page_icon="🎓", layout="wide")

# ---------------- model ----------------
with open("model.json") as f:
    m = json.load(f)

def predict(info):
    row = dict(m["defaults"])
    row.update(info)
    z = m["intercept"]
    for col, w in zip(m["columns"], m["coef"]):
        x = row[col]
        if col in m["scaler"]:
            s = m["scaler"][col]
            x = (x - s["mean"]) / s["scale"]
        z += w * x
    return 1 / (1 + math.exp(-z))

def risk_level(p):
    if p < 0.30:
        return "Low Risk", "#16a34a", "The student looks on track. Keep monitoring progress."
    elif p < 0.60:
        return "Medium Risk", "#f59e0b", "There are some warning signs. A check-in with an advisor is a good idea."
    return "High Risk", "#dc2626", "Strong warning signs. Early support is strongly recommended."

def effects(info):
    base = predict({})
    return {k: predict({k: v}) - base for k, v in info.items()}

# ---------------- style ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&display=swap');
.stApp {background: linear-gradient(160deg, #f4f9f8 0%, #eef2fb 100%);}
.pill {display:inline-block; padding:6px 16px; border-radius:999px; background:#e3f1ef; color:#0f5f58;
       font-weight:600; font-size:.9rem; border:1px solid #cfe5e2;}
.hero {text-align:center; padding: 10px 0 18px 0;}
.hero h1 {font-family:'Fraunces', Georgia, serif; font-size:2.8rem; color:#0b2a3c; margin:14px 0 6px 0;}
.hero p {color:#5b6b78; font-size:1.05rem; max-width:680px; margin:0 auto;}
div[data-testid="stVerticalBlockBorderWrapper"] {background:white; border-radius:18px;}
h3.sec {font-family:'Fraunces', Georgia, serif; color:#0b2a3c; margin:0 0 2px 0;}
p.sub {color:#6b7a86; margin:0 0 10px 0;}
.factor {display:flex; justify-content:space-between; align-items:center; padding:10px 4px; border-bottom:1px solid #e6ebf0;}
.factor:last-child {border-bottom:none;}
.factor .t {font-weight:700; color:#0b2a3c;}
.factor .d {color:#5b6b78; font-size:.92rem;}
.up {color:#c2410c; font-weight:700; white-space:nowrap;}
.down {color:#15803d; font-weight:700; white-space:nowrap;}
.label {font-weight:700; color:#475569; margin:10px 0 2px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <span class="pill">🎓 Student retention analytics</span>
  <h1>Student Dropout Risk Prediction</h1>
  <p>Enter a few details about a student to estimate their dropout probability, along with a clear breakdown of what drives it.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- examples ----------------
examples = {
    "Enter my own details": dict(age=20, tuition="Yes", debtor="No", scholar="No", gender="Female", a1=5, g1=12.0, a2=5, g2=12.0),
    "Strong student": dict(age=19, tuition="Yes", debtor="No", scholar="Yes", gender="Female", a1=6, g1=14.0, a2=6, g2=14.0),
    "Borderline student": dict(age=22, tuition="Yes", debtor="No", scholar="No", gender="Male", a1=3, g1=10.5, a2=2, g2=10.0),
    "Struggling student": dict(age=24, tuition="No", debtor="Yes", scholar="No", gender="Male", a1=2, g1=8.0, a2=1, g2=6.0),
    "No units passed": dict(age=30, tuition="No", debtor="Yes", scholar="No", gender="Male", a1=0, g1=0.0, a2=0, g2=0.0),
}
choice = st.selectbox("Try an example student", list(examples.keys()))
d = examples[choice]
k = choice

# ---------------- inputs ----------------
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown('<h3 class="sec">Student background</h3><p class="sub">Age, finances and support</p>', unsafe_allow_html=True)
        age = st.slider("Age at enrollment", 17, 60, d["age"], key="age" + k)
        gender = st.radio("Gender", ["Female", "Male"], index=["Female", "Male"].index(d["gender"]), horizontal=True, key="g" + k)
        tuition = st.radio("Tuition fees up to date?", ["Yes", "No"], index=["Yes", "No"].index(d["tuition"]), horizontal=True, key="t" + k)
        debtor = st.radio("Debtor?", ["No", "Yes"], index=["No", "Yes"].index(d["debtor"]), horizontal=True, key="d" + k)
        scholar = st.radio("Scholarship holder?", ["No", "Yes"], index=["No", "Yes"].index(d["scholar"]), horizontal=True, key="s" + k)
with col2:
    with st.container(border=True):
        st.markdown('<h3 class="sec">Academic performance</h3><p class="sub">Results from the first year</p>', unsafe_allow_html=True)
        a1 = st.slider("1st semester units approved", 0, 20, d["a1"], key="a1" + k)
        g1 = st.slider("1st semester grade", 0.0, 20.0, d["g1"], key="g1" + k)
        a2 = st.slider("2nd semester units approved", 0, 20, d["a2"], key="a2" + k)
        g2 = st.slider("2nd semester grade", 0.0, 20.0, d["g2"], key="g2" + k)

info = {
    "Age at enrollment": age,
    "Tuition fees up to date": 1 if tuition == "Yes" else 0,
    "Debtor": 1 if debtor == "Yes" else 0,
    "Scholarship holder": 1 if scholar == "Yes" else 0,
    "Gender": 1 if gender == "Male" else 0,
    "Curricular units 1st sem (approved)": a1,
    "Curricular units 1st sem (grade)": g1,
    "Curricular units 2nd sem (approved)": a2,
    "Curricular units 2nd sem (grade)": g2,
}

go = st.button("Predict dropout risk", type="primary", use_container_width=True)

# ---------------- result ----------------
if go:
    p = predict(info)
    level, color, msg = risk_level(p)
    angle = p * 180 - 90

    r1, r2 = st.columns([1, 1.3])
    with r1:
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align:center">
              <h3 class="sec">Predicted dropout probability</h3>
              <svg viewBox="0 0 200 120" width="100%" style="max-width:320px">
                <defs><linearGradient id="g" x1="0" x2="1">
                  <stop offset="0%" stop-color="#16a34a"/><stop offset="50%" stop-color="#f59e0b"/><stop offset="100%" stop-color="#dc2626"/>
                </linearGradient></defs>
                <path d="M 15 100 A 85 85 0 0 1 185 100" fill="none" stroke="url(#g)" stroke-width="16" stroke-linecap="round"/>
                <line x1="100" y1="100" x2="100" y2="34" stroke="#0b2a3c" stroke-width="4" stroke-linecap="round"
                      transform="rotate({angle:.1f} 100 100)"/>
                <circle cx="100" cy="100" r="7" fill="#0b2a3c"/>
              </svg>
              <div style="font-size:3rem; font-weight:800; color:{color}; line-height:1">{p*100:.1f}%</div>
              <div style="display:inline-block; margin-top:10px; padding:6px 18px; border-radius:999px; background:{color}; color:white; font-weight:700">{level}</div>
              <p style="color:#5b6b78; margin-top:12px">{msg}</p>
            </div>
            """, unsafe_allow_html=True)

    eff = effects(info)
    meta = {
        "Tuition fees up to date": ("💳", "Tuition payments",
            "Unpaid tuition is one of the strongest warning signs.", "Fees are up to date, which lowers risk."),
        "Debtor": ("🧾", "Debt status",
            "Students with outstanding debt drop out more often.", "No outstanding debt, which lowers risk."),
        "Scholarship holder": ("🎓", "Scholarship",
            "Not having a scholarship means less financial support.", "A scholarship gives financial support and lowers risk."),
        "Age at enrollment": ("🎂", "Age",
            f"Older students tend to drop out more. This student enrolled at {age}.", f"Younger students tend to stay. This student enrolled at {age}."),
        "Gender": ("👤", "Gender",
            "In this dataset, this group had a higher dropout rate.", "In this dataset, this group had a lower dropout rate."),
        "Curricular units 1st sem (approved)": ("📘", "1st semester units passed",
            f"Only {a1} units passed. Passing fewer units raises risk.", f"{a1} units passed, which lowers risk."),
        "Curricular units 1st sem (grade)": ("📝", "1st semester grade",
            f"A grade of {g1:.1f} is below the typical student.", f"A grade of {g1:.1f} is above the typical student."),
        "Curricular units 2nd sem (approved)": ("📗", "2nd semester units passed",
            f"Only {a2} units passed. This is the strongest academic signal.", f"{a2} units passed, which lowers risk."),
        "Curricular units 2nd sem (grade)": ("📝", "2nd semester grade",
            f"A grade of {g2:.1f} is below the typical student.", f"A grade of {g2:.1f} is above the typical student."),
    }

    def block(items, up):
        html = ""
        for name, delta in items:
            icon, title, why_up, why_down = meta[name]
            cls = "up" if up else "down"
            html += f'<div class="factor"><div><div class="t">{icon} {title}</div><div class="d">{why_up if up else why_down}</div></div><div class="{cls}">{delta*100:+.0f} pts</div></div>'
        return html

    ordered = sorted([(n, v) for n, v in eff.items() if n != "Gender"], key=lambda x: abs(x[1]), reverse=True)
    raises = [(n, v) for n, v in ordered if v >= 0.01][:4]
    lowers = [(n, v) for n, v in ordered if v <= -0.01][:4]

    with r2:
        with st.container(border=True):
            st.markdown('<h3 class="sec">Why this result?</h3><p class="sub">Compared with a typical student</p>', unsafe_allow_html=True)
            if raises:
                st.markdown('<div class="label">What raises the risk</div>' + block(raises, True), unsafe_allow_html=True)
            if lowers:
                st.markdown('<div class="label">What lowers the risk</div>' + block(lowers, False), unsafe_allow_html=True)
            if not raises and not lowers:
                st.write("This student is very close to the typical profile.")

    # ---------------- graphs ----------------
    st.markdown("### 📊 Visual breakdown")
    gcol1, gcol2 = st.columns(2)
    short = {
        "Age at enrollment": "Age", "Tuition fees up to date": "Tuition", "Debtor": "Debt",
        "Scholarship holder": "Scholarship", "Gender": "Gender",
        "Curricular units 1st sem (approved)": "1st sem units", "Curricular units 1st sem (grade)": "1st sem grade",
        "Curricular units 2nd sem (approved)": "2nd sem units", "Curricular units 2nd sem (grade)": "2nd sem grade",
    }
    with gcol1:
        with st.container(border=True):
            st.markdown('<h3 class="sec">Effect of each factor</h3><p class="sub">Change in dropout probability (percentage points)</p>', unsafe_allow_html=True)
            df_eff = pd.DataFrame({
                "Raises risk": [max(v, 0) * 100 for v in eff.values()],
                "Lowers risk": [min(v, 0) * 100 for v in eff.values()],
            }, index=[short[n] for n in eff.keys()])
            try:
                st.bar_chart(df_eff, color=["#dc2626", "#16a34a"], horizontal=True)
            except TypeError:
                st.bar_chart(df_eff)
    with gcol2:
        with st.container(border=True):
            st.markdown('<h3 class="sec">How this student compares</h3><p class="sub">Average results of students who stayed vs dropped out</p>', unsafe_allow_html=True)
            df_cmp = pd.DataFrame({
                "This student": [a1, g1, a2, g2],
                "Stayed (avg)": [5.69, 12.19, 5.58, 12.22],
                "Dropped out (avg)": [2.53, 7.28, 1.95, 5.97],
            }, index=["1st sem units", "1st sem grade", "2nd sem units", "2nd sem grade"])
            try:
                st.bar_chart(df_cmp, color=["#2563eb", "#16a34a", "#dc2626"], stack=False)
            except TypeError:
                st.bar_chart(df_cmp, color=["#2563eb", "#16a34a", "#dc2626"])

    with st.expander("🔍 View technical details (for advanced users)"):
        st.write("Inputs sent to the model (all other features use typical values):")
        st.dataframe(pd.DataFrame([info]))
        st.write(f"Raw model probability: {p:.4f}")
else:
    st.info("Choose an example or enter details above, then click **Predict dropout risk**.")

# ---------------- about ----------------
with st.expander("📈 About the model"):
    a, b, c, e = st.columns(4)
    a.metric("Accuracy", "88.7%")
    b.metric("Precision", "87.1%")
    c.metric("Recall", "76.1%")
    e.metric("ROC-AUC", "0.932")
    st.markdown("""
**Model:** Logistic Regression trained on 4,424 students (Portuguese higher-education dataset, 34 features).
**Risk levels:** Low is below 30%, Medium is 30-60%, High is 60% or more.
**Limitations:** the app asks for 9 key inputs and uses typical values for the rest. The model uses 2nd-semester results, so it flags risk after the first year. It supports decisions and is not a final judgement about any student.
""")
st.caption("Built during the Big Brains Machine Learning internship.")
