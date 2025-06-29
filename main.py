import streamlit as st
from llm_utils import get_llm_client, classify_text_sensitivity, rephrase_query
from ui_components import render_sidebar, render_title, render_chat, render_input_area, render_privacy_analysis

CHAT_COL_RATIO = [3, 2]  # Chat column is wider than privacy analysis

def main():
    st.set_page_config(page_title="🛡️ Contextual Privacy Chat Assistant", page_icon="🛡️")
    render_sidebar()
    render_title()

    # --- Initialize session state ---
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "analysis_history" not in st.session_state:
        st.session_state["analysis_history"] = []

    client = get_llm_client()

    # --- Layout: left_col (chat) wider, right_col (privacy) smaller ---
    left_col, right_col = st.columns(CHAT_COL_RATIO, gap="large")

    with left_col:
        render_chat(st.session_state["chat_history"])
        user_input, send_clicked, privacy_clicked = render_input_area()

        if send_clicked and user_input:
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )
                llm_reply = response.choices[0].message.content.strip()
            except Exception as e:
                llm_reply = f"LLM error: {e}"
            st.session_state["chat_history"].append({
                "user": user_input,
                "llm": llm_reply
            })
            st.session_state["last_user_input"] = user_input
            st.session_state["input_value"] = ""
            st.rerun()

        if privacy_clicked and user_input:
            analysis = classify_text_sensitivity(client, user_input)
            safe_query = rephrase_query(client, user_input, analysis) if analysis else ""
            st.session_state["analysis_history"].append({
                "user": user_input,
                "analysis": analysis,
                "safe_query": safe_query
            })
            st.session_state["last_user_input"] = user_input
            st.session_state["input_value"] = ""
            st.rerun()

    with right_col:
        render_privacy_analysis(st.session_state["analysis_history"])

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center;'>Powered by <b>Copilot</b></div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()