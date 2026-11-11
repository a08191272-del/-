import streamlit as st
import json
import os
import pandas as pd
from datetime import date

# ---------------------------------------------------------
# 1. إعداد وحفظ البيانات باستخدام ملفات JSON السريعة
# ---------------------------------------------------------
DB_FILE = 'school_data.json'

def load_data():
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": [
                {"id": 1, "username": "admin", "password": "121", "role": "admin", "name": "Administrator"}
            ],
            "classes": [
                {"id": 1, "class_name": "سادس/1"},
                {"id": 2, "class_name": "سادس/2"},
                {"id": 3, "class_name": "سابع/1"},
                {"id": 4, "class_name": "سابع/2"}
            ],
            "students": [],
            "attendance": [],
            "violations": []
        }
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return load_data()

def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# ---------------------------------------------------------
# 2. الهوية البصرية وتنسيقات الفيديو
# ---------------------------------------------------------
st.set_page_config(page_title="مدرسة السلطان فيصل بن تركي (5-7)", layout="wide", page_icon="🏫")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 70% 30%, #1e293b 0%, #0b1329 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .video-header-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .intro-video {
        width: 100%;
        max-height: 400px;
        object-fit: cover;
    }
    .noor-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.95) 100%), 
                    url('https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 50px 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .login-card-noor {
        background: rgba(30, 41, 59, 0.85);
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4) !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: block !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #075985 100%) !important;
    }
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
    }
    div[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-left: 1px solid rgba(255, 255, 255, 0.05);
    }
    div[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# ---------------------------------------------------------
# 3. عرض الفيديو في البداية
# ---------------------------------------------------------
st.markdown("""
    <div class="video-header-container">
        <video class="intro-video" autoplay loop muted playsinline>
            <source src="video_1.mp4" type="video/mp4">
            متصفحك لا يدعم تشغيل الفيديو.
        </video>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. شاشة تسجيل الدخول
# ---------------------------------------------------------
if not st.session_state.logged_in:
    col_left, col_right = st.columns([1.3, 1], gap="large")
    
    with col_left:
        st.markdown("""
            <div class='noor-banner'>
                <div style='font-size: 1.8rem; font-weight: bold; margin-bottom: 10px; color: #38bdf8;'>🏫 مدرسة السلطان فيصل بن تركي</div>
                <h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 15px; line-height: 1.3;'>أهلاً بك في المتعة الحقيقية للتعلم الذكي</h1>
                <p style='font-size: 1.1rem; color: #cbd5e1; margin-bottom: 25px;'>بوابة شؤون الطلاب والمتابعة السلوكية والتعليم الأساسي (5-7)</p>
                <div>
                    <span style='background: rgba(56, 189, 248, 0.2); padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; border: 1px solid #38bdf8;'>وزارة التربية والتعليم</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("<div class='login-card-noor'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #ffffff; margin-bottom: 5px; font-weight: 700;'>تسجيل الدخول</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8; margin-bottom: 25px; font-size: 0.95rem;'>أدخل بيانات الكادر التعليمي للمتابعة</p>", unsafe_allow_html=True)
        
        username_input = st.text_input("اسم الدخول (Username)")
        password_input = st.text_input("كلمة المرور (Password)", type="password")
        
        st.markdown("<div style='margin: 10px 0 20px 0;'><a href='#' style='color: #38bdf8; text-decoration: none; font-size: 0.9rem;'>أنسيت بيانات الدخول؟</a></div>", unsafe_allow_html=True)
        
        if st.button("تسجيل الدخول", use_container_width=True):
            user_found = None
            for u in data["users"]:
                if str(u["username"]) == username_input and str(u["password"]) == password_input:
                    user_found = u
                    break
            
            if user_found:
                st.session_state.logged_in = True
                st.session_state.user = user_found
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. داخل النظام (اللوحة والخدمات الكاملة)
# ---------------------------------------------------------
else:
    user = st.session_state.user
    st.sidebar.markdown(f"### 👋 Welcome")
    st.sidebar.markdown(f"**{user['name']}**")
    st.sidebar.info(f"Permissions: {user['role']}")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Main Menu")
    menu_options = ["📋 رصد الغياب والحضور", "⚠️ تسجيل المخالفات السلوكية", "📚 إضافة صفوف وطلاب", "👥 إدارة المعلمين", "📊 التقارير العامة", "⚙️ إدارة النسخ الاحتياطي"]
    choice = st.sidebar.radio("Navigation", menu_options, label_visibility="collapsed")

    if choice == "📋 رصد الغياب والحضور":
        st.markdown("<div class='main-header'>🏫 تسجيل ورصد الحضور والغياب اليومي</div>", unsafe_allow_html=True)
        
        class_names = [c["class_name"] for c in data["classes"]]
        selected_class = st.selectbox("Class select edition", class_names)
        att_date = st.date_input("Date", date.today())
        
        if selected_class:
            st.markdown(f"### طلاب صف {selected_class}")
            class_students = [s for s in data["students"] if s["class_name"] == selected_class]
            
            if not class_students:
                st.info("لا يوجد طلاب مسجلين في هذا الصف حالياً. قم بإضافتهم من قسم (إضافة صفوف وطلاب).")
            else:
                records = []
                for student in class_students:
                    col1, col2 = st.columns([3, 2])
                    col1.write(student['name'])
                    status = col2.selectbox("Status", ["حاضر", "غائب", "متأخر", "غائب بعذر"], key=f"att_{student['id']}")
                    records.append({
                        "student_id": student['id'],
                        "student_name": student['name'],
                        "class_name": selected_class,
                        "status": status,
                        "date": str(att_date),
                        "recorded_by": user['name']
                    })
                
                if st.button("حفظ سجل الغياب"):
                    data["attendance"].extend(records)
                    save_data(data)
                    st.success("تم حفظ الحضور والغياب بنجاح تام!")

    elif choice == "⚠️ تسجيل المخالفات السلوكية":
        st.markdown("<div class='main-header'>⚠️ تسجيل ومتابعة المخالفات السلوكية</div>", unsafe_allow_html=True)
        class_names = [c["class_name"] for c in data["classes"]]
        selected_class = st.selectbox("اختر الصف", class_names)
        
        if selected_class:
            class_students = [s for s in data["students"] if s["class_name"] == selected_class]
            if class_students:
                student_names = {s['id']: s['name'] for s in class_students}
                selected_student_id = st.selectbox("اختر الطالب", options=list(student_names.keys()), format_func=lambda x: student_names[x])
                v_type = st.selectbox("نوع المخالفة", ["عدم إحضار أدوات/كتب", "استخدام الهاتف", "التأخر عن الحصة", "إثارة الشغب", "سلوك غير لائق"])
                v_action = st.text_input("الإجراء المتخذ (تنبيه شفوي / استدعاء ولي أمر...)")
                v_date = st.date_input("تاريخ المخالفة", date.today())
                
                if st.button("توثيق المخالفة"):
                    new_violation = {
                        "id": len(data["violations"]) + 1,
                        "student_id": selected_student_id,
                        "student_name": student_names[selected_student_id],
                        "class_name": selected_class,
                        "violation_type": v_type,
                        "action": v_action,
                        "date": str(v_date),
                        "recorded_by": user['name']
                    }
                    data["violations"].append(new_violation)
                    save_data(data)
                    st.success(f"تم تسجيل المخالفة للطالب {student_names[selected_student_id]} بنجاح.")

    elif choice == "📚 إضافة صفوف وطلاب":
        st.markdown("<div class='main-header'>📚 إدارة الصفوف والطلاب</div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["إضافة صف/شعبة", "إضافة طالب جديد"])
        
        with tab1:
            new_class = st.text_input("اسم الصف/الشعبة (مثال: سادس/1)")
            if st.button("حفظ الصف الجديد"):
                if new_class:
                    if any(c["class_name"] == new_class for c in data["classes"]):
                        st.warning("هذا الصف مسجل مسبقاً.")
                    else:
                        data["classes"].append({"id": len(data["classes"]) + 1, "class_name": new_class})
                        save_data(data)
                        st.success(f"تمت إضافة الصف {new_class} بنجاح!")
                        st.rerun()
                else:
                    st.error("الرجاء إدخال اسم الصف.")
                    
        with tab2:
            class_names = [c["class_name"] for c in data["classes"]]
            selected_class = st.selectbox("اختر الصف لإضافة الطالب", class_names)
            student_name = st.text_input("اسم الطالب الثلاثي")
            if st.button("تسجيل الطالب"):
                if student_name and selected_class:
                    data["students"].append({
                        "id": len(data["students"]) + 1,
                        "name": student_name,
                        "class_name": selected_class
                    })
                    save_data(data)
                    st.success(f"تم تسجيل الطالب {student_name} بنجاح!")
                    st.rerun()
                else:
                    st.error("الرجاء إكمال البيانات.")

    elif choice == "👥 إدارة المعلمين":
        st.markdown("<div class='main-header'>👥 إدارة حسابات الكادر التعليمي</div>", unsafe_allow_html=True)
        with st.form("add_teacher"):
            t_name = st.text_input("اسم المعلم الكامل")
            t_username = st.text_input("اسم المستخدم للدخول")
            t_password = st.text_input("كلمة المرور")
            if st.form_submit_button("إضافة حساب معلم"):
                if t_name and t_username and t_password:
                    if any(u["username"] == t_username for u in data["users"]):
                        st.error("اسم المستخدم مسجل مسبقاً.")
                    else:
                        data["users"].append({
                            "id": len(data["users"]) + 1,
                            "username": t_username,
                            "password": t_password,
                            "role": "teacher",
                            "name": t_name
                        })
                        save_data(data)
                        st.success(f"تم إنشاء حساب المعلم {t_name} بنجاح!")
                        st.rerun()
                else:
                    st.error("يرجى ملء كافة الحقول.")
        
        st.subheader("قائمة المعلمين")
        df_users = pd.DataFrame(data["users"])
        if not df_users.empty:
            st.dataframe(df_users[['id', 'name', 'username', 'role']], use_container_width=True)

    elif choice == "📊 التقارير العامة":
        st.markdown("<div class='main-header'>📊 التقارير والسجلات المدرسية</div>", unsafe_allow_html=True)
        tab_att, tab_viol = st.tabs(["سجل الحضور والغياب", "سجل المخالفات السلوكية"])
        with tab_att:
            df_att = pd.DataFrame(data["attendance"])
            st.dataframe(df_att, use_container_width=True)
        with tab_viol:
            df_viol = pd.DataFrame(data["violations"])
            st.dataframe(df_viol, use_container_width=True)

    elif choice == "⚙️ إدارة النسخ الاحتياطي":
        st.markdown("<div class='main-header'>⚙️ إدارة النسخ الاحتياطي واستعادة البيانات</div>", unsafe_allow_html=True)
        st.info("من هنا يمكنك تحميل نسخة احتياطية لكافة بيانات النظام (الطلاب، الحضور، المعلمين)، أو رفع ملف النسخة الاحتياطية واستعادته بضغطة زر لتظهر لك كل البيانات فوراً.")
        
        col_dl, col_ul = st.columns(2)
        
        with col_dl:
            st.subheader("📥 تحميل نسخة احتياطية")
            json_str = json.dumps(data, ensure_ascii=False, indent=4)
            st.download_button(
                label="تحميل ملف البيانات الحالي",
                data=json_str,
                file_name="school_data_backup.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_ul:
            st.subheader("📤 استعادة البيانات")
            uploaded_file = st.file_uploader("اختر ملف النسخة الاحتياطية (.json)", type=["json"])
            if uploaded_file is not None:
                if st.button("تحميل الملف واستعادة كافة البيانات", use_container_width=True):
                    try:
                        restored_data = json.load(uploaded_file)
                        save_data(restored_data)
                        st.success("تم استعادة كافة بيانات الطلاب والغياب والمعلمين بنجاح تام! قم بتحديث الصفحة.")
                        st.rerun()
                    except Exception as e:
                        st.error("حدث خطأ أثناء قراءة الملف، تأكد أنه ملف نسخ احتياطي صالح.")
