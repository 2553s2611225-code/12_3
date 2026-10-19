import random
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 디자인 (Simple & Soft UI)
# ==========================================
st.set_page_config(
    page_title="취미 모아 - 맞춤 여가 추천",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (심플하고 부드러운 UI)
st.markdown("""
    <style>
    /* 메인 배경 및 폰트 깔끔하게 */
    .main {
        background-color: #f8f9fa;
    }
    
    /* 카드 스타일링 */
    .hobby-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }
    .hobby-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    
    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background-color: #eef2ff;
        color: #4f46e5;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 8px;
    }
    
    /* 팁 박스 */
    .tip-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 12px 16px;
        border-radius: 4px;
        margin-top: 10px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 데이터베이스 (기본 취미 데이터)
# ==========================================
HOBBIES = [
    # 운동 / 스포츠
    {
        "name": "실내 클라이밍 ( 볼더링 )",
        "category": "운동 / 스포츠",
        "location": "실내",
        "budget": "중간 (회당 2~3만원)",
        "companion": "혼자 또는 함께",
        "time": "1~2시간",
        "difficulty": "중급",
        "desc": "벽면의 홀드를 잡고 목표 지점까지 올라가는 전신 운동입니다. 문제 해결의 재미와 성취감이 뛰어납니다.",
        "prep": "암벽화, 초크 bags (클라이밍장에서 대여 가능)",
        "steps": ["가까운 실내 암벽장 방문하기", "일일 강습 신청하여 안전 수칙 익히기", "쉬운 난이도(초보자용 문제)부터 차근차근 도전하기"]
    },
    {
        "name": "러닝 및 마라톤",
        "category": "운동 / 스포츠",
        "location": "실외",
        "budget": "저렴 (0~10만원)",
        "companion": "혼자",
        "time": "30분~1시간",
        "difficulty": "초급",
        "desc": "장비 부담 없이 즉시 시작할 수 있는 유산소 운동입니다. 심폐 지구력 향상과 스트레스 해소에 좋습니다.",
        "prep": "편안한 러닝화, 운동복",
        "steps": ["발에 맞는 러닝화 구매하기", "가까운 공원이나 러닝 코스 탐색하기", "20분 걷기와 뛰기를 반복하며 가볍게 시작하기"]
    },
    {
        "name": "요가 / 필라테스",
        "category": "운동 / 스포츠",
        "location": "실내",
        "budget": "중간 (월 10~20만원)",
        "companion": "혼자",
        "time": "1시간",
        "difficulty": "초급",
        "desc": "몸의 균형을 잡고 코어 근육을 강화하며 유연성을 높이는 운동입니다. 마음의 안정에도 도움을 줍니다.",
        "prep": "요가 매트, 편안한 운동복",
        "steps": ["유튜브의 초보자용 요가 영상 따라하기", "체형 교정이나 자세 관찰을 위해 스튜디오 체험 수업 들어보기", "매일 아침 10분 스트레칭 습관 만들기"]
    },
    
    # 음악 / 사운드
    {
        "name": "우쿨렐레 연주",
        "category": "음악 / 사운드",
        "location": "실내",
        "budget": "저렴 (5~15만원)",
        "companion": "혼자",
        "time": "30분~1시간",
        "difficulty": "초급",
        "desc": "기타보다 크기가 작고 줄이 4개뿐이라 입문이 매우 쉬운 현악기입니다. 밝고 경쾌한 소리가 특징입니다.",
        "prep": "소프라노 또는 콘서트 우쿨렐레, 튜너",
        "steps": ["입문용 우쿨렐레 준비하기", "기본 4가지 코드(C, G, Am, F) 연습하기", "쉬운 가요나 동요 한 곡 완곡해보기"]
    },
    {
        "name": "LP 음반 수집 및 감상",
        "category": "음악 / 사운드",
        "location": "실내",
        "budget": "높음 (20만원 이상)",
        "companion": "혼자",
        "time": "1시간 이상",
        "difficulty": "초급",
        "desc": "아날로그 특유의 따뜻하고 풍부한 음색을 즐기는 취미입니다. 앨범 커버를 수집하는 재미도 있습니다.",
        "prep": "턴테이블, LP 바이닐, 스피커",
        "steps": ["가까운 LP 카페나 레코드 숍 방문해보기", "입문용 일체형/입문형 턴테이블 알아보기", "좋아하는 아티스트의 LP 1장 구매하기"]
    },

    # 공예 / 디자인
    {
        "name": "터프팅 (Tufting) 카페 카펫 만들기",
        "category": "공예 / 디자인",
        "location": "실내",
        "budget": "중간 (회당 5~10만원)",
        "companion": "함께",
        "time": "3~4시간",
        "difficulty": "초급",
        "desc": "터프팅 건을 이용해 원단에 실을 쏘아 자신만의 터프팅 러그나 거울, 소품을 만드는 시각적/감각적 공예입니다.",
        "prep": "원데이 클래스 예약 (장비 및 재료 제공)",
        "steps": ["만들고 싶은 도안 구상하기", "공방 원데이 클래스 예약하기", "직접 실을 쏘아 나만의 카펫 완성하기"]
    },
    {
        "name": "도자기 물레 체험",
        "category": "공예 / 디자인",
        "location": "실내",
        "budget": "중간 (회당 4~7만원)",
        "companion": "함께",
        "time": "2시간",
        "difficulty": "초급",
        "desc": "흙의 촉감을 느끼며 집중력을 발휘해 나만의 컵, 접시, 화병 등을 만드는 정성 어린 취미입니다.",
        "prep": "편안한 복장 (흙이 묻어도 되는 옷)",
        "steps": ["도예 공방 원데이 클래스 찾기", "물레로 그릇 모양 빚어보기", "가마 구이기 과정을 거쳐 3~4주 후 완성품 수령하기"]
    },

    # 예술 / 문화
    {
        "name": "오일 파스텔 드로잉",
        "category": "예술 / 문화",
        "location": "실내",
        "budget": "저렴 (2~5만원)",
        "companion": "혼자",
        "time": "1시간",
        "difficulty": "초급",
        "desc": "부드럽고 질감이 살아있는 그림을 그릴 수 있는 재료입니다. 손으로 문지르는 기법이 쉽고 표현력이 좋습니다.",
        "prep": "오일 파스텔 세트, 찰색용 종이(스케치북), 찰필",
        "steps": ["기본 오일 파스텔 24색 세트 구매하기", "풍경이나 과일 등 쉬운 사진 따라 그려보기", "블렌딩(문지르기) 기법 익히기"]
    },
    {
        "name": "독서 모임 참여하기",
        "category": "예술 / 문화",
        "location": "실내",
        "budget": "저렴 (1~3만원)",
        "companion": "함께",
        "time": "2시간",
        "difficulty": "초급",
        "desc": "같은 책을 읽고 다양한 사람들과 시각과 생각을 공유하며 깊이 있는 소통을 즐기는 취미입니다.",
        "prep": "지정 도서, 메모장",
        "steps": ["소모임이나 문토, 소셜 클럽 앱에서 관심 독서모임 검색하기", "지정 도서 정독하고 나만의 생각 정리해보기", "모임에 참여하여 자유롭게 이야기 나누기"]
    }
]

# ==========================================
# 3. 사이드바 - 검색 및 필터 설정
# ==========================================
st.sidebar.title("🎨 취미 모아")
st.sidebar.caption("나에게 딱 맞는 여가 시간을 찾아보세요.")
st.sidebar.divider()

# 카테고리 선택
categories = ["전체"] + list(set(h["category"] for h in HOBBIES))
selected_category = st.sidebar.selectbox("📂 카테고리 선택", categories)

# 상세 필터
st.sidebar.subheader("🎯 맞춤 조건 필터")
filter_location = st.sidebar.radio("장소", ["상관없음", "실내", "실외"], horizontal=True)
filter_companion = st.sidebar.radio("동반자", ["상관없음", "혼자", "함께"], horizontal=True)

st.sidebar.divider()

# Gemini AI 비서 섹션 (선택적)
st.sidebar.subheader("🤖 AI 취미 추천")
use_ai = st.sidebar.checkbox("Gemini AI 기반 맞춤 추천 받기")

# ==========================================
# 4. 메인 화면 구성
# ==========================================
st.title("🌱 새로운 여가 & 취미 추천")
st.write("일상의 지루함을 깨뜨릴 나만의 취미를 찾아보세요.")

# ----- 조건 기반 데이터 필터링 -----
filtered_hobbies = HOBBIES.copy()

if selected_category != "전체":
    filtered_hobbies = [h for h in filtered_hobbies if h["category"] == selected_category]

if filter_location != "상관없음":
    filtered_hobbies = [h for h in filtered_hobbies if h["location"] == filter_location]

if filter_companion != "상관없음":
    filtered_hobbies = [h for h in filtered_hobbies if h["companion"] in [filter_companion, "혼자 또는 함께"]]

# ----- 상단: 랜덤 한 줄 추천 버튼 -----
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"📌 추천 취미 리스트 ({len(filtered_hobbies)}개)")
with col2:
    if st.button("🎲 무작위 뽑기", use_container_width=True):
        if filtered_hobbies:
            random_hobby = random.choice(filtered_hobbies
                                        
