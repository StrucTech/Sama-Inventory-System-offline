#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Activity Log to verify quantity differences are recorded correctly.
فحص سجل الأنشطة للتأكد من تسجيل الفروقات بشكل صحيح
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sheets.manager import SheetsManager

def check_activity_log():
    """Check the activity log for quantity difference records."""
    
    print("📋 فحص سجل الأنشطة لعمليات تعديل الكميات")
    print("=" * 60)
    
    # Initialize sheets manager
    sheets_manager = SheetsManager('config/credentials.json', 'Inventory Management')
    
    if not sheets_manager.connect():
        print("❌ فشل الاتصال بـ Google Sheets")
        return False
    
    print("✅ تم الاتصال بـ Google Sheets بنجاح")
    
    try:
        # Get activity log data
        activity_sheet = sheets_manager.spreadsheet.worksheet('Activity_Log_v2_20251108')
        all_data = activity_sheet.get_all_values()
        
        if len(all_data) < 2:
            print("❌ لا توجد بيانات في سجل الأنشطة")
            return False
        
        headers = all_data[0]
        print(f"\n📊 أعمدة سجل الأنشطة:")
        for i, header in enumerate(headers):
            print(f"   {i+1}. {header}")
        
        # Filter for update operations (تعديل)
        update_operations = []
        for row in all_data[1:]:
            if len(row) >= 3 and row[2] == "تعديل":  # نوع العملية في العمود الثالث
                update_operations.append(row)
        
        print(f"\n🔍 تم العثور على {len(update_operations)} عملية تعديل")
        
        if update_operations:
            print("\n📝 آخر 5 عمليات تعديل:")
            print("-" * 100)
            
            # Show last 5 update operations
            recent_updates = update_operations[-5:] if len(update_operations) >= 5 else update_operations
            
            for i, row in enumerate(recent_updates, 1):
                print(f"\n{i}. التاريخ: {row[0] if len(row) > 0 else 'غير محدد'}")
                print(f"   الوقت: {row[1] if len(row) > 1 else 'غير محدد'}")
                print(f"   العنصر: {row[3] if len(row) > 3 else 'غير محدد'}")
                print(f"   التصنيف: {row[4] if len(row) > 4 else 'غير محدد'}")
                print(f"   الكمية المضافة: {row[5] if len(row) > 5 else 'غير محدد'}")
                print(f"   الكمية المخرجة: {row[6] if len(row) > 6 else 'غير محدد'}")
                print(f"   الكمية السابقة: {row[7] if len(row) > 7 else 'غير محدد'}")
                print(f"   الكمية الحالية: {row[8] if len(row) > 8 else 'غير محدد'}")
                print(f"   المستخدم: {row[9] if len(row) > 9 else 'غير محدد'}")
                print(f"   التفاصيل: {row[11] if len(row) > 11 else 'غير محدد'}")
                
                # Calculate difference if possible
                try:
                    if len(row) > 8 and row[7] and row[8]:
                        old_qty = float(row[7])
                        new_qty = float(row[8])
                        difference = new_qty - old_qty
                        print(f"   ✅ الفرق المحسوب: {difference:+.1f}")
                        
                        # Check if it matches the recorded quantities
                        added = float(row[5]) if len(row) > 5 and row[5] and row[5] != "0" else 0
                        removed = float(row[6]) if len(row) > 6 and row[6] and row[6] != "0" else 0
                        recorded_diff = added - removed
                        
                        if abs(difference - recorded_diff) < 0.1:
                            print(f"   ✅ التسجيل صحيح: {recorded_diff:+.1f}")
                        else:
                            print(f"   ❌ خطأ في التسجيل: متوقع {difference:+.1f}, مسجل {recorded_diff:+.1f}")
                            
                except (ValueError, TypeError) as e:
                    print(f"   ⚠️ لا يمكن حساب الفرق: {e}")
        
        print(f"\n📈 إحصائيات:")
        print(f"   إجمالي السجلات: {len(all_data) - 1}")
        print(f"   عمليات التعديل: {len(update_operations)}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص سجل الأنشطة: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        check_activity_log()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الفحص بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ في الفحص: {e}")
        import traceback
        traceback.print_exc()