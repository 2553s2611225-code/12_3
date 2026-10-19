import random
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 디자인
# ==========================================
st.set_page_config(
    page_title="취미 모아 - 맞춤 여가 추천",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (심플하고 부드러운 UI)
CSS_CODE = """
<style>
.main {
    background-color: #f8f9fa;
}
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
</style>
"""
st.markdown(CSS_CODE, unsafe_allow_html=True)


# ==========================================
# 2. 데이터베이스 (총 20개 엄선 취미 데이터)
# ==========================================
HOBBIES = [
    # 🎨 그림 / 미술 (6개)
    {
        "id": "urban_sketch",
        "name": "어반 스케치 (Urban Sketching)",
        "category": "그림 / 미술",
        "location": "실외",
        "budget": "저렴 (2~5만원)",
        "companion": "혼자",
        "time": "1~2시간",
        "difficulty": "초급",
        "desc": "자신이 살고 있거나 여행 간 도시의 풍경, 카페, 거리를 펜과 수채화로 현장에서 직접 담아내는 드로잉입니다.",
        "prep": "워터브러시, 미니 수채화 키트, 드로잉 북",
        "steps": ["야외 카페나 공원 등 마음에 드는 스팟 찾기", "펜으로 윤곽선 빠르게 스케치하기", "워터브러시로 가볍게 색칠해 완성하기"]
    },
    {
        "id": "tablet_drawing",
        "name": "태블릿 디지털 드로잉",
        "category": "그림 / 미술",
        "location": "실내",
        "budget": "높음 (태블릿 소지 시 저렴)",
        "companion": "혼자",
        "time": "1시간",
        "difficulty": "초급",
        "desc": "프로크리에이트나 클립스튜디오 앱을 활용해 인물, 이모티콘, 굿즈 아트워크 등을 자유롭게 그립니다.",
        "prep": "태블릿 PC, 전용 펜슬, 드로잉 앱",
        "steps": ["기본 레이어와 브러시 개념 익히기", "유튜브 초보 튜토리얼 따라 그려보기", "나만의 캐릭터나 배경화면 만들기"]
    },
    {
        "id": "oil_pastel",
        "name": "오일 파스텔 드로잉",
        "category": "그림 / 미술",
        "location": "실내",
        "budget": "저렴 (2~5만원)",
        "companion": "혼자",
        "time": "1시간",
        "difficulty": "초급",
        "desc": "부드럽고 크리미한 질감이 특징으로, 손가락으로 문질러 꾸덕하고 감성적인 풍경화를 쉽게 만듭니다.",
        "prep": "오일 파스텔 세트, 찰색용 종이, 찰필",
        "steps": ["기본 24색 세트 구매하기", "노을빛 하늘이나 과일 등 간단한 소재 선택", "손가락으로 부드럽게 문질러 블렌딩하기"]
    },
    {
        "id": "acrylic_backdrop",
        "name": "아크릴 백드롭 페인팅",
        "category": "그림 / 미술",
        "location": "실내",
        "budget": "중간 (회당 4~7만원)",
        "companion": "함께",
        "time": "2시간",
        "difficulty": "초급",
        "desc": "모델링 페이스트와 아크릴 물감을 나이프로 섞어 캔버스에 질감 있는 추상화를 그리는 요즘 대세 원데이 클래스입니다.",
        "prep": "캔버스, 아크릴 물감, 나이프, 페이스트",
        "steps": ["원하는 인테리어 컬러 조합 정하기", "나이프로 질감을 살려 캔버스 칠하기", "잘 말려서 방에 인테리어 소품으로 걸어두기"]
    },
    {
        "id": "watercolor",
        "name": "투명 수채화 일러스트",
        "category": "그림 / 미술",
        "location": "실내",
        "budget": "저렴 (3~6만원)",
        "companion": "혼자",
        "time": "1~2시간",
        "difficulty": "중급",
        "desc": "물과 물감의 번짐을 이용해 맑고 투명한 감성을 표현합니다. 식물, 디저트 등을 그릴 때 제격입니다.",
        "prep": "수채화 물감, 붓, 수채화 전용 종이(300g)",
        "steps": ["물이 번지는 번지기 기법 연습하기", "단순한 잎사귀나 열매부터 스케치", "물조절 감각을 익히며 조심스럽게 채색하기"]
    },
    {
        "id": "oil_painting",
        "name": "오일 페인팅 (유화) 클래스",
        "category": "그림 / 미술",
        "location": "실내",
        "budget": "중간 (월 10~15만원)",
        "companion": "혼자",
        "time": "2~3시간",
        "difficulty": "중급",
        "desc": "깊이 있고 클래식한 서양화 기법으로, 느리지만 지속적인 덧칠을 통해 묵직하고 완성도 높은 작품을 남깁니다.",
        "prep": "성인 미술 화실 (재료 제공)",
        "steps": ["가까운 성인 미술 화실 탐색 및 등록", "기초 조색법과 캔버스 밑작업 배우기", "좋아하는 명화 모작이나 풍경화 완성하기"]
    },

    # ⚽ 운동 / 스포츠 (4개)
    {
        "id": "climbing",
        "name": "실내 클라이밍 (볼더링)",
        "category": "운동 / 스포츠",
        "location": "실내",
        "budget": "중간 (회당 2~3만원)",
        "companion": "혼자 또는 함께",
        "time": "1~2시간",
        "difficulty": "중급",
        "desc": "벽면의 홀드를 잡고 목표 지점까지 올라가는 전신 운동으로, 문제를 해결하는 재미가 뛰어납니다.",
        "prep": "암벽화, 초크 bags (암벽장 대여 가능)",
        "steps": ["실내 암벽장 일일 강습 신청", "기초 이동 자세 익히기", "초급 난이도 문제부터 하나씩 도전하기"]
    },
    {
        "id": "running",
        "name": "러닝 및 마라톤",
        "category": "운동 / 스포츠",
        "location": "실외",
        "budget": "저렴 (0~10만원)",
        "companion": "혼자",
        "time": "30분~1시간",
        "difficulty": "초급",
        "desc": "장비 부담 없이 즉시 시작할 수 있는 유산소 운동입니다. 심폐 지구력 향상과 스트레스 해소에 좋습니다.",
        "prep": "편안한 러닝화, 운동복",
        "steps": ["발에 맞는 쿠션감 좋은 러닝화 구매", "가까운 공원이나 러닝 코스 탐색", "20분 걷기와 뛰기를 반복하며 가볍게 시작"]
    },
    {
        "id": "yoga_pilates",
        "name": "요가 / 필라테스",
        "category": "운동 / 스포츠",
        "location": "실내",
        "budget": "중간 (월 10~20만원)",
        "companion": "혼자",
        "time": "1시간",
        "difficulty": "초급",
        "desc": "몸의 균형을 잡고 코어 근육을 강화하며 유연성을 높입니다. 마음의 안정에도 큰 도움을 줍니다.",
        "prep": "요가 매트, 편안한 운동복",
        "steps": ["유튜브의 초보자용 요가 영상 따라하기", "기초 호흡법과 스트레칭 자세 익히기", "매일 아침 10분 스트레칭 습관화하기"]
    },
    {
        "id": "tennis",
        "name": "실내 테니스 / 파델",
        "category": "운동 / 스포츠",
        "location": "실내",
        "budget": "중간 (월 15~25만원)",
        "companion": "함께",
        "time": "1~2시간",
        "difficulty": "중급",
        "desc": "빠른 코트 이동과 라켓 스트로크를 통해 칼로리 소모가 높으며 다이내믹한 주말 레저로 좋습니다.",
        "prep": "테니스 라켓, 테니스화",
        "steps": ["실내 테니스장 기초 레슨 등록", "기초 포핸드/백핸드 스윙 동작 배우기", "볼 머신기 활용해 스트로크 연습하기"]
    },

    # 🎵 음악 / 사운드 (3개)
    {
        "id": "ukulele",
        "name": "우쿨렐레 연주",
        "category": "음악 / 사운드",
        "location": "실내",
        "budget": "저렴 (5~15만원)",
        "companion": "혼자",
        "time": "30분~1시간",
        "difficulty": "초급",
        "desc": "기타보다 작고 줄이 4개뿐이라 입문이 매우 쉬운 아기자기한 악기입니다.",
        "prep": "우쿨렐레, 튜너",
        "steps": ["입문용 우쿨렐레 구매하기", "기본 C, G, Am, F 코드 잡기", "쉬운 가요 한 곡 완곡해보기"]
    },
    {
        "id": "lp_collecting",
        "name": "LP 음반 수집 및 감상",
        "category": "음악 / 사운드",
        "location": "실내",
        "budget": "높음 (20만원 이상)",
        "companion": "혼자",
        "time": "1시간 이상",
        "difficulty": "초급",
        "desc": "아날로그 특유의 따뜻하고 풍부한 음색을 즐깁니다. 커버 실물을 수집하고 장식하는 재미도 큽니다.",
        "prep": "턴테이블, LP 바이닐, 스피커",
        "steps": ["가까운 LP 카페 방문해 보기", "입문용 턴테이블 알아보기", "최애 아티스트의 첫 바이닐 구매하기"]
    },
    {
        "id": "kalimba",
        "name": "칼림바 (Hand Piano) 연주",
        "category": "음악 / 사운드",
        "location": "실내",
        "budget": "저렴 (2~4만원)",
        "companion": "혼자",
        "time": "30분",
        "difficulty": "초급",
        "desc": "손가락으로 쇠 건반을 튕겨 오르골 같은 영롱한 소리를 냅니다. 층간소음 부담이 전혀 없는 악기입니다.",
        "prep": "17키 칼림바, 조율 망치",
        "steps": ["기초 숫자 악보 읽는 법 배우기", "애니메이션 OST 연주해 보기", "맑은 울림을 들으며 힐링하기"]
    },

    # 🛠️ 공예 / 핸드메이드 (4개)
    {
        "id": "tufting",
        "name": "터프팅 (Tufting) 러그 만들기",
        "category": "공예 / 핸드메이드",
        "location": "실내",
        "budget": "중간 (회당 5~10만원)",
        "companion": "함께",
        "time": "3~4시간",
        "difficulty": "초급",
        "desc": "터프팅 건을 이용해 원단에 실을 쏘아 나만의 캐릭터 러그, 미니 거울, 소품을 만드는 감각적 공예입니다.",
        "prep": "원데이 클래스 예약",
        "steps": ["원하는 캐릭터나 무늬 도안 구상", "공방에서 터프팅 건 기본 작동법 스킬 익히기", "직접 실을 쏘아 실물 러그 완성하기"]
    },
    {
        "id": "pottery",
        "name": "도자기 물레 체험",
        "category": "공예 / 핸드메이드",
        "location": "실내",
        "budget": "중간 (회당 4~7만원)",
        "companion": "함께",
        "time": "2시간",
        "difficulty": "초급",
        "desc": "부드러운 흙의 촉감을 느끼며 집중력을 발휘해 나만의 컵, 접시, 화병 등을 정성껏 빚어냅니다.",
        "prep": "편안한 옷차림",
        "steps": ["도예 공방 체험 예약", "물레 위에서 중심을 잡고 형태 만들기", "가마 구이기 과정을 거쳐 3~4주 후 수령"]
    },
    {
        "id": "leather_craft",
        "name": "가죽 소품 (카드지갑) 만들기",
        "category": "공예 / 핸드메이드",
        "location": "실내",
        "budget": "중간 (회당 4~8만원)",
        "companion": "혼자 또는 함께",
        "time": "2~3시간",
        "difficulty": "초급",
        "desc": "천연 가죽을 직접 재단하고 전통 새들 스티치 바느질을 통해 오래 쓸 수 있는 나만의 지갑을 만듭니다.",
        "prep": "가죽 공방 원데이 재료",
        "steps": ["원하는 가죽 색상과 실 선택", "스티치 구멍 내기(치즐 작업)", "한 땀 한 땀 바느질하여 각인 넣기"]
    },
    {
        "id": "candle_making",
        "name": "소이 캔들 & 방향제 조향",
        "category": "공예 / 핸드메이드",
        "location": "실내",
        "budget": "저렴 (회당 3~5만원)",
        "companion": "함께",
        "time": "1~2시간",
        "difficulty": "초급",
        "desc": "천연 왁스와 오일을 조향해 은은한 향이 나는 캔들과 디퓨저, 석고 방향제를 제작합니다.",
        "prep": "캔들 공방 재료 제공",
        "steps": ["선호하는 오일 향 3가지 시향 및 블렌딩", "왁스 녹여 원하는 색소 첨가", "드라이플라워 올려서 오더메이드 디자인 완성"]
    },

    # 📚 문화 / 요리 / 라이프 (3개)
    {
        "id": "book_club",
        "name": "독서 모임 참여하기",
        "category": "문화 / 소셜",
        "location": "실내",
        "budget": "저렴 (1~3만원)",
        "companion": "함께",
        "time": "2시간",
        "difficulty": "초급",
        "desc": "같은 책을 읽고 다양한 사람들과 시각과 생각을 공유하며 깊이 있는 대화를 나누는 소모임 취미입니다.",
        "prep": "지정 도서, 메모장",
        "steps": ["소모임이나 문토 앱에서 모임 검색", "지정 도서 읽고 인상 깊은 구절 메모", "모임에 참석해 의견 나누기"]
    },
    {
        "id": "hand_drip",
        "name": "홈 핸드드립 커피",
        "category": "요리 / 가드닝",
        "location": "실내",
        "budget": "저렴 (5~10만원)",
        "companion": "혼자",
        "time": "30분",
        "difficulty": "초급",
        "desc": "다양한 산지의 원두를 직접 그라인딩하여 온도를 맞춘 물로 나만의 홈카페 커피를 내립니다.",
        "prep": "드립포트, 수동 그라인더, 원두, 필터",
        "steps": ["좋아하는 향미의 신선한 원두 준비", "알맞은 굵기로 원두 갈기", "뜸들이기와 드립 추출을 진행해 완벽한 커피 즐기기"]
    },
    {
        "id": "gardening",
        "name": "반려식물 홈 가드닝",
        "category": "요리 / 가드닝",
        "location": "실내",
        "budget": "저렴 (2~5만원)",
        "companion": "혼자",
        "time": "20분",
        "difficulty": "초급",
        "desc": "몬스테라, 스킨답서스 등 순한 식물들을 돌보며 마음의 휴식과 푸르름을 느낍니다.",
        "prep": "반려식물 화분, 분갈이 흙, 물뿌리개",
        "steps": ["우리 집 햇빛 환경에 맞는 식물 선택", "겉흙이 말랐을 때 적절히 물주기", "새 잎이 피어나는 과정 관찰하며 일기 작성"]
    }
]

# ==========================================
# 3. 사이드바 - 검색 및 필터 설정
# ==========================================
st.sidebar.title("🎨 취미 모아")
st.sidebar.caption("나에게 딱 맞는 여가 시간을 찾아보세요.")
st.sidebar.divider()

# 카테고리 선택
categories = ["전체"] + sorted(list(set(h["category"] for h in HOBBIES)))
selected_category = st.sidebar.selectbox("📂 카테고리 선택", categories)

# 상세 필터
st.sidebar.subheader("🎯 맞춤 조건 필터")
filter_location = st.sidebar.radio("장소", ["상관없음", "실내", "실외"], horizontal=True)
filter_companion = st.sidebar.radio("동반자", ["상관없음", "혼자", "함께"], horizontal=True)

st.sidebar.divider()

# Gemini AI 비서 섹션
st.sidebar.subheader("🤖 AI 취미 추천")
use_ai = st.sidebar.checkbox("Gemini AI 기반 맞춤 추천 받기")

# ==========================================
# 4. 메인 화면 구성
# ==========================================
st.title("🌱 새로운 여가 & 취미 추천")
st.write("일상의 지루함을 깨뜨릴 나만의 취미를 찾아보세요.")

# 조건 기반 필터링
filtered_hobbies = HOBBIES.copy()

if selected_category != "전체":
    filtered_hobbies = [h for h in filtered_hobbies if h["category"] == selected_category]

if filter_location != "상관없음":
    filtered_hobbies = [h for h in filtered_hobbies if h["location"] == filter_location]

if filter_companion != "상관없음":
    filtered_hobbies = [h for h in filtered_hobbies if h["companion"] in [filter_companion, "혼자 또는 함께"]]

# 상단: 무작위 추천 버튼
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"📌 추천 취미 리스트 ({len(filtered_hobbies)}개)")
with col2:
    if st.button("🎲 무작위 뽑기", use_container_width=True):
        if filtered_hobbies:
            random_hobby = random.choice(filtered_hobbies)
            st.toast(f"오늘의 추천: {random_hobby['name']}!", icon="✨")

