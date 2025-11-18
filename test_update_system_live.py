#!/usr/bin/env python3
"""
اختبار نظام التحديث - محاكاة فحص الإصدارات الجديدة
"""

import requests
import json
from datetime import datetime

def test_update_check():
    """اختبار فحص التحديثات من GitHub"""
    
    print("🧪 اختبار نظام التحديث...")
    print("=" * 50)
    
    # معلومات النظام الحالي
    current_version = "1.2.4"  # محاكاة الإصدار القديم
    api_url = "https://api.github.com/repos/StrucTech/Sama-Inventory-System/releases/latest"
    
    print(f"📱 الإصدار الحالي: {current_version}")
    print(f"🌐 فحص: {api_url}")
    
    try:
        # محاكاة ما يحدث في البرنامج
        print("\n🔍 جاري فحص التحديثات...")
        
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            release_data = response.json()
            
            # استخراج معلومات الإصدار
            latest_version = release_data['tag_name'].replace('v', '')
            release_name = release_data['name']
            published_date = release_data['published_at']
            download_url = None
            
            # البحث عن ملف ZIP
            for asset in release_data.get('assets', []):
                if asset['name'].endswith('.zip'):
                    download_url = asset['browser_download_url']
                    break
            
            print(f"\n📊 نتائج الفحص:")
            print(f"   🏷️ أحدث إصدار: {latest_version}")
            print(f"   📅 تاريخ النشر: {published_date}")
            print(f"   📝 اسم الإصدار: {release_name}")
            
            # مقارنة الإصدارات
            def compare_versions(current, latest):
                """مقارنة بسيطة للإصدارات"""
                try:
                    current_parts = [int(x) for x in current.split('.')]
                    latest_parts = [int(x) for x in latest.split('.')]
                    
                    # مقارنة كل جزء
                    for i in range(max(len(current_parts), len(latest_parts))):
                        c = current_parts[i] if i < len(current_parts) else 0
                        l = latest_parts[i] if i < len(latest_parts) else 0
                        
                        if l > c:
                            return True
                        elif l < c:
                            return False
                    return False
                except:
                    return latest != current
            
            # التحقق من وجود تحديث
            has_update = compare_versions(current_version, latest_version)
            
            print(f"\n🎯 النتيجة:")
            if has_update:
                print(f"   🎉 يتوفر تحديث جديد!")
                print(f"   ⬆️ من {current_version} إلى {latest_version}")
                
                if download_url:
                    print(f"   📥 رابط التحميل: {download_url}")
                    
                    # محاكاة ما سيظهر للمستخدم
                    print(f"\n📢 ما سيراه المستخدم:")
                    print(f"   العنوان: 'تحديث جديد متوفر'")
                    print(f"   الرسالة: 'الإصدار {latest_version} متوفر للتحميل'")
                    print(f"   الأزرار: [تحديث الآن] [عرض التفاصيل] [لاحقاً]")
                else:
                    print(f"   ⚠️ لم يتم العثور على ملف للتحميل")
            else:
                print(f"   ✅ البرنامج محدث (نفس الإصدار أو أحدث)")
            
            return has_update, latest_version
            
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ خطأ في فحص التحديثات: {e}")
        return False, None

def simulate_user_experience():
    """محاكاة تجربة المستخدم"""
    
    print(f"\n" + "=" * 50)
    print("🎭 محاكاة تجربة المستخدم:")
    print("=" * 50)
    
    scenarios = [
        {
            "user": "مستخدم لديه إصدار 1.2.4",
            "current": "1.2.4", 
            "description": "سيرى إشعار تحديث إلى 1.2.5"
        },
        {
            "user": "مستخدم لديه إصدار 1.2.3", 
            "current": "1.2.3",
            "description": "سيرى إشعار تحديث إلى 1.2.5"
        },
        {
            "user": "مستخدم لديه إصدار 1.2.5",
            "current": "1.2.5", 
            "description": "لن يرى أي إشعار (محدث)"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n👤 {scenario['user']}:")
        print(f"   📱 الإصدار الحالي: {scenario['current']}")
        print(f"   💭 ما سيحدث: {scenario['description']}")

def test_update_timing():
    """اختبار توقيت فحص التحديثات"""
    
    print(f"\n" + "=" * 50) 
    print("⏰ اختبار توقيت الفحص:")
    print("=" * 50)
    
    # قراءة إعدادات التحديث
    try:
        with open("update_info.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        check_mode = config.get('check_mode', 'unknown')
        auto_update = config.get('auto_update', False)
        check_interval = config.get('check_interval', 24)
        
        print(f"📋 الإعدادات الحالية:")
        print(f"   🔄 وضع الفحص: {check_mode}")
        print(f"   ⚡ التحديث التلقائي: {'مفعل' if auto_update else 'معطل'}")
        print(f"   ⏱️ فترة الفحص: {check_interval} ({'دائماً' if check_interval == 0 else 'ساعة'})")
        
        print(f"\n🎯 النتيجة:")
        if check_mode == "always" and auto_update:
            print(f"   ✅ سيتم فحص التحديثات في كل مرة يفتح البرنامج")
            print(f"   ⚡ الفحص فوري (أقل من ثانية)")
            print(f"   🔔 إشعار فوري عند توفر تحديث جديد")
        else:
            print(f"   ⚠️ الإعدادات قد تحتاج تعديل لضمان الفحص التلقائي")
        
    except Exception as e:
        print(f"❌ خطأ في قراءة الإعدادات: {e}")

def main():
    """الدالة الرئيسية"""
    
    print("🔄 اختبار نظام التحديث التلقائي")
    print("تحديد ما إذا كان سيظهر إشعار للمستخدمين")
    print("=" * 60)
    
    # 1. اختبار فحص التحديثات
    has_update, latest_version = test_update_check()
    
    # 2. محاكاة تجربة المستخدم
    simulate_user_experience()
    
    # 3. اختبار توقيت الفحص
    test_update_timing()
    
    # 4. الخلاصة
    print(f"\n" + "=" * 60)
    print("📝 الخلاصة:")
    
    if has_update:
        print(f"   🎉 نعم! البرنامج القديم سيكتشف التحديث الجديد")
        print(f"   📢 سيظهر إشعار بالإصدار {latest_version}")
        print(f"   ⚡ الفحص يحدث عند فتح البرنامج")
    else:
        print(f"   ℹ️ لم يتم اكتشاف إصدار أحدث حالياً")
        print(f"   🔄 بمجرد نشر Release جديد، سيظهر الإشعار")
    
    print(f"\n🚀 لضمان عمل النظام:")
    print(f"   1️⃣ أنشئ GitHub Release جديد")
    print(f"   2️⃣ ارفع ملف ZIP")
    print(f"   3️⃣ انشر الإصدار")
    print(f"   4️⃣ المستخدمين سيرون الإشعار فوراً!")

if __name__ == "__main__":
    main()