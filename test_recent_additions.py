#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار وظيفة تعديل آخر كمية مضافة
"""

from sheets.manager import SheetsManager
from datetime import datetime, timedelta

def test_recent_additions():
    print("🔍 اختبار وظيفة تعديل آخر كمية مضافة")
    
    # الاتصال بـ Google Sheets
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل في الاتصال بـ Google Sheets")
        return
    
    print("✅ تم الاتصال بـ Google Sheets")
    
    # اختبار الوصول لـ activity sheet
    try:
        try:
            activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
            print("✅ تم الوصول لـ activity sheet")
        except Exception as e:
            print(f"❌ لا يمكن الوصول لـ activity sheet: {e}")
            return
        
        # جلب البيانات
        all_values = activity_sheet.get_all_values()
        print(f"📊 إجمالي الصفوف في activity sheet: {len(all_values)}")
        
        if not all_values or len(all_values) < 2:
            print("⚠️ لا توجد بيانات في activity sheet")
            return
            
        headers = all_values[0]
        print(f"📋 Headers: {headers}")
        
        # اختبار البحث عن عمليات حديثة لعنصر معين
        test_item_name = "test_item_fixed"  # العنصر الذي أضفناه للاختبار
        test_username = "test_user"
        
        print(f"\n🔍 البحث عن عمليات حديثة للعنصر: {test_item_name}")
        print(f"👤 المستخدم: {test_username}")
        
        # تصفية العمليات
        recent_additions = []
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        for i, row in enumerate(all_values[1:], 2):  # تجاهل الـ header
            if len(row) >= 12:  # التأكد من وجود جميع الأعمدة
                date_str = row[0]  # التاريخ
                time_str = row[1]  # الوقت  
                operation_type = row[2]  # نوع العملية
                activity_item = row[3]  # العنصر
                category = row[4]  # التصنيف
                quantity_added = row[5]  # الكمية المضافة
                quantity_removed = row[6]  # الكمية المسحوبة
                previous_quantity = row[7]  # الكمية السابقة
                current_quantity = row[8]  # الكمية الحالية
                recipient_name = row[9]  # اسم المستلم/المستخدم
                project_number = row[10]  # رقم المشروع
                details = row[11] if len(row) > 11 else ""  # التفاصيل
                
                print(f"\n📝 صف {i}: {operation_type} - {activity_item} - {recipient_name}")
                print(f"   التاريخ: {date_str} {time_str}")
                print(f"   الكمية المضافة: {quantity_added}")
                print(f"   التفاصيل: {details}")
                
                # التحقق من أن العملية مطابقة
                is_matching_operation = (
                    operation_type in ["إضافة", "تحديث", "إضافة عنصر", "تحديث كمية"] and 
                    activity_item == test_item_name and 
                    (recipient_name == test_username or details.find(test_username) != -1) and
                    float(quantity_added or 0) > 0
                )
                
                if is_matching_operation:
                    print(f"✅ عملية مطابقة!")
                    try:
                        # تحويل التاريخ والوقت
                        activity_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                        
                        # التحقق من أن العملية خلال آخر 24 ساعة
                        if activity_datetime >= cutoff_time:
                            print(f"✅ العملية خلال آخر 24 ساعة")
                            recent_additions.append({
                                'datetime': activity_datetime,
                                'quantity_added': float(quantity_added or 0),
                                'operation_type': operation_type,
                                'details': details
                            })
                        else:
                            print(f"⚠️ العملية خارج نطاق الـ 24 ساعة")
                    except (ValueError, IndexError) as e:
                        print(f"❌ خطأ في تحويل التاريخ: {e}")
                else:
                    print(f"❌ العملية غير مطابقة")
        
        print(f"\n📊 النتيجة النهائية:")
        print(f"   العمليات الحديثة الموجودة: {len(recent_additions)}")
        
        if recent_additions:
            total_added = sum(addition['quantity_added'] for addition in recent_additions)
            print(f"   إجمالي الكمية المضافة: {total_added}")
            
            for i, addition in enumerate(recent_additions, 1):
                print(f"   العملية {i}: {addition['operation_type']} - {addition['quantity_added']} - {addition['datetime']}")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recent_additions()