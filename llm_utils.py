import os
import re
import json
from openai import OpenAI
from prompts import ANALYSIS_SYSTEM_PROMPT, REPHRASE_SYSTEM_PROMPT

def get_llm_client():
    return OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def classify_text_sensitivity(client, text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        raw_content = response.choices[0].message.content
        json_str = extract_json(raw_content)
        if json_str:
            return json.loads(json_str)
        else:
            return {}
    except Exception as e:
        import streamlit as st
        st.error(f"An error occurred during classification: {e}")
        return {}

def rephrase_query(client, original_text: str, analysis: dict) -> str:
    non_essential_info = analysis.get('sensitive_attributes_not_essential_to_the_context', [])
    user_prompt_for_rephrasing = (
        f"Original Text: \"{original_text}\"\n\n"
        f"Based on analysis, the following information is considered non-essential: {non_essential_info}\n\n"
        "Please reformulate the 'Original Text' following the system instructions."
    )
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": REPHRASE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt_for_rephrasing}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        import streamlit as st
        st.error(f"An error occurred during rephrasing: {e}")
        return "Could not rephrase the query due to an error."