# streamlit_app.py
import streamlit as st
import pandas as pd
import tempfile
from full_system import run_full_algorithm_from_df

st.set_page_config(page_title="Thời khóa biểu", layout="centered")

st.title("🗓️ Tạo thời khóa biểu")

uploaded_file = st.file_uploader("📄 Tải lên file Timetable.xlsx", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        required_columns = {"Trường_Viện_Khoa", "Mã_lớp", "Phòng"}
        if not required_columns.issubset(df.columns):
            st.error("❌ File phải chứa các cột: Trường_Viện_Khoa, Mã_lớp, Phòng")
        else:
            st.success(f"✅ Đã đọc {len(df)} dòng dữ liệu. Gồm {df['Trường_Viện_Khoa'].nunique()} nhóm.")

            if st.button("🚀 Tạo thời khóa biểu"):
                with st.spinner("⏳ Đang chạy thuật toán di truyền..."):
                    result_df = run_full_algorithm_from_df(df)
                    st.success("🎉 Tạo lịch thành công!")
                    st.dataframe(result_df.head(50))

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        result_df.to_excel(tmp.name, index=False)
                        st.download_button(
                            label="📅 Tải file Full_Timetable.xlsx",
                            data=open(tmp.name, "rb").read(),
                            file_name="Full_Timetable.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

    except Exception as e:
        st.error(f"❌ Lỗi khi xử lý file: {e}")
