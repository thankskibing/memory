from openai import OpenAI
import streamlit as st
import html

# ✅ 페이지 설정
st.set_page_config(page_title="말감 챗봇")
st.image("logo.png", width=100)
st.title("뭐가 궁금한감?")

# ✅ 스타일 정의 - 왼/오 정렬용
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    padding-bottom: 90px;
}

.chat-wrapper {
    display: flex;
    margin-bottom: 20px;  /* 👈 말풍선 간 거리 */
}

.chat-wrapper.user {
    justify-content: flex-end;
}

.chat-wrapper.assistant {
    justify-content: flex-start;
}

.chat-bubble {
    padding: 12px 16px;
    border-radius: 16px;
    max-width: 80%;
    line-height: 1.5;
    font-size: 16px;
    word-wrap: break-word;
    display: inline-block;
}

.user-bubble {
    background-color: #DCF8C6;
    border-bottom-right-radius: 0px;
}

.assistant-bubble {
    background-color: #F1F0F0;
    border-bottom-left-radius: 0px;
}
</style>
""", unsafe_allow_html=True)

# ✅ OpenAI 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ 세션 초기화
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

system_message = '''
너의 이름은 말감이야.
너는 궁금한 점에 답변도 해주고 서울의 잊혀가는 장소에 대한 정보 추천, 걷기 코스를 추천해주는 역할을 해
모든 문장 끝에 '감'으로 끝맺음을 지어줘
영어로 질문을 받아도 무조건 한글로 답변해줘.
한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘
모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘
'''
welcome_text = "안녕하세요! 나는 여러분을 도와줄 ‘말하는 감자 말감이’예요. 궁금한 점이나 고민이 있다면 자유롭게 물어보라감!😊"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": welcome_text}
    ]

# ✅ 메시지 출력
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    role = msg["role"]
    text = html.escape(msg["content"])  # 이모지 외 HTML 안전 처리

    if role == "user":
        st.markdown(f'''
        <div class="chat-wrapper user">
            <div class="chat-bubble user-bubble">{text}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-wrapper assistant">
            <div class="chat-bubble assistant-bubble">{text}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ 사용자 입력
if prompt := st.chat_input("뭐가 궁금한감?😊"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=st.session_state.messages,
        stream=True,
    )

    assistant_text = ""
    for chunk in stream:
        assistant_text += chunk.choices[0].delta.content or ""

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text}
    )
