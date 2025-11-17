"""
مدير المشاريع - إدارة المشاريع المتاحة في Google Sheets
يتعامل مع شيت "Projects" لتخزين بيانات المشاريع
"""

import gspread
from typing import Optional, Dict, List
import datetime

class ProjectsManager:
    """مدير المشاريع لإدارة المشاريع المتاحة"""
    
    def __init__(self, credentials_file: str, spreadsheet_name: str):
        """
        تهيئة مدير المشاريع
        
        Args:
            credentials_file: مسار ملف بيانات اعتماد Google API
            spreadsheet_name: اسم جدول Google Sheets
        """
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.projects_sheet_name = "Projects"
        
        self.client = None
        self.spreadsheet = None
        self.projects_sheet = None
        
    def connect(self) -> bool:
        """
        الاتصال بـ Google Sheets وإعداد شيت المشاريع
        
        Returns:
            True إذا نجح الاتصال، False إذا فشل
        """
        try:
            # الاتصال بـ Google Sheets
            self.client = gspread.service_account(filename=self.credentials_file)
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            
            # الحصول على شيت المشاريع أو إنشاؤه
            try:
                self.projects_sheet = self.spreadsheet.worksheet(self.projects_sheet_name)
            except gspread.WorksheetNotFound:
                # إنشاء شيت المشاريع مع العناوين
                self.projects_sheet = self.spreadsheet.add_worksheet(
                    title=self.projects_sheet_name,
                    rows=1000,
                    cols=7
                )
                
                # إضافة العناوين
                headers = ["رقم المشروع", "اسم المشروع", "الوصف", "تاريخ البداية", "تاريخ النهاية المتوقعة", "الحالة", "المدير المسؤول", "الميزانية"]
                self.projects_sheet.update("A1:G1", [headers])
                
                print(f"✅ تم إنشاء شيت المشاريع '{self.projects_sheet_name}' بنجاح")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Google Sheets: {e}")
            return False
    
    def generate_project_id(self) -> str:
        """
        توليد رقم تعريفي فريد للمشروع
        
        Returns:
            رقم تعريفي فريد (مثل: PRJ_001)
        """
        try:
            if not self.projects_sheet:
                return "PRJ_001"
            
            # الحصول على جميع الأرقام التعريفية الموجودة
            all_values = self.projects_sheet.get_all_values()
            if len(all_values) <= 1:  # فقط العناوين
                return "PRJ_001"
            
            # البحث عن أعلى رقم تعريفي
            max_id = 0
            for row in all_values[1:]:  # تخطي العناوين
                if len(row) > 0 and row[0]:  # العمود A (رقم المشروع)
                    try:
                        # استخراج الرقم من PRJ_XXX
                        if row[0].startswith("PRJ_"):
                            num = int(row[0].split("_")[1])
                            max_id = max(max_id, num)
                    except:
                        continue
            
            # إنشاء الرقم التعريفي الجديد
            new_id = max_id + 1
            return f"PRJ_{new_id:03d}"
            
        except Exception as e:
            print(f"❌ خطأ في توليد رقم المشروع: {e}")
            return "PRJ_001"
    
    def create_project(self, name: str, description: str = "", status: str = "نشط") -> str:
        """
        إنشاء مشروع جديد
        
        Args:
            name: اسم المشروع
            description: وصف المشروع
            status: حالة المشروع (افتراضي: نشط)
            
        Returns:
            رقم المشروع الجديد إذا نجح، فارغ إذا فشل
        """
        try:
            if not self.projects_sheet:
                print("❌ لم يتم الاتصال بشيت المشاريع")
                return ""
            
            # التحقق من صحة البيانات
            if not name or not name.strip():
                print("❌ اسم المشروع لا يمكن أن يكون فارغاً")
                return ""
            
            # توليد رقم المشروع
            project_id = self.generate_project_id()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # إعداد بيانات المشروع الجديد
            project_data = [
                project_id,  # رقم المشروع
                name.strip(),  # اسم المشروع
                description.strip(),  # الوصف
                current_time,  # تاريخ البداية
                "",  # تاريخ النهاية المتوقعة (يمكن تحديده لاحقاً)
                status,  # الحالة
                "",  # المدير المسؤول (يمكن تحديده لاحقاً)
                ""   # الميزانية (يمكن تحديدها لاحقاً)
            ]
            
            # إضافة المشروع إلى الشيت
            next_row = len(self.projects_sheet.get_all_values()) + 1
            self.projects_sheet.update(f"A{next_row}:H{next_row}", [project_data])
            
            print(f"✅ تم إنشاء المشروع '{name}' برقم '{project_id}'")
            return project_id
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء المشروع: {e}")
            return ""
    
    def get_all_projects(self) -> List[Dict]:
        """
        الحصول على جميع المشاريع
        
        Returns:
            قائمة بجميع المشاريع
        """
        try:
            if not self.projects_sheet:
                return []
            
            projects_data = self.projects_sheet.get_all_records()
            projects_list = []
            
            for project in projects_data:
                projects_list.append({
                    "project_id": project.get("رقم المشروع", ""),
                    "name": project.get("اسم المشروع", ""),
                    "description": project.get("الوصف", ""),
                    "status": project.get("الحالة", ""),  # تصحيح اسم العمود
                    "created_date": project.get("تاريخ البداية", ""),  # تصحيح اسم العمود
                    "start_date": project.get("تاريخ البداية", ""),
                    "end_date": project.get("تاريخ النهاية المتوقعة", "")  # تصحيح اسم العمود
                })
            
            return projects_list
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على المشاريع: {e}")
            return []
    
    def get_active_projects(self) -> List[Dict]:
        """
        الحصول على المشاريع النشطة فقط
        
        Returns:
            قائمة بالمشاريع النشطة
        """
        try:
            all_projects = self.get_all_projects()
            active_projects = [p for p in all_projects if p.get("status", "") == "نشط"]
            return active_projects
            
        except Exception as e:
            print(f"❌ خطأ في الحصول على المشاريع النشطة: {e}")
            return []
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict]:
        """
        الحصول على مشروع بالرقم التعريفي
        
        Args:
            project_id: رقم تعريف المشروع
            
        Returns:
            معلومات المشروع أو None إذا لم يتم العثور عليه
        """
        try:
            all_projects = self.get_all_projects()
            for project in all_projects:
                if project.get("project_id", "") == project_id:
                    return project
            return None
            
        except Exception as e:
            print(f"❌ خطأ في البحث عن المشروع: {e}")
            return None
    
    def update_project_status(self, project_id: str, new_status: str) -> bool:
        """
        تحديث حالة مشروع
        
        Args:
            project_id: رقم تعريف المشروع
            new_status: الحالة الجديدة
            
        Returns:
            True إذا تم التحديث بنجاح
        """
        try:
            if not self.projects_sheet:
                print("❌ لم يتم الاتصال بشيت المشاريع")
                return False
            
            # البحث عن المشروع
            projects_data = self.projects_sheet.get_all_records()
            
            for i, project in enumerate(projects_data, start=2):
                if project.get("رقم المشروع", "") == project_id:
                    # تحديث الحالة (العمود F)
                    try:
                        self.projects_sheet.update(f"F{i}", [[new_status]])
                        print(f"✅ تم تحديث حالة المشروع '{project_id}' إلى '{new_status}'")
                        return True
                    except Exception as update_error:
                        print(f"❌ خطأ في تحديث الحالة: {update_error}")
                        return False
            
            print(f"❌ لم يتم العثور على مشروع برقم '{project_id}'")
            return False
            
        except Exception as e:
            print(f"❌ خطأ في تحديث حالة المشروع: {e}")
            return False
    
    def get_project_count(self) -> int:
        """
        الحصول على عدد المشاريع
        
        Returns:
            عدد المشاريع المسجلة
        """
        try:
            if not self.projects_sheet:
                return 0
            
            projects_data = self.projects_sheet.get_all_records()
            return len(projects_data)
            
        except Exception as e:
            print(f"❌ خطأ في حساب عدد المشاريع: {e}")
            return 0