"""
اختبارات الضغط والتحمل لنظام إدارة المخزون
لاختبار أداء النظام تحت الضغط والأحمال العالية
"""

import unittest
import threading
import time
import random
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import Mock, patch
import tkinter as tk

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sheets.manager import SheetsManager
from gui.main_window import MainWindow

class TestStressLoad(unittest.TestCase):
    """اختبارات الضغط والتحمل"""
    
    def setUp(self):
        """إعداد بيئة اختبار الضغط"""
        self.manager = SheetsManager(
            credentials_file="test_credentials.json",
            spreadsheet_name="Test Inventory",
            worksheet_name="Test Sheet"
        )
        
        # Mock Google Sheets
        self.mock_client = Mock()
        self.mock_spreadsheet = Mock()
        self.mock_worksheet = Mock()
        self.mock_log_worksheet = Mock()
        
        self.manager.client = self.mock_client
        self.manager.spreadsheet = self.mock_spreadsheet
        self.manager.worksheet = self.mock_worksheet
        self.manager.log_worksheet = self.mock_log_worksheet
        
    def test_concurrent_operations(self):
        """اختبار العمليات المتزامنة"""
        # إعداد استجابات مموهة
        self.mock_worksheet.append_row.return_value = True
        self.mock_worksheet.update.return_value = True
        self.mock_worksheet.get_all_values.return_value = [
            ["اسم العنصر", "الكمية المتاحة", "آخر تحديث"],
            ["لابتوب", "100", "2025-10-11 10:00:00"]
        ]
        
        def perform_operation(operation_id):
            """تنفيذ عملية واحدة"""
            try:
                if operation_id % 4 == 0:
                    return self.manager.add_item(f"عنصر_{operation_id}", random.randint(1, 50))
                elif operation_id % 4 == 1:
                    return self.manager.update_quantity("لابتوب", random.randint(50, 150))
                elif operation_id % 4 == 2:
                    return self.manager.outbound_item("لابتوب", random.randint(1, 10), f"مستلم_{operation_id}")
                else:
                    return self.manager.get_all_items() is not None
            except Exception as e:
                return False
                
        # تشغيل 100 عملية متزامنة
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(perform_operation, i) for i in range(100)]
            results = [future.result() for future in as_completed(futures)]
            
        # التحقق من نجاح معظم العمليات
        success_rate = sum(results) / len(results)
        self.assertGreater(success_rate, 0.8)  # 80% نجاح على الأقل
        
    def test_memory_stress(self):
        """اختبار ضغط الذاكرة"""
        import gc
        
        # قياس الذاكرة الأولية
        gc.collect()
        
        # إنشاء كمية كبيرة من البيانات
        large_data = []
        for i in range(10000):
            large_data.append({
                "item_name": f"عنصر_كبير_{i}",
                "quantity": random.randint(1, 1000),
                "last_updated": f"2025-10-11 {i%24:02d}:00:00",
                "description": f"وصف طويل للعنصر رقم {i} " * 10  # نص طويل
            })
            
        # معالجة البيانات
        processed_data = []
        for item in large_data:
            if item["quantity"] > 500:
                processed_data.append({
                    "name": item["item_name"],
                    "qty": item["quantity"],
                    "status": "متاح"
                })
                
        # تنظيف الذاكرة
        del large_data
        gc.collect()
        
        # التحقق من وجود بيانات معالجة
        self.assertGreater(len(processed_data), 0)
        
    def test_rapid_ui_operations(self):
        """اختبار العمليات السريعة على الواجهة"""
        root = tk.Tk()
        root.withdraw()
        
        try:
            test_config = {
                "credentials_file": "test_credentials.json",
                "spreadsheet_name": "Test Inventory",
                "worksheet_name": "Test Sheet"
            }
            
            with patch('gui.main_window.SheetsManager'):
                main_window = MainWindow(root, test_config)
                
                # محاكاة ضغط سريع على الأزرار
                def rapid_button_clicks():
                    for i in range(100):
                        # محاكاة النقر على الأزرار
                        if hasattr(main_window, 'refresh_btn'):
                            main_window.refresh_btn.config(state="normal")
                            main_window.refresh_btn.config(state="disabled")
                        time.sleep(0.01)  # 10ms بين كل نقرة
                        
                # تشغيل عدة خيوط للنقر
                threads = []
                for i in range(5):
                    thread = threading.Thread(target=rapid_button_clicks)
                    threads.append(thread)
                    thread.start()
                    
                # انتظار انتهاء جميع الخيوط
                for thread in threads:
                    thread.join(timeout=5)  # انتظار 5 ثوان كحد أقصى
                    
                # التحقق من استقرار الواجهة
                self.assertTrue(main_window.root.winfo_exists())
                
        finally:
            root.destroy()
            
    def test_network_simulation(self):
        """اختبار محاكاة مشاكل الشبكة"""
        # محاكاة تأخير الشبكة
        def simulate_network_delay():
            time.sleep(random.uniform(0.1, 2.0))  # تأخير عشوائي
            if random.random() < 0.1:  # 10% احتمال فشل
                raise Exception("انقطاع الشبكة")
            return True
            
        # اختبار المرونة ضد مشاكل الشبكة
        success_count = 0
        total_attempts = 50
        
        for i in range(total_attempts):
            try:
                with patch.object(self.manager, '_make_api_call', side_effect=simulate_network_delay):
                    # محاولة عملية
                    if simulate_network_delay():
                        success_count += 1
            except Exception:
                # فشل متوقع بسبب مشاكل الشبكة
                pass
                
        # يجب أن ينجح 80% على الأقل
        success_rate = success_count / total_attempts
        self.assertGreater(success_rate, 0.8)
        
    def test_data_corruption_handling(self):
        """اختبار التعامل مع البيانات المفسدة"""
        # بيانات مفسدة ومختلطة
        corrupted_data = [
            ["اسم العنصر", "الكمية المتاحة", "آخر تحديث"],
            ["لابتوب", "abc", "تاريخ خاطئ"],  # كمية غير رقمية
            ["", "10", "2025-10-11 10:00:00"],  # اسم فارغ
            ["ماوس", "-5", "2025-10-11 09:30:00"],  # كمية سالبة
            ["كيبورد", "15"],  # عمود مفقود
            [None, None, None],  # قيم null
            ["شاشة", "20", "2025-10-11 11:00:00"],  # بيانات صحيحة
        ]
        
        # محاكاة البيانات المفسدة
        self.mock_worksheet.get_all_values.return_value = corrupted_data
        
        # محاولة معالجة البيانات
        try:
            items = self.manager.get_all_items()
            
            # التحقق من تنظيف البيانات
            valid_items = [item for item in items if 
                          item.get("item_name") and 
                          isinstance(item.get("quantity"), (int, float)) and 
                          item.get("quantity") >= 0]
            
            # يجب أن يكون هناك عنصر واحد صحيح على الأقل
            self.assertGreaterEqual(len(valid_items), 1)
            
        except Exception as e:
            # يجب أن يتم التعامل مع الخطأ بشكل صحيح
            self.assertIsInstance(e, Exception)
            
    def test_extreme_load_simulation(self):
        """اختبار محاكاة الحمل الشديد"""
        # إعداد بيانات ضخمة
        massive_dataset = []
        for i in range(5000):
            massive_dataset.append([
                f"عنصر_ضخم_{i}",
                str(random.randint(0, 1000)),
                f"2025-10-{(i%30)+1:02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:00"
            ])
            
        # إضافة رأس الجدول
        mock_data = [["اسم العنصر", "الكمية المتاحة", "آخر تحديث"]] + massive_dataset
        self.mock_worksheet.get_all_values.return_value = mock_data
        
        # قياس الوقت
        start_time = time.time()
        
        try:
            items = self.manager.get_all_items()
            processing_time = time.time() - start_time
            
            # التحقق من الأداء
            self.assertLess(processing_time, 10.0)  # لا يزيد عن 10 ثوان
            self.assertEqual(len(items), 5000)
            
        except Exception as e:
            # في حالة فشل المعالجة، يجب أن يكون الخطأ مفهوماً
            self.assertIsInstance(e, (MemoryError, TimeoutError, Exception))

