# -*- coding: utf-8 -*-
"""
مدير ملفات Excel لنظام إدارة المخزن
يقوم بإنشاء وإدارة ملفات Excel المطلوبة
"""

import pandas as pd
import os
from datetime import datetime


class ExcelManager:
    """مدير ملفات Excel"""
    
    def __init__(self, base_path="data"):
        self.base_path = base_path
        self.master_items_file = os.path.join(base_path, "Master_Items.xlsx")  # للتوافق مع الملفات القديمة
        
    def get_project_items_file(self, project_name):
        """الحصول على مسار ملف العناصر الخاص بالمشروع"""
        if not os.path.exists("projects"):
            os.makedirs("projects", exist_ok=True)
        return os.path.join("projects", f"{project_name}_Items.xlsx")
    
    def create_project_items_file(self, project_name):
        """إنشاء ملف العناصر الخاص بالمشروع"""
        project_items_file = self.get_project_items_file(project_name)
        
        if not os.path.exists(project_items_file):
            # إنشاء DataFrame فارغ مع الأعمدة المطلوبة
            columns = [
                'Item_ID',          # رقم تسلسلي
                'اسم_العنصر',        # اسم العنصر
                'التصنيف',          # التصنيف
                'مدة_الصلاحية_بالأيام',  # مدة الصلاحية
                'وصف'              # وصف العنصر
            ]
            
            df = pd.DataFrame(columns=columns)
            
            # إنشاء المجلد إذا لم يكن موجوداً
            os.makedirs("projects", exist_ok=True)
            
            # حفظ الملف
            df.to_excel(project_items_file, index=False, engine='openpyxl')
            print(f"تم إنشاء ملف العناصر للمشروع: {project_items_file}")
        
        return project_items_file
        
    def create_master_items_file(self):
        """إنشاء ملف العناصر الأساسي (للتوافق مع الملفات القديمة)"""
        if not os.path.exists(self.master_items_file):
            # إنشاء DataFrame فارغ مع الأعمدة المطلوبة
            columns = [
                'Item_ID',          # رقم تسلسلي
                'اسم_العنصر',        # اسم العنصر
                'التصنيف',          # التصنيف
                'مدة_الصلاحية_بالأيام',  # مدة الصلاحية
                'وصف'              # وصف العنصر
            ]
            
            df = pd.DataFrame(columns=columns)
            
            # إضافة بيانات عينة للتوضيح
            sample_data = [
                {
                    'Item_ID': 1,
                    'اسم_العنصر': 'أسمنت',
                    'التصنيف': 'مواد بناء',
                    'مدة_الصلاحية_بالأيام': 180,
                    'وصف': 'أسمنت عادي 50 كيس'
                },
                {
                    'Item_ID': 2,
                    'اسم_العنصر': 'حديد تسليح',
                    'التصنيف': 'مواد بناء',
                    'مدة_الصلاحية_بالأيام': None,
                    'وصف': 'حديد تسليح قطر 12 مم'
                },
                {
                    'Item_ID': 3,
                    'اسم_العنصر': 'بويات',
                    'التصنيف': 'تشطيبات',
                    'مدة_الصلاحية_بالأيام': 365,
                    'وصف': 'بويات داخلية'
                }
            ]
            
            df = pd.DataFrame(sample_data)
            
            # إنشاء المجلد إذا لم يكن موجوداً
            os.makedirs(self.base_path, exist_ok=True)
            
            # حفظ الملف
            df.to_excel(self.master_items_file, index=False, engine='openpyxl')
            print(f"تم إنشاء ملف العناصر الأساسي: {self.master_items_file}")
    
    def create_site_transactions_file(self, project_name):
        """إنشاء ملف حركات المشروع"""
        project_file = os.path.join("projects", f"{project_name}_Transactions.xlsx")
        
        if not os.path.exists(project_file):
            # إنشاء DataFrame فارغ مع الأعمدة المطلوبة (مع أرقام المعاملات)
            columns = [
                'رقم_المعاملة',      # رقم المعاملة المميز
                'المشروع',           # اسم المشروع
                'التاريخ',           # تاريخ العملية
                'اسم_العنصر',        # اسم العنصر
                'التصنيف',          # التصنيف
                'نوع_العملية',       # دخول/خروج/تعديل
                'الكمية',           # الكمية
                'اسم_المستلم',       # اسم المستلم
                'مدة_الصلاحية_بالأيام',  # مدة الصلاحية
                'ملاحظات',          # ملاحظات
                'رقم_المعاملة_المرجعية'  # رقم المعاملة المرجعية للتعديلات
            ]
            
            df = pd.DataFrame(columns=columns)
            
            # إنشاء مجلد المشاريع إذا لم يكن موجوداً
            os.makedirs("projects", exist_ok=True)
            
            # حفظ الملف
            df.to_excel(project_file, index=False, engine='openpyxl')
            print(f"تم إنشاء ملف حركات المشروع: {project_file}")
            
        return project_file
    
    def get_item_info(self, item_id, project_name=None):
        """الحصول على معلومات العنصر من ملف العناصر الخاص بالمشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.get_project_items_file(project_name)
            else:
                items_file = self.master_items_file
            
            if not os.path.exists(items_file):
                return None
            
            df = pd.read_excel(items_file, engine='openpyxl')
            item = df[df['Item_ID'] == item_id]
            
            if not item.empty:
                return {
                    'اسم العنصر': item.iloc[0]['اسم_العنصر'],
                    'التصنيف': item.iloc[0]['التصنيف'],
                    'مدة الصلاحية (أيام)': item.iloc[0]['مدة_الصلاحية_بالأيام'],
                    'وصف': item.iloc[0]['وصف'],
                    'Item_ID': item.iloc[0]['Item_ID']
                }
            else:
                return None
        except Exception as e:
            print(f"خطأ في قراءة ملف العناصر: {e}")
            return None
    
    def generate_transaction_id(self, project_name):
        """توليد رقم معاملة مميز"""
        try:
            project_file = os.path.join("projects", f"{project_name}_Transactions.xlsx")
            
            if os.path.exists(project_file):
                df = pd.read_excel(project_file, engine='openpyxl')
                
                # التحقق من وجود عمود رقم المعاملة والتوافق مع الملفات القديمة
                if not df.empty and 'رقم_المعاملة' in df.columns:
                    # الحصول على أعلى رقم موجود
                    max_id = df['رقم_المعاملة'].max()
                    return max_id + 1 if not pd.isna(max_id) else 1
                else:
                    # للملفات القديمة، نبدأ من رقم الصفوف + 1
                    return len(df) + 1 if not df.empty else 1
            else:
                return 1
                
        except Exception as e:
            # في حالة الخطأ، نستخدم timestamp كرقم مميز
            return int(datetime.now().timestamp())

    def ensure_columns_compatibility(self, df):
        """ضمان توافق الأعمدة مع الملفات القديمة"""
        required_columns = [
            'رقم_المعاملة', 'المشروع', 'التاريخ', 'اسم_العنصر', 'التصنيف',
            'نوع_العملية', 'الكمية', 'اسم_المستلم', 'مدة_الصلاحية_بالأيام', 
            'ملاحظات', 'رقم_المعاملة_المرجعية'
        ]
        
        # إضافة الأعمدة المفقودة
        for col in required_columns:
            if col not in df.columns:
                if col == 'رقم_المعاملة':
                    # إضافة أرقام تسلسلية للمعاملات الموجودة
                    df[col] = range(1, len(df) + 1)
                elif col == 'رقم_المعاملة_المرجعية':
                    # القيمة الافتراضية للمعاملات القديمة
                    df[col] = None
                else:
                    df[col] = df.get(col, None)
        
        return df[required_columns]  # إعادة ترتيب الأعمدة

    def add_transaction(self, project_name, item_info, operation_type, quantity, receiver_name, notes="", reference_id=None):
        """إضافة حركة جديدة مع رقم تسلسلي"""
        try:
            project_file = self.create_site_transactions_file(project_name)
            
            # قراءة الملف الحالي
            try:
                df = pd.read_excel(project_file, engine='openpyxl')
                # ضمان توافق الأعمدة
                df = self.ensure_columns_compatibility(df)
            except:
                # إذا كان الملف فارغاً
                df = pd.DataFrame(columns=[
                    'رقم_المعاملة', 'المشروع', 'التاريخ', 'اسم_العنصر', 'التصنيف', 
                    'نوع_العملية', 'الكمية', 'اسم_المستلم', 'مدة_الصلاحية_بالأيام', 'ملاحظات', 'رقم_المعاملة_المرجعية'
                ])
            
            # توليد رقم المعاملة
            transaction_id = self.generate_transaction_id(project_name)
            
            # إضافة الحركة الجديدة
            shelf_life = item_info.get('مدة الصلاحية (أيام)', None)
            if shelf_life is not None and pd.notna(shelf_life):
                shelf_life = int(shelf_life)
            else:
                shelf_life = None
                
            new_transaction = {
                'رقم_المعاملة': transaction_id,
                'المشروع': project_name,
                'التاريخ': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'اسم_العنصر': item_info.get('اسم العنصر', ''),
                'التصنيف': item_info.get('التصنيف', ''),
                'نوع_العملية': operation_type,
                'الكمية': float(quantity),
                'اسم_المستلم': receiver_name,
                'مدة_الصلاحية_بالأيام': shelf_life,
                'ملاحظات': notes if notes else '',
                'رقم_المعاملة_المرجعية': reference_id
            }
            
            # إضافة الصف الجديد
            df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)
            
            # حفظ الملف
            df.to_excel(project_file, index=False, engine='openpyxl')
            
            return True
            
        except Exception as e:
            print(f"خطأ في إضافة الحركة: {e}")
            return False
    
    def record_transaction(self, project_name, item_name, quantity, operation_type, notes="", custom_date=None, reference_id=None, category=None, item_details=None):
        """تسجيل معاملة مع إمكانية تحديد التاريخ والتصنيف وتفاصيل العنصر"""
        try:
            project_file = self.create_site_transactions_file(project_name)
            
            # إذا تم توفير تفاصيل العنصر (مثل عند التعديل)، استخدمها
            if item_details is not None:
                item_info = item_details
            else:
                # الحصول على معلومات العنصر من قاعدة البيانات
                item_info = self.get_item_info(item_name)
                if not item_info:
                    # إنشاء معلومات افتراضية إذا لم توجد
                    item_info = {
                        'اسم العنصر': item_name,
                        'التصنيف': 'غير محدد',
                        'مدة الصلاحية (أيام)': None
                    }
            
            # قراءة الملف الحالي
            try:
                df = pd.read_excel(project_file, engine='openpyxl')
                # ضمان توافق الأعمدة
                df = self.ensure_columns_compatibility(df)
            except:
                df = pd.DataFrame(columns=[
                    'رقم_المعاملة', 'المشروع', 'التاريخ', 'اسم_العنصر', 'التصنيف', 
                    'نوع_العملية', 'الكمية', 'اسم_المستلم', 'مدة_الصلاحية_بالأيام', 'ملاحظات', 'رقم_المعاملة_المرجعية'
                ])
            
            # تحديد التاريخ
            transaction_date = custom_date if custom_date else datetime.now()
            if isinstance(transaction_date, str):
                transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d %H:%M:%S')
            
            # إعداد بيانات المعاملة
            # محاولة الحصول على الصلاحية من أسماء أعمدة مختلفة
            shelf_life = None
            for key in ['مدة الصلاحية (أيام)', 'أيام_الصلاحية', 'مدة_الصلاحية_بالأيام', 'مدة الصلاحية']:
                if key in item_info:
                    shelf_life = item_info.get(key, None)
                    if shelf_life is not None and pd.notna(shelf_life):
                        shelf_life = int(shelf_life) if shelf_life else None
                    break
                
            # توليد رقم المعاملة
            transaction_id = self.generate_transaction_id(project_name)
            
            # استخدام التصنيف الممرر كمعامل أو التصنيف من معلومات العنصر
            item_category = category if category is not None else item_info.get('التصنيف', 'غير محدد')
            
            new_transaction = {
                'رقم_المعاملة': transaction_id,
                'المشروع': project_name,
                'التاريخ': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'اسم_العنصر': item_name,
                'التصنيف': item_category,
                'نوع_العملية': operation_type,
                'الكمية': float(quantity),
                'اسم_المستلم': 'النظام',  # للمعاملات التلقائية
                'مدة_الصلاحية_بالأيام': shelf_life,
                'ملاحظات': notes,
                'رقم_المعاملة_المرجعية': reference_id
            }
            
            # إضافة الصف الجديد
            df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)
            
            # حفظ الملف
            df.to_excel(project_file, index=False, engine='openpyxl')
            
            return True
            
        except Exception as e:
            print(f"خطأ في تسجيل المعاملة: {e}")
            return False
    
    def get_inventory_summary(self, project_name):
        """الحصول على ملخص المخزون الحالي"""
        try:
            project_file = os.path.join("projects", f"{project_name}_Transactions.xlsx")
            
            if not os.path.exists(project_file):
                return pd.DataFrame()
            
            df = pd.read_excel(project_file, engine='openpyxl')
            
            if df.empty:
                return pd.DataFrame()
            
            # حساب المخزون لكل عنصر
            inventory = []
            
            for item_name in df['اسم_العنصر'].unique():
                item_data = df[df['اسم_العنصر'] == item_name]
                
                # حساب الداخل والخارج والتعديلات
                incoming = item_data[item_data['نوع_العملية'] == 'دخول']['الكمية'].sum()
                outgoing = item_data[item_data['نوع_العملية'] == 'خروج']['الكمية'].sum()
                
                # إضافة عمليات التعديل
                modifications_increase = item_data[item_data['نوع_العملية'] == 'تعديل زيادة']['الكمية'].sum()
                modifications_decrease = item_data[item_data['نوع_العملية'] == 'تعديل نقص']['الكمية'].sum()
                
                current_stock = incoming - outgoing + modifications_increase - modifications_decrease
                
                # الحصول على آخر معلومات للعنصر
                last_entry = item_data.iloc[-1]
                
                inventory.append({
                    'اسم_العنصر': item_name,
                    'التصنيف': last_entry['التصنيف'],
                    'الكمية_الحالية': current_stock,
                    'إجمالي_الداخل': incoming,
                    'إجمالي_الخارج': outgoing,
                    'مدة_الصلاحية_بالأيام': last_entry['مدة_الصلاحية_بالأيام']
                })
            
            return pd.DataFrame(inventory)
            
        except Exception as e:
            print(f"خطأ في حساب المخزون: {e}")
            return pd.DataFrame()
    
    def get_all_projects(self):
        """الحصول على قائمة بجميع المشاريع"""
        try:
            projects = []
            if os.path.exists("projects"):
                for file in os.listdir("projects"):
                    if file.endswith("_Transactions.xlsx"):
                        project_name = file.replace("_Transactions.xlsx", "")
                        projects.append(project_name)
            return projects
        except:
            return []
    
    def get_next_item_id(self, project_name=None):
        """الحصول على الرقم التسلسلي التالي للعناصر في المشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.get_project_items_file(project_name)
            else:
                items_file = self.master_items_file
            
            if not os.path.exists(items_file):
                return 1
            
            df = pd.read_excel(items_file, engine='openpyxl')
            if df.empty:
                return 1
            return df['Item_ID'].max() + 1
        except:
            return 1
    
    def add_new_item(self, item_name, category, shelf_life, description, project_name=None):
        """إضافة عنصر جديد لملف العناصر الخاص بالمشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.create_project_items_file(project_name)
            else:
                items_file = self.master_items_file
                if not os.path.exists(items_file):
                    os.makedirs(self.base_path, exist_ok=True)
            
            # قراءة الملف الحالي
            if os.path.exists(items_file):
                df = pd.read_excel(items_file, engine='openpyxl')
            else:
                df = pd.DataFrame(columns=['Item_ID', 'اسم_العنصر', 'التصنيف', 'مدة_الصلاحية_بالأيام', 'وصف'])
            
            # الحصول على الرقم التسلسلي التالي
            new_id = self.get_next_item_id(project_name)
            
            # إضافة العنصر الجديد
            new_item = {
                'Item_ID': new_id,
                'اسم_العنصر': item_name,
                'التصنيف': category,
                'مدة_الصلاحية_بالأيام': shelf_life if shelf_life else None,
                'وصف': description
            }
            
            df = pd.concat([df, pd.DataFrame([new_item])], ignore_index=True)
            
            # حفظ الملف
            df.to_excel(items_file, index=False, engine='openpyxl')
            
            return new_id
            
        except Exception as e:
            print(f"خطأ في إضافة العنصر الجديد: {e}")
            return None
    
    def get_all_categories(self, project_name=None):
        """الحصول على جميع التصنيفات المتاحة في المشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.get_project_items_file(project_name)
                if not os.path.exists(items_file):
                    self.create_project_items_file(project_name)
            else:
                items_file = self.master_items_file
                if not os.path.exists(items_file):
                    self.create_master_items_file()
            
            df = pd.read_excel(items_file, engine='openpyxl')
            
            # استخراج التصنيفات الفريدة (بدون القيم الفارغة)
            categories = df['التصنيف'].dropna().unique().tolist()
            
            # ترتيب التصنيفات أبجدياً
            categories.sort()
            
            return categories
            
        except Exception as e:
            print(f"خطأ في تحميل التصنيفات: {e}")
            return []
    
    def get_items_by_category(self, category, project_name=None):
        """الحصول على العناصر حسب التصنيف في المشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.get_project_items_file(project_name)
                if not os.path.exists(items_file):
                    self.create_project_items_file(project_name)
            else:
                items_file = self.master_items_file
                if not os.path.exists(items_file):
                    self.create_master_items_file()
            
            df = pd.read_excel(items_file, engine='openpyxl')
            
            # تصفية العناصر حسب التصنيف
            filtered_items = df[df['التصنيف'] == category]
            
            return filtered_items
            
        except Exception as e:
            print(f"خطأ في تحميل العناصر حسب التصنيف: {e}")
            return pd.DataFrame()
    
    def get_all_items(self, project_name=None):
        """الحصول على جميع العناصر في المشروع"""
        try:
            # إذا لم يتم تحديد المشروع، استخدم الملف الأساسي (للتوافق)
            if project_name:
                items_file = self.get_project_items_file(project_name)
                if not os.path.exists(items_file):
                    self.create_project_items_file(project_name)
            else:
                items_file = self.master_items_file
                if not os.path.exists(items_file):
                    self.create_master_items_file()
            
            df = pd.read_excel(items_file, engine='openpyxl')
            return df
            
        except Exception as e:
            print(f"خطأ في تحميل جميع العناصر: {e}")
            return pd.DataFrame()
    
    def get_current_inventory(self, project_name):
        """الحصول على المخزون الحالي لمشروع"""
        try:
            return self.get_inventory_summary(project_name)
        except Exception as e:
            print(f"خطأ في تحميل المخزون الحالي: {e}")
            return pd.DataFrame()


# إنشاء instance للاستخدام
excel_manager = ExcelManager()