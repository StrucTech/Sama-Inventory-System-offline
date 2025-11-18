#!/usr/bin/env python3
"""
اختبار تكامل نظام التحديث الجديد مع البرنامج الرئيسي
"""

import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater

def test_main_integration():
    """اختبار تكامل النظام الجديد"""
    
    print("🧪 اختبار تكامل نظام التحديث الجديد")
    print("=" * 50)
    
    # محاكاة ما يحدث في البرنامج الرئيسي
    print("🚀 محاكاة بدء تشغيل البرنامج...")
    
    try:
        # إنشاء كائن التحديث (كما في البرنامج الفعلي)
        updater = AutoUpdater()
        
        print(f"\n📊 معلومات النظام:")
        print(f"   📌 الإصدار الحالي: {updater.current_version}")
        print(f"   🔄 وضع الفحص: {updater.get_check_mode_info()}")
        print(f"   ⚙️ التحديث التلقائي: {'مفعل ✅' if updater.auto_update else 'معطل ❌'}")
        print(f"   ⏱️ فترة الفحص: {updater.check_interval} {'(دائماً)' if updater.check_interval == 0 else 'ساعة'}")
        
        # اختبار منطق التحديث
        print(f"\n🔍 اختبار منطق الفحص:")
        should_check = updater.should_check_for_updates()
        print(f"   النتيجة: {'سيتم الفحص ✅' if should_check else 'لن يتم الفحص ❌'}")
        
        if should_check:
            print(f"\n📡 محاكاة فحص التحديثات...")
            # هنا في البرنامج الفعلي سيتم استدعاء:
            # update_info = updater.check_for_updates()
            print(f"   (في البرنامج الفعلي: سيتم الاتصال بـ GitHub)")
            print(f"   (سيتم فحص الإصدار الأحدث)")
            print(f"   (سيتم عرض رسالة التحديث إذا توفر)")
            
        # اختبار تحديث تاريخ آخر فحص
        print(f"\n📅 اختبار تحديث تاريخ آخر فحص...")
        updater.update_last_check_date()
        print(f"   ✅ تم تحديث التاريخ")
        
        # اختبار الفحص مرة أخرى
        print(f"\n🔄 اختبار الفحص مرة أخرى:")
        should_check_again = updater.should_check_for_updates()
        print(f"   النتيجة: {'سيتم الفحص ✅' if should_check_again else 'لن يتم الفحص ❌'}")
        
        print(f"\n" + "=" * 50)
        print(f"✅ جميع اختبارات التكامل نجحت!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ في اختبار التكامل: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_modes():
    """اختبار سلوك النظام مع الأوضاع المختلفة"""
    
    print(f"\n🎯 اختبار الأوضاع المختلفة:")
    print(f"-" * 30)
    
    updater = AutoUpdater()
    
    modes = [
        ("always", "فحص دائم"),
        ("daily", "فحص يومي"), 
        ("weekly", "فحص أسبوعي"),
        ("manual", "فحص يدوي")
    ]
    
    for mode, description in modes:
        print(f"\n🔧 اختبار وضع: {description} ({mode})")
        updater.set_check_mode(mode)
        
        should_check = updater.should_check_for_updates()
        status = "✅ سيفحص" if should_check else "❌ لن يفحص"
        
        print(f"   النتيجة: {status}")
        print(f"   الوصف: {updater.get_check_mode_info()}")

def main():
    """الدالة الرئيسية"""
    
    try:
        # اختبار التكامل الرئيسي
        success = test_main_integration()
        
        if success:
            # اختبار الأوضاع المختلفة
            test_different_modes()
            
            print(f"\n🎉 جميع الاختبارات تمت بنجاح!")
            print(f"⚡ النظام الجديد جاهز للاستخدام")
            print(f"🔄 سيتحقق من التحديثات في كل مرة يفتح البرنامج")
        else:
            print(f"\n❌ فشلت بعض الاختبارات")
            
    except Exception as e:
        print(f"\n💥 خطأ عام في الاختبار: {e}")

if __name__ == "__main__":
    main()