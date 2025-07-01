import streamlit as st
import pandas as pd
import tempfile
from App import genetic_algorithm 
import os

DAYS = ['T2', 'T3', 'T4', 'T5', 'T6']
SLOTS = ['Sáng', 'Chiều']

def main():
    st.title("📅 Thời khóa biểu cho giáo viên ")

    uploaded_file = st.file_uploader("📤 Tải file Timetable.xlsx", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df = df[['Mã_lớp', 'Phòng']].dropna()
            classes = df['Mã_lớp'].unique().tolist()
            rooms = df['Phòng'].unique().tolist()

            st.success(f"✅ Đã đọc dữ liệu: {len(classes)} lớp, {len(rooms)} phòng.")

            if st.button("🚀 Tạo thời khóa biểu"):
                with st.spinner("Đang chạy thuật toán..."):
                    best_schedule = genetic_algorithm(classes, rooms)

                    output = pd.DataFrame([
                        {"Mã_lớp": cls, "Thứ": day, "Buổi": slot, "Phòng": room}
                        for cls, (day, slot, room) in best_schedule.items()
                    ])

                    st.success("🎉 Tạo thời khóa biểu thành công!")

                    st.dataframe(output)

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        output.to_excel(tmp.name, index=False)
                        st.download_button(
                            label="📥 Tải file kết quả",
                            data=open(tmp.name, "rb").read(),
                            file_name="Best_Timetable.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

        except Exception as e:
            st.error(f"❌ Lỗi khi xử lý file: {e}")

if __name__ == "__main__":
    main()
