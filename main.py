import streamlit as st
from response import generate_response
import io

SYSTEM_PROMPT = """You are a Math Mastermind. For every math problem:
Show step-by-step solution 2) Explain reasoning 3) Give alternate method if possible
Verify answer if possible 5) Use proper notation 6) Break complex problems into parts
Format: Problem → Steps → Final Answer → Concepts used. Be precise and educational."""

def math_generate(problem: str, level: str, temperature=0.1, max_tokens=1024) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nMath Problem ({level}): {problem}"
    return generate_response(prompt, temperature=temperature, max_tokens=max_tokens)

def export_txt(history):
    txt = "\n\n".join([f"Q{i}: {h['q']}\nA{i}: {h['a']}" for i, h in enumerate(history, 1)])
    return io.BytesIO(txt.encode("utf-8"))

def setup_ui():
    st.set_page_config(page_title="🧮 Math Mastermind", layout = "centered")
    st.title("🧮 Math Mastermind")
    st.write("Can solve any math problem with a detailed step-by-step explanation/s.")
    
    with st.expander("Examples"):
        st.markdown('- Algebra: "Solve x when 2x + 3 - 5x^3 = 0"\n'
                    '- Calculus: "Derivative of sin(x^2) + ln(x)"\n'
                    '- Geometry: "Find the area of a square with the height of 6m and width of 5m')
        
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", 0)
    
    c1, c2 = st.columns([1, 2])
    if c1.button("🗑️ Clear"):
        st.session_state.history = []; st.rerun()
        
    if st.session_state.history:
        c2.download_button("Export", export_txt(st.session_state.history), "Math_Mastermind_Solutions.txt", "text/plain")
        
    with st.form("math_form", clear_on_submit=True):
        q = st.text_area("📝 Enter your math problem: ", height=100, placeholder="Example: Solve x^2 + 5x +6 = 0 for x", key=f"q_{st.session_state.k}")
        a, b = st.columns([3, 1])
        solve = a.form_submit_button("Solve", use_container_width=True)
        level = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
        
        if solve:
            if not q.strip():
                st.warning("Enter a problem first.")
            else:
                with st.spinner("Solving..."):
                    ans = math_generate(q.strip(), level)
                st.session_state.history.insert(0, {"q": q.strip(), "a": ans, "lvl": level})
                st.session_state.k += 1; st.rerun()
                
    if not st.session_state.history:
        return
    st.markdown("### Solution History (Latest First)")
    
if __name__ == "__main__":
    setup_ui()
       