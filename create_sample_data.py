#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ملف إنشاء البيانات التجريبية لنظام إدارة المخازن
يقوم بإضافة بيانات واقعية مباشرة في ملفات Excel للاختبار
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random

def create_comprehensive_sample_data():
    """إنشاء بيانات تجريبية شاملة للمشاريع"""
    
    # قائمة المواد التجريبية الواقعية
    sample_items = [
        # المواد الغذائية الأساسية
        {"name": "أرز بسمتي", "category": "حبوب", "shelf_life": 730, "min_stock": 50},
        {"name": "سكر أبيض", "category": "محليات", "shelf_life": 365, "min_stock": 25},
        {"name": "زيت عباد الشمس", "category": "زيوت", "shelf_life": 365, "min_stock": 20},
        {"name": "دقيق قمح", "category": "حبوب", "shelf_life": 180, "min_stock": 30},
        {"name": "شاي أحمر", "category": "مشروبات", "shelf_life": 365, "min_stock": 15},
        {"name": "قهوة تركية", "category": "مشروبات", "shelf_life": 180, "min_stock": 10},
        {"name": "معكرونة", "category": "حبوب", "shelf_life": 365, "min_stock": 40},
        {"name": "عدس أحمر", "category": "بقوليات", "shelf_life": 365, "min_stock": 20},
        {"name": "فاصولياء بيضاء", "category": "بقوليات", "shelf_life": 365, "min_stock": 15},
        {"name": "حمص حب", "category": "بقوليات", "shelf_life": 365, "min_stock": 25},
        
        # منتجات الألبان
        {"name": "حليب مجفف", "category": "ألبان", "shelf_life": 30, "min_stock": 50},
        {"name": "جبن أبيض", "category": "ألبان", "shelf_life": 15, "min_stock": 30},
        {"name": "زبدة طبيعية", "category": "ألبان", "shelf_life": 20, "min_stock": 15},
        {"name": "لبن رائب", "category": "ألبان", "shelf_life": 7, "min_stock": 40},
        {"name": "كريمة طبخ", "category": "ألبان", "shelf_life": 10, "min_stock": 20},
        
        # اللحوم والدواجن (مجمدة)
        {"name": "دجاج مجمد", "category": "لحوم", "shelf_life": 90, "min_stock": 100},
        {"name": "لحم بقري", "category": "لحوم", "shelf_life": 120, "min_stock": 50},
        {"name": "سمك فيليه", "category": "أسماك", "shelf_life": 60, "min_stock": 30},
        {"name": "روبيان مجمد", "category": "أسماك", "shelf_life": 90, "min_stock": 20},
        
        # الخضروات المحفوظة
        {"name": "طماطم معلبة", "category": "خضروات", "shelf_life": 365, "min_stock": 50},
        {"name": "ذرة معلبة", "category": "خضروات", "shelf_life": 365, "min_stock": 30},
        {"name": "فطر معلب", "category": "خضروات", "shelf_life": 180, "min_stock": 20},
        {"name": "زيتون أخضر", "category": "مخللات", "shelf_life": 365, "min_stock": 25},
        {"name": "خيار مخلل", "category": "مخللات", "shelf_life": 180, "min_stock": 15},
        
        # التوابل والبهارات
        {"name": "فلفل أسود", "category": "توابل", "shelf_life": 365, "min_stock": 10},
        {"name": "كمون مطحون", "category": "توابل", "shelf_life": 180, "min_stock": 5},
        {"name": "كركم", "category": "توابل", "shelf_life": 365, "min_stock": 8},
        {"name": "قرفة", "category": "توابل", "shelf_life": 365, "min_stock": 5},
        {"name": "هيل", "category": "توابل", "shelf_life": 180, "min_stock": 3},
        
        # الحلويات والسناكس
        {"name": "شوكولاتة", "category": "حلويات", "shelf_life": 120, "min_stock": 100},
        {"name": "بسكويت", "category": "حلويات", "shelf_life": 90, "min_stock": 80},
        {"name": "رقائق ذرة", "category": "سناكس", "shelf_life": 60, "min_stock": 50},
        {"name": "مكسرات مشكلة", "category": "مكسرات", "shelf_life": 120, "min_stock": 20},
        
        # منتجات التنظيف
        {"name": "صابون غسيل", "category": "تنظيف", "shelf_life": 730, "min_stock": 30},
        {"name": "شامبو", "category": "عناية شخصية", "shelf_life": 365, "min_stock": 25},
        {"name": "معجون أسنان", "category": "عناية شخصية", "shelf_life": 365, "min_stock": 40},
        {"name": "منظف أطباق", "category": "تنظيف", "shelf_life": 365, "min_stock": 20},
        
        # الأدوية والمكملات
        {"name": "فيتامين سي", "category": "مكملات", "shelf_life": 30, "min_stock": 100},
        {"name": "مسكن ألم", "category": "أدوية", "shelf_life": 45, "min_stock": 200},
        {"name": "شراب كحة", "category": "أدوية", "shelf_life": 60, "min_stock": 50},
        {"name": "كريم جروح", "category": "أدوية", "shelf_life": 90, "min_stock": 30}
    ]
    
    # أسماء المستلمين المختلفة
    receivers = [
        "أحمد محمد", "فاطمة علي", "محمد حسن", "عائشة أحمد", "علي محمود",
        "نور الدين", "سارة يوسف", "خالد عبدالله", "مريم حسين", "عبدالله صالح",
        "ليلى عثمان", "حسام الدين", "رقية محمد", "يوسف إبراهيم", "زينب عمر"
    ]
    
    # ملاحظات متنوعة
    notes_templates = [
        "شحنة جديدة من المورد الرئيسي",
        "تجديد المخزون الأساسي",
        "طلبية خاصة للعملاء",
        "مخزون إضافي لفترة الذروة", 
        "توزيع على المتاجر الفرعية",
        "شحنة طارئة",
        "مخزون احتياطي",
        "طلبية موسمية",
        "تسليم مجدول",
        "توريد أسبوعي"
    ]
    
    return sample_items, receivers, notes_templates

