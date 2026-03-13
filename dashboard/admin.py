import streamlit as st
import requests

API = "http://127.0.0.1:5000/analyze"

st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .stApp {
        background-color: #0f0f0f;
        color: #e8e8e8;
    }
    section[data-testid="stSidebar"] {
        background-color: #161616;
        border-right: 1px solid #2a2a2a;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'IBM Plex Sans', sans-serif !important;
        color: #e8e8e8 !important;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #1e1e1e !important;
        border: 1px solid #333 !important;
        color: #e8e8e8 !important;
        border-radius: 6px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 0 2px rgba(74,158,255,0.15) !important;
    }
    .stButton > button {
        background-color: #4a9eff !important;
        color: #000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 24px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #2d82e0 !important;
    }
    .section-title {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #888;
        margin: 0 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #2a2a2a;
    }
    .result-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .badge-fake {
        display: inline-block;
        background: rgba(255,80,80,0.15);
        color: #ff5050;
        border: 1px solid rgba(255,80,80,0.4);
        border-radius: 6px;
        padding: 6px 18px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }
    .badge-real {
        display: inline-block;
        background: rgba(50,200,120,0.15);
        color: #32c878;
        border: 1px solid rgba(50,200,120,0.4);
        border-radius: 6px;
        padding: 6px 18px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.08em;
    }
    .conf-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px;
        color: #666;
        margin-top: 10px;
    }
    .conf-bar-bg {
        background: #252525;
        border-radius: 4px;
        height: 8px;
        margin-top: 6px;
        overflow: hidden;
    }
    .phrase-tag {
        display: inline-block;
        background: rgba(255,80,80,0.1);
        color: #ff8080;
        border: 1px solid rgba(255,80,80,0.25);
        border-radius: 4px;
        padding: 4px 12px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px;
        margin: 4px 6px 4px 0;
    }
    .explanation-row {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 10px 0;
        border-bottom: 1px solid #222;
        font-size: 14px;
        color: #ccc;
        line-height: 1.6;
    }
    .explanation-row:last-child { border-bottom: none; }
    .exp-icon { color: #ffb432; font-size: 15px; }
    .badge-trusted {
        display: inline-block;
        background: rgba(50,200,120,0.15);
        color: #32c878;
        border: 1px solid rgba(50,200,120,0.4);
        border-radius: 6px;
        padding: 6px 16px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 14px;
        font-weight: 600;
    }
    .badge-untrusted {
        display: inline-block;
        background: rgba(255,180,50,0.15);
        color: #ffb432;
        border: 1px solid rgba(255,180,50,0.4);
        border-radius: 6px;
        padding: 6px 16px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 14px;
        font-weight: 600;
    }
    .metric-box {
        text-align: center;
        padding: 10px 0;
    }
    .metric-num {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 36px;
        font-weight: 700;
        color: #4a9eff;
    }
    .metric-label {
        font-size: 12px;
        color: #555;
        font-family: 'IBM Plex Mono', monospace;
        margin-top: 4px;
    }
    h2 {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔍 Fake News Detector")
    st.markdown("<p style='color:#555; font-size:13px; margin-top:-6px;'>ML-powered misinformation analysis</p>", unsafe_allow_html=True)
    st.markdown("---")
    text = st.text_area("News Article", placeholder="Paste the news article text here...", height=240)
    source = st.text_input("News Source", placeholder="e.g. Reuters, BBC, CNN")
    analyze_btn = st.button("Analyze Article")
    st.markdown("---")
    st.markdown("<p style='color:#3a3a3a; font-size:12px;'>Trusted: Reuters · BBC · Associated Press</p>", unsafe_allow_html=True)

st.markdown("## Analysis Results")

if analyze_btn:
    if not text.strip():
        st.warning("Please enter some article text to analyze.")
    else:
        with st.spinner("Analyzing article..."):
            try:
                response = requests.post(API, json={"text": text, "source": source}, timeout=10)
                result = response.json()

                if "error" in result:
                    st.error(f"API Error: {result['error']}")
                    st.stop()

                pred        = result.get("prediction", {})
                phrases     = result.get("suspicious_phrases", [])
                explanations= result.get("explanation", [])
                trusted     = result.get("trusted_source", False)
                metrics     = result.get("metrics", {})

                verdict     = str(pred.get("prediction", "unknown")).upper()
                confidence  = pred.get("confidence", 0)

                st.markdown('<p class="section-title">1 · Prediction</p>', unsafe_allow_html=True)
                badge = f'<span class="badge-fake">FAKE</span>' if verdict == "FAKE" else f'<span class="badge-real">REAL</span>'
                bar_color = "#ff5050" if verdict == "FAKE" else "#32c878"
                st.markdown(f"""
                <div class="result-card">
                    <table style="width:100%; border-collapse:collapse;">
                        <tr>
                            <td style="width:50%; padding-right:24px; border-right:1px solid #2a2a2a;">
                                <p style="color:#666; font-size:12px; margin:0 0 8px; font-family:'IBM Plex Mono',monospace; text-transform:uppercase; letter-spacing:0.08em;">Prediction</p>
                                {badge}
                            </td>
                            <td style="padding-left:24px;">
                                <p style="color:#666; font-size:12px; margin:0 0 6px; font-family:'IBM Plex Mono',monospace; text-transform:uppercase; letter-spacing:0.08em;">Confidence</p>
                                <p style="font-family:'IBM Plex Mono',monospace; font-size:24px; font-weight:700; color:#fff; margin:0;">{int(confidence*100)}%</p>
                                <div class="conf-bar-bg">
                                    <div style="width:{int(confidence*100)}%; height:8px; background:{bar_color}; border-radius:4px;"></div>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<p class="section-title">2 · Suspicious Claims</p>', unsafe_allow_html=True)
                if phrases:
                    tags = "".join([f'<span class="phrase-tag">⚠ {p}</span>' for p in phrases])
                    st.markdown(f"""
                    <div class="result-card">
                        <p style="color:#666; font-size:13px; margin:0 0 12px;">The following suspicious phrases were detected in the article:</p>
                        <div>{tags}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-card">
                        <p style="color:#555; font-size:14px; margin:0;">✅ No suspicious phrases detected in this article.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<p class="section-title">3 · Explanation</p>', unsafe_allow_html=True)
                if explanations:
                    rows = "".join([f'<div class="explanation-row"><span class="exp-icon">⚠</span><span>{e}</span></div>' for e in explanations])
                    st.markdown(f"""
                    <div class="result-card">
                        {rows}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-card">
                        <p style="color:#555; font-size:14px; margin:0;">No specific explanations — no suspicious patterns found.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('<p class="section-title">4 · Source Trusted</p>', unsafe_allow_html=True)
                if trusted:
                    src_badge = '<span class="badge-trusted">✓ Trusted Source</span>'
                    src_note  = "This source is in the verified trusted sources list."
                    note_color = "#32c878"
                else:
                    src_badge = '<span class="badge-untrusted">⚠ Unverified Source</span>'
                    src_note  = "This source is not in the trusted sources list. Verify independently."
                    note_color = "#ffb432"
                st.markdown(f"""
                <div class="result-card">
                    <table style="width:100%; border-collapse:collapse;">
                        <tr>
                            <td style="width:50%; padding-right:20px;">
                                <p style="color:#666; font-size:12px; margin:0 0 8px; font-family:'IBM Plex Mono',monospace; text-transform:uppercase; letter-spacing:0.08em;">Source Name</p>
                                <p style="font-size:16px; color:#ddd; margin:0; font-weight:500;">{source if source.strip() else "— Not provided —"}</p>
                            </td>
                            <td style="padding-left:20px; border-left:1px solid #2a2a2a;">
                                <p style="color:#666; font-size:12px; margin:0 0 8px; font-family:'IBM Plex Mono',monospace; text-transform:uppercase; letter-spacing:0.08em;">Status</p>
                                {src_badge}
                                <p style="color:{note_color}; font-size:12px; margin:10px 0 0;">{src_note}</p>
                            </td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<p class="section-title">5 · System Metrics</p>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="result-card">
                    <div class="metric-box">
                        <div class="metric-num">{metrics.get('articles_analyzed', 0)}</div>
                        <div class="metric-label">Total Articles Analyzed This Session</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to Flask API. Make sure `python app.py` is running on port 5000.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

else:
    st.markdown("""
    <div style="text-align:center; padding:100px 20px;">
        <p style="font-size:52px; margin-bottom:16px;">🔍</p>
        <p style="font-size:16px; color:#444;">Enter an article in the sidebar and click <strong style="color:#4a9eff;">Analyze Article</strong></p>
        <p style="font-size:13px; color:#333; margin-top:8px;">Results will appear here: Prediction · Suspicious Claims · Explanation · Source · Metrics</p>
    </div>
    """, unsafe_allow_html=True)