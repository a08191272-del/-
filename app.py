import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client, Client

# ---------------------------------------------------------
# 1. بيانات الربط السحابي (Supabase)
# ---------------------------------------------------------
SUPABASE_URL = "https://knnqvqifwngvtjijjpvq.supabase.co"
SUPABASE_KEY = "sb_publishable_..." # ضع مفتاحك هنا

st.set_page_config(page_title="مدرسة السلطان فيصل بن تركي (5-7)", layout="wide", page_icon="🏫")

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

def fetch_data(table_name):
    try:
        response = supabase.table(table_name).select("*").execute()
        return pd.DataFrame(response.data)
    except:
        return pd.DataFrame()

def insert_data(table_name, records):
    try:
        supabase.table(table_name).insert(records).execute()
        return True
    except Exception as e:
        return False

# إضافة الصفوف افتراضياً إذا كانت قاعدة البيانات فارغة لتوفير وقتك
def seed_default_classes():
    df_c = fetch_data("classes")
    if df_c.empty or len(df_c) < 5:
        default_classes = []
        grades = ["سادس", "سابع", "ثامن", "تاسع"]
        for g in grades:
            for i in range(1, 17):
                default_classes.append({"class_name": f"{g}/{i}"})
        try:
            supabase.table("classes").upsert(default_classes, on_conflict="class_name").execute()
        except:
            pass

seed_default_classes()

# ---------------------------------------------------------
# 2. الواجهة وتنسيقات التصميم والفيديو
# ---------------------------------------------------------
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
# 3. الفيديو الترحيبي
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
# 4. تسجيل الدخول
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
        
        if st.button("تسجيل الدخول", use_container_width=True):
            if username_input == "admin" and password_input == "121":
                st.session_state.logged_in = True
                st.session_state.user = {"username": "admin", "role": "admin", "name": "مدير النظام"}
                st.rerun()
            else:
                df_users = fetch_data("users")
                if not df_users.empty and 'username' in df_users.columns:
                    user_match = df_users[(df_users['username'].astype(str) == username_input) & (df_users['password'].astype(str) == password_input)]
                    if not user_match.empty:
                        user = user_match.iloc[0]
                        st.session_state.logged_in = True
                        st.session_state.user = {"username": user['username'], "role": user['role'], "name": user['name']}
                        st.rerun()
                    else:
                        st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. لوحة النظام الأساسية
