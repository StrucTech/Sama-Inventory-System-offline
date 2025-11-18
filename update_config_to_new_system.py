#!/usr/bin/env python3
"""
سكريبت تحديث إعدادات التحديث إلى النظام الجديد
"""

import os
import sys
import json
from datetime import datetime

def update_config_to_new_system():
    """تحديث ملف الإعدادات للنظام الجديد"""
    
    config_file = "update_info.json"
    
    print("🔄 تحديث إعدادات نظام التحديث...")
    print("-" * 40)
    
    try:
        # قراءة الملف الحالي
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ تم قراءة الملف الحالي")
        else:
            print(f"⚠️ ملف الإعدادات غير موجود، سيتم إنشاؤه")
            config = {}
        
        # عرض الإعدادات الحالية
        print(f"\n📋 الإعدادات الحالية:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        # التحديث للنظام الجديد
        config.update({
            "check_interval": 0,  # فحص دائماً (الافتراضي الجديد)
            "check_mode": "always",  # وضع الفحص
            "auto_update": True,
            "last_check": "",  # سيتم تحديثه عند أول فحص
            "updated_to_new_system": True,
            "updated_date": datetime.now().isoformat()
        })
        
        # التأكد من وجود البيانات الأساسية
        if "current_version" not in config:
            config["current_version"] = "1.2.4"
        
        if "update_url" not in config:
            config["update_url"] = "https://api.github.com/repos/StrucTech/Sama-Inventory-System/releases/latest"
        
        # حفظ الملف المحدث
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 الإعدادات الجديدة:")
        for key, value in config.items():
            if key == 'updated_date' and value:
                try:
                    update_date = datetime.fromisoformat(value)
                    print(f"   {key}: {update_date.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    print(f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n✅ تم تحديث ملف الإعدادات بنجاح!")
        print(f"🔄 النظام سيتحقق من التحديثات في كل مرة يفتح البرنامج")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث الإعدادات: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_instructions():
    """عرض تعليمات الاستخدام"""
    
    print(f"\n" + "=" * 50)
    print(f"📖 تعليمات الاستخدام الجديدة:")
    print(f"=" * 50)
    
    instructions = """
🔄 النظام الجديد:
   • يتحقق من التحديثات في كل مرة يفتح البرنامج
   • لا توجد حاجة للانتظار 24 ساعة
   • فحص سريع وفوري عند كل تشغيل

⚙️ الأوضاع المتاحة:
   • always  : فحص في كل مرة (افتراضي)
   • daily   : فحص يومياً (كل 24 ساعة)
   • weekly  : فحص أسبوعياً
   • manual  : فحص يدوي فقط

🛠️ لتغيير وضع الفحص:
   from auto_updater import AutoUpdater
   updater = AutoUpdater()
   updater.set_check_mode("daily")  # مثال

📊 لمعرفة الوضع الحالي:
   updater.get_check_mode_info()
   
✨ ميزات إضافية:
   • رسائل توضيحية عند الفحص
   • إحصائيات وقت آخر فحص
   • حفظ تلقائي للإعدادات
"""
    
    print(instructions)

def main():
    """الدالة الرئيسية"""
    
    print("🚀 تحديث نظام التحديثات إلى الإصدار الجديد")
    print("=" * 50)
    
    # تحديث الإعدادات
    if update_config_to_new_system():
        # عرض التعليمات
        show_usage_instructions()
        
        print(f"\n🎉 تم التحديث بنجاح!")
        print(f"⚡ البرنامج الآن سيتحقق من التحديثات فوراً عند كل تشغيل")
    else:
        print(f"\n❌ فشل في التحديث")

if __name__ == "__main__":
    main()