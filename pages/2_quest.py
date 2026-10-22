import json
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

# 마음 한 걸음 — Streamlit Community Cloud용 간단한 퀘스트 앱
# 참고: Community Cloud의 로컬 파일은 영구 저장이 보장되지 않습니다.
# 공개 다중 사용자 서비스에서는 사용자별 인증과 외부 DB를 추가하세요.

st.set_page_config(
    page_title="마음 한 걸음 | 일일 퀘스트",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "quest_records.json"

QUESTS = [
    {"id": "walk", "title": "하루 5분 걷기", "description": "가능하다면 잠깐 바깥 공기를 쐬거나 실내에서 가볍게 움직여요.", "category": "몸 돌보기"},
    {"id": "strengths", "title": "나의 장점 5가지", "description": "작은 장점도 괜찮아요. 하나만 적어도 충분해요.", "category": "나를 알아가기"},
    {"id": "diary", "title": "오늘의 일기", "description": "오늘 있었던 일을 한두 문장으로 기록해요.", "category": "마음 정리"},
    {"id": "good_moment", "title": "좋았던 순간 기록", "description": "아주 사소한 순간이라도 괜찮아요. 기억하고 싶은 일을 떠올려요.", "category": "작은 기쁨"},
    {"id": "breathing", "title": "천천히 숨 고르기", "description": "편안한 자세로 잠깐 쉬면서 호흡에 집중해요.", "category": "마음 돌보기"},
    {"id": "kind_words", "title": "나에게 다정한 말", "description": "친구에게 해줄 법한 따뜻한 말을 나에게도 건네요.", "category": "자기 응원"},
    {"id": "water", "title": "물 한 잔 마시기", "description": "잠깐 멈춰 물을 마시며 나를 돌봐요.", "category": "몸 돌보기"},
    {"id": "pause", "title": "좋아하는 것 5분 하기", "description": "음악 듣기, 그림 그리기 등 내가 편안한 일을 해봐요.", "category": "회복 시간"},
    {"id": "boundary", "title": "오늘의 감정 알아차리기", "description": "지금 느끼는 감정을 판단하지 않고 이름 붙여봐요.", "category": "마음 정리"},
    {"id": "thanks", "title": "고마웠던 일 하나", "description": "누군가 또는 나 자신에게 고마웠던 일을 떠올려요.", "category": "작은 기쁨"},
    {"id": "rest", "title": "쉬는 시간 5분 갖기", "description": "아무것도 해내지 않아도 되는 짧은 휴식 시간을 가져요.", "category": "회복 시간"},
    {"id": "support", "title": "믿을 만한 사람 떠올리기", "description": "필요할 때 이야기할 수 있는 사람이나 도움받을 곳을 생각해요.", "category": "연결하기"},
]

CSS = """
<style>
:root { color-scheme: light; }

/* 이미지의 분홍, 주황, 보라 노을빛 느낌을 반영한 부드러운 배경 연출 */
.stApp {
  background:
    radial-gradient(circle at 85% 15%, rgba(255, 182, 193, 0.45) 0%, transparent 40%),
    radial-gradient(circle at 15% 75%, rgba(200, 162, 235, 0.35) 0%, transparent 45%),
    linear-gradient(135deg, #fce4ec 0%, #f3e5f5 45%, #fff3e0 100%);
  background-attachment: fixed;
}

.block-container { max-width: 1120px; padding-top: 1.4rem; padding-bottom: 2.2rem; }

/* 히어로 세션 - 석양빛 하늘과 어우러지는 반투명 글래스모피즘 분위기 */
.hero {
  background: linear-gradient(135deg, rgba(255, 209, 227, 0.85) 0%, rgba(225, 190, 231, 0.85) 50%, rgba(255, 224, 178, 0.85) 100%);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 34px;
  padding: 26px 28px 24px;
  box-shadow: 0 14px 35px rgba(216, 112, 147, 0.15);
  backdrop-filter: blur(8px);
}

.top-title {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 240, 245, 0.9) 100%);
  border: 1px solid #f3c4d3; border-radius: 12px;
  text-align: center; color: #5c3c52; padding: 11px 12px;
  font-weight: 750; letter-spacing: .045em; margin: 0 auto 20px;
  max-width: 620px; box-shadow: 0 2px 0 rgba(255,255,255,.9) inset, 0 4px 10px rgba(186, 104, 129, 0.1);
}

.intro-pill {
  background: rgba(255, 255, 255, 0.65); border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 16px; padding: 12px 16px; margin-bottom: 20px; color: #584153;
}

.quest-card {
  border: 1px solid rgba(255,255,255,0.8); border-radius: 18px;
  min-height: 154px; padding: 17px 15px 13px; color: #4a3e4e;
  box-shadow: 0 9px 18px rgba(186, 104, 129, 0.1);
  margin-bottom: 9px; position: relative; overflow: hidden;
}
.quest-card:before {
  content: ""; position: absolute; left: 13px; right: 13px; top: 7px;
  height: 7px; background: rgba(255, 255, 255, 0.6); border-radius: 99px;
}

/* 이미지 계열에 어울리는 소프트 일몰 컬러 파렛트 */
.quest-card.yellow { background: linear-gradient(145deg, #ffe0b2 0%, #ffcc80 100%); color: #4e342e; }
.quest-card.pink { background: linear-gradient(145deg, #f8bbd0 0%, #f48fb1 100%); color: #4a148c; }
.quest-card.blue { background: linear-gradient(145deg, #e1bee7 0%, #ce93d8 100%); color: #311b92; }
.quest-card.mint { background: linear-gradient(145deg, #ffd180 0%, #ffab40 100%); color: #3e2723; }

.quest-title { font-size: 1.06rem; font-weight: 800; margin: 8px 0 7px; line-height: 1.25; }
.quest-desc { font-size: .86rem; line-height: 1.45; min-height: 42px; }
.quest-tag { font-size: .72rem; opacity: .88; margin-top: 8px; font-weight: 650; }

.metric-card {
  background: rgba(255, 255, 255, 0.85); border: 1px solid #f8bbd0; border-radius: 28px;
  padding: 18px 14px; text-align: center; margin: 10px 0 16px;
  box-shadow: 0 10px 24px rgba(216, 112, 147, 0.12);
  backdrop-filter: blur(4px);
}
.metric-label { font-size: .9rem; color: #7b5e78; font-weight: 750; }
.metric-value { font-size: 2rem; font-weight: 850; color: #ba68c8; margin-top: 5px; letter-spacing: -.03em; }
.metric-emoji { font-size: 1.35rem; margin-bottom: 4px; }
.small-note { color: #6a4c68; font-size: .9rem; }

div[data-testid="stCheckbox"] label { font-size: .92rem; color: #4a3e4e; }
div.stButton > button {
  border-radius: 14px; min-height: 2.8rem; font-weight: 700;
  border: 1px solid rgba(225, 190, 231, 0.6);
  box-shadow: 0 4px 10px rgba(186, 104, 129, 0.08);
}
div[data-testid="stProgressBar"] > div { border-radius: 99px; }
div[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #f48fb1, #ba68c8); border-radius: 99px; }
div[data-testid="stExpander"] { background: rgba(255, 255, 255, 0.8); border-radius: 16px; border: 1px solid #f8bbd0; }

@media (max-width: 700px) {
  .block-container { padding-left: .7rem; padding-right: .7rem; }
  .hero { padding: 17px 12px; border-radius: 24px; }
  .quest-card { min-height: 170px; padding: 14px 11px 10px; }
  .quest-title { font-size: .98rem; }
  .quest-desc { font-size: .82rem; }
  .metric-card { padding: 14px 8px; border-radius: 22px; }
  .metric-value { font-size: 1.6rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def read_records():
    """저장 파일을 안전하게 읽습니다. 파일이 없거나 손상되면 빈 기록으로 시작합니다."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            return {}
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, TypeError):
        return {}