def generate_realistic_transactions(project_name, num_transactions=150):
    """توليد معاملات واقعية للمشروع"""
    
    sample_items, receivers, notes_templates = create_comprehensive_sample_data()
    transactions = []
    
    # تاريخ البداية (آخر 6 أشهر)
    start_date = datetime.now() - timedelta(days=180)
    transaction_id = 1
    
    for i in range(num_transactions):
        # اختيار عشوائي للمادة
        item = random.choice(sample_items)
        
        # تحديد نوع العملية (80% دخول، 20% خروج)
        operation_type = "دخول" if random.random() < 0.8 else "خروج"
        
        # تحديد الكمية حسب نوع العملية
        if operation_type == "دخول":
            quantity = random.randint(20, 200)  # كميات أكبر للدخول
        else:
            quantity = random.randint(5, 50)   # كميات أصغر للخروج
        
        # تاريخ عشوائي خلال الفترة المحددة
        days_offset = random.randint(0, 180)
        transaction_date = start_date + timedelta(days=days_offset)
        
        # إضافة وقت عشوائي
        hour = random.randint(8, 18)  # ساعات العمل
        minute = random.randint(0, 59)
        transaction_date = transaction_date.replace(hour=hour, minute=minute)
        
        # اختيار مستلم عشوائي للخروج، أو "المخزن الرئيسي" للدخول
        if operation_type == "خروج":
            receiver = random.choice(receivers)
        else:
            receiver = "المخزن الرئيسي"
        
        # ملاحظة عشوائية
        note = random.choice(notes_templates)
        
        # إنشاء المعاملة
        transaction = {
            'رقم_المعاملة': f'{project_name.upper()}_T{transaction_id:04d}',
            'المشروع': project_name,
            'التاريخ': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'اسم_العنصر': item["name"],
            'التصنيف': item["category"],
            'نوع_العملية': operation_type,
            'الكمية': float(quantity),
            'اسم_المستلم': receiver,
            'مدة_الصلاحية_بالأيام': item["shelf_life"],
            'ملاحظات': note
        }
        
        transactions.append(transaction)
        transaction_id += 1
    
    return transactions

