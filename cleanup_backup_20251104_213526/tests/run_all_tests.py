"""
سكريبت تشغيل جميع الاختبارات الشاملة
يقوم بتشغيل جميع أنواع الاختبارات وإنتاج تقرير شامل
"""

import os
import sys
import time
import subprocess
import json
from datetime import datetime

def run_test_suite(test_file, test_name):
    """تشغيل مجموعة اختبارات واحدة"""
    print(f"\nتشغيل {test_name}...")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # تشغيل الاختبارات
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # تحليل النتائج
        success = result.returncode == 0
        output = result.stdout + result.stderr
        
        return {
            "name": test_name,
            "file": test_file,
            "success": success,
            "duration": duration,
            "output": output,
            "return_code": result.returncode
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        return {
            "name": test_name,
            "file": test_file,
            "success": False,
            "duration": duration,
            "output": f"خطأ في تشغيل الاختبار: {str(e)}",
            "return_code": -1
        }

def extract_test_stats(output):
    """استخراج إحصائيات الاختبارات من النتائج"""
    stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        
        # البحث عن أرقام النتائج
        if "نجح:" in line:
            try:
                stats["passed"] = int(line.split("نجح:")[1].strip())
            except:
                pass
                
        if "فشل:" in line:
            try:
                stats["failed"] = int(line.split("فشل:")[1].strip())
            except:
                pass
                
        if "أخطاء:" in line:
            try:
                stats["errors"] = int(line.split("أخطاء:")[1].strip())
            except:
                pass
                
        if "المجموع:" in line:
            try:
                stats["total"] = int(line.split("المجموع:")[1].strip())
            except:
                pass
    
    # حساب المجموع إذا لم يتم العثور عليه
    if stats["total"] == 0:
        stats["total"] = stats["passed"] + stats["failed"] + stats["errors"]
    
    return stats

def generate_html_report(results, total_stats):
    """إنتاج تقرير HTML شامل"""
    html_content = f"""
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير الاختبارات الشامل - نظام إدارة المخزون</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .success {{ color: #4CAF50; }}
        .warning {{ color: #FF9800; }}
        .error {{ color: #f44336; }}
        .info {{ color: #2196F3; }}
        
        .test-results {{
            padding: 30px;
        }}
        
        .test-suite {{
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .test-suite-header {{
            padding: 20px;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .test-suite-success {{
            background: #e8f5e8;
            border-right: 5px solid #4CAF50;
        }}
        
        .test-suite-failed {{
            background: #fce8e6;
            border-right: 5px solid #f44336;
        }}
        
        .test-details {{
            padding: 20px;
            background: #f9f9f9;
            border-top: 1px solid #ddd;
        }}
        
        .test-output {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
            transition: width 0.3s ease;
        }}
        
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
            padding: 20px;
            border-top: 1px solid #ddd;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: 1fr;
            }}
            
            .stat-number {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 تقرير الاختبارات الشامل</h1>
            <p>نظام إدارة المخزون - اختبارات شاملة</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-number info">{total_stats['total']}</div>
                <div class="stat-label">إجمالي الاختبارات</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number success">{total_stats['passed']}</div>
                <div class="stat-label">نجح</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number warning">{total_stats['failed']}</div>
                <div class="stat-label">فشل</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number error">{total_stats['errors']}</div>
                <div class="stat-label">أخطاء</div>
            </div>
        </div>
        
        <div style="padding: 0 30px;">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {(total_stats['passed']/max(total_stats['total'],1))*100:.1f}%"></div>
            </div>
            <p style="text-align: center; color: #666;">
                معدل النجاح: {(total_stats['passed']/max(total_stats['total'],1))*100:.1f}%
            </p>
        </div>
        
        <div class="test-results">
            <h2>📋 تفاصيل النتائج</h2>
"""
    
    for result in results:
        status_class = "test-suite-success" if result['success'] else "test-suite-failed"
        status_icon = "✅" if result['success'] else "❌"
        stats = extract_test_stats(result['output'])
        
        html_content += f"""
            <div class="test-suite">
                <div class="test-suite-header {status_class}">
                    {status_icon} {result['name']}
                    <span style="float: left; font-size: 0.9em;">
                        ⏱️ {result['duration']:.2f}s | 
                        ✅ {stats['passed']} | 
                        ❌ {stats['failed']} | 
                        🔥 {stats['errors']}
                    </span>
                </div>
                
                <div class="test-details">
                    <p><strong>الملف:</strong> {result['file']}</p>
                    <p><strong>الوقت المستغرق:</strong> {result['duration']:.2f} ثانية</p>
                    <p><strong>رمز الإرجاع:</strong> {result['return_code']}</p>
                    
                    <details>
                        <summary style="cursor: pointer; padding: 10px 0; font-weight: bold;">
                            📄 عرض تفاصيل النتائج
                        </summary>
                        <div class="test-output">{result['output']}</div>
                    </details>
                </div>
            </div>
        """
    
    html_content += f"""
        </div>
        
        <div class="timestamp">
            <p>تم إنتاج هذا التقرير في: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🏗️ نظام إدارة المخزون - اختبارات الجودة الشاملة</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def main():
    """تشغيل جميع الاختبارات وإنتاج التقرير"""
    print("بدء الاختبارات الشاملة لنظام إدارة المخزون")
    print("=" * 70)
    
    # قائمة الاختبارات
    test_suites = [
        ("test_complete.py", "الاختبارات الأساسية الشاملة"),
        ("test_stress.py", "اختبارات الضغط والتحمل"),
        ("test_security.py", "اختبارات الأمان والحماية")
    ]
    
    all_results = []
    total_stats = {"total": 0, "passed": 0, "failed": 0, "errors": 0}
    
    start_time = time.time()
    
    # تشغيل كل مجموعة اختبارات
    for test_file, test_name in test_suites:
        result = run_test_suite(test_file, test_name)
        all_results.append(result)
        
        # استخراج الإحصائيات
        stats = extract_test_stats(result['output'])
        total_stats["total"] += stats["total"]
        total_stats["passed"] += stats["passed"]
        total_stats["failed"] += stats["failed"]
        total_stats["errors"] += stats["errors"]
        
        # طباعة النتيجة
        status = "✅ نجح" if result['success'] else "❌ فشل"
        print(f"{status} - {test_name} ({result['duration']:.2f}s)")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # طباعة الملخص النهائي
    print("\n" + "=" * 70)
    print("📊 ملخص النتائج النهائية:")
    print(f"⏱️  الوقت الإجمالي: {total_duration:.2f} ثانية")
    print(f"📈 إجمالي الاختبارات: {total_stats['total']}")
    print(f"✅ نجح: {total_stats['passed']}")
    print(f"❌ فشل: {total_stats['failed']}")
    print(f"🔥 أخطاء: {total_stats['errors']}")
    
    success_rate = (total_stats['passed'] / max(total_stats['total'], 1)) * 100
    print(f"📊 معدل النجاح: {success_rate:.1f}%")
    
    # تقييم الجودة
    if success_rate >= 95:
        print("🏆 تقييم الجودة: ممتاز!")
    elif success_rate >= 85:
        print("🥈 تقييم الجودة: جيد جداً")
    elif success_rate >= 70:
        print("🥉 تقييم الجودة: جيد")
    else:
        print("⚠️  تقييم الجودة: يحتاج تحسين")
    
    print("=" * 70)
    
    # إنتاج تقرير HTML
    try:
        html_report = generate_html_report(all_results, total_stats)
        report_path = os.path.join(os.path.dirname(__file__), "test_report.html")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
            
        print(f"📄 تم إنتاج التقرير المفصل: {report_path}")
        
        # فتح التقرير في المتصفح (اختياري)
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
            print("🌐 تم فتح التقرير في المتصفح")
        except:
            print("💡 يمكنك فتح التقرير يدوياً في المتصفح")
            
    except Exception as e:
        print(f"❌ خطأ في إنتاج التقرير: {e}")
    
    # إنتاج تقرير JSON للمعالجة الآلية
    try:
        json_report = {
            "timestamp": datetime.now().isoformat(),
            "total_duration": total_duration,
            "summary": total_stats,
            "success_rate": success_rate,
            "results": all_results
        }
        
        json_path = os.path.join(os.path.dirname(__file__), "test_results.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
            
        print(f"📋 تم حفظ النتائج في: {json_path}")
        
    except Exception as e:
        print(f"❌ خطأ في حفظ النتائج: {e}")
    
    # تحديد رمز الإرجاع
    overall_success = all(result['success'] for result in all_results)
    
    if overall_success:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للإنتاج.")
        return 0
    else:
        print("\n⚠️  بعض الاختبارات فشلت. يرجى مراجعة التقرير.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)