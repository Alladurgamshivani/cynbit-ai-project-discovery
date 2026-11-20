import json
import html
import streamlit as st
from backend.analyzer import analyze_lead
from backend.conversation import answer_followup

st.set_page_config(
    page_title="Cynbit | Project Intelligence",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual system ----------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
  --ink: #eaf2f5; --muted: #91a5b2; --panel: rgba(17, 31, 43, .82);
  --line: rgba(148, 178, 190, .16); --mint: #75f0c3; --cyan: #63c9f4;
  --violet: #a78bfa; --bg: #07111b;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 12% 5%, rgba(34, 130, 127, .18), transparent 34%),
    radial-gradient(ellipse at 88% 12%, rgba(90, 86, 190, .18), transparent 32%),
    linear-gradient(145deg, #07111b 0%, #0a1723 48%, #08121d 100%);
  color: var(--ink);
}
[data-testid="stHeader"] { background: rgba(7,17,27,.65); }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(11,25,36,.98), rgba(8,17,27,.98));
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div { padding-top: 1.4rem; }
.block-container { padding-top: 2.1rem; padding-bottom: 4rem; max-width: 1440px; }
h1,h2,h3,h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.035em; }
h1 { color: #f3fbff; }
p, label, .stMarkdown { color: #d5e2e8; }
.small-muted { color: var(--muted); font-size: .88rem; }
.brand-mark {
  display:flex; align-items:center; gap:10px; margin-bottom:1.8rem;
  font-family:'Space Grotesk'; font-weight:700; letter-spacing:.04em;
}
.brand-icon {
  width:38px;height:38px;border-radius:13px;display:grid;place-items:center;
  color:#07111b;font-size:21px;font-weight:700;
  background:linear-gradient(135deg,var(--mint),var(--cyan));
  box-shadow:0 0 28px rgba(117,240,195,.28);
}
.hero {
  position:relative; overflow:hidden; padding:30px 32px; border-radius:26px;
  border:1px solid rgba(117,240,195,.22);
  background:linear-gradient(115deg,rgba(18,48,58,.92),rgba(24,34,61,.84));
  box-shadow:0 24px 70px rgba(0,0,0,.22);
  animation: rise .7s ease both;
}
.hero:before {
  content:""; position:absolute; width:300px;height:300px;right:-75px;top:-175px;
  border-radius:50%; border:1px solid rgba(117,240,195,.22);
  box-shadow:0 0 0 28px rgba(117,240,195,.035),0 0 0 58px rgba(117,240,195,.025);
  animation: drift 9s ease-in-out infinite;
}
.hero:after {
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(110deg,transparent 25%,rgba(255,255,255,.055) 48%,transparent 68%);
  transform:translateX(-120%); animation: sheen 7s ease-in-out 1.2s infinite;
}
.eyebrow { color:var(--mint); font-size:.72rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; }
.hero-title { font-family:'Space Grotesk'; font-size:clamp(1.8rem,3vw,2.8rem); line-height:1.08; font-weight:700; color:#f4fbff; margin:.55rem 0 .65rem; max-width:760px; }
.hero-copy { color:#b7cbd3; max-width:700px; font-size:1rem; line-height:1.65; }
.pill {
 display:inline-flex;align-items:center;gap:7px;padding:7px 11px;border-radius:999px;
 border:1px solid rgba(117,240,195,.25);background:rgba(117,240,195,.08);
 color:#a7f7d7;font-size:.75rem;font-weight:600;
}
.pulse-dot { width:7px;height:7px;border-radius:50%;background:var(--mint);box-shadow:0 0 0 0 rgba(117,240,195,.55);animation:pulse 2s infinite; }
.section-kicker { color:var(--mint);font-size:.72rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.25rem; }
.section-title { font-family:'Space Grotesk';font-size:1.45rem;font-weight:700;color:#edf7fa;margin:0 0 .25rem; }
.panel {
  background:linear-gradient(145deg,rgba(20,37,50,.92),rgba(13,27,39,.9));
  border:1px solid var(--line); border-radius:20px; padding:20px 22px;
  box-shadow:0 12px 34px rgba(0,0,0,.14);
}
.metric-card {
  min-height:132px; padding:19px 20px; border-radius:19px;
  background:linear-gradient(145deg,rgba(21,43,56,.96),rgba(13,28,41,.92));
  border:1px solid var(--line); position:relative; overflow:hidden;
  animation: rise .55s ease both;
}
.metric-card:after {content:"";position:absolute;width:120px;height:120px;right:-55px;bottom:-65px;border-radius:50%;background:rgba(99,201,244,.08);}
.metric-label {color:#9bb0bc;font-size:.78rem;font-weight:600;letter-spacing:.04em;}
.metric-value {font-family:'Space Grotesk';font-size:2rem;font-weight:700;color:#f3fbff;margin-top:7px;}
.metric-sub {font-size:.75rem;color:#8fa7b4;margin-top:2px;}
.score-track {height:8px;border-radius:99px;background:#263b49;overflow:hidden;margin-top:12px;}
.score-fill {height:100%;border-radius:99px;background:linear-gradient(90deg,var(--mint),var(--cyan));animation: fillbar 1.2s ease both;}
.info-row {display:flex;justify-content:space-between;gap:15px;padding:10px 0;border-bottom:1px solid rgba(148,178,190,.11);font-size:.9rem;}
.info-row:last-child {border-bottom:0;}
.info-label {color:#91a8b5;}
.info-value {color:#eff8fb;font-weight:600;text-align:right;}
.tag {
 display:inline-block;padding:6px 10px;margin:4px 5px 4px 0;border-radius:999px;
 color:#b9f8df;background:rgba(117,240,195,.09);border:1px solid rgba(117,240,195,.17);font-size:.78rem;
}
.warn-tag {color:#f5d69a;background:rgba(245,180,75,.08);border-color:rgba(245,180,75,.18);}
.question {
 padding:12px 14px;margin:8px 0;border-radius:12px;background:rgba(99,201,244,.055);
 border:1px solid rgba(99,201,244,.13);color:#d9edf5;font-size:.9rem;
}
.step {
 display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-bottom:1px solid rgba(148,178,190,.1);
}
.step:last-child {border-bottom:0;}
.step-num {width:27px;height:27px;flex:0 0 27px;display:grid;place-items:center;border-radius:9px;background:rgba(117,240,195,.12);color:var(--mint);font-weight:700;font-size:.8rem;}
.stButton > button, .stDownloadButton > button {
 border:0!important;border-radius:12px!important;padding:.72rem 1.15rem!important;
 color:#07151d!important;font-weight:700!important;
 background:linear-gradient(100deg,#75f0c3,#70d8e8)!important;
 box-shadow:0 8px 24px rgba(79,205,184,.18)!important;transition:transform .2s,box-shadow .2s!important;
}
.stButton > button:hover, .stDownloadButton > button:hover {transform:translateY(-2px);box-shadow:0 12px 30px rgba(79,205,184,.28)!important;}
.stTextArea textarea,.stTextInput input {
 background:rgba(8,20,30,.85)!important;color:#eaf5f8!important;border:1px solid rgba(148,178,190,.24)!important;border-radius:13px!important;
}
div[data-baseweb="select"] > div {background:rgba(8,20,30,.85);border-color:rgba(148,178,190,.24);border-radius:12px;}
hr {border-color:rgba(148,178,190,.14)!important;}
footer {visibility:hidden;}
@keyframes rise {from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse {0%{box-shadow:0 0 0 0 rgba(117,240,195,.55)}70%{box-shadow:0 0 0 8px rgba(117,240,195,0)}100%{box-shadow:0 0 0 0 rgba(117,240,195,0)}}
@keyframes sheen {0%,55%{transform:translateX(-120%)}85%,100%{transform:translateX(120%)}}
@keyframes drift {0%,100%{transform:translate(0,0)}50%{transform:translate(-18px,18px)}}
@keyframes fillbar {from{width:0}to{width:var(--score-width)}}
@media (prefers-reduced-motion: reduce) { *,*::before,*::after {animation:none!important;transition:none!important;scroll-behavior:auto!important;} }

/* Professional client-facing light theme */
:root {
  --ink:#182b3a; --muted:#647787; --panel:#ffffff; --line:#e4ebef;
  --mint:#087f72; --cyan:#287f9a; --violet:#64748b; --bg:#f4f7f8;
}
.stApp {
  background:
    radial-gradient(ellipse at 90% 0%, rgba(8,127,114,.045), transparent 28%),
    #f4f7f8 !important;
  color:#182b3a !important;
}
[data-testid="stHeader"] {background:rgba(244,247,248,.92)!important;}
[data-testid="stSidebar"] {
  background:#ffffff!important;
  border-right:1px solid #e5ecef!important;
}
[data-testid="stSidebar"] * {color:#243746;}
.block-container {max-width:1360px;padding-top:1.7rem;}
h1,h2,h3,h4 {color:#172d3c!important;}
p,label,.stMarkdown {color:#344b5a;}
.small-muted {color:#708391!important;}
.brand-icon {
  color:#fff!important;
  background:#087f72!important;
  box-shadow:none!important;
}
.hero {
  background:#ffffff!important;
  border:1px solid #e1e9ed!important;
  border-radius:18px!important;
  box-shadow:0 12px 34px rgba(24,43,58,.055)!important;
}
.hero:before {border-color:rgba(8,127,114,.10)!important;box-shadow:0 0 0 28px rgba(8,127,114,.025),0 0 0 58px rgba(8,127,114,.018)!important;}
.hero:after {background:linear-gradient(110deg,transparent 25%,rgba(8,127,114,.035) 48%,transparent 68%)!important;}
.eyebrow,.section-kicker {color:#087f72!important;}
.hero-title {color:#172d3c!important;}
.hero-copy {color:#617582!important;}
.pill {color:#087f72!important;background:#edf7f5!important;border:1px solid #d4ebe5!important;}
.pulse-dot {background:#0a9a81!important;box-shadow:0 0 0 0 rgba(10,154,129,.28)!important;}
.panel,.metric-card {
  background:#ffffff!important;border:1px solid #e3eaee!important;
  border-radius:16px!important;box-shadow:0 8px 24px rgba(24,43,58,.045)!important;
}
.metric-label,.metric-sub,.info-label {color:#718391!important;}
.metric-value,.section-title,.info-value {color:#1b3444!important;}
.score-track {background:#e8eff1!important;}
.score-fill {background:linear-gradient(90deg,#087f72,#42a99a)!important;}
.info-row,.step {border-color:#edf1f3!important;}
.info-value {color:#263e4d!important;}
.tag {color:#126b61!important;background:#edf7f5!important;border-color:#d6ebe5!important;}
.warn-tag {color:#8a5b0b!important;background:#fff8e9!important;border-color:#f1e4c7!important;}
.question {background:#f4f9fa!important;border-color:#e1ecef!important;color:#344b5a!important;}
.stButton>button,.stDownloadButton>button {
  color:#fff!important;background:#087f72!important;box-shadow:none!important;border-radius:10px!important;
}
.stButton>button:hover,.stDownloadButton>button:hover {
  background:#066b60!important;box-shadow:0 6px 16px rgba(8,127,114,.16)!important;
}
.stTextArea textarea,.stTextInput input {
  background:#fff!important;color:#1b3444!important;border:1px solid #dce5e9!important;border-radius:10px!important;
}
div[data-baseweb="select"]>div {background:#fff!important;border-color:#dce5e9!important;}
[data-testid="stChatMessage"] {background:#fff;border:1px solid #e4ebef;border-radius:14px;padding:12px 14px;}
[data-testid="stChatInput"] {border-color:#dce5e9!important;}
@keyframes rise {from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes sheen {0%,72%{transform:translateX(-120%)}90%,100%{transform:translateX(120%)}}
@keyframes drift {0%,100%{transform:translate(0,0)}50%{transform:translate(-8px,8px)}}
@media (prefers-reduced-motion: reduce) { *,*::before,*::after {animation:none!important;transition:none!important;} }


/* Layered CSS 3D hero scene: perspective, depth and continuous motion */
.hero-3d {
  display:grid!important;
  grid-template-columns:minmax(0,1.35fr) minmax(280px,.85fr);
  align-items:center; min-height:330px;
  padding:38px 42px!important; isolation:isolate;
}
.hero-copy-block {position:relative;z-index:2;}
.scene-3d {
  position:relative; height:260px; min-width:260px;
  perspective:900px; transform-style:preserve-3d;
  display:flex;align-items:center;justify-content:center;
  animation:sceneFloat 7s ease-in-out infinite;
}
.core-sphere {
  position:absolute;width:142px;height:142px;border-radius:50%;
  background:
    radial-gradient(circle at 30% 25%,rgba(255,255,255,.95) 0 2%,rgba(185,255,235,.85) 5%,transparent 20%),
    radial-gradient(circle at 35% 30%,#a8f4df 0%,#36b9a0 24%,#087f72 54%,#164e62 78%,#102e40 100%);
  box-shadow:
    inset -20px -24px 35px rgba(5,34,48,.45),
    inset 10px 12px 22px rgba(255,255,255,.36),
    0 22px 45px rgba(8,127,114,.28),
    0 0 65px rgba(45,177,158,.18);
  transform:translateZ(35px);
  animation:sphereRotate 12s linear infinite, sphereBob 5s ease-in-out infinite;
}
.core-highlight {
  position:absolute;top:17px;left:25px;width:40px;height:22px;border-radius:50%;
  background:rgba(255,255,255,.55);filter:blur(9px);transform:rotate(-28deg);
}
.orbit {
  position:absolute;border:1px solid rgba(8,127,114,.38);
  border-radius:50%;transform-style:preserve-3d;
  box-shadow:0 0 18px rgba(8,127,114,.08);
}
.orbit-one {width:220px;height:86px;transform:rotateX(68deg) rotateZ(-25deg);animation:orbitA 12s linear infinite;}
.orbit-two {width:225px;height:95px;transform:rotateY(65deg) rotateZ(35deg);border-color:rgba(49,129,163,.42);animation:orbitB 15s linear infinite;}
.orbit-three {width:190px;height:190px;transform:rotateX(72deg) rotateY(28deg);border-style:dashed;border-color:rgba(8,127,114,.23);animation:orbitC 20s linear infinite;}
.orb-shadow {
  position:absolute;width:180px;height:32px;bottom:22px;border-radius:50%;
  background:radial-gradient(ellipse,rgba(8,65,75,.20),transparent 70%);
  filter:blur(8px);transform:rotateX(68deg) translateZ(-20px);
}
.float-chip {
  position:absolute;padding:7px 11px;border-radius:9px;
  background:rgba(255,255,255,.88);border:1px solid rgba(8,127,114,.16);
  box-shadow:0 8px 20px rgba(25,65,75,.10);
  color:#17675e;font-size:9px;font-weight:800;letter-spacing:.12em;
  transform:translateZ(65px);backdrop-filter:blur(8px);
}
.chip-a {top:23px;left:12%;animation:chipFloatA 5s ease-in-out infinite;}
.chip-b {right:2%;top:48%;animation:chipFloatB 6s ease-in-out infinite;}
.chip-c {bottom:25px;left:17%;animation:chipFloatC 5.5s ease-in-out infinite;}
@keyframes sceneFloat {0%,100%{transform:translateY(0) rotateY(-5deg)}50%{transform:translateY(-9px) rotateY(5deg)}}
@keyframes sphereBob {0%,100%{translate:0 0}50%{translate:0 -8px}}
@keyframes sphereRotate {0%,100%{filter:hue-rotate(0deg)}50%{filter:hue-rotate(9deg)}}
@keyframes orbitA {from{transform:rotateX(68deg) rotateZ(-25deg)}to{transform:rotateX(68deg) rotateZ(335deg)}}
@keyframes orbitB {from{transform:rotateY(65deg) rotateZ(35deg)}to{transform:rotateY(65deg) rotateZ(-325deg)}}
@keyframes orbitC {from{transform:rotateX(72deg) rotateY(28deg) rotateZ(0)}to{transform:rotateX(72deg) rotateY(28deg) rotateZ(360deg)}}
@keyframes chipFloatA {0%,100%{translate:0 0}50%{translate:0 -9px}}
@keyframes chipFloatB {0%,100%{translate:0 0}50%{translate:0 8px}}
@keyframes chipFloatC {0%,100%{translate:0 0}50%{translate:0 -7px}}
@media(max-width:850px) {
 .hero-3d {grid-template-columns:1fr;padding:28px!important;}
 .scene-3d {height:220px;min-width:220px;margin-top:8px;}
}
@media(prefers-reduced-motion:reduce) {
 .scene-3d,.core-sphere,.orbit,.float-chip {animation:none!important;}
}

</style>
""", unsafe_allow_html=True)

def esc(value):
    return html.escape(str(value if value is not None else "Not specified"))

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand-mark"><div class="brand-icon">✳</div><div>CYNBIT <span style="color:#087f72">PROJECT DESK</span></div></div>', unsafe_allow_html=True)
    st.markdown("### Workspace")
    st.markdown('<div class="small-muted">AI-assisted project discovery and client conversations</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("---")
    st.markdown("**Scoring methodology**")
    st.caption("Transparent, rule-based inquiry readiness score. It is not a trained conversion probability.")
    st.markdown('<div class="pill"><span class="pulse-dot"></span> Prototype environment</div>', unsafe_allow_html=True)
    st.markdown("<br><div class='small-muted'>Cynbit AI Project Discovery<br>Assessment proof of concept · v1.1</div>", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero hero-3d">
  <div class="hero-copy-block">
    <div class="eyebrow">CYNBIT · PROJECT INTELLIGENCE</div>
    <div class="hero-title">From first inquiry<br>to a clearer project plan.</div>
    <div class="hero-copy">Understand customer goals, surface unanswered questions and keep every project conversation grounded in context.</div>
    <div style="margin-top:20px"><span class="pill"><span class="pulse-dot"></span> Project workspace</span></div>
  </div>
  <div class="scene-3d" aria-hidden="true">
    <div class="orb-shadow"></div>
    <div class="orbit orbit-one"></div>
    <div class="orbit orbit-two"></div>
    <div class="orbit orbit-three"></div>
    <div class="core-sphere"><div class="core-highlight"></div></div>
    <div class="float-chip chip-a">DISCOVER</div>
    <div class="float-chip chip-b">STRUCTURE</div>
    <div class="float-chip chip-c">CLARIFY</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
left_intro, right_intro = st.columns([1.5, 1])
with left_intro:
    st.markdown('<div class="section-kicker">01 / INTAKE</div><div class="section-title">Start with a customer inquiry</div><div class="small-muted">Choose a sample scenario or paste a real inquiry with personal details removed.</div>', unsafe_allow_html=True)
with right_intro:
    st.markdown('<div style="text-align:right;padding-top:18px" class="small-muted">Structured extraction&nbsp;&nbsp;·&nbsp;&nbsp;Explainable scoring&nbsp;&nbsp;·&nbsp;&nbsp;Human review</div>', unsafe_allow_html=True)

examples = {
    "Healthcare chatbot": "We are a healthcare company looking for a multilingual AI chatbot for our website. It should answer common patient questions and integrate with our existing website. Budget is around INR 200000. We hope to launch in 2 months.",
    "Website redesign": "We need to redesign our company website and make it mobile friendly. We have not finalized the budget or timeline yet.",
    "AI document automation": "Our finance team manually extracts information from invoices. We want an AI solution that reads PDF invoices, extracts vendor, invoice number, date and total, and exports the data to our ERP. Budget 5 lakh. Delivery in 3 months.",
}
sample_col, status_col = st.columns([1.3, 1])
with sample_col:
    choice = st.selectbox("Sample scenario", ["Write my own"] + list(examples))
with status_col:
    st.markdown('<div style="padding-top:29px"><span class="small-muted">Demo data only · No customer records stored by this app</span></div>', unsafe_allow_html=True)

if "inquiry_text" not in st.session_state:
    st.session_state.inquiry_text = examples.get(choice, "")
if choice != "Write my own":
    st.session_state.inquiry_text = examples[choice]

inquiry = st.text_area(
    "Customer message",
    key="inquiry_text",
    height=145,
    placeholder="Example: We need an AI solution that can automate...",
    help="Use at least 20 characters. Avoid pasting personal or confidential customer information.",
)
run_col, hint_col = st.columns([1, 3])
with run_col:
    analyze = st.button("Analyze project inquiry", type="primary", use_container_width=True)
with hint_col:
    st.markdown('<div class="small-muted" style="padding:12px 0">The assistant will extract requirements, assess completeness and draft discovery questions.</div>', unsafe_allow_html=True)

if analyze:
    if len(inquiry.strip()) < 20:
        st.error("Please enter a more detailed inquiry (at least 20 characters).")
    else:
        try:
            with st.spinner("Reading the inquiry and organizing project details..."):
                result = analyze_lead(inquiry)
            st.session_state["result"] = result
            st.session_state["last_inquiry"] = inquiry
            st.session_state["chat_messages"] = []
        except requests.RequestException as exc:
            st.error(f"Could not reach the API: {exc}")
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")

result = st.session_state.get("result")
if result:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">02 / ANALYSIS</div><div class="section-title">Project intelligence overview</div><div class="small-muted">A structured view of the customer request, with the evidence and gaps made visible.</div>', unsafe_allow_html=True)
    score = max(0, min(100, int(result.get("lead_score", 0))))
    priority = esc(result.get("priority", "Unrated"))
    score_color = "#75f0c3" if score >= 70 else "#f3c879" if score >= 40 else "#f28e91"

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">INQUIRY READINESS</div><div class="metric-value">{score}<span style="font-size:1rem;color:#8fa7b4"> / 100</span></div><div class="score-track"><div class="score-fill" style="--score-width:{score}%;width:{score}%"></div></div><div class="metric-sub">Rule-based score</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">PRIORITY LEVEL</div><div class="metric-value" style="color:{score_color}">{priority}</div><div class="metric-sub">Based on current scoring criteria</div></div>', unsafe_allow_html=True)
    with m3:
        completeness = max(0, min(100, int(result.get("completeness_score", 0))))
        st.markdown(f'<div class="metric-card"><div class="metric-label">INFORMATION COMPLETENESS</div><div class="metric-value">{completeness}<span style="font-size:1rem;color:#8fa7b4">%</span></div><div class="score-track"><div class="score-fill" style="--score-width:{completeness}%;width:{completeness}%"></div></div><div class="metric-sub">Based on extracted fields</div></div>', unsafe_allow_html=True)

    st.caption(result.get("scoring_note", "This is an illustrative heuristic score, not a conversion probability."))
    st.markdown("<br>", unsafe_allow_html=True)
    overview, requirements = st.columns([1, 1.15])
    with overview:
        st.markdown('<div class="panel"><div class="section-kicker">PROJECT PROFILE</div><div class="section-title" style="font-size:1.2rem">What the customer needs</div>', unsafe_allow_html=True)
        fields = [
            ("Industry", result.get("industry")),
            ("Project type", result.get("project_type")),
            ("Recommended service", result.get("recommended_service")),
            ("Budget", result.get("budget") or "Not specified"),
            ("Timeline", result.get("timeline") or "Not specified"),
            ("Integrations", ", ".join(result.get("integrations", [])) or "Not specified"),
        ]
        for label, value in fields:
            st.markdown(f'<div class="info-row"><span class="info-label">{esc(label)}</span><span class="info-value">{esc(value)}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with requirements:
        reqs = result.get("requirements", [])
        missing = result.get("missing_information", [])
        st.markdown('<div class="panel"><div class="section-kicker">REQUIREMENTS MAP</div><div class="section-title" style="font-size:1.2rem">Extracted capabilities</div>', unsafe_allow_html=True)
        if reqs:
            st.markdown("".join(f'<span class="tag">{esc(item)}</span>' for item in reqs), unsafe_allow_html=True)
        else:
            st.markdown('<span class="small-muted">No requirements detected yet.</span>', unsafe_allow_html=True)
        st.markdown('<div style="height:12px"></div><div class="section-kicker" style="color:#f3c879">INFORMATION GAPS</div>', unsafe_allow_html=True)
        if missing:
            st.markdown("".join(f'<span class="tag warn-tag">{esc(item)}</span>' for item in missing), unsafe_allow_html=True)
        else:
            st.markdown('<span class="pill">No checklist gaps detected</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    follow_col, score_col = st.columns([1.1, .9])
    with follow_col:
        st.markdown('<div class="panel"><div class="section-kicker">DISCOVERY ASSIST</div><div class="section-title" style="font-size:1.2rem">Questions to ask next</div>', unsafe_allow_html=True)
        for i, question in enumerate(result.get("follow_up_questions", []), 1):
            st.markdown(f'<div class="step"><div class="step-num">{i:02d}</div><div>{esc(question)}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with score_col:
        st.markdown('<div class="panel"><div class="section-kicker">SCORING TRANSPARENCY</div><div class="section-title" style="font-size:1.2rem">Why this score?</div>', unsafe_allow_html=True)
        for key, value in result.get("score_breakdown", {}).items():
            label = esc(key.replace("_", " ").title())
            st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">+{int(value)}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">03 / HANDOFF</div><div class="section-title">Project discovery brief</div><div class="small-muted">A first-draft summary for a human team member to review before contacting the customer.</div>', unsafe_allow_html=True)
    st.text_area("Generated project brief", result.get("project_brief", ""), height=190, key="brief_output")
    d1, d2 = st.columns([1, 3])
    with d1:
        st.download_button(
            "↓  Download JSON",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name="lead_analysis.json",
            mime="application/json",
            use_container_width=True,
        )
    with d2:
        st.markdown('<div class="small-muted" style="padding:12px 0">Human review is required. The prototype does not send messages, create quotes or update a CRM.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-kicker">04 / CONTINUE THE CONVERSATION</div>'
        '<div class="section-title">Ask about your project</div>'
        '<div class="small-muted">Ask follow-up questions about the requirements you just submitted. '
        'Answers use this inquiry and its analysis as context.</div>',
        unsafe_allow_html=True,
    )

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about scope, features, integrations, budget or timeline...")
    if prompt:
        st.session_state["chat_messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Checking your project context..."):
                chat_result = answer_followup(
                    question=prompt,
                    original_inquiry=st.session_state.get("last_inquiry", inquiry),
                    analysis=result,
                    history=st.session_state["chat_messages"][:-1],
                )
                answer = chat_result["answer"]
                st.markdown(answer)
                if chat_result["mode"] == "fallback":
                    st.caption("Contextual demo response · Configure GROQ_API_KEY for open-ended LLM answers.")
        st.session_state["chat_messages"].append({"role": "assistant", "content": answer})

    if st.session_state["chat_messages"]:
        if st.button("Clear conversation", key="clear_project_chat"):
            st.session_state["chat_messages"] = []
            st.rerun()

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel">
      <div class="section-kicker">HOW IT WORKS</div>
      <div class="section-title">From inquiry to discovery-ready brief</div>
      <div class="step"><div class="step-num">01</div><div><b>Understand</b><br><span class="small-muted">Read the customer's message and identify the business context.</span></div></div>
      <div class="step"><div class="step-num">02</div><div><b>Structure</b><br><span class="small-muted">Extract project type, requirements, budget, timeline and integrations.</span></div></div>
      <div class="step"><div class="step-num">03</div><div><b>Prioritize</b><br><span class="small-muted">Apply transparent scoring criteria and surface missing information.</span></div></div>
      <div class="step"><div class="step-num">04</div><div><b>Prepare</b><br><span class="small-muted">Generate follow-up questions and a draft project discovery brief.</span></div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center;margin-top:42px;color:#6f8794;font-size:.75rem">CYNBIT PROJECT INTELLIGENCE · PROOF OF CONCEPT · HUMAN-IN-THE-LOOP</div>', unsafe_allow_html=True)
