import streamlit as st
import streamlit.components.v1 as components
from asl_1 import text_to_gloss

# UI Config
st.set_page_config(page_title="SignAI Gloss", layout="centered")

# The UI (Paste your minimalist index.html here internally)
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #0a0a0c; --card: #16161a; --primary: #6366f1; --text-main: #f8fafc; }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background: var(--bg); color: var(--text-main); font-family: 'Outfit', sans-serif; text-align: center; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .gloss-card { background: var(--card); border-radius: 20px; padding: 40px; margin-bottom: 20px; width: 90%; max-width: 500px; min-height: 150px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.05); }
        .gloss-result { font-family: 'JetBrains Mono', monospace; font-size: 2rem; text-transform: uppercase; color: var(--primary); }
        .input-group { background: var(--card); border-radius: 15px; display: flex; padding: 5px; width: 90%; max-width: 500px; border: 1px solid rgba(255,255,255,0.1); }
        input { flex: 1; background: transparent; border: none; color: white; padding: 10px; outline: none; }
        .btn-primary { background: var(--primary); color: white; border-radius: 10px; border:none; padding: 0 15px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <div class="gloss-card"><div id="gloss-output" style="color:#475569">Your translation...</div></div>
    <div class="input-group">
        <input type="text" id="text-input" placeholder="Type a sentence...">
        <button class="btn-primary" id="go-btn">GO</button>
    </div>
    <script>
        const textInput = document.getElementById('text-input');
        const goBtn = document.getElementById('go-btn');
        const glossOutput = document.getElementById('gloss-output');

        function sendToStreamlit(text) {
            window.parent.postMessage({ type: 'streamlit:set_widget_value', data: { widget_id: 'user_text', value: text } }, '*');
        }

        window.addEventListener('message', (e) => {
            if (e.data && e.data.type === 'gloss_result') {
                glossOutput.className = 'gloss-result';
                glossOutput.textContent = e.data.text;
            }
        });

        goBtn.onclick = () => sendToStreamlit(textInput.value);
        textInput.onkeypress = (e) => { if (e.key === 'Enter') sendToStreamlit(textInput.value); };
    </script>
</body>
</html>
"""

user_text = st.text_input("", key="user_text", label_visibility="collapsed")
if user_text:
    gloss = " ".join(text_to_gloss(user_text))
    components.html(html_code + f"<script>window.postMessage({{type:'gloss_result', text:'{gloss}'}}, '*');</script>", height=500)
else:
    components.html(html_code, height=500)

st.markdown("<style>#MainMenu, footer, header {visibility: hidden;}</style>", unsafe_allow_html=True)
