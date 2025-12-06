#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ملف اختبار البيانات التجريبية
للتأكد من صحة البيانات المُنشأة
"""

import pandas as pd
import os
from datetime import datetime

def test_sample_data():
    """اختبار البيانات التجريبية المُنشأة"""
    
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        print("❌ مجلد المشاريع غير موجود!")
        return
    
    print("🔍 فحص البيانات التجريبية...")
    print("=" * 50)
    
    projects = []
    for file in os.listdir(projects_dir):
        if file.endswith("_Transactions.xlsx"):
            project_name = file.replace("_Transactions.xlsx", "")
            projects.append(project_name)
    
    if not projects:
        print("❌ لا توجد مشاريع!")
        return
    
    total_transactions = 0
    
    for project in projects:
        transactions_file = os.path.join(projects_dir, f"{project}_Transactions.xlsx")
        
        try:
            df = pd.read_excel(transactions_file, engine='openpyxl')
            
            # إحصائيات أساسية
            incoming = len(df[df['نوع_العملية'] == 'دخول'])
            outgoing = len(df[df['نوع_العملية'] == 'خروج'])
            total = len(df)
            
            # تواريخ
            df['التاريخ'] = pd.to_datetime(df['التاريخ'])
            min_date = df['التاريخ'].min().strftime('%Y-%m-%d')
            max_date = df['التاريخ'].max().strftime('%Y-%m-%d')
            
            # عدد المواد المختلفة
            unique_items = df['اسم_العنصر'].nunique()
            
            # التصنيفات
            categories = df['التصنيف'].nunique()
            
            print(f"📦 مشروع: {project}")
            print(f"   📊 إجمالي المعاملات: {total}")
            print(f"   ⬆️  معاملات دخول: {incoming} ({incoming/total*100:.1f}%)")
            print(f"   ⬇️  معاملات خروج: {outgoing} ({outgoing/total*100:.1f}%)")
            print(f"   📅 فترة البيانات: {min_date} إلى {max_date}")
            print(f"   🏷️  عدد المواد: {unique_items}")
            print(f"   📂 عدد التصنيفات: {categories}")
            
            # عرض عينة من البيانات
            sample_items = df['اسم_العنصر'].head(5).tolist()
            print(f"   🔸 عينة مواد: {', '.join(sample_items)}")
            
            total_transactions += total
            print()
            
        except Exception as e:
            print(f"❌ خطأ في قراءة مشروع {project}: {e}")
    
    print("=" * 50)
    print(f"✅ إجمالي المعاملات في جميع المشاريع: {total_transactions}")
    print(f"📁 عدد المشاريع: {len(projects)}")
    print(f"📈 متوسط المعاملات لكل مشروع: {total_transactions/len(projects):.0f}")
    
    print("\n🎯 البيانات جاهزة للاختبار!")
    print("   يمكنك الآن تشغيل البرنامج: python main.py")

def show_inventory_summary():
    """عرض ملخص المخزون لمشروع واحد كمثال"""
    
    try:
        # أخذ مثال من أحد المشاريع
        sample_project = "مخزن_المواد_الغذائية"
        transactions_file = os.path.join("projects", f"{sample_project}_Transactions.xlsx")
        
        if not os.path.exists(transactions_file):
            print("❌ ملف المشروع التجريبي غير موجود!")
            return
        
        df = pd.read_excel(transactions_file, engine='openpyxl')
        
        print(f"\n📋 ملخص المخزون لمشروع: {sample_project}")
        print("=" * 60)
        
        # حساب المخزون الحالي
        inventory = {}
        
        for _, transaction in df.iterrows():
            item_name = transaction['اسم_العنصر']
            quantity = float(transaction['الكمية'])
            operation = transaction['نوع_العملية']
            
            if item_name not in inventory:
                inventory[item_name] = {'in': 0, 'out': 0, 'current': 0}
            
            if operation == 'دخول':
                inventory[item_name]['in'] += quantity
            else:
                inventory[item_name]['out'] += quantity
            
            inventory[item_name]['current'] = inventory[item_name]['in'] - inventory[item_name]['out']
        
        # عرض أفضل 10 مواد من ناحية الكمية
        sorted_items = sorted(inventory.items(), key=lambda x: x[1]['current'], reverse=True)[:10]
        
        print("🔝 أعلى 10 مواد في المخزون:")
        print("العنصر".ljust(25) + "الكمية الحالية".ljust(15) + "الدخول".ljust(15) + "الخروج")
        print("-" * 70)
        
        for item_name, data in sorted_items:
            current = int(data['current'])
            incoming = int(data['in'])
            outgoing = int(data['out'])
            
            print(f"{item_name[:24].ljust(25)}{str(current).ljust(15)}{str(incoming).ljust(15)}{str(outgoing)}")
        
        print("\n⚠️ تنبيهات:")
        
        # مواد بكمية قليلة (أقل من 20)
        low_stock = [(name, data['current']) for name, data in inventory.items() if 0 < data['current'] < 20]
        if low_stock:
            print("📉 مواد بكمية منخفضة:")
            for name, qty in low_stock[:5]:
                print(f"   • {name}: {int(qty)} وحدة")
        
        # مواد منتهية
        empty_stock = [(name, data['current']) for name, data in inventory.items() if data['current'] <= 0]
        if empty_stock:
            print("🚫 مواد منتهية من المخزون:")
            for name, qty in empty_stock[:5]:
                print(f"   • {name}: {int(qty)} وحدة")
                
    except Exception as e:
        print(f"❌ خطأ في عرض ملخص المخزون: {e}")

if __name__ == "__main__":
    print("🧪 اختبار البيانات التجريبية لنظام إدارة المخازن")
    print("=" * 60)
    
    test_sample_data()
    show_inventory_summary()
    
    print("\n" + "=" * 60)
    print("🎉 انتهى الاختبار بنجاح!")