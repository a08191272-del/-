import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="مدرسة السلطان فيصل بن تركي (5-7)",
    page_icon="🏫",
    layout="wide"
)

# عنوان النظام الرئيسي
st.title("🏫 مدرسة السلطان فيصل بن تركي (صفوف 5-7)")
st.markdown("---")

# تهيئة الجلسة لحفظ البيانات مؤقتاً وإتاحة إضافة صفوف جديدة مرنة
if 'grades_list' not in st.session_state:
    st.session_state.grades_list = ["الصف الخامس", "الصف السادس", "الصف السابع"]

if 'sections_list' not in st.session_state:
    st.session_state.sections_list = ["1", "2", "3", "4"]

if 'students_df' not in st.session_state:
    st.session_state.students_df = pd.DataFrame(columns=["اسم الطالب", "الصف", "الشعبة"])

if 'attendance_df' not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(columns=["التاريخ", "اسم الطالب", "الصف والشعبة", "الحالة"])

if 'violations_df' not in st.session_state:
    st.session_state.violations_df = pd.DataFrame(columns=["التاريخ", "اسم الطالب", "الصف والشعبة", "نوع المخالفة", "الإجراء المتخذ"])

# القائمة الجانبية للتنقل
menu = st.sidebar.selectbox(
    "القائمة الرئيسية",
    ["إعدادات الصفوف والشعب", "إدارة الطلاب", "تسجيل الغياب", "رصد المخالفات", "التقارير والبيانات"]
)

# 0. قسم إعدادات الصفوف والشعب (لكي تختار أو تضيف المعلمة الصفوف على راحتها)
if menu == "إعدادات الصفوف والشعب":
    st.header("⚙️ تخصيص وإضافة الصفوف والشعب")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("إضافة صف جديد")
        with st.form("add_grade_form"):
            new_grade = st.text_input("اسم الصف الجديد (مثلاً: الصف الثامن)")
            g_submit = st.form_submit_button("إضافة الصف")
            if g_submit and new_grade.strip():
                if new_grade not in st.session_state.grades_list:
                    st.session_state.grades_list.append(new_grade.strip())
                    st.success(f"تم إضافة الصف '{new_grade}' بنجاح!")
                else:
                    st.warning("هذا الصف موجود مسبقاً.")
                    
    with col2:
        st.subheader("إضافة شعبة جديدة")
        with st.form("add_section_form"):
            new_sec = st.text_input("رقم أو رمز الشعبة الجديدة (مثلاً: 5 أو أ)")
            s_submit = st.form_submit_button("إضافة الشعبة")
            if s_submit and new_sec.strip():
                if new_sec not in st.session_state.sections_list:
                    st.session_state.sections_list.append(new_sec.strip())
                    st.success(f"تم إضافة الشعبة '{new_sec}' بنجاح!")
                else:
                    st.warning("هذه الشعبة موجودة مسبقاً.")

    st.markdown("---")
    st.write("📌 **الصفوف المتاحة حالياً:**", ", ".join(st.session_state.grades_list))
    st.write("📌 **الشعب المتاحة حالياً:**", ", ".join(st.session_state.sections_list))

# 1. قسم إدارة الطلاب
elif menu == "إدارة الطلاب":
    st.header("👥 إضافة وإدارة الطلاب")
    
    if not st.session_state.grades_list or not st.session_state.sections_list:
        st.warning("الرجاء إضافة صفوف وشعب أولاً من قائمة (إعدادات الصفوف والشعب).")
    else:
        with st.form("add_student_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                student_name = st.text_input("اسم الطالب الرباعي")
            with col2:
                selected_grade = st.selectbox("اختر الصف", st.session_state.grades_list)
            with col3:
                selected_section = st.selectbox("اختر الشعبة", st.session_state.sections_list)
                
            submit_btn = st.form_submit_button("حفظ وإضافة الطالب")
            
            if submit_btn:
                if student_name.strip() != "":
                    new_row = pd.DataFrame({"اسم الطالب": [student_name], "الصف": [selected_grade], "الشعبة": [selected_section]})
                    st.session_state.students_df = pd.concat([st.session_state.students_df, new_row], ignore_index=True)
                    st.success(f"تم إضافة الطالب {student_name} بنجاح!")
                else:
                    st.error("الرجاء إدخال اسم الطالب بشكل صحيح.")

    st.subheader("📋 قائمة الطلاب المسجلين")
    if not st.session_state.students_df.empty:
        st.dataframe(st.session_state.students_df, use_container_width=True)
    else:
        st.info("لا يوجد طلاب مسجلين حتى الآن.")

# 2. قسم تسجيل الغياب
elif menu == "تسجيل الغياب":
    st.header("📝 تسجيل الحضور والغياب اليومي")
    
    if st.session_state.students_df.empty:
        st.warning("الرجاء إضافة طلاب أولاً.")
    else:
        with st.form("attendance_form"):
            att_date = st.date_input("تاريخ اليوم", datetime.today())
            
            f_grade = st.selectbox("تصفية حسب الصف", st.session_state.grades_list, key="att_g")
            f_section = st.selectbox("تصفية حسب الشعبة", st.session_state.sections_list, key="att_s")
            
            filtered_students = st.session_state.students_df[
                (st.session_state.students_df["الصف"] == f_grade) & 
                (st.session_state.students_df["الشعبة"] == f_section)
            ]
            
            attendance_status = {}
            if not filtered_students.empty:
                st.write(f"**طلاب {f_grade} - الشعبة {f_section}:**")
                for idx, row in filtered_students.iterrows():
                    status = st.radio(f"{row['اسم الطالب']}", ["حاضر", "غائب", "متأخر"], horizontal=True, key=f"std_{idx}")
                    attendance_status[row['اسم الطالب']] = status
            else:
                st.info("لا توجد أسماء طلاب مسجلة في هذا الصف والشعبة حالياً.")
            
            att_submit = st.form_submit_button("حفظ سجل الغياب")
            
            if att_submit and not filtered_students.empty:
                new_records = []
                for name, status in attendance_status.items():
                    new_records.append({
                        "التاريخ": str(att_date),
                        "اسم الطالب": name,
                        "الصف والشعبة": f"{f_grade} (شعبة {f_section})",
                        "الحالة": status
                    })
                df_new_att = pd.DataFrame(new_records)
                st.session_state.attendance_df = pd.concat([st.session_state.attendance_df, df_new_att], ignore_index=True)
                st.success("تم حفظ الغياب بنجاح!")

        if not st.session_state.attendance_df.empty:
            st.subheader("سجلات الغياب السابقة")
            st.dataframe(st.session_state.attendance_df, use_container_width=True)

# 3. قسم رصد المخالفات
elif menu == "رصد المخالفات":
    st.header("⚠️ رصد المخالفات والسلوكيات")
    
    if st.session_state.students_df.empty:
        st.warning("الرجاء إضافة طلاب أولاً.")
    else:
        with st.form("violation_form"):
            v_date = st.date_input("تاريخ المخالفة", datetime.today())
            student_names_list = st.session_state.students_df["اسم الطالب"].tolist()
            selected_student = st.selectbox("اختر الطالب", student_names_list)
            
            violation_type = st.selectbox("نوع المخالفة", [
                "تأخر عن الحصة",
                "إزعاج داخل الصف",
                "عدم إحضار الواجبات/الكتب",
                "سلوك غير لائق",
                "أخرى"
            ])
            action_taken = st.text_input("الإجراء المتخذ (تنبيه شفوي، تحويل للإدارة، إلخ)")
            
            v_submit = st.form_submit_button("حفظ المخالفة")
            
            if v_submit:
                student_row = st.session_state.students_df[st.session_state.students_df["اسم الطالب"] == selected_student].iloc[0]
                v_record = pd.DataFrame({
                    "التاريخ": [str(v_date)],
                    "اسم الطالب": [selected_student],
                    "الصف والشعبة": [f"{student_row['الصف']} (شعبة {student_row['الشعبة']})"],
                    "نوع المخالفة": [violation_type],
                    "الإجراء المتخذ": [action_taken if action_taken else "لا يوجد"]
                })
                st.session_state.violations_df = pd.concat([st.session_state.violations_df, v_record], ignore_index=True)
                st.success(f"تم تسجيل المخالفة للطالب {selected_student} بنجاح!")

        if not st.session_state.violations_df.empty:
            st.subheader("سجل المخالفات المسجلة")
            st.dataframe(st.session_state.violations_df, use_container_width=True)

# 4. التقارير والبيانات
elif menu == "التقارير والبيانات":
    st.header("📊 التقارير والإحصائيات العامة")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("إجمالي الطلاب", len(st.session_state.students_df))
    with col2:
        st.metric("إجمالي المخالفات", len(st.session_state.violations_df))
        
    st.markdown("---")
    st.subheader("قائمة الطلاب الكاملة")
    if not st.session_state.students_df.empty:
        st.dataframe(st.session_state.students_df, use_container_width=True)
    else:
        st.info("لا توجد بيانات مسجلة.")
