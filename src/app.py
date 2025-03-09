import streamlit as st
import pandas as pd
import os

def search_page():
    st.title("검색 화면")
    search_query = st.text_input("검색어")
    
    if st.button("검색"):
        st.write(f"'{search_query}'에 대한 검색을 수행합니다.")

def manage_page():
    st.title("관리 화면")
    file_path = "./data.csv"
    
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["url", "method", "keyword"])
        df.to_csv(file_path, index=False)
    else:
        df = pd.read_csv(file_path)
    
    st.dataframe(df)
    
    with st.form("입력 폼"):
        url = st.text_input("URL")
        method = st.text_input("Method")
        keyword = st.text_input("Keyword")
        submit_button = st.form_submit_button("추가")
    
    if submit_button:
        new_data = pd.DataFrame([[url, method, keyword]], columns=["url", "method", "keyword"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.rerun()
    
    if st.button("삭제"):
        df = df.iloc[:-1]
        df.to_csv(file_path, index=False)
        st.rerun()

def login_page():
    st.title("로그인 화면")
    user_id = st.text_input("아이디")
    user_pw = st.text_input("패스워드", type="password")
    
    if st.button("로그인"):
        if user_id == "tonykim" and user_pw == "kimyeongjun!23":
            st.session_state["authenticated"] = True
            st.session_state["page"] = "검색"
            st.rerun()
        else:
            st.error("아이디 또는 패스워드가 잘못되었습니다.")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "로그인"
    
    if not st.session_state["authenticated"]:
        login_page()
    else:
        st.sidebar.title("메뉴")
        page = st.sidebar.radio("이동", ["검색", "관리"])
        st.sidebar.button("로그아웃", on_click=lambda: st.session_state.update({"authenticated": False, "page": "로그인"}))
        
        if page == "검색":
            search_page()
        elif page == "관리":
            manage_page()

if __name__ == "__main__":
    main()
