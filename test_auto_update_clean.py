#!/usr/bin/env python3
"""
اختبار فوري للتحديث التلقائي
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater
import json
from datetime import datetime, timedelta

def force_update_check():
    """إجبار فحص التحديثات فوراً"""
    
    print("🧪 اختبار فوري للتحديث التلقائي")
    print("=" * 50)
    
    try:
        with open('update_info.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📋 الإصدار الحالي: {config.get('current_version')}")
        
        # تعديل تاريخ آخر فحص لإجبار الفحص
        old_date = datetime.now() - timedelta(hours=25)
        config['last_check'] = old_date.isoformat()
        
        with open('update_info.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"⏰ تم تعديل تاريخ آخر فحص إلى: {old_date}")
        
        # إنشاء مثيل المحدث واختباره
        updater = AutoUpdater()
        
        should_check = updater.should_check_for_updates()
        print(f"📅 يحتاج فحص: {'نعم' if should_check else 'لا'}")
        
        if should_check:
            print("🔍 بدء فحص التحديثات...")
            update_info = updater.check_for_updates()
            
            if update_info:
                print(f"✅ وُجد تحديث!")
                print(f"   الإصدار الجديد: {update_info.get('version')}")
                print(f"   رابط التحميل: {update_info.get('download_url', 'غير متاح')}")
            else:
                print("ℹ️ لا توجد تحديثات متاحة")
        
        # إعادة تعيين التاريخ الأصلي
        config['last_check'] = datetime.now().isoformat()
        with open('update_info.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ تم الانتهاء من الاختبار")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

def simulate_user_experience():
    """محاكاة تجربة المستخدم"""
    
    print("\n🎭 محاكاة تجربة المستخدم")
    print("-" * 30)
    
    print("📱 سيناريو: مستخدم يشغل البرنامج القديم (1.2.2)")
    print("⏰ الوقت: بعد 24 ساعة من إطلاق 1.2.3")
    print("")
    
    print("🔄 البرنامج يبدأ...")
    print("  ✅ تحميل النظام")
    print("  🔍 فحص التحديثات التلقائي")
    print("  📡 الاتصال بـ GitHub API")
    print("  🆕 وُجد إصدار جديد: 1.2.3")
    print("  💬 عرض رسالة التحديث")
    print("")
    
    print("💬 رسالة للمستخدم:")
    print("┌─────────────────────────────────┐")
    print("│ 🔄 تحديث متاح - الإصدار 1.2.3 │")
    print("│                                 │")
    print("│ ✨ ميزات جديدة:               │")
    print("│ • نظام فلاتر محسن              │") 
    print("│ • قيود وصول للمستخدمين        │")
    print("│ • واجهة أفضل وأسرع            │")
    print("│                                 │")
    print("│ 📥 تحديث الآن؟                │")
    print("│ [نعم] [لاحقاً] [لا تسأل مرة أخرى]│")
    print("└─────────────────────────────────┘")
    print("")
    
    print("👆 المستخدم يختار: [نعم]")
    print("  📥 بدء تحميل التحديث...")
    print("  📊 شريط التقدم: ████████████ 100%")
    print("  💾 تطبيق التحديث...")
    print("  🔄 إعادة تشغيل البرنامج...")
    print("  ✅ البرنامج الآن يعمل بالإصدار 1.2.3!")

if __name__ == "__main__":
    force_update_check()
    simulate_user_experience()