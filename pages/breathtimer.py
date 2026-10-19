import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="쉼 - 4-6 호흡 가이드",
    page_icon="🧘",
    layout="centered"
)

# 2. 스타일링 (커스텀 CSS)
st.markdown("""
    <style>
    .main {
        background-color: #F7FAF9;
    }
    .breath-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 250px;
        margin: 20px 0;
    }
    .breath-circle {
        border-radius: 50%;
        background: linear-gradient(135deg, #A8E6CF 0%, #3D84A8 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        font-size: 24px;
        transition: all 1s ease-in-out;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_style_html=True)

# 3. 세션 상태 초기화
if "session_running" not in st.session_state:
    st.session_state.session_running = False
if "history" not in st.session_state:
    st.session_state.history = []

# 4. 헤더
st.title("🧘 쉼(Breathing Space)")
st.subheader("마음의 안정을 찾는 4-6 호흡법")
st.caption("들이마시기 4초, 내쉬기 6초의 리듬으로 부교감 신경을 활성화하여 스트레스를 줄여줍니다.")

st.divider()

# 5. 탭 구성
tab1, tab2, tab3 = st.tabs(["🫁 호흡 시작하기", "📊 효과 및 가이드", "📝 호흡 기록"])

with tab1:
    st.markdown("### 호흡 세션 설정")
    
    col1, col2 = st.columns(2)
    with col1:
        session_minutes = st.selectbox("목표 호흡 시간", [1, 2, 3, 5, 10], index=1, format_func=lambda x: f"{x}분")
    with col2:
        pre_stress = st.slider("현재 스트레스 / 불안 정도", 1, 10, 5, help="1: 매우 편안함, 10: 매우 불안함")

    st.write("")
    
    # 세션 시작/중지 버튼
    start_btn = st.button("▶️ 호흡 세션 시작하기", use_container_width=True, type="primary")

    if start_btn:
        st.session_state.session_running = True
        
        total_seconds = session_minutes * 60
        cycle_time = 10  # 들이마시기 4초 + 내쉬기 6초 = 10초
        cycles = total_seconds // cycle_time
        
        status_text = st.empty()
        timer_text = st.empty()
        circle_placeholder = st.empty()
        progress_bar = st.progress(0)

        try:
            for cycle in range(int(cycles)):
                # ------------------- 들이마시기 (4초) -------------------
                for s in range(1, 5):
                    status_text.markdown("### 🌬️ **천천히 들이마시세요...**")
                    timer_text.markdown(f"**{s}초 / 4초**")
                    
                    # 동적 원 크기 조절 (100px -> 220px)
                    size = 100 + (s * 30)
                    circle_placeholder.markdown(f"""
                        <div class="breath-box">
                            <div class="breath-circle" style="width: {size}px; height: {size}px;">
                                들이마시기
                            </div>
                        </div>
                    """, unsafe_style_html=True)
                    
                    time.sleep(1)
                    
                # ------------------- 내쉬기 (6초) -------------------
                for s in range(1, 7):
                    status_text.markdown("### 😮‍💨 **천천히 내쉬세요...**")
                    timer_text.markdown(f"**{s}초 / 6초**")
                    
                    # 동적 원 크기 조절 (220px -> 100px)
                    size = 220 - (s * 20)
                    circle_placeholder.markdown(f"""
                        <div class="breath-box">
                            <div class="breath-circle" style="width: {size}px; height: {size}px; background: linear-gradient(135deg, #46CDCF 0%, #3D84A8 100%);">
                                내쉬기
                            </div>
                        </div>
                    """, unsafe_style_html=True)
                    
                    time.sleep(1)

                # 진행률 업데이트
                progress_bar.progress((cycle + 1) / cycles)

            # 완료 상태
            status_text.markdown("🎉 **호흡 세션이 완료되었습니다!**")
            timer_text.empty()
            circle_placeholder.markdown("""
                <div class="breath-box">
                    <div class="breath-circle" style="width: 150px; height: 150px;">
                        완료!
                    </div>
                </div>
            """, unsafe_style_html=True)
            
            st.balloons()
            
            # 세션 완료 기록
            st.session_state.history.append({
                "시간": time.strftime("%Y-%m-%d %H:%M"),
                "목표 시간": f"{session_minutes}분",
                "사전 스트레스": pre_stress
            })
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

with tab2:
    st.markdown("### 💡 4-6 호흡법이란?")
    st.info("""
    **4-6 호흡법**은 4초 동안 숨을 깊게 들이마시고, 6초 동안 천천히 내쉬는 심호흡 기법입니다.
    
    * **부교감 신경 활성화**: 숨을 내쉬는 시간을 들이마시는 시간보다 길게 가져가면 자율신경계 중 '부교감 신경'이 자극되어 심장 박동이 정돈되고 몸이 안정 상태로 전환됩니다.
    * **불안 및 공황 완화**: 갑작스러운 긴장, 발표 전, 수면 전 마음을 정돈할 때 매우 효과적입니다.
    """)
    
    st.markdown("### 🧘‍♂️ 올바른 호흡 팁")
    st.markdown("""
    1. **편안한 자세**: 의자에 바르게 앉거나 편하게 눕습니다.
    2. **코로 들이마시기**: 4초 동안 코로 깊게 배를 채우듯 숨을 쉬세요 (복식호흡).
    3. **입으로 내쉬기**: 6초 동안 입을 살짝 벌려 '휘-' 소리를 내며 천천히 숨을 배출하세요.
    """)

with tab3:
    st.markdown("### 📝 나의 호흡 세션 기록")
    if st.session_state.history:
        st.dataframe(st.session_state.history, use_container_width=True)
    else:
        st.write("아직 진행한 호흡 세션 기록이 없습니다. '호흡 시작하기' 탭에서 첫 세션을 완료해보세요!")