# Gemini AI 처리
if use_ai:
    st.info("💡 AI 코치가 당신의 상황에 딱 맞는 독창적인 취미를 제안합니다.")
    user_prompt = st.text_input("현재 기분이나 관심사를 적어주세요. (예: 그림 그리는 걸 좋아하지만 똥손이라 걱정돼)", "")
    
    if st.button("AI 맞춤 분석 실행", type="primary"):
        if not user_prompt:
            st.warning("기분이나 상태를 입력해 주세요!")
        else:
            try:
                from google import genai
                
                api_key = st.secrets.get("GEMINI_API_KEY")
                if not api_key:
                    st.error("🔑 Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
                else:
                    client = genai.Client(api_key=api_key)
                    
                    with st.spinner("AI가 최적의 취미를 찾고 있습니다..."):
                        prompt_text = f"사용자 상태: '{user_prompt}'. 이 사용자에게 어울리는 그림/미술, 운동, 음악, 공예 등의 분야 중 구체적인 취미 2가지를 추천해줘. 각 취미별로 이름, 추천 이유, 시작하는 법 1줄을 친절하게 작성해줘."
                        response = client.models.generate_content(
                            model="gemini-2.5-flash-lite",
                            contents=prompt_text
                        )
                        
                        st.markdown("---")
                        st.markdown("### 🤖 Gemini AI 추천 결과")
                        st.write(response.text)
                        st.markdown("---")
            except Exception as e:
                st.error(f"AI 추천을 가져오는 중 오류가 발생했습니다: {e}")

# 취미 목록 출력
if not filtered_hobbies:
    st.warning("선택하신 조건에 맞는 취미가 없습니다. 필터를 변경해 보세요!")
else:
    for hobby in filtered_hobbies:
        card_html = f"""
        <div class="hobby-card">
            <h3>{hobby['name']}</h3>
            <div>
                <span class="tag">📁 {hobby['category']}</span>
                <span class="tag">📍 {hobby['location']}</span>
                <span class="tag">👥 {hobby['companion']}</span>
                <span class="tag">💰 {hobby['budget']}</span>
                <span class="tag">⏱️ {hobby['time']}</span>
            </div>
            <p style="margin-top: 12px; color: #4b5563;">{hobby['desc']}</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        with st.expander(f"🔍 {hobby['name']} 상세 가이드 & 도전하기"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**🎒 필요 준비물**")
                st.info(hobby['prep'])
            with c2:
                st.write("**📊 난이도**")
                st.caption(f"난이도 수준: {hobby['difficulty']}")
            
            st.divider()
            
            # --- 시작하는 3단계 (체크리스트 + 진행도) ---
            st.write("**🚀 시작하는 3단계 체크리스트**")
            
            # 체크 해제/체크 상태 관리
            completed_count = 0
            total_steps = len(hobby['steps'])
            
            for idx, step in enumerate(hobby['steps'], 1):
                key = f"chk_{hobby['id']}_{idx}"
                # 체크박스 생성
                is_checked = st.checkbox(f"{idx}단계: {step}", key=key)
                if is_checked:
                    completed_count += 1
            
            # 진행도 calculation & progress bar
            progress_ratio = completed_count / total_steps
            st.progress(progress_ratio)
            
            # 진행 상태 텍스트
            if completed_count == total_steps:
                st.success(f"🎉 축하합니다! {hobby['name']} 입문 준비가 완료되었습니다!")
            else:
                st.caption(f"진행도: {completed_count}/{total_steps} 단계 완료 ({int(progress_ratio * 100)}%)")

st.markdown("---")
st.caption("© 2026 취미 모아 - Streamlit으로 제작된 부드럽고 가벼운 여가 추천 앱")