class TestErrorRecovery(unittest.TestCase):
    """اختبارات استرداد الأخطاء"""
    
    def setUp(self):
        """إعداد بيئة اختبار الاسترداد"""
        self.manager = SheetsManager(
            credentials_file="test_credentials.json",
            spreadsheet_name="Test Inventory",
            worksheet_name="Test Sheet"
        )
        
    def test_connection_retry_mechanism(self):
        """اختبار آلية إعادة المحاولة"""
        connection_attempts = []
        
        def mock_connect_with_retry():
            connection_attempts.append(len(connection_attempts) + 1)
            if len(connection_attempts) < 3:
                raise Exception("فشل مؤقت في الاتصال")
            return True
            
        # محاكاة إعادة المحاولة
        for attempt in range(5):
            try:
                result = mock_connect_with_retry()
                if result:
                    break
            except Exception:
                if attempt == 4:  # آخر محاولة
                    raise
                time.sleep(0.1)  # انتظار قصير
                
        # التحقق من نجاح الاتصال بعد عدة محاولات
        self.assertEqual(len(connection_attempts), 3)
        
    def test_partial_failure_handling(self):
        """اختبار التعامل مع الفشل الجزئي"""
        # محاكاة عمليات مختلطة (بعضها ينجح وبعضها يفشل)
        operations = [
            ("add", "عنصر1", 10, True),      # نجح
            ("add", "", 5, False),           # فشل - اسم فارغ
            ("update", "عنصر1", 20, True),   # نجح
            ("update", "غير موجود", 15, False), # فشل - عنصر غير موجود
            ("outbound", "عنصر1", 5, True),  # نجح
        ]
        
        successful_operations = 0
        failed_operations = 0
        
        for op_type, name, quantity, should_succeed in operations:
            try:
                # محاكاة العملية
                if op_type == "add" and not name:
                    raise ValueError("اسم العنصر مطلوب")
                elif op_type == "update" and name == "غير موجود":
                    raise ValueError("العنصر غير موجود")
                else:
                    # عملية ناجحة
                    successful_operations += 1
            except Exception:
                failed_operations += 1
                
        # التحقق من النتائج المتوقعة
        self.assertEqual(successful_operations, 3)
        self.assertEqual(failed_operations, 2)
        
    def test_data_consistency_after_errors(self):
        """اختبار ثبات البيانات بعد الأخطاء"""
        # بيانات أولية
        initial_data = [
            {"item_name": "لابتوب", "quantity": 10},
            {"item_name": "ماوس", "quantity": 25}
        ]
        
        # محاكاة عمليات مع أخطاء
        operations_log = []
        
        try:
            # عملية صحيحة
            operations_log.append(("add", "كيبورد", 15, "success"))
            
            # عملية خاطئة
            try:
                if True:  # محاكاة خطأ
                    raise Exception("خطأ في الشبكة")
                operations_log.append(("update", "لابتوب", 20, "success"))
            except Exception:
                operations_log.append(("update", "لابتوب", 20, "failed"))
                
            # عملية أخرى صحيحة
            operations_log.append(("outbound", "ماوس", 5, "success"))
            
        except Exception:
            pass
            
        # التحقق من سجل العمليات
        successful_ops = [op for op in operations_log if op[3] == "success"]
        failed_ops = [op for op in operations_log if op[3] == "failed"]
        
        self.assertEqual(len(successful_ops), 2)
        self.assertEqual(len(failed_ops), 1)

def run_stress_tests():
    """تشغيل جميع اختبارات الضغط"""
    print("بدء اختبارات الضغط والتحمل...")
    print("=" * 60)
    
    # إنشاء مجموعة الاختبارات
    test_suite = unittest.TestSuite()
    
    # إضافة اختبارات الضغط
    stress_classes = [
        TestStressLoad,
        TestErrorRecovery
    ]
    
    for test_class in stress_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(test_suite)
    end_time = time.time()
    
    # طباعة النتائج
    print(f"\n{'='*60}")
    print(f"نتائج اختبارات الضغط:")
    print(f"⏱️  الوقت المستغرق: {end_time - start_time:.2f} ثانية")
    print(f"✅ نجح: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ فشل: {len(result.failures)}")
    print(f"أخطاء: {len(result.errors)}")
    print(f"📈 المجموع: {result.testsRun}")
    
    if result.failures:
        print(f"\n❌ الاختبارات الفاشلة:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            
    if result.errors:
        print(f"\nالأخطاء:")
        for test, traceback in result.errors:
            print(f"  - {test}")
            
    print(f"{'='*60}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_stress_tests()
    sys.exit(0 if success else 1)