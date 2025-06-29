import streamlit as st
from style import TITLE_HTML, PRIVACY_CSS

def render_sidebar():
    st.sidebar.title("🛡️ Privacy Chat Assistant")
    st.sidebar.markdown("""
    Welcome!  
    - Type your message in the chat box.
    - Click **Send** to chat with the LLM.
    - Click **Apply Privacy Detector** to analyze and get a privacy-preserving suggestion.
    - Click **Apply Reformulation** to edit your query with the suggestion.
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("🔒 Your data is processed securely and never stored.")

def render_title():
    st.markdown(TITLE_HTML, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

def render_chat(chat_history):
    chat_container = st.container()
    with chat_container:
        for entry in chat_history:
            with st.chat_message("user"):
                st.markdown(entry["user"])
            if entry.get("llm"):
                with st.chat_message("assistant"):
                    st.markdown(entry["llm"])
    st.divider()

def render_input_area():
    input_area = st.container()
    with input_area:
        st.markdown(
            "<div style='display: flex; flex-direction: column; align-items: center;'>",
            unsafe_allow_html=True
        )
        input_placeholder = st.empty()
        # 每次页面加载时自动清空输入框
        if "input_value" not in st.session_state or st.session_state.get("reset_input", False):
            st.session_state["input_value"] = ""
            st.session_state["reset_input"] = False
        user_input = input_placeholder.text_input(
            "Type your message...",
            value=st.session_state["input_value"],
            key="chat_input"
        )
        col_send, col_privacy = st.columns([1, 1], gap="small")
        with col_send:
            send_clicked = st.button("🚀 Send", use_container_width=True)
        with col_privacy:
            privacy_clicked = st.button("🛡️ Apply Privacy Detector", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    return user_input, send_clicked, privacy_clicked

def render_privacy_analysis(analysis_history):
    st.markdown(PRIVACY_CSS, unsafe_allow_html=True)
    st.markdown("<div class='privacy-section'>", unsafe_allow_html=True)
    if analysis_history:
        last = analysis_history[-1]
        analysis = last["analysis"]
        if analysis:
            st.markdown("<div class='privacy-header'>🎯 Primary Context</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='privacy-box'>{analysis.get('primary_context', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown("<div class='privacy-header'>✅ Essential Attributes</div>", unsafe_allow_html=True)
            essentials = analysis.get("attributes_essential_to_the_context", [])
            st.markdown(
                f"<div class='privacy-box privacy-box-green'>{', '.join(essentials) if essentials else 'None found.'}</div>",
                unsafe_allow_html=True
            )

            st.markdown("<div class='privacy-header'>⚠️ Non-Essential Sensitive Info</div>", unsafe_allow_html=True)
            non_essentials = analysis.get("sensitive_attributes_not_essential_to_the_context", [])
            st.markdown(
                f"<div class='privacy-box privacy-box-yellow'>{', '.join(non_essentials) if non_essentials else 'None found.'}</div>",
                unsafe_allow_html=True
            )

            st.markdown("<div class='privacy-header'>🔄 Suggested Reformulation</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='privacy-box privacy-box-gray'>{last['safe_query']}</div>",
                unsafe_allow_html=True
            )

            if st.button("✏️ Apply Reformulation", key="apply_reformulation"):
                reformulated_query = last["safe_query"]
                st.session_state["input_value"] = reformulated_query
                st.session_state["reset_input"] = True
                st.rerun()
        else:
            st.info("No analysis available yet. Enter a message in the chat and click Apply Privacy Detector.")
    else:
        st.info("No analysis available yet. Enter a message in the chat and click Apply Privacy Detector.")
    st.markdown("</div>", unsafe_allow_html=True)
