from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="탐방GO 챗봇")
st.image("logo.png", width=100)
st.title("기억산책 챗봇")
# st.caption("안녕하세요! 저는 기억산책의 친구봇 ‘기억이’예요. 궁금한 점이나 어디로 갈지 고민이라면 언제든 물어보세요!😊")

# ——— 1) CSS 인라인 정의 ———
st.markdown(
    unsafe_allow_html=True
)

# ——— 2) OpenAI 클라이언트 초기화 ———
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ——— 3) 세션 상태 초기화 ———
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
    # system 메시지는 보여주진 않고, 대화 히스토리에만 보관합니다.
    # st.session_state.messages = [{"role": "system", "content": system_message}]
     st.session_state.messages = [
        {"role": "system",    "content": system_message},
        {"role": "assistant", "content": welcome_text}
    ]

# ——— 4) 히스토리 렌더링 ———
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    text = msg["content"]
    if role == "user":
        st.markdown(f'<div class="chat-bubble user-bubble">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble assistant-bubble">{text}</div>', unsafe_allow_html=True)

# ——— 5) 사용자 입력 및 응답 처리 ———
if prompt := st.chat_input("무엇을 도와드릴까요?😊"):
    # 1) 사용자 메시지 히스토리에 추가 & 렌더
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f'<div class="chat-bubble user-bubble">{prompt}</div>',
        unsafe_allow_html=True
    )

    # 2) OpenAI 스트리밍 호출 (stream=True 유지해도 되고, stream=False로 바꿔도 무방)
    stream = client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=st.session_state.messages,
        stream=True,
    )

    # 3) 스트림 전체를 받아서 한 문자열로 합치기
    assistant_text = ""
    for chunk in stream:
        # delta는 객체이므로 .content로 가져옵니다.
        assistant_text += chunk.choices[0].delta.content or ""

    # 4) 반복문이 끝난 뒤 한 번만 말풍선에 렌더링
    st.markdown(
        f'<div class="chat-bubble assistant-bubble">{assistant_text}</div>',
        unsafe_allow_html=True
    )

    # 5) 최종 응답을 세션 히스토리에 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text}
    )