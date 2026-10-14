import datetime
import json
import os
import random
import streamlit as st

# Gemini API 라이브러리 예외 처리 임포트
try:
  import google.generativeai as genai

  GEMINI_AVAILABLE = True
except ImportError:
  GEMINI_AVAILABLE = False

# 페이지 기본 설정
st.set_page_config(
    page_title="마음 돌봄 토닥토닥 퀘스트", page_icon="🌱", layout="centered"
)

# 화면 스타일링 (CSS)
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 데이터 저장 파일 경로
DATA_FILE = "quest_data.json"


def load_data():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except Exception:
      pass
  return {"streak": 0, "last_completed_date": "", "history": {}}


def save_data(data):
  try:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=4)
  except Exception as e:
    st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")


# 세션 상태 초기화
if "app_data" not in st.session_state:
  st.session_state.app_data = load_data()

# 기본 퀘스트 풀
DEFAULT_QUESTS = [
    {"id": 1, "task": "따스한 햇살 느끼며 가벼운 산책 5분 하기", "category": "신체 활력"},
    {"id": 2, "task": "오늘 나를 칭찬하고 싶은 점 3가지 적어보기", "category": "자존감 회복"},
    {"id": 3, "task": "좋아하는 음악을 들으며 깊게 심호흡 3번 하기", "category": "정서 안정"},
    {"id": 4, "task": "오늘 하루 중 가장 편안했던 순간 기록하기", "category": "마음 돌봄"},
    {"id": 5, "task": "따뜻한 물 한 잔 마시며 온전히 쉬어보기", "category": "자기 돌봄"},
    {"id": 6, "task": "나에게 힘이 되는 따뜻한 한마디 건네기", "category": "마음 돌봄"},
]

today_str = datetime.date.today().strftime("%Y-%m-%d")
history = st.session_state.app_data["history"]

# 오늘 날짜의 퀘스트가 없으면 랜덤으로 3개 할당
if today_str not in history:
  selected = random.sample(DEFAULT_QUESTS, 3)
  history[today_str] = {
      "quests": [{"id": q["id"], "task": q["task"], "category": q["category"], "completed": False} for q in selected],
      "ai_message": "",
  }
  save_data(st.session_state.app_data)

# 헤더 영역
st.title("🌱 마음 돌봄 토닥토닥 퀘스트")
st.write(
    "오늘 하루, 나를 위한 따뜻한 행동들로 마음의 힘을 채워보세요. 당신은 혼자가 아니며, 충분히 소중한 사람입니다."
)
st.markdown("---")

# 오늘의 퀘스트 진행 상황
st.subheader(f"📅 오늘의 퀘스트 ({today_str})")
today_quests = history[today_str]["quests"]

completed_count = sum(1 for q in today_quests if q["completed"])
total_count = len(today_quests)
progress_ratio = completed_count / total_count if total_count > 0 else 0

# 실시간 달성률 시각화
st.markdown("### 📊 실시간 달성률")
st.progress(progress_ratio)
st.metric(
    label="오늘의 완료율",
    value=f"{int(progress_ratio * 100)}%",
    delta=f"{completed_count}/{total_count} 완료",
)

st.markdown("---")

# 체크박스 리스트
st.subheader("✨ 오늘의 실천 목록")
for i, q in enumerate(today_quests):
  is_checked = st.checkbox(
      f"**[{q['category']}]** {q['task']}",
      value=q["completed"],
      key=f"quest_{today_str}_{i}",
  )
  if is_checked != q["completed"]:
    today_quests[i]["completed"] = is_checked
    save_data(st.session_state.app_data)
    st.rerun()

# 연속 실천일(Streak) 계산 로직
all_done = total_count > 0 and all(q["completed"] for q in today_quests)
if all_done:
  last_date = st.session_state.app_data.get("last_completed_date", "")
  yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

  if last_date != today_str:
    if last_date == yesterday_str:
      st.session_state.app_data["streak"] += 1
    elif last_date == "":
      st.session_state.app_data["streak"] = 1
    elif last_date != today_str:
      st.session_state.app_data["streak"] = 1

    st.session_state.app_data["last_completed_date"] = today_str
    save_data(st.session_state.app_data)

# 통계 지표 표시
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
  st.metric(
      label="🔥 연속 실천 일수 (Streak)",
      value=f"{st.session_state.app_data['streak']}일째",
  )
with col2:
  st.metric(label="🌟 누적 참여일", value=f"{len(history)}일")

# AI 따뜻한 위로 응원 메시지 (Gemini 연동)
st.markdown("---")
st.subheader("💬 따뜻한 위로와 응원 한마디")

if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] and GEMINI_AVAILABLE:
  if not history[today_str]["ai_message"]:
    try:
      genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
      model = genai.GenerativeModel("gemini-2.5-flash-lite")

      prompt = f"""
            사용자가 오늘 따돌림이나 정서적 불안을 이겨내기 위해 마음 돌봄 퀘스트를 진행 중입니다.
            오늘 완료한 퀘스트 수는 {completed_count}/{total_count}개입니다.
            사용자에게 따뜻하고 진심 어린 위로, 그리고 지치지 않도록 다정하게 격려해주는 3줄 이내의 응원 메시지를 한국어로 작성해주세요.
            부담스럽지 않고 포근한 어조로 부탁합니다.
            """
      response = model.generate_content(prompt)
      history[today_str]["ai_message"] = response.text
      save_data(st.session_state.app_data)
    except Exception as e:
      history[today_str]["ai_message"] = (
          "오늘 하루도 정말 애썼어요. 당신의 존재 자체로 소중합니다. 작은 걸음이지만 천천히 함께 나아가봐요."
      )

  st.info(history[today_str]["ai_message"])
else:
  st.info(
      "🌿 오늘 하루도 정말 수고 많았어요. 당신은 그 자체로 빛나고 소중한 사람입니다. 천천히, 내 속도대로 나아가면 돼요."
  )
  if not GEMINI_AVAILABLE or "GEMINI_API_KEY" not in st.secrets:
    st.caption(
        "(참고: `GEMINI_API_KEY`가 설정되지 않았거나 라이브러리가 없어 기본"
        " 위로 메시지가 출력됩니다.)"
    )

# 푸터 안내
st.markdown("---")
st.caption(
    "💡 이 앱은 마음의 안정을 찾고 작은 성취감을 통해 회복을 돕기 위해"
    " 만들어졌습니다. 언제나 당신을 응원합니다."
)