def write_records(records):
    """기록 저장 실패가 앱 전체 오류로 이어지지 않도록 처리합니다."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        temp_file = DATA_FILE.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        temp_file.replace(DATA_FILE)
        return True
    except OSError:
        return False


def get_today_quests(day_string):
    """날짜별 기본 퀘스트 4개를 일정하게 선택합니다."""
    rng = random.Random(day_string)
    return rng.sample(QUESTS, 4)


def calculate_streak(completed_dates, today):
    """오늘 실천했으면 오늘부터, 아직 실천 전이면 어제부터 연속 기록을 셉니다."""
    done = set(completed_dates)
    cursor = today
    if cursor.isoformat() not in done:
        cursor = today - timedelta(days=1)
    streak = 0
    while cursor.isoformat() in done:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


today = date.today()
today_key = today.isoformat()

# 익명 세션 키: 앱이 열려 있는 동안 기록을 구분합니다.
if "session_key" not in st.session_state:
    st.session_state.session_key = uuid.uuid4().hex
if "quest_override" not in st.session_state:
    st.session_state.quest_override = {}

records = read_records()
user_key = st.session_state.session_key
user_record = records.get(user_key, {"days": {}})
if not isinstance(user_record, dict):
    user_record = {"days": {}}
days = user_record.setdefault("days", {})

if today_key not in days:
    days[today_key] = {"quests": [q["id"] for q in get_today_quests(today_key)], "completed": []}

today_data = days[today_key]
if st.session_state.quest_override.get(today_key):
    today_data["quests"] = st.session_state.quest_override[today_key]
    valid_ids = set(today_data["quests"])
    today_data["completed"] = [q for q in today_data.get("completed", []) if q in valid_ids]

quest_by_id = {q["id"]: q for q in QUESTS}
selected_quests = [quest_by_id[qid] for qid in today_data.get("quests", []) if qid in quest_by_id]
completed = set(today_data.get("completed", []))

# 헤더와 안내
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="top-title">🌱 마음 한 걸음 · 일일 퀘스트</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="intro-pill"><strong>오늘의 작은 목표</strong><br>'
    '<span class="small-note">완벽하게 해내는 것보다, 나를 위해 작은 한 걸음을 내딛는 것이 중요해요.</span></div>',
    unsafe_allow_html=True,
)

left, right = st.columns([2.15, 1], gap="large")
with left:
    card_cols = st.columns(2, gap="medium")
    new_completed = set(completed)
    for idx, quest in enumerate(selected_quests):
        with card_cols[idx % 2]:
            is_done = quest["id"] in completed
            status = "✓ 완료했어요" if is_done else "오늘의 작은 도전"
            card_colors = ["yellow", "pink", "blue", "mint"]
            card_color = card_colors[idx % len(card_colors)]
            st.markdown(
                f'<div class="quest-card {card_color}"><div class="quest-title">{quest["title"]}</div>'
                f'<div class="quest-desc">{quest["description"]}</div>'
                f'<div class="quest-tag">{quest["category"]} · {status}</div></div>',
                unsafe_allow_html=True,
            )
            checked = st.checkbox(
                "완료 표시",
                value=is_done,
                key=f"done_{today_key}_{quest['id']}",
                help="완료 표시를 바꾸면 기록에 자동 저장됩니다.",
            )
            if checked:
                new_completed.add(quest["id"])
            else:
                new_completed.discard(quest["id"])

    today_data["completed"] = [qid for qid in today_data["quests"] if qid in new_completed]
    completed_count = len(today_data["completed"])
    total_count = len(selected_quests)
    completion_rate = int(round(completed_count / total_count * 100)) if total_count else 0

    st.progress(completion_rate / 100 if total_count else 0)
    st.caption(f"오늘 {total_count}개 중 {completed_count}개 완료 · 달성률 {completion_rate}%")

    b1, b2 = st.columns([1, 1])
    with b1:
        if st.button("🎲 퀘스트 다시 뽑기", use_container_width=True):
            old_done = set(today_data.get("completed", []))
            new_quests = random.sample(QUESTS, 4)
            st.session_state.quest_override[today_key] = [q["id"] for q in new_quests]
            today_data["quests"] = [q["id"] for q in new_quests]
            # 새로 뽑은 퀘스트는 새로 시작하도록 완료 상태를 초기화합니다.
            today_data["completed"] = []
            records[user_key] = user_record
            if write_records(records):
                st.toast("새로운 퀘스트를 준비했어요.")
            st.rerun()
    with b2:
        if st.button("오늘 기록 저장", use_container_width=True, type="primary"):
            records[user_key] = user_record
            if write_records(records):
                st.success("오늘의 기록을 저장했어요.")
            else:
                st.warning("현재 환경에서 파일을 저장하지 못했어요. 앱 관리자에게 알려주세요.")

with right:
    st.markdown('<div class="metric-card"><div class="metric-emoji">📈</div><div class="metric-label">일일 퀘스트 달성률</div>'
                f'<div class="metric-value">{completion_rate}<span style="font-size:1rem">%</span></div></div>', unsafe_allow_html=True)
    streak_value = calculate_streak([d for d, v in days.items() if v.get("completed")], today)
    st.markdown('<div class="metric-card"><div class="metric-emoji">🌱</div><div class="metric-label">연속 실천일</div>'
                f'<div class="metric-value">{streak_value}<span style="font-size:1rem">일</span></div></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="metric-card"><div class="metric-emoji">💗</div><div class="metric-label">오늘의 응원</div>'
                '<div style="margin-top:8px; line-height:1.55; color:#6a4c68;">천천히 가도 괜찮아요.<br>쉬어가는 날도 과정의 일부예요.</div></div>',
                unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 완료 상태를 자동 저장합니다.
records[user_key] = user_record
if not write_records(records):
    st.warning("기록 파일을 저장하지 못했습니다. 배포 환경의 쓰기 권한을 확인해 주세요.")

with st.expander("📅 지난 기록 보기"):
    dated_records = sorted(days.items(), reverse=True)
    if not dated_records:
        st.info("아직 기록이 없어요. 오늘의 퀘스트부터 시작해 보세요.")
    else:
        for day, data in dated_records[:14]:
            ids = data.get("quests", [])
            done_ids = set(data.get("completed", []))
            count = len([qid for qid in ids if qid in done_ids])
            total = len(ids)
            rate = int(round(count / total * 100)) if total else 0
            st.write(f"**{day}** — {count}/{total}개 완료 ({rate}%)")

st.caption("이 앱은 자기 돌봄을 돕는 도구이며, 괴롭힘이나 심리적 어려움을 혼자 견디라는 뜻은 아니에요. 힘들다면 믿을 수 있는 어른이나 상담 전문가에게 도움을 요청해도 괜찮아요.")
