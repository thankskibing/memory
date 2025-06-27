from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="기억산책 챗봇")
st.image("logo.png", width=100)
st.title("기억산책 챗봇")

# ✅ 스타일 정의 - CSS 추가
st.markdown(
    """
    <style>
    .chat-bubble {
        display: inline-block;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 12px;
        line-height: 1.5;
        word-wrap: break-word;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #DCF8C6;
        text-align: left;
        margin-left: auto;
        border-bottom-right-radius: 0px;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        text-align: left;
        margin-right: auto;
        border-bottom-left-radius: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ OpenAI 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✅ 세션 상태 초기화
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"

system_message = '''
너의 이름은 기억봇이야.
너는 궁금한 점에 답변도 해주고 서울의 잊혀가는 장소에 대한 정보 추천, 걷기 코스를 추천해주는 역할을 해
너는 항상 존댓말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대로 끝내줘
항상 존댓말로 친근하게 대답해줘.
영어로 질문을 받아도 무조건 한글로 답변해줘.
한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘
모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘
'''
welcome_text = "안녕하세요! 저는 기억산책의 친구봇 ‘기억이’예요. 궁금한 점이나 어디로 갈지 고민이라면 언제든 물어보세요!😊"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",    "content": system_message},
        {"role": "assistant", "content": welcome_text}
    ]

# ✅ 히스토리 렌더링
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    text = msg["content"]
    if role == "user":
        st.markdown(f'<div class="chat-bubble user-bubble">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble assistant-bubble">{text}</div>', unsafe_allow_html=True)

# ✅ 사용자 입력 받기
if prompt := st.chat_input("무엇을 도와드릴까요?😊"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)

    # ✅ OpenAI 응답 생성
    stream = client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=st.session_state.messages,
        stream=True,
    )

    assistant_text = ""
    for chunk in stream:
        assistant_text += chunk.choices[0].delta.content or ""

    st.markdown(f'<div class="chat-bubble assistant-bubble">{assistant_text}</div>', unsafe_allow_html=True)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text}
    )
