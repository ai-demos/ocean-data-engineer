import streamlit as st

from app.password import check_password

st.set_page_config(
    page_title="DE LLM",
    page_icon=":snowman:",
)

st.title(":snowman: Ocean Data Engineer")
st.markdown('<a href="https://github.com/phidatahq/phidata"><h4>by phidata</h4></a>', unsafe_allow_html=True)


def main() -> None:
    st.markdown("### Select your Junior Data Engineer:")
    st.markdown("#### 1. Ocean Data Engineer")
    st.markdown("#### 2. DuckGPT Local")
    st.markdown("#### 3. DuckGPT S3")
    st.markdown("#### 4. Python Data Engineer")
    st.sidebar.success("Select App from above")


if check_password():
    main()
