
import streamlit as st

st.set_page_config(
    page_title="마음 쉼터",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #F7F8F1;
    font-family: 'Noto Sans KR', sans-serif;
    color: #304334;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: #B9D8AB;
    border: 1px solid #96BA8A;
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 24px;
}

.hero-label {
    font-size: 14px;
    font-weight: 700;
    color: #496B46;
    margin-bottom: 12px;
}

.hero h1 {
    color: #29462D;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.5;
    margin: 0 0 10px 0;
}

.hero p {
    color: #3F6043;
    font-size: 15px;
    line-height: 1.9;
    margin: 0;
}

.intro {
    font-size: 22px;
    font-weight: 800;
    color: #38563A;
    margin: 24px 0 6px 0;
}

.subintro {
    font-size: 14px;
    color: #738071;
    line-height: 1.8;
    margin-bottom: 20px;
}

.nav-card {
    border-radius: 20px;
    padding: 22px 18px;
    min-height: 175px;
    margin-bottom: 10px;
    border: 1px solid rgba(65, 90, 60, 0.12);
}

.nav-card h3 {
    font-size: 19px;
    margin: 0 0 12px 0;
    font-weight: 800;
}

.nav-card p {
    font-size: 13px;
    line-height: 1.8;
    margin: 0;
}

.green { background: #DCEBCF; color: #35543A; }
.blue { background: #DFE8F5; color: #3B5270; }
.yellow { background: #F3E7D0; color: #6B5637; }
.pink { background: #F2E1E4; color: #704A53; }

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 43px;
    font-weight: 600;
    border: 1px solid #C8D9BF;
    background: #FFFFFF;
    color: #3E6040;
}

div.stButton > button:hover {
    background: #E6EFDF;
    border-color: #8EAF82;
    color: #29462D;
}

.footer {
    text-align: center;
    color: #7B8977;
    font-size: 12px;
    line-height: 1.9;
    padding: 25px 0 8px 0;
}

@media (max-width: 640px) {
    .hero { padding: 23px; }
    .hero h1 { font-size: 27px; }
    .nav-card { min-height: 150px; padding: 16px; }
}
</style>
""", unsafe_allow_html=True)


# 메인 소개 영역
st.markdown("""
<div class="hero">
    <div class="hero-label">🌿 마음 쉼터</div>
    <h1>당신의 마음이 쉬어 가는 곳</h1>
    <p>
        따돌림으로 힘들었던 마음, 혼자 간직하지 않아도 괜찮아요.<br>
        잠시 쉬어 가면서 내 마음을 이해하고 필요한 도움을 찾아보세요.
    </p>
</div>
""", unsafe_allow_html=True)


# 서비스 소개
st.markdown(
    '<div class="intro">어떤 도움이 필요하신가요?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subintro">'
    '원하는 공간을 선택해 보세요. 각 메뉴에서 관련 정보를 확인할 수 있어요.'
    '</div>',
    unsafe_allow_html=True,
)


# 메뉴 데이터
pages = [
    {
        "title": "💚 마음 체크인",
        "desc": "지금 느끼는 감정을 알아보고<br>나에게 필요한 위로를 찾아요.",
        "style": "green",
        "path": "pages/1_마음_체크인.py",
        "key": "checkin",
    },
    {
        "title": "🌬️ 마음 돌봄",
        "desc": "편안한 호흡과 작은 활동으로<br>잠시 나를 돌봐요.",
        "style": "blue",
        "path": "pages/2_마음_돌봄.py",
        "key": "care",
    },
    {
        "title": "🫶 도움 찾기",
        "desc": "믿을 수 있는 사람과 기관에<br>도움을 요청하는 방법을 알아봐요.",
        "style": "yellow",
        "path": "pages/3_도움_찾기.py",
        "key": "help",
    },
]


# 첫 번째 줄: 카드 3개
cols = st.columns(3, gap="medium")

for col, item in zip(cols, pages):
    with col:
        st.markdown(
            f"""
            <div class="nav-card {item['style']}">
                <h3>{item['title']}</h3>
                <p>{item['desc']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "페이지 둘러보기 →",
            key=item["key"],
            use_container_width=True,
        ):
            st.session_state["target_page"] = item["path"]
            st.session_state["target_title"] = item["title"]


# 두 번째 줄: 마음 기록
st.markdown("""
<div class="nav-card pink">
    <h3>📔 마음 기록</h3>
    <p>말하기 어려웠던 감정과 생각을<br>
    나만의 글로 정리해 보세요.</p>
</div>
""", unsafe_allow_html=True)

if st.button("마음 기록 페이지 둘러보기 →", key="journal"):
    st.session_state["target_page"] = "pages/4_마음_기록.py"
    st.session_state["target_title"] = "📔 마음 기록"


# 사이트 목적
st.markdown('<div class="intro">마음 쉼터를 만든 이유</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="nav-card green" style="min-height:0;">
    <h3>💌 당신의 잘못이 아니에요.</h3>
    <p>
        따돌림은 마음에 상처를 남길 수 있지만,
        그 경험이 당신의 가치를 결정하지는 않아요.<br>
        마음 쉼터는 자신의 감정을 이해하고,
        혼자 감당하기 어려운 순간에 안전한 도움을 찾도록
        돕기 위해 만들어졌습니다.<br><br>
        모든 문제를 오늘 해결하지 않아도 괜찮아요.
        작은 한 걸음부터 시작해도 충분합니다.
    </p>
</div>
""", unsafe_allow_html=True)


# 페이지 이동 안내
if "target_page" in st.session_state:
    target = st.session_state["target_page"]
    title = st.session_state["target_title"]

    st.info(
        f"선택한 메뉴: {title}\n\n"
        f"이동할 페이지 경로: `{target}`\n\n"
        "하위 페이지 파일을 만들면 실제 페이지 이동이 가능합니다."
    )


# 하단
st.markdown("""
<div class="footer">
    🌿 마음 쉼터<br>
    당신은 존중받을 가치가 있는 사람입니다.<br>
    이 사이트는 정서적 지지와 정보 제공을 위한 공간입니다.
</div>
""", unsafe_allow_html=True)