# ---------------------------------------------------------
else:
    user = st.session_state.user
    st.sidebar.markdown(f"### 👋 مرحباً بك")
    st.sidebar.markdown(f"**{user['name']}**")
    st.sidebar.info(f"الصلاحية: {user['role']}")
    
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### القائمة الرئيسية")
    menu_options = ["📋 رصد الغياب والحضور", "⚠️ تسجيل المخالفات السلوكية", "📚 إضافة صفوف وطلاب", "👥 إدارة المعلمين", "📊 التقارير العامة"]
    choice = st.sidebar.radio("Navigation", menu_options, label_visibility="collapsed")

    if choice == "📋 رصد الغياب والحضور":
        st.markdown("<div class='main-header'>🏫 تسجيل ورصد الحضور والغياب اليومي</div>", unsafe_allow_html=True)
        
        df_classes = fetch_data("classes")
        class_list = df_classes['class_name'].tolist() if not df_classes.empty and 'class_name' in df_classes.columns else ["سادس/1"]
        selected_class = st.selectbox("اختر الصف", class_list)
        att_date = st.date_input("تاريخ الحضور", date.today())
        
        if selected_class:
            st.markdown(f"### طلاب صف {selected_class}")
            df_students = fetch_data("students")
            class_students = df_students[df_students['class_name'] == selected_class] if not df_students.empty and 'class_name' in df_students.columns else pd.DataFrame()
            
            if class_students.empty:
                st.info("لا يوجد طلاب مسجلين في هذا الصف حالياً. قم بإضافتهم فوراً من قسم (إضافة صفوف وطلاب).")
            else:
                records = []
                for idx, row in class_students.iterrows():
                    col1, col2 = st.columns([3, 2])
                    col1.write(row['name'])
                    status = col2.selectbox("الحالة", ["حاضر", "غائب", "متأخر", "غائب بعذر"], key=f"att_{idx}")
                    records.append({
                        "student_name": row['name'],
                        "class_name": selected_class,
                        "status": status,
                        "date": str(att_date),
                        "recorded_by": user['name']
                    })
                
                if st.button("حفظ سجل الغياب سحابياً"):
                    if insert_data("attendance", records):
                        st.success("تم حفظ الحضور والغياب سحابياً وفورياً بنجاح تام!")
                    else:
                        st.error("حدث خطأ أثناء الحفظ، تأكد من الاتصال.")

    elif choice == "⚠️ تسجيل المخالفات السلوكية":
        st.markdown("<div class='main-header'>⚠️ تسجيل ومتابعة المخالفات السلوكية</div>", unsafe_allow_html=True)
        df_classes = fetch_data("classes")
        class_list = df_classes['class_name'].tolist() if not df_classes.empty and 'class_name' in df_classes.columns else []
        selected_class = st.selectbox("اختر الصف", class_list)
        
        if selected_class:
            df_students = fetch_data("students")
            class_students = df_students[df_students['class_name'] == selected_class] if not df_students.empty and 'class_name' in df_students.columns else pd.DataFrame()
                
            if class_students.empty:
                st.warning("لا يوجد طلاب في هذا الصف بعد.")
            else:
                student_name = st.selectbox("اختر الطالب", options=class_students['name'].tolist())
                v_type = st.selectbox("نوع المخالفة", ["عدم إحضار أدوات/كتب", "استخدام الهاتف", "التأخر عن الحصة", "إثارة الشغب", "سلوك غير لائق"])
                v_action = st.text_input("الإجراء المتخذ (تنبيه شفوي / استدعاء ولي أمر...)")
                v_date = st.date_input("تاريخ المخالفة", date.today())
                
                if st.button("توثيق المخالفة سحابياً"):
                    new_v = [{
                        "student_name": student_name,
                        "class_name": selected_class,
                        "violation_type": v_type,
                        "action": v_action,
                        "date": str(v_date),
                        "recorded_by": user['name']
                    }]
                    if insert_data("violations", new_v):
                        st.success(f"تم تسجيل المخالفة للطالب {student_name} سحابياً بنجاح.")

    elif choice == "📚 إضافة صفوف وطلاب":
        st.markdown("<div class='main-header'>📚 إدارة الصفوف والطلاب</div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["إضافة صف/شعبة جديدة", "إضافة طالب جديد"])
        
        with tab1:
            new_class = st.text_input("اسم الصف/الشعبة الجديد (مثال: سادس/17 أو سابع/17)")
            if st.button("حفظ الصف الجديد سحابياً"):
                if new_class:
                    if insert_data("classes", [{"class_name": new_class}]):
                        st.success(f"تمت إضافة الصف {new_class} بنجاح للسحابة!")
                        st.rerun()
                    else:
                        st.error("الصف موجود مسبقاً أو حدث خطأ.")
                else:
                    st.error("الرجاء إدخال اسم الصف.")
                    
        with tab2:
            df_classes = fetch_data("classes")
            class_list = df_classes['class_name'].tolist() if not df_classes.empty and 'class_name' in df_classes.columns else []
            selected_class = st.selectbox("اختر الصف لإضافة الطالب إليه", class_list)
            student_name = st.text_input("اسم الطالب الثلاثي")
            if st.button("تسجيل الطالب سحابياً"):
                if student_name and selected_class:
                    if insert_data("students", [{"name": student_name, "class_name": selected_class}]):
                        st.success(f"تم تسجيل الطالب {student_name} في صف {selected_class} بنجاح!")
                        st.rerun()
                    else:
                        st.error("خطأ في حفظ الطالب.")
                else:
                    st.error("الرجاء إكمال اسم الطالب واختيار الصف.")

    elif choice == "👥 إدارة المعلمين":
        st.markdown("<div class='main-header'>👥 إدارة حسابات الكادر التعليمي</div>", unsafe_allow_html=True)
        with st.form("add_teacher"):
            t_name = st.text_input("اسم المعلم الكامل")
            t_username = st.text_input("اسم المستخدم للدخول")
            t_password = st.text_input("كلمة المرور")
            if st.form_submit_button("إضافة حساب معلم جديد"):
                if t_name and t_username and t_password:
                    if insert_data("users", [{"username": t_username, "password": t_password, "role": "teacher", "name": t_name}]):
                        st.success(f"تم إنشاء حساب المعلم {t_name} بنجاح!")
                        st.rerun()
                    else:
                        st.error("اسم المستخدم مستخدم مسبقاً أو حدث خطأ.")
                else:
                    st.error("يرجى ملء كافة الحقول.")
        
        st.subheader("قائمة المعلمين المسجلين")
        df_users = fetch_data("users")
        if not df_users.empty and 'name' in df_users.columns:
            st.dataframe(df_users[['name', 'username', 'role']], use_container_width=True)

    elif choice == "📊 التقارير العامة":
        st.markdown("<div class='main-header'>📊 التقارير والسجلات المدرسية</div>", unsafe_allow_html=True)
        tab_att, tab_viol = st.tabs(["سجل الحضور والغياب", "سجل المخالفات السلوكية"])
        with tab_att:
            st.dataframe(fetch_data("attendance"), use_container_width=True)
        with tab_viol:
            st.dataframe(fetch_data("violations"), use_container_width=True)
