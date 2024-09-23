import streamlit as st


st.set_page_config(page_title="FGO 模拟", page_icon='assets/images/favicon_fgo.png')

pages = [
    st.Page("./pages/home.py",title='主页'),
    st.Page("./pages/shuffle.py", title="发牌概率计算器🎲"),
    st.Page("./pages/damage_calculator.py", title="伤害计算器♨️"),
    st.Page("./pages/refund.py", title="回收计算器🏄"),
    ]

pg = st.navigation(pages)
pg.run()



