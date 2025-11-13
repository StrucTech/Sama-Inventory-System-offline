"""
مدير المستخدمين - إدارة حسابات المستخدمين في Google Sheets
يتعامل مع شيت "Users" لتخزين البيانات بدون تشفير
"""

import gspread
from typing import Optional, Dict, List
import datetime
from sheets.manager import SheetsManager

class UsersManager:
    """مدير المستخدمين لتسجيل الدخول والحسابات الجديدة"""
    
    def __init__(self, credentials_file: str, spreadsheet_name: str):
        """
        تهيئة مدير المستخدمين
        
        Args:
            credentials_file: مسار ملف بيانات اعتماد Google API
            spreadsheet_name: اسم جدول Google Sheets
        """
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.users_sheet_name = "Users"
        
        self.client = None
        self.spreadsheet = None
        self.users_sheet = None
        
    def connect(self) -> bool:
        """
        الاتصال بـ Google Sheets وإعداد شيت المستخدمين
        
        Returns:
            True إذا نجح الاتصال، False إذا فشل
        """
        try:
            # الاتصال بـ Google Sheets
            self.client = gspread.service_account(filename=self.credentials_file)
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            
            # الحصول على شيت المستخدمين أو إنشاؤه
            try:
                self.users_sheet = self.spreadsheet.worksheet(self.users_sheet_name)
            except gspread.WorksheetNotFound:
                # إنشاء شيت المستخدمين مع العناوين الجديدة
                self.users_sheet = self.spreadsheet.add_worksheet(
                    title=self.users_sheet_name,
                    rows=1000,
                    cols=8  # زيادة عدد الأعمدة
                )
                
                # إضافة العناوين المحدثة
                headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "تاريخ الإنشاء", "آخر تسجيل دخول", "الحالة"]
                self.users_sheet.update("A1:H1", [headers])
                
                print(f"✅ تم إنشاء شيت المستخدمين '{self.users_sheet_name}' بنجاح")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Google Sheets: {e}")
            return False
    

    def create_user(self, username: str, password: str, user_type: str = "user") -> bool:
        """
        إنشاء مستخدم جديد
        
        Args:
            username: اسم المستخدم
            password: كلمة المرور (بدون تشفير)
            user_type: نوع المستخدم (admin/user)
            
        Returns:
            True إذا تم إنشاء المستخدم بنجاح، False إذا فشل
        """
        try:
            if not self.users_sheet:
                print("❌ لم يتم الاتصال بشيت المستخدمين")
                return False
            
            # التحقق من صحة البيانات
            if not username or not username.strip():
                print("❌ اسم المستخدم لا يمكن أن يكون فارغاً")
                return False
                
            if not password or not password.strip():
                print("❌ كلمة المرور لا يمكن أن تكون فارغة")
                return False
                
            if len(username.strip()) < 3:
                print("❌ اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
                return False
                
            if len(password.strip()) < 4:
                print("❌ كلمة المرور يجب أن تكون 4 أحرف على الأقل")
                return False
            
            # التحقق من عدم وجود المستخدم مسبقاً
            if self.user_exists(username):
                print(f"❌ المستخدم '{username}' موجود بالفعل")
                return False
            
            # إعداد بيانات المستخدم الجديد
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            project_id = ""  # فارغ في البداية، سيتم تعيينه بواسطة الأدمن
            project_name = ""  # فارغ في البداية
            
            user_data = [
                username.strip(),
                password.strip(),  # تخزين كلمة المرور بدون تشفير كما طلبت
                user_type,
                project_id,  # رقم المشروع (فارغ)
                project_name,  # اسم المشروع (فارغ)
                "نشط",  # الحالة
                current_time,  # تاريخ الإنشاء
                ""  # آخر تسجيل دخول (فارغ)
            ]
            
            # إضافة المستخدم إلى الشيت
            next_row = len(self.users_sheet.get_all_values()) + 1
            self.users_sheet.update(f"A{next_row}:H{next_row}", [user_data])
            
            print(f"✅ تم إنشاء المستخدم '{username}' بنجاح")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء المستخدم: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        التحقق من صحة تسجيل الدخول
        
        Args:
            username: اسم المستخدم
            password: كلمة المرور
            
        Returns:
            معلومات المستخدم إذا تم التحقق بنجاح، None إذا فشل
        """
        try:
            if not self.users_sheet:
                print("❌ لم يتم الاتصال بشيت المستخدمين")
                return None
            
            # الحصول على جميع المستخدمين
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "تاريخ الإنشاء", "آخر تسجيل دخول", "الحالة"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            
            for i, user in enumerate(users_data, start=2):  # البداية من الصف 2
                if (user.get("اسم المستخدم", "").strip().lower() == username.strip().lower() and
                    user.get("كلمة المرور", "").strip() == password.strip()):
                    
                    # تحديث آخر تسجيل دخول (العمود H الآن)
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        self.users_sheet.update(f"H{i}", [[current_time]])
                    except Exception as update_error:
                        print(f"⚠️ تحذير: فشل في تحديث آخر دخول: {update_error}")
                    
                    # إرجاع معلومات المستخدم مع البيانات الجديدة
                    user_info = {
                        "username": user.get("اسم المستخدم", ""),
                        "user_type": user.get("نوع المستخدم", "user"),
                        "user_id": user.get("رقم التعريف", ""),  # إضافة رقم التعريف
                        "project_id": user.get("رقم المشروع", ""),
                        "project_name": user.get("اسم المشروع", ""),
                        "created_date": user.get("تاريخ الإنشاء", ""),
                        "last_login": current_time,
                        "status": user.get("الحالة", "نشط"),
                        "row": i  # رقم الصف في الشيت
                    }
                    
                    print(f"✅ تم تسجيل دخول المستخدم '{username}' بنجاح")
                    return user_info
            
            print(f"❌ اسم المستخدم أو كلمة المرور غير صحيحة")
            return None
            
        except Exception as e:
            print(f"❌ خطأ في التحقق من المستخدم: {e}")
            return None
    
    def user_exists(self, username: str) -> bool:
        """
        التحقق من وجود المستخدم
        
        Args:
            username: اسم المستخدم
            
        Returns:
            True إذا كان المستخدم موجوداً، False إذا لم يكن موجوداً
        """
        try:
            if not self.users_sheet:
                return False
            
            users_data = self.users_sheet.get_all_records()
            
            for user in users_data:
                if user.get("اسم المستخدم", "").strip().lower() == username.strip().lower():
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ خطأ في التحقق من وجود المستخدم: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """
        الحصول على قائمة جميع المستخدمين
        
        Returns:
            قائمة بمعلومات جميع المستخدمين
        """
        try:
            if not self.users_sheet:
                return []
            
            users_data = self.users_sheet.get_all_records()
            
            users_list = []
            for user in users_data:
                user_info = {
                    "username": user.get("اسم المستخدم", ""),
                    "user_type": user.get("نوع المستخدم", "user"),
                    "created_date": user.get("تاريخ الإنشاء", ""),
                    "last_login": user.get("آخر تسجيل دخول", ""),
                    "status": user.get("الحالة", "نشط")
                }
                users_list.append(user_info)
            
            return users_list
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على قائمة المستخدمين: {e}")
            return 0
    
    def assign_user_to_project(self, user_id: str, project_id: str) -> bool:
        """
        تعيين مستخدم لمشروع معين (للأدمن فقط)
        
        Args:
            user_id: رقم تعريف المستخدم
            project_id: رقم تعريف المشروع
            
        Returns:
            True إذا تم التعيين بنجاح
        """
        try:
            if not self.users_sheet:
                print("❌ لم يتم الاتصال بشيت المستخدمين")
                return False
            
            # البحث عن المستخدم باسم المستخدم (بدلاً من رقم التعريف)
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم المشروع", "اسم المشروع", "الحالة", "تاريخ الإنشاء", "آخر تسجيل دخول"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            
            for i, user in enumerate(users_data, start=2):
                if user.get("اسم المستخدم", "") == user_id:
                    # تحديث رقم المشروع (العمود D الآن)
                    try:
                        self.users_sheet.update(f"D{i}", [[project_id]])
                        print(f"✅ تم تعيين المستخدم '{user.get('اسم المستخدم', '')}' للمشروع '{project_id}'")
                        return True
                    except Exception as update_error:
                        print(f"❌ خطأ في تحديث المشروع: {update_error}")
                        return False
            
            print(f"❌ لم يتم العثور على مستخدم باسم '{user_id}'")
            return False
            
        except Exception as e:
            print(f"❌ خطأ في تعيين المستخدم للمشروع: {e}")
            return False
    
    def get_users_without_project(self) -> List[Dict]:
        """
        الحصول على قائمة بالمستخدمين الذين لم يتم تعيين مشروع لهم
        
        Returns:
            قائمة بالمستخدمين بدون مشروع
        """
        try:
            if not self.users_sheet:
                return []
            
            # تحديد العناوين المتوقعة
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم المشروع", "اسم المشروع", "الحالة", "تاريخ الإنشاء", "آخر تسجيل دخول"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            users_without_project = []
            
            for user in users_data:
                # التحقق من أن المستخدم عادي وليس له مشروع
                if (user.get("نوع المستخدم", "") == "user" and 
                    not user.get("رقم المشروع", "").strip()):
                    users_without_project.append({
                        "username": user.get("اسم المستخدم", ""),
                        "project_name": user.get("اسم المشروع", ""),
                        "created_date": user.get("تاريخ الإنشاء", "")
                    })
            
            return users_without_project
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على المستخدمين بدون مشروع: {e}")
            return []
    
    def get_user_count(self) -> int:
        """
        الحصول على عدد المستخدمين
        
        Returns:
            عدد المستخدمين المسجلين
        """
        try:
            if not self.users_sheet:
                return 0
            
            # تحديد العناوين المتوقعة
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "تاريخ الإنشاء", "آخر تسجيل دخول", "الحالة"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            return len(users_data)
            
        except Exception as e:
            print(f"❌ خطأ في حساب عدد المستخدمين: {e}")
            return 0
    
    def create_admin_user(self, username: str = "admin", password: str = "admin123") -> bool:
        """
        إنشاء مستخدم أدمن افتراضي
        
        Args:
            username: اسم المستخدم الأدمن (افتراضي: admin)
            password: كلمة المرور (افتراضي: admin123)
            
        Returns:
            True إذا تم إنشاء الأدمن بنجاح
        """
        try:
            # التحقق من عدم وجود مستخدم أدمن مسبقاً
            if self.user_exists(username):
                print(f"⚠️ المستخدم '{username}' موجود بالفعل")
                return False
            
            result = self.create_user(username, password, "admin")
            if result:
                print(f"🔑 تم إنشاء حساب الأدمن الافتراضي:")
                print(f"   👤 اسم المستخدم: {username}")
                print(f"   🔒 كلمة المرور: {password}")
                print(f"   ⚠️ يُنصح بتغيير كلمة المرور بعد أول تسجيل دخول")
            
            return result
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء حساب الأدمن: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """
        الحصول على جميع المستخدمين
        
        Returns:
            قائمة بجميع المستخدمين مع معلوماتهم
        """
        try:
            if not self.users_sheet:
                return []
            
            # تحديد العناوين المتوقعة
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "تاريخ الإنشاء", "آخر تسجيل دخول", "الحالة"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            
            users_list = []
            for user in users_data:
                users_list.append({
                    "username": user.get("اسم المستخدم", ""),
                    "user_type": user.get("نوع المستخدم", "user"),
                    "user_id": user.get("رقم التعريف", ""),
                    "project_id": user.get("رقم المشروع", ""),
                    "created_date": user.get("تاريخ الإنشاء", ""),
                    "last_login": user.get("آخر تسجيل دخول", ""),
                    "status": user.get("الحالة", "نشط")
                })
            
            return users_list
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على المستخدمين: {e}")
            return []
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """
        الحصول على مستخدم معين بمعرفه
        
        Args:
            user_id: رقم التعريف للمستخدم
            
        Returns:
            معلومات المستخدم أو None إذا لم يوجد
        """
        try:
            if not self.users_sheet or not user_id:
                return None
            
            # البحث عن المستخدم
            expected_headers = ["اسم المستخدم", "كلمة المرور", "نوع المستخدم", "رقم التعريف", "رقم المشروع", "تاريخ الإنشاء", "آخر تسجيل دخول", "الحالة"]
            users_data = self.users_sheet.get_all_records(expected_headers=expected_headers)
            
            for user in users_data:
                if user.get("رقم التعريف") == user_id:
                    return {
                        "username": user.get("اسم المستخدم", ""),
                        "user_type": user.get("نوع المستخدم", "user"),
                        "user_id": user.get("رقم التعريف", ""),
                        "project_id": user.get("رقم المشروع", ""),
                        "created_date": user.get("تاريخ الإنشاء", ""),
                        "last_login": user.get("آخر تسجيل دخول", ""),
                        "status": user.get("الحالة", "نشط")
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على المستخدم {user_id}: {e}")
            return None
