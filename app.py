"""Disclosure Lens web app.  Run locally with:  python3 -m streamlit run app.py"""
import html

import streamlit as st

from disclosure_lens.metrics import annotate, summarize
from disclosure_lens.preprocess import parse_document

st.set_page_config(page_title="Disclosure Lens", page_icon="🔍", layout="wide")

GREEN, RED, GREY = "#2e9e5b", "#d64545", "#b8bfc8"


def fact_color(d):
    return GREEN if d == 1 else RED if d == -1 else GREY


def tone_color(t):
    return GREEN if t > 0.05 else RED if t < -0.05 else GREY


def pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


st.title("🔍 Disclosure Lens")
st.caption("Where did the company put the important information, and how was it worded?")

with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
    pasted = st.text_area("...or paste text here", height=200,
                          help="Separate paragraphs with a blank line.")
    use_sample = st.button("Use sample press release")

text = None
if uploaded is not None:
    text = uploaded.read().decode("utf-8", errors="ignore")
elif pasted.strip():
    text = pasted
elif use_sample or st.session_state.get("use_sample"):
    st.session_state["use_sample"] = True
    text = open("data/sample_release.txt", encoding="utf-8").read()

if not text:
    st.info("Upload a file, paste text, or click **Use sample press release** in the sidebar.")
    st.stop()

records = annotate(parse_document(text))
s = summarize(records)

# ---------- Disclosure Profile ----------
st.subheader("Disclosure Profile")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Information order**")
    st.metric("Avg position of negatives", pct(s.get("mean_pos_negative")))
    st.metric("Avg position of positives", pct(s.get("mean_pos_positive")))
    st.metric("Placement asymmetry", pct(s.get("placement_asymmetry")),
              help="Positive = bad news appears later than good news.")
    st.metric("Distance from headline", f"{s['distance_from_headline']} sentences"
              if "distance_from_headline" in s else "n/a")
with c2:
    st.markdown("**Hedging**")
    st.metric("Hedge density near negatives", pct(s.get("hedge_near_negative")))
    st.metric("Hedge density near positives", pct(s.get("hedge_near_positive")))
    ha = s.get("hedging_asymmetry")
    if ha is not None:
        st.metric("Hedging asymmetry", f"{ha:.1f}x")
    elif s.get("hedge_near_negative"):
        st.metric("Hedging asymmetry", "undefined", help="No hedging near positives at all.")
    else:
        st.metric("Hedging asymmetry", "n/a")
with c3:
    st.markdown("**Tone vs. facts**")
    st.metric("Negative facts in positive language", pct(s.get("framing_ratio")))
    gap = s.get("mean_tone_gap_on_negatives")
    st.metric("Mean tone gap on negatives", "n/a" if gap is None else f"{gap:.2f}",
              help="Higher = more positive wording around negative facts.")

# ---------- Position strip ----------
st.subheader("Where the information sits")
blocks = "".join(
    f'<div title="Sentence {r["index"]}" style="flex:1;height:26px;background:{fact_color(r["direction"])};'
    f'border-right:1px solid white;{"outline:2px solid #222;outline-offset:-2px;" if r["material_neg"] else ""}"></div>'
    for r in records)
st.markdown(f'<div style="display:flex;width:100%;border-radius:4px;overflow:hidden">{blocks}</div>'
            f'<div style="display:flex;justify-content:space-between;font-size:12px;color:#666">'
            f'<span>Start of document</span><span>End of document</span></div>',
            unsafe_allow_html=True)
st.caption("Each block is one sentence. Green = positive fact, red = negative fact, grey = neutral. "
           "Black outline = material negative.")

# ---------- Disclosure Map ----------
st.subheader("Disclosure Map")
st.caption("Left strip = what the FACT says. Right strip = how the WORDING sounds. "
           "When they disagree on a negative fact, the row is flagged.")
rows = []
for r in records:
    spin = r["direction"] == -1 and r["tone"] > 0
    flag = ('<span style="background:#fff3cd;color:#8a6d00;padding:1px 6px;border-radius:4px;'
            'font-size:11px;margin-left:6px">possible spin</span>') if spin else ""
    mat = ('<span style="background:#fde2e2;color:#a12626;padding:1px 6px;border-radius:4px;'
           'font-size:11px;margin-left:6px">material</span>') if r["material_neg"] else ""
    rows.append(
        f'<div style="display:flex;align-items:stretch;margin-bottom:4px;font-size:14px">'
        f'<div style="width:10px;background:{fact_color(r["direction"])}"></div>'
        f'<div style="width:10px;background:{tone_color(r["tone"])};margin-right:10px"></div>'
        f'<div style="width:38px;color:#888">{r["index"]}</div>'
        f'<div style="flex:1;padding:2px 0">{html.escape(r["text"])}{mat}{flag}</div>'
        f'<div style="width:90px;text-align:right;color:#666">hedge {r["hedge_density"] * 100:.1f}%</div>'
        f'</div>')
st.markdown("".join(rows), unsafe_allow_html=True)

st.divider()
st.caption("These are patterns to examine, not verdicts. Late placement or heavy hedging can have innocent "
           "explanations. The tone word list is a placeholder pending the Loughran-McDonald dictionary.")