def create_sample_excel_files():
    """إنشاء ملفات Excel بالبيانات التجريبية"""
    
    projects = ["مخزن_المواد_الغذائية", "مخزن_المستلزمات_الطبية", "مخزن_العام"]
    
    for project in projects:
        print(f"إنشاء بيانات تجريبية للمشروع: {project}")
        
        # إنشاء المعاملات
        transactions = generate_realistic_transactions(project, 200)
        
        # إنشاء DataFrame
        df = pd.DataFrame(transactions)
        
        # ترتيب حسب التاريخ
        df['التاريخ'] = pd.to_datetime(df['التاريخ'])
        df = df.sort_values('التاريخ')
        df['التاريخ'] = df['التاريخ'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # حفظ ملف المعاملات
        transactions_file = os.path.join("projects", f"{project}_Transactions.xlsx")
        os.makedirs("projects", exist_ok=True)
        
        df.to_excel(transactions_file, index=False, engine='openpyxl')
        
        # إنشاء ملف التعديلات الفارغ
        modifications_file = os.path.join("projects", f"{project}_Modifications.xlsx")
        modifications_df = pd.DataFrame(columns=[
            'رقم_التعديل', 'المشروع', 'تاريخ_التعديل', 'رقم_المعاملة_الأصلية',
            'اسم_العنصر_القديم', 'اسم_العنصر_الجديد', 'الكمية_القديمة', 'الكمية_الجديدة',
            'نوع_العملية_القديمة', 'نوع_العملية_الجديدة', 'اسم_المستلم_القديم', 'اسم_المستلم_الجديد',
            'التصنيف_القديم', 'التصنيف_الجديد', 'مدة_الصلاحية_القديمة', 'مدة_الصلاحية_الجديدة',
            'الملاحظات_القديمة', 'الملاحظات_الجديدة', 'سبب_التعديل'
        ])
        modifications_df.to_excel(modifications_file, index=False, engine='openpyxl')
        
        print(f"✅ تم إنشاء {len(transactions)} معاملة للمشروع {project}")

def add_data_to_existing_projects():
    """إضافة بيانات للمشاريع الموجودة"""
    
    existing_projects = []
    projects_dir = "projects"
    
    if os.path.exists(projects_dir):
        for file in os.listdir(projects_dir):
            if file.endswith("_Transactions.xlsx"):
                project_name = file.replace("_Transactions.xlsx", "")
                existing_projects.append(project_name)
    
    for project in existing_projects:
        transactions_file = os.path.join("projects", f"{project}_Transactions.xlsx")
        
        try:
            # قراءة البيانات الموجودة
            existing_df = pd.read_excel(transactions_file, engine='openpyxl')
            
            # إضافة بيانات إضافية إذا كانت قليلة
            if len(existing_df) < 50:
                print(f"إضافة بيانات تجريبية للمشروع الموجود: {project}")
                
                new_transactions = generate_realistic_transactions(project, 100)
                new_df = pd.DataFrame(new_transactions)
                
                # دمج البيانات
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                
                # ترتيب حسب التاريخ
                combined_df['التاريخ'] = pd.to_datetime(combined_df['التاريخ'])
                combined_df = combined_df.sort_values('التاريخ')
                combined_df['التاريخ'] = combined_df['التاريخ'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # حفظ الملف المحدث
                combined_df.to_excel(transactions_file, index=False, engine='openpyxl')
                
                print(f"✅ تم إضافة {len(new_transactions)} معاملة جديدة للمشروع {project}")
            else:
                print(f"⏭️ المشروع {project} يحتوي على بيانات كافية ({len(existing_df)} معاملة)")
                
        except Exception as e:
            print(f"❌ خطأ في معالجة المشروع {project}: {e}")

if __name__ == "__main__":
    print("🚀 بدء إنشاء البيانات التجريبية لنظام إدارة المخازن")
    print("=" * 60)
    
    # إضافة بيانات للمشاريع الموجودة
    print("\n📂 فحص المشاريع الموجودة...")
    add_data_to_existing_projects()
    
    print("\n📋 إنشاء مشاريع تجريبية جديدة...")
    create_sample_excel_files()
    
    print("\n" + "=" * 60)
    print("✅ تم إنشاء جميع البيانات التجريبية بنجاح!")
    print("\n📊 المشاريع المتاحة الآن:")
    
    projects_dir = "projects"
    if os.path.exists(projects_dir):
        for file in os.listdir(projects_dir):
            if file.endswith("_Transactions.xlsx"):
                project_name = file.replace("_Transactions.xlsx", "")
                transactions_file = os.path.join(projects_dir, file)
                df = pd.read_excel(transactions_file, engine='openpyxl')
                print(f"  • {project_name}: {len(df)} معاملة")
    
    print("\n🎯 يمكنك الآن تشغيل البرنامج واستخدام البيانات التجريبية!")
    print("   أمر التشغيل: python main.py")