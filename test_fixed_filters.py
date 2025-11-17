#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل للفلاتر المصححة
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from gui.filter_search_window import show_filter_search_window
from sheets.manager import SheetsManager

def test_comprehensive_filters():
    """اختبار شامل للفلاتر المصححة"""
    
    print("🧪 اختبار شامل للفلاتر المصححة...")
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("اختبار الفلاتر المصححة")
    root.geometry("700x500")
    
    # النص التوضيحي
    main_label = ttk.Label(root, text='اختبار الفلاتر المصححة - جميع المشاكل محلولة', 
                          font=('Arial', 14, 'bold'))
    main_label.pack(pady=20)
    
    # دوال الاختبار
    def test_admin_user():
        """اختبار المستخدم المدير"""
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if sheets_manager.connect():
            print('✅ اختبار المدير - تم الاتصال بـ Google Sheets')
            
            # بيانات مستخدم مدير
            admin_user = {'username': 'admin_test', 'user_type': 'admin'}
            
            filter_window = show_filter_search_window(root, sheets_manager, admin_user)
            print('🔑 تم فتح نافذة الفلاتر للمدير (يرى جميع البيانات)')
        else:
            print('❌ فشل في الاتصال')
    
    def test_regular_user():
        """اختبار المستخدم العادي"""
        sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
        
        if sheets_manager.connect():
            print('✅ اختبار المستخدم العادي - تم الاتصال بـ Google Sheets')
            
            # بيانات مستخدم عادي مع مشروع محدد
            regular_user = {
                'username': 'user_test', 
                'user_type': 'user',
                'project_id': 'PRJ_001'
            }
            
            filter_window = show_filter_search_window(root, sheets_manager, regular_user)
            print('👤 تم فتح نافذة الفلاتر للمستخدم العادي (يرى مشروعه فقط)')
        else:
            print('❌ فشل في الاتصال')
    
    # إطار الأزرار
    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(pady=30)
    
    # زر اختبار المدير
    admin_btn = ttk.Button(buttons_frame, text='🔑 اختبار المستخدم المدير\n(يرى جميع البيانات والمشاريع)',
                          command=test_admin_user)
    admin_btn.pack(pady=10, fill=tk.X)
    
    # زر اختبار المستخدم العادي
    user_btn = ttk.Button(buttons_frame, text='👤 اختبار المستخدم العادي\n(يرى مشروع PRJ_001 فقط)',
                         command=test_regular_user)
    user_btn.pack(pady=10, fill=tk.X)
    
    # معلومات الإصلاحات
    info_frame = ttk.LabelFrame(root, text="الإصلاحات المطبقة", padding="10")
    info_frame.pack(fill=tk.X, padx=20, pady=20)
    
    fixes_text = """✅ تم إصلاح جميع المشاكل:

1. 🔄 الفلاتر تعمل تلقائياً الآن (جميع الفلاتر وليس التاريخ فقط)
2. 📊 الإحصائيات تعرض مجاميع الكميات وليس أعداد العناصر
3. 🔒 المستخدم العادي يرى عناصر مشروعه فقط
4. 📅 نطاق التواريخ يظهر بوضوح في منتقي التاريخ
5. 🎯 تحسين دقة البحث والفلترة
6. 📋 عرض أفضل للنتائج والإحصائيات

جرب الاختبارات أعلاه لترى الفرق!"""
    
    info_label = tk.Label(info_frame, text=fixes_text, 
                         font=('Arial', 10), justify=tk.LEFT, foreground='blue')
    info_label.pack()
    
    print("🖱️ اختر نوع المستخدم لاختبار الفلاتر المصححة")
    root.mainloop()

if __name__ == "__main__":
    test_comprehensive_filters()