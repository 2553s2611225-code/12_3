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

/* 이미지 계열에 어울리는 소프트 일
