import streamlit as st

st.set_page_config(
    page_title="마음돌봄 | 당신을 위한 작은 쉼",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------
# 사이트 주소
# -----------------------------------------------
SITES = [
    {
        "key": "hobby",
        "name": "취미모아",
        "emoji": "🎨",
        "style": "hobby",
        "description": (
            "내가 좋아하는 것을 하나씩 발견해 봐요. "
            "그림, 음악, 만들기처럼 다양한 취미를 통해 "
            "일상 속 작은 즐거움을 찾아가는 공간이에요."
        ),
        "caption": "나의 관심사 발견하기 · 즐거운 활동 모으기",
        "url": "https://kewqre3tacunfguk6aqdq2.streamlit.app/favored",
    },
    {
        "key": "quest",
        "name": "토닥토닥 퀘스트",
        "emoji": "🌱",
        "style": "quest",
        "description": (
            "거창한 변화 대신 오늘 할 수 있는 작은 미션부터! "
            "나에게 따뜻한 말 건네기, 기분 적어 보기 등 "
            "부담 없는 마음 돌봄 습관을 소개하는 공간이에요."
        ),
        "caption": "작은 미션 도전하기 · 나를 다정하게 대하기",
        "url": "https://kewqre3tacunfguk6aqdq2.streamlit.app/quest",
    },
    {
        "key": "rest",
        "name": "쉼",
        "emoji": "☁️",
        "style": "rest",
        "description": (
            "복잡한 생각과 긴장으로 가득한 순간, "
            "천천히 호흡하며 몸과 마음을 가라앉혀 봐요. "
            "편안한 호흡 운동과 간단한 이완 방법을 안내하는 공간이에요."
        ),
        "caption": "호흡 연습하기 · 긴장 완화하기",
        "url": "https://kewqre3tacunfguk6aqdq2.streamlit.app/breathtimer",
    },
]

# -----------------------------------------------
# 디자인 CSS
# -----------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

:root {
    --ink: #344C3A;
    --muted: #596B5C;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, #EEF3E7 0%, transparent 35%),
        radial-gradient(ellipse at 95% 35%, #F0EDF8 0%, transparent 32%),
        #FAF9F4;
    color: var(--ink);
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container {
    max-width: 1120px;
    padding: 2rem 1.5rem;
}

.brand {
    text-align: center;
    padding: 12px 0 25px;
}

.brand-tag {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: #E5EFDF;
    color: #52754C;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 14px;
}

.brand h1 {
    font-size: clamp(42px, 6vw, 66px);
    font-weight: 900;
    line-height: 1.3;
    letter-spacing: -2px;
    color: #35563A;
    margin: 0;
}

.brand h1 span {
    color: #7C9F72;
}

.brand p {
    font-size: 17px;
    font-weight: 600;
    line-height: 2;
    color: #596D5B;
    margin: 17px auto 0;
}

.hero {
    background: linear-gradient(120deg, #D9E9CF, #EEF3E5);
    border: 1px solid #D0E0C7;
    border-radius: 27px;
    padding: 28px 30px;
    margin: 14px 0 34px;
    box-shadow: 0 8px 25px rgba(84, 112, 77, 0.06);
}

.hero-label {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #56794F;
    margin-bottom: 10px;
}

.hero h2 {
    font-size: 24px;
    line-height: 1.5;
    font-weight: 800;
    color: #35563A;
    margin: 0 0 9px;
}

.hero p {
    font-size: 15px;
    line-height: 2;
    font-weight: 500;
    color: #506851;
    margin: 0;
}

.section-heading {
    font-size: 26px;
    font-weight: 900;
    color: #38573D;
    margin: 34px 0 8px;
    letter-spacing: -0.6px;
}

.section-subheading {
    font-size: 15px;
    line-height: 1.9;
    font-weight: 500;
    color: #637465;
    margin-bottom: 20px;
}

.site-card {
    border-radius: 23px;
    padding: 24px 21px;
    height: 265px;
    box-sizing: border-box;
    border: 1px solid rgba(72, 93, 70, 0.12);
    box-shadow: 0 7px 20px rgba(62, 80, 61, 0.045);
    margin-bottom: 12px;
}

.hobby {
    background: linear-gradient(150deg, #E5F0DA, #D7E8CD);
}

.quest {
    background: linear-gradient(150deg, #F0ECFA, #E4E1F3);
}

.rest {
    background: linear-gradient(150deg, #E5F1F5, #D7E9EF);
}

.site-emoji {
    font-size: 39px;
    line-height: 1.4;
    margin-bottom: 12px;
}

.site-card h3 {
    font-size: 23px;
    line-height: 1.5;
    font-weight: 900;
    margin: 0 0 12px;
    letter-spacing: -0.5px;
}

.hobby h3 { color: #365C39; }
.quest h3 { color: #514B7A; }
.rest h3 { color: #365F70; }

.site-card p {
    font-size: 15px;
    font-weight: 600;
    line-height: 1.95;
    margin: 0 0 13px;
}

.hobby p { color: #4C6749; }
.quest p { color: #5F5A7D; }
.rest p { color: #4C6974; }

.card-caption {
    font-size: 13px;
    font-weight: 700;
    line-height: 1.8;
    opacity: 0.88;
}

/* 이동 버튼 */
div[data-testid="stLinkButton"] a {
    width: 100%;
    min-height: 49px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    border: 1px solid #CFDCC8;
    background: #FFFFFF;
    color: #3C5C40;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 15px;
    font-weight: 800;
    text-decoration: none;
    transition: all 0.2s ease;
}

div[data-testid="stLinkButton"] a:hover {
    background: #EDF4E8;
    color: #2E4D32;
    border-color: #8EAF83;
}

.purpose {
    background: linear-gradient(120deg, #F5E9E9, #F8EEEE);
    border: 1px solid #EAD8DA;
    border-radius: 23px;
    padding: 26px;
    margin-top: 15px;
}

.purpose h3 {
    color: #754F57;
    font-size: 22px;
    font-weight: 900;
    margin: 0 0 12px;
}

.purpose p {
    color: #755C61;
    font-size: 15px;
    font-weight: 500;
    line-height: 2.1;
    margin: 0;
}

.footer {
    text-align: center;
    padding: 35px 0 12px;
    color: #738173;
    font-size: 13px;
    font-weight: 500;
    line-height: 2;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1.2rem 1rem 1.5rem;
    }

    .brand h1 {
        letter-spacing: -1px;
    }

    .brand p {
        font-size: 15px;
    }

    .hero {
        padding: 23px 20px;
    }

    .hero h2 {
        font-size: 21px;
    }

    .site-card {
        height: auto;
        min-height: 265px;
        padding: 21px;
    }

    .site-card h3 {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------
# 메인 제목
# -----------------------------------------------
st.markdown("""
<div class="brand">
    <div class="brand-tag">🌿 나를 위한 작은 마음 여행</div>
    <h1>마음<span>돌봄</span></h1>
    <p>
        힘들었던 마음에 다정한 쉼표를 놓아 주세요.<br>
        나에게 맞는 즐거움과 작은 회복을 찾아가는 공간입니다.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# 소개 배너
# -----------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-label">A LITTLE CARE FOR YOUR HEART</div>
    <h2>오늘도 여기까지 온 당신, 정말 수고했어요. 🌷</h2>
    <p>
        따돌림으로 상처받았거나 사람들과의 관계 때문에 힘들었던 마음을
        혼자 감당하지 않아도 괜찮아요.<br>
        새로운 즐거움을 찾고, 작은 미션에 도전하고, 호흡을 가다듬으며
        나만의 속도로 마음을 돌봐 보세요.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# 사이트 이동 카드
# -----------------------------------------------
st.markdown(
    '<div class="section-heading">어떤 마음 돌봄이 필요하신가요?</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="section-subheading">
    지금 나에게 가장 끌리는 공간을 선택해 보세요.
    세 가지 공간은 서로 다른 방식으로 당신의 일상을 응원합니다.
</div>
""", unsafe_allow_html=True)

columns = st.columns(3, gap="medium")

for column, site in zip(columns, SITES):
    with column:
        st.markdown(
            f"""
            <div class="site-card {site['style']}">
                <div class="site-emoji">{site['emoji']}</div>
                <h3>{site['name']}</h3>
                <p>{site['description']}</p>
                <div class="card-caption">{site['caption']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.link_button(
            "사이트 이동하기 →",
            url=site["url"],
            help=f"{site['name']} 사이트를 새 탭에서 엽니다.",
            use_container_width=True,
        )


# -----------------------------------------------
# 사이트 개설 목적
# -----------------------------------------------
st.markdown(
    '<div class="section-heading">마음돌봄을 만든 이유 💌</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="purpose">
    <h3>당신의 잘못이 아니며, 당신은 존중받을 가치가 있어요.</h3>
    <p>
        따돌림은 자신감과 사람을 믿는 마음에 상처를 남길 수 있어요.
        그 경험이 끝난 뒤에도 외로움이나 불안이 남을 수 있고,
        다시 즐거운 일상을 시작하는 데 시간이 필요할 수도 있습니다.<br><br>
        마음돌봄은 그런 경험을 가볍게 여기지 않고, 각자의 속도에 맞춰
        즐거움을 발견하고, 작은 목표를 실천하고, 호흡을 통해 긴장을
        완화할 수 있도록 돕기 위해 만들어졌습니다.<br><br>
        이곳이 모든 문제를 해결해 주는 것은 아니지만,
        스스로를 조금 더 다정하게 대하는 시작점이 되기를 바랍니다.
        괴롭힘이 계속되거나 안전이 걱정된다면 믿을 수 있는 어른이나
        전문기관에 도움을 요청해도 괜찮아요.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------
# 하단
# -----------------------------------------------
st.markdown("""
<div class="footer">
    🌿 마음돌봄 · 나를 위한 다정한 한 걸음<br>
    당신의 감정은 소중하고, 당신은 존중받을 가치가 있습니다.
</div>
""", unsafe_allow_html=True)
