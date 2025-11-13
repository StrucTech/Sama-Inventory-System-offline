import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import socket
import urllib.request
import urllib.error

def check_internet_connection():
    """فحص الاتصال بالإنترنت"""
    try:
        # محاولة الاتصال بـ Google DNS
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error:
        try:
            # محاولة بديلة - فحص الاتصال بـ Google
            urllib.request.urlopen('http://www.google.com', timeout=3)
            return True
        except urllib.error.URLError:
            return False

def show_no_internet_message():
    """عرض رسالة عدم وجود اتصال بالإنترنت"""
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية
    
    messagebox.showerror(
        "خطأ في الاتصال", 
        "⚠️ لا يوجد اتصال بالإنترنت!\n\n"
        "يرجى التأكد من:\n"
        "• الاتصال بالإنترنت\n"
        "• إعدادات الشبكة\n"
        "• جدار الحماية\n\n"
        "ثم حاول مرة أخرى."
    )
    root.destroy()

# مخطط الألوان الفاخر للتطبيق
LUXURY_COLORS = {
    # الألوان الأساسية - درجات الذهبي والأزرق الداكن
    'primary_gold': '#DAA520',           # ذهبي داكن
    'primary_dark': '#1A1A2E',          # أزرق داكن عميق
    'secondary_gold': '#FFD700',        # ذهبي فاتح
    'secondary_dark': '#16213E',        # أزرق داكن ثانوي
    
    # ألوان الخلفية
    'bg_main': '#0F1419',              # خلفية رئيسية داكنة
    'bg_card': '#1E2A4A',              # خلفية البطاقات
    'bg_hover': '#2C3E60',             # لون عند التمرير
    
    # ألوان النصوص
    'text_primary': '#FFFFFF',         # نص أبيض رئيسي
    'text_secondary': '#BDC3C7',       # نص رمادي فاتح
    'text_accent': '#F39C12',          # نص ذهبي للتأكيد
    
    # ألوان الحالة
    'success': '#27AE60',              # أخضر للنجاح
    'warning': '#F39C12',              # برتقالي للتحذير
    'error': '#E74C3C',                # أحمر للخطأ
    'info': '#3498DB',                 # أزرق للمعلومات
    
    # ألوان الرسوم البيانية
    'chart_1': '#DAA520',              # ذهبي
    'chart_2': '#4A90E2',              # أزرق
    'chart_3': '#50E3C2',              # تركوازي
    'chart_4': '#F5A623',              # برتقالي ذهبي
    'chart_5': '#7ED321',              # أخضر
    'chart_6': '#BD10E0',              # بنفسجي
}

# استيراد اختياري للمكتبات الرسومية
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
    import seaborn as sns
    
    # إعداد الخط العربي لـ matplotlib
    import matplotlib.font_manager as fm
    
    # البحث عن خط عربي مناسب
    arabic_fonts = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans', 'Liberation Sans']
    selected_font = None
    
    for font_name in arabic_fonts:
        try:
            plt.rcParams['font.family'] = font_name
            plt.rcParams['axes.unicode_minus'] = False
            selected_font = font_name
            break
        except:
            continue
    
    if not selected_font:
        plt.rcParams['font.family'] = ['sans-serif']
    
    print(f"✅ تم تحميل مكتبات الرسوم البيانية مع خط: {selected_font or 'افتراضي'}")
    CHARTS_AVAILABLE = True
    
except ImportError as e:
    CHARTS_AVAILABLE = False
    print("⚠️ مكتبات الرسوم البيانية غير متوفرة:", e)
    print("   يمكن تثبيتها باستخدام: pip install matplotlib seaborn numpy")

def fix_arabic_text(text):
    """إصلاح النص العربي للعرض الصحيح"""
    if not text:
        return text
    
    # تحويل إلى نص إذا لم يكن كذلك
    text = str(text)
    
    try:
        # محاولة استخدام مكتبة python-bidi إذا كانت متوفرة
        try:
            from bidi.algorithm import get_display
            import arabic_reshaper
            
            # إعادة تشكيل النص العربي
            reshaped_text = arabic_reshaper.reshape(text)
            # تطبيق خوارزمية bidi
            display_text = get_display(reshaped_text)
            return display_text
        except ImportError:
            # حل بديل محسن للنص العربي
            print("⚠️ مكتبات إصلاح العربية غير متوفرة - استخدام حل بديل محسن")
            
            # التحقق من وجود نص عربي
            arabic_chars = any('\u0600' <= char <= '\u06FF' for char in text)
            if arabic_chars:
                # تطبيق إصلاحات محسنة للنص العربي
                lines = text.split('\n')
                fixed_lines = []
                for line in lines:
                    if any('\u0600' <= char <= '\u06FF' for char in line):
                        # عكس ترتيب الكلمات العربية فقط
                        import re
                        # تقسيم إلى كلمات
                        words = line.split()
                        arabic_words = []
                        mixed_words = []
                        
                        for word in words:
                            if any('\u0600' <= char <= '\u06FF' for char in word):
                                arabic_words.append(word)
                            else:
                                mixed_words.append(word)
                        
                        # إعادة ترتيب الكلمات العربية من اليمين لليسار
                        if arabic_words:
                            # عكس ترتيب الكلمات العربية
                            arabic_words.reverse()
                            fixed_line = ' '.join(arabic_words + mixed_words)
                        else:
                            fixed_line = line
                        
                        fixed_lines.append(fixed_line)
                    else:
                        fixed_lines.append(line)
                return '\n'.join(fixed_lines)
            else:
                return text
            
    except Exception as e:
        print(f"⚠️ خطأ في إصلاح النص العربي: {e}")
        return text

def fix_mixed_text(text_with_variables):
    """إصلاح النص المختلط الذي يحتوي على متغيرات عربية"""
    if not text_with_variables:
        return text_with_variables
    
    # تطبيق إصلاح النص على النص الكامل
    return fix_arabic_text(str(text_with_variables))

class AnalyticsWindow:
    """نافذة التحليل والرؤى المتقدمة للبيانات"""
    
    def __init__(self, parent, enhanced_manager, current_user):
        # فحص الاتصال بالإنترنت قبل بدء التطبيق
        if not check_internet_connection():
            show_no_internet_message()
            return
            
        self.parent = parent
        self.enhanced_manager = enhanced_manager
        self.current_user = current_user
        
        # البيانات
        self.all_data = []
        self.inventory_data = []
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.window.title("📊 تحليل ورؤى البيانات - لوحة تحكم إدارية")
        
        # تحديد حجم النافذة (يمكن تعديل هذه القيم)
        # الخيار 1: حجم ثابت
        self.window.geometry("1300x900+50+30")  # عرض x ارتفاع + موضع X + موضع Y
        
        # الخيار 2: للعودة للحجم الكامل، احذف السطر السابق واستخدم هذا:
        # self.window.state('zoomed')
        
        self.window.resizable(True, True)
        
        # تكوين دعم اللغة العربية
        try:
            # تعيين خط يدعم العربية لجميع عناصر tkinter
            arabic_font = ('Tahoma', 10)
            self.window.option_add('*Font', arabic_font)
            
            # تكوين الاتجاه للنافذة
            try:
                self.window.tk.call('tk', 'scaling', 1.0)
            except:
                pass
        except:
            pass
        
        # تطبيق الـ Theme الفاخر
        if CHARTS_AVAILABLE:
            try:
                # إعداد ألوان matplotlib الفاخرة
                plt.style.use('dark_background')
                
                # تخصيص الألوان
                plt.rcParams['figure.facecolor'] = LUXURY_COLORS['bg_main']
                plt.rcParams['axes.facecolor'] = LUXURY_COLORS['bg_card']
                plt.rcParams['axes.edgecolor'] = LUXURY_COLORS['primary_gold']
                plt.rcParams['axes.labelcolor'] = LUXURY_COLORS['text_primary']
                plt.rcParams['text.color'] = LUXURY_COLORS['text_primary']
                plt.rcParams['xtick.color'] = LUXURY_COLORS['text_secondary']
                plt.rcParams['ytick.color'] = LUXURY_COLORS['text_secondary']
                plt.rcParams['grid.color'] = LUXURY_COLORS['primary_gold']
                plt.rcParams['grid.alpha'] = 0.3
                
                # إنشاء مجموعة ألوان مخصصة
                luxury_palette = [
                    LUXURY_COLORS['primary_gold'],
                    LUXURY_COLORS['chart_2'], 
                    LUXURY_COLORS['chart_3'],
                    LUXURY_COLORS['chart_4'],
                    LUXURY_COLORS['chart_5'],
                    LUXURY_COLORS['chart_6']
                ]
                sns.set_palette(luxury_palette)
                
            except Exception as e:
                print(f"⚠️ خطأ في تطبيق الألوان الفاخرة: {e}")
                try:
                    plt.style.use('seaborn-v0_8-darkgrid')
                    sns.set_palette("husl")
                except:
                    try:
                        plt.style.use('seaborn-darkgrid')  # إصدار أقدم
                        sns.set_palette("husl")
                    except:
                        pass  # استخدام التنسيق الافتراضي
        
        # إنشاء الواجهة
        self.create_interface()
        
        # تحميل البيانات
        self.load_data()
        
        # تكوين المحاذاة اليمنى للنصوص العربية - تم إزالتها
        
        # عرض التحليلات الأولية
        self.generate_analytics()
    
    def create_interface(self):
        """إنشاء واجهة نافذة التحليل"""
        
        # تطبيق الألوان الفاخرة على النافذة
        self.window.configure(bg=LUXURY_COLORS['bg_main'])
        
        # إطار رئيسي مع شريط تمرير
        main_canvas = tk.Canvas(self.window, bg=LUXURY_COLORS['bg_main'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # إضافة دعم التمرير بالماوس
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_from_mousewheel(event):
            main_canvas.unbind_all("<MouseWheel>")
        
        main_canvas.bind('<Enter>', _bind_to_mousewheel)
        main_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # العنوان الرئيسي
        title_frame = tk.Frame(scrollable_frame, bg=LUXURY_COLORS['bg_main'])
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # العنوان الفاخر مع إضاءة ذهبية
        title_text = "✨ لوحة تحكم التحليل والرؤى ✨"
        title_label = tk.Label(title_frame, text=title_text, 
                              font=("Tahoma", 24, "bold"), 
                              fg=LUXURY_COLORS['primary_gold'],
                              bg=LUXURY_COLORS['bg_main'])
        title_label.pack()
        
        # العنوان الفرعي الأنيق
        subtitle_text = "📈 تحليل شامل ومتطور لبيانات المخزون والعمليات"
        subtitle_label = tk.Label(title_frame, text=subtitle_text, 
                                 font=("Tahoma", 14), 
                                 fg=LUXURY_COLORS['text_secondary'],
                                 bg=LUXURY_COLORS['bg_main'])
        subtitle_label.pack(pady=(5, 15))
        
        # إطار الملخص التنفيذي
        self.create_executive_summary(scrollable_frame)
        
        # إطار الرسوم البيانية
        self.create_charts_section(scrollable_frame)
        
        # أزرار التحكم الفاخرة
        control_frame = tk.Frame(scrollable_frame, bg=LUXURY_COLORS['bg_main'])
        control_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # زر التحديث الذهبي
        refresh_btn = tk.Button(control_frame, 
                               text="🔄 تحديث البيانات", 
                               command=self.refresh_analytics,
                               font=("Tahoma", 12, "bold"),
                               bg=LUXURY_COLORS['primary_gold'],
                               fg=LUXURY_COLORS['primary_dark'],
                               activebackground=LUXURY_COLORS['secondary_gold'],
                               activeforeground=LUXURY_COLORS['primary_dark'],
                               bd=2,
                               relief='raised',
                               padx=20,
                               pady=8,
                               cursor='hand2')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # زر الإغلاق الأنيق
        close_btn = tk.Button(control_frame, 
                             text="❌ إغلاق", 
                             command=self.window.destroy,
                             font=("Tahoma", 12, "bold"),
                             bg=LUXURY_COLORS['error'],
                             fg=LUXURY_COLORS['text_primary'],
                             activebackground='#C0392B',
                             activeforeground=LUXURY_COLORS['text_primary'],
                             bd=2,
                             relief='raised',
                             padx=15,
                             pady=8,
                             cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
    
    def create_executive_summary(self, parent):
        """إنشاء قسم الملخص التنفيذي"""
        # إطار فاخر للملخص التنفيذي
        summary_frame = tk.LabelFrame(parent, 
                                     text="� الملخص التنفيذي", 
                                     font=("Tahoma", 14, "bold"),
                                     fg=LUXURY_COLORS['primary_gold'],
                                     bg=LUXURY_COLORS['bg_main'],
                                     bd=2,
                                     relief='raised')
        summary_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # إطار الإحصائيات السريعة مع خلفية داكنة
        stats_frame = tk.Frame(summary_frame, bg=LUXURY_COLORS['bg_main'])
        stats_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # تقسيم إلى 4 أعمدة
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        # إنشاء بطاقات الإحصائيات
        self.total_items_card = self.create_stat_card(stats_frame, "📦", "إجمالي العناصر", "0", 0)
        self.total_operations_card = self.create_stat_card(stats_frame, "⚙️", "إجمالي العمليات", "0", 1)
        self.active_projects_card = self.create_stat_card(stats_frame, "🏗️", "المشاريع النشطة", "0", 2)
        self.efficiency_card = self.create_stat_card(stats_frame, "📈", "مؤشر الكفاءة", "0%", 3)
    
    def create_stat_card(self, parent, icon, title, value, column):
        """إنشاء بطاقة إحصائية فاخرة"""
        # إطار البطاقة بتصميم فاخر
        card_frame = tk.Frame(parent, 
                             bg=LUXURY_COLORS['bg_card'],
                             bd=2, 
                             relief='raised',
                             padx=15, 
                             pady=12)
        card_frame.grid(row=0, column=column, padx=12, pady=8, sticky="ew")
        
        # الأيقونة بألوان ذهبية متدرجة
        icon_colors = [LUXURY_COLORS['primary_gold'], LUXURY_COLORS['secondary_gold'], 
                      LUXURY_COLORS['chart_4'], LUXURY_COLORS['warning']]
        icon_label = tk.Label(card_frame, text=icon, 
                             font=("Arial", 28), 
                             fg=icon_colors[column],
                             bg=LUXURY_COLORS['bg_card'])
        icon_label.pack(pady=(0, 8))
        
        # العنوان بنص أبيض أنيق
        title_label = tk.Label(card_frame, text=title, 
                              font=("Tahoma", 11, "bold"), 
                              fg=LUXURY_COLORS['text_primary'],
                              bg=LUXURY_COLORS['bg_card'])
        title_label.pack(pady=(0, 5))
        
        # القيمة بلون ذهبي بارز
        value_label = tk.Label(card_frame, text=value, 
                              font=("Arial", 18, "bold"), 
                              fg=LUXURY_COLORS['primary_gold'],
                              bg=LUXURY_COLORS['bg_card'])
        value_label.pack()
        
        return value_label
    
    def create_charts_section(self, parent):
        """إنشاء قسم الرسوم البيانية"""
        charts_frame = ttk.LabelFrame(parent, text="📈 الرسوم البيانية التفاعلية", padding="10")
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # إطار الرسوم البيانية - تقسيم إلى 2x2
        charts_grid = ttk.Frame(charts_frame)
        charts_grid.pack(fill=tk.BOTH, expand=True)
        
        # تكوين الشبكة
        charts_grid.columnconfigure(0, weight=1)
        charts_grid.columnconfigure(1, weight=1)
        charts_grid.rowconfigure(0, weight=1)
        charts_grid.rowconfigure(1, weight=1)
        
        # الرسم البياني 1: العمليات عبر الزمن
        self.operations_chart_frame = ttk.Frame(charts_grid)
        self.operations_chart_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        
        # الرسم البياني 2: توزيع العناصر حسب التصنيف
        self.categories_chart_frame = ttk.Frame(charts_grid)
        self.categories_chart_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
        
        # الرسم البياني 3: أنشطة المشاريع
        self.projects_chart_frame = ttk.Frame(charts_grid)
        self.projects_chart_frame.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")
        
        # الرسم البياني 4: الكميات والمخزون  
        self.inventory_chart_frame = ttk.Frame(charts_grid)
        self.inventory_chart_frame.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")
        
        # شرح مؤشر الكفاءة
        efficiency_info_frame = ttk.LabelFrame(parent, text="ℹ️ شرح مؤشر الكفاءة", padding="10")
        efficiency_info_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        efficiency_text = """
مؤشر الكفاءة = (العمليات الداخلة ÷ العمليات الخارجة) × 100

📊 تفسير المؤشر:
• 100% - 120%: توازن مثالي في العمليات ✅
• أكثر من 120%: فائض في الإضافات (قد يحتاج مراجعة التوزيع) ⚠️  
• أقل من 80%: نقص في الإضافات (قد يحتاج زيادة المخزون) ⚠️
• أقل من 50%: خطر نفاد المخزون (يحتاج تدخل فوري) 🚨

المؤشر يساعد في مراقبة التوازن بين عمليات الإدخال والإخراج لضمان استدامة المخزون.
        """
        
        efficiency_label = tk.Label(efficiency_info_frame, 
                                   text=efficiency_text.strip(),
                                   font=("Tahoma", 10), 
                                   justify=tk.RIGHT,
                                   anchor='e')
        efficiency_label.pack(fill=tk.X)
    
    def create_text_chart(self, parent, title, message):
        """إنشاء رسم نصي بديل عندما لا تتوفر مكتبات الرسوم"""
        text_frame = ttk.LabelFrame(parent, text=fix_arabic_text(title), padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        message_label = tk.Label(text_frame, text=fix_arabic_text(message), 
                                font=("Tahoma", 12), fg="#666666",
                                wraplength=200, justify=tk.CENTER)
        message_label.pack(expand=True)
        
        if not CHARTS_AVAILABLE:
            install_label = tk.Label(text_frame, 
                                    text=fix_arabic_text("لتفعيل الرسوم البيانية:\npip install matplotlib seaborn numpy"), 
                                    font=("Tahoma", 10), fg="#999999")
            install_label.pack(pady=(10, 0))
    
    def load_data(self):
        """تحميل البيانات من Google Sheets"""
        try:
            print("📊 تحميل بيانات التحليل...")
            
            # تحميل بيانات سجل النشاط
            self.all_data = self.enhanced_manager.get_activity_log_new_format()
            print(f"✅ تم تحميل {len(self.all_data)} سجل نشاط")
            
            # تحميل بيانات المخزون الحالي
            try:
                self.inventory_data = self.enhanced_manager.get_all_items()
                print(f"✅ تم تحميل {len(self.inventory_data)} عنصر من المخزون")
            except:
                self.inventory_data = []
                print("⚠️ تعذر تحميل بيانات المخزون")
            
        except Exception as e:
            print(f"❌ خطأ في تحميل البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحميل البيانات:\n{e}")
            self.all_data = []
            self.inventory_data = []
    
    def generate_analytics(self):
        """توليد التحليلات المبسطة"""
        if not self.all_data:
            self.show_no_data_message()
            return
        
        try:
            # تحديث الملخص التنفيذي
            self.update_executive_summary()
            
            # إنشاء الرسوم البيانية
            self.create_operations_chart()
            self.create_categories_chart()
            self.create_projects_chart()
            self.create_inventory_chart()
            
        except Exception as e:
            print(f"❌ خطأ في توليد التحليلات: {e}")
            messagebox.showerror("خطأ", f"فشل في توليد التحليلات:\n{e}")
    
    def update_executive_summary(self):
        """تحديث الملخص التنفيذي"""
        try:
            # حساب الإحصائيات
            total_operations = len(self.all_data)
            unique_items = len(set(record[3] for record in self.all_data if len(record) > 3 and record[3]))
            active_projects = len(set(record[10] for record in self.all_data if len(record) > 10 and record[10]))
            
            # حساب مؤشر الكفاءة (نسبة الإضافة إلى الإخراج)
            inbound = sum(1 for record in self.all_data if len(record) > 2 and record[2] == "إضافة")
            outbound = sum(1 for record in self.all_data if len(record) > 2 and record[2] == "إخراج")
            efficiency = (inbound / max(outbound, 1)) * 100 if outbound > 0 else 100
            
            # تحديث البطاقات
            self.total_items_card.config(text=str(unique_items))
            self.total_operations_card.config(text=str(total_operations))
            self.active_projects_card.config(text=str(active_projects))
            self.efficiency_card.config(text=f"{efficiency:.1f}%")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث الملخص التنفيذي: {e}")
    
    def create_operations_chart(self):
        """إنشاء رسم بياني للعمليات عبر الزمن"""
        if not CHARTS_AVAILABLE:
            self.create_text_chart(self.operations_chart_frame, "العمليات عبر الزمن", 
                                  "مكتبات الرسوم البيانية غير متوفرة")
            return
            
        try:
            # إنشاء Figure بحجم أكبر
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            # تجميع البيانات حسب التاريخ
            daily_operations = defaultdict(int)
            for record in self.all_data:
                if len(record) > 1 and record[1]:
                    try:
                        date = datetime.strptime(record[1], "%Y-%m-%d").date()
                        daily_operations[date] += 1
                    except:
                        continue
            
            if daily_operations:
                dates = sorted(daily_operations.keys())
                counts = [daily_operations[date] for date in dates]
                
                ax.plot(dates, counts, marker='o', linewidth=2, markersize=6, color='#2196F3')
                ax.fill_between(dates, counts, alpha=0.3, color='#2196F3')
                ax.set_title(fix_arabic_text('العمليات اليومية عبر الزمن'), fontsize=12, fontweight='bold')
                ax.set_xlabel(fix_arabic_text('التاريخ'))
                ax.set_ylabel(fix_arabic_text('عدد العمليات'))
                ax.grid(True, alpha=0.3)
                
                # تنسيق التواريخ
                fig.autofmt_xdate()
            else:
                # إضافة بيانات وهمية للعرض
                from datetime import date, timedelta
                today = date.today()
                dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
                counts = [5, 8, 12, 3, 15, 7, 10]
                
                ax.plot(dates, counts, marker='o', linewidth=2, markersize=6, color='#2196F3', alpha=0.7)
                ax.fill_between(dates, counts, alpha=0.2, color='#2196F3')
                ax.set_title(fix_arabic_text('العمليات اليومية (مثال توضيحي)'), fontsize=12, fontweight='bold')
                ax.set_xlabel(fix_arabic_text('التاريخ'))
                ax.set_ylabel(fix_arabic_text('عدد العمليات'))
                ax.grid(True, alpha=0.3)
                
                # تنسيق التواريخ
                fig.autofmt_xdate()
                
                # إضافة ملاحظة
                ax.text(dates[3], max(counts) + 2, fix_arabic_text('* بيانات توضيحية'), 
                       ha='center', fontsize=9, style='italic', color='gray')
            
            # إضافة الرسم إلى الواجهة
            canvas = FigureCanvasTkAgg(fig, self.operations_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء رسم العمليات: {e}")
    
    def create_categories_chart(self):
        """إنشاء رسم بياني لتوزيع التصنيفات"""
        if not CHARTS_AVAILABLE:
            self.create_text_chart(self.categories_chart_frame, "توزيع التصنيفات", 
                                  "مكتبات الرسوم البيانية غير متوفرة")
            return
            
        try:
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # تجميع البيانات حسب التصنيف
            categories = Counter(record[4] for record in self.all_data 
                               if len(record) > 4 and record[4])
            
            if categories:
                labels = list(categories.keys())
                sizes = list(categories.values())
                colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
                
                # إصلاح النصوص العربية للتسميات
                fixed_labels = [fix_arabic_text(label) for label in labels]
                
                wedges, texts, autotexts = ax.pie(sizes, labels=fixed_labels, autopct='%1.1f%%', 
                                                 colors=colors, startangle=90)
                ax.set_title(fix_arabic_text('توزيع العناصر حسب التصنيف'), fontsize=12, fontweight='bold')
                
                # تحسين النصوص
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                # إضافة بيانات وهمية للعرض
                labels = [fix_arabic_text('أدوات'), fix_arabic_text('مواد'), fix_arabic_text('معدات')]
                sizes = [30, 45, 25]
                colors = ['#FF9999', '#66B2FF', '#99FF99']
                
                wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                                 colors=colors, startangle=90, alpha=0.7)
                ax.set_title(fix_arabic_text('توزيع التصنيفات (مثال توضيحي)'), fontsize=12, fontweight='bold')
                
                # إضافة ملاحظة
                ax.text(0, -1.3, fix_arabic_text('* هذا مثال توضيحي - سيتم تحديثه عند إدخال البيانات'), 
                       ha='center', fontsize=9, style='italic', color='gray')
            
            canvas = FigureCanvasTkAgg(fig, self.categories_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء رسم التصنيفات: {e}")
    
    def create_projects_chart(self):
        """إنشاء رسم بياني لأنشطة المشاريع"""
        if not CHARTS_AVAILABLE:
            self.create_text_chart(self.projects_chart_frame, "نشاط المشاريع", 
                                  "مكتبات الرسوم البيانية غير متوفرة")
            return
            
        try:
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # تجميع البيانات حسب المشروع
            projects = Counter(record[10] for record in self.all_data 
                             if len(record) > 10 and record[10])
            
            if projects:
                project_names = list(projects.keys())[:10]  # أفضل 10 مشاريع
                project_counts = [projects[name] for name in project_names]
                
                bars = ax.bar(range(len(project_names)), project_counts, 
                             color=plt.cm.Paired(np.linspace(0, 1, len(project_names))))
                ax.set_title(fix_arabic_text('نشاط المشاريع (أفضل 10)'), fontsize=12, fontweight='bold')
                ax.set_xlabel(fix_arabic_text('المشاريع'))
                ax.set_ylabel(fix_arabic_text('عدد العمليات'))
                ax.set_xticks(range(len(project_names)))
                # إصلاح النصوص العربية لأسماء المشاريع
                fixed_project_names = [fix_arabic_text(name) for name in project_names]
                ax.set_xticklabels(fixed_project_names, rotation=45, ha='right')
                
                # إضافة قيم على الأعمدة
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom')
            else:
                # إضافة بيانات وهمية للعرض
                project_names = [fix_arabic_text('مشروع أ'), fix_arabic_text('مشروع ب'), 
                               fix_arabic_text('مشروع ج'), fix_arabic_text('مشروع د')]
                project_counts = [25, 18, 12, 8]
                
                bars = ax.bar(range(len(project_names)), project_counts, 
                             color=['#FF7F7F', '#7FFF7F', '#7F7FFF', '#FFFF7F'], alpha=0.7)
                ax.set_title(fix_arabic_text('نشاط المشاريع (مثال توضيحي)'), fontsize=12, fontweight='bold')
                ax.set_xlabel(fix_arabic_text('المشاريع'))
                ax.set_ylabel(fix_arabic_text('عدد العمليات'))
                ax.set_xticks(range(len(project_names)))
                ax.set_xticklabels(project_names, rotation=45, ha='right')
                
                # إضافة قيم على الأعمدة
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom')
                
                # إضافة ملاحظة
                ax.text(1.5, -5, fix_arabic_text('* هذا مثال توضيحي - سيتم تحديثه عند إدخال البيانات'), 
                       ha='center', fontsize=9, style='italic', color='gray')
            
            canvas = FigureCanvasTkAgg(fig, self.projects_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء رسم المشاريع: {e}")
    
    def create_inventory_chart(self):
        """إنشاء رسم بياني للمخزون والكميات"""
        if not CHARTS_AVAILABLE:
            self.create_text_chart(self.inventory_chart_frame, "المخزون والكميات", 
                                  "مكتبات الرسوم البيانية غير متوفرة")
            return
            
        try:
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # تحليل حركة الكميات
            item_quantities = defaultdict(list)
            
            for record in self.all_data:
                if len(record) > 5 and record[3] and record[5]:
                    try:
                        item_name = record[3]
                        quantity = float(record[5])
                        operation_type = record[2] if len(record) > 2 else ""
                        
                        if operation_type == "إضافة":
                            item_quantities[item_name].append(quantity)
                        elif operation_type == "إخراج":
                            item_quantities[item_name].append(-quantity)
                    except:
                        continue
            
            if item_quantities:
                # حساب إجمالي الكمية لكل عنصر
                items = []
                net_quantities = []
                
                for item, quantities in item_quantities.items():
                    net_qty = sum(quantities)
                    if net_qty != 0:  # تجاهل العناصر بصفر صافي
                        items.append(item)
                        net_quantities.append(net_qty)
                
                # ترتيب حسب الكمية (أعلى 10)
                sorted_data = sorted(zip(items, net_quantities), key=lambda x: abs(x[1]), reverse=True)[:10]
                items, net_quantities = zip(*sorted_data) if sorted_data else ([], [])
                
                if items:
                    colors = ['#4CAF50' if qty > 0 else '#F44336' for qty in net_quantities]
                    bars = ax.bar(range(len(items)), net_quantities, color=colors)
                    
                    ax.set_title(fix_arabic_text('صافي الكميات (أعلى 10 عناصر)'), fontsize=12, fontweight='bold')
                    ax.set_xlabel(fix_arabic_text('العناصر'))
                    ax.set_ylabel(fix_arabic_text('صافي الكمية'))
                    ax.set_xticks(range(len(items)))
                    # إصلاح النصوص العربية لأسماء العناصر
                    fixed_items = [fix_arabic_text(item) for item in items]
                    ax.set_xticklabels(fixed_items, rotation=45, ha='right')
                    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                    
                    # إضافة قيم على الأعمدة
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.1f}', ha='center', 
                               va='bottom' if height > 0 else 'top')
                else:
                    # عرض رسم توضيحي بسيط
                    self.show_simple_inventory_demo(ax)
            else:
                # عرض رسم توضيحي بسيط
                self.show_simple_inventory_demo(ax)
            
            canvas = FigureCanvasTkAgg(fig, self.inventory_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء رسم المخزون: {e}")
    
    def show_simple_inventory_demo(self, ax):
        """عرض رسم توضيحي بسيط للمخزون"""
        # بيانات وهمية للعرض
        items = [fix_arabic_text('أدوات'), fix_arabic_text('مواد خام'), 
                fix_arabic_text('معدات'), fix_arabic_text('قطع غيار')]
        quantities = [45, -15, 30, -8]
        colors = ['#4CAF50' if qty > 0 else '#F44336' for qty in quantities]
        
        bars = ax.bar(range(len(items)), quantities, color=colors, alpha=0.7)
        
        ax.set_title(fix_arabic_text('صافي الكميات (مثال توضيحي)'), fontsize=12, fontweight='bold')
        ax.set_xlabel(fix_arabic_text('العناصر'))
        ax.set_ylabel(fix_arabic_text('صافي الكمية'))
        ax.set_xticks(range(len(items)))
        ax.set_xticklabels(items, rotation=45, ha='right')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # إضافة قيم على الأعمدة
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height}', ha='center', 
                   va='bottom' if height > 0 else 'top')
        
        # إضافة ملاحظة
        ax.text(1.5, max(quantities) + 5, fix_arabic_text('* بيانات توضيحية - القيم الإيجابية فائض والسالبة عجز'), 
               ha='center', fontsize=9, style='italic', color='gray')
    
    # Function removed for simplified interface
    
    # Function removed for simplified interface
    
    # Function removed for simplified interface
    
    # Function removed for simplified interface
    
    # Function removed for simplified interface
    
    def show_no_data_message(self):
        """عرض رسالة عدم وجود بيانات"""
        # تحديث الإحصائيات بقيم صفرية
        self.total_items_card.config(text="0")
        self.total_operations_card.config(text="0") 
        self.active_projects_card.config(text="0")
        self.efficiency_card.config(text="0%")
    
    def refresh_analytics(self):
        """تحديث جميع التحليلات"""
        try:
            print("🔄 تحديث التحليلات...")
            
            # فحص الاتصال بالإنترنت قبل تحديث البيانات
            print("🔍 فحص الاتصال بالإنترنت...")
            if not check_internet_connection():
                messagebox.showerror("خطأ في الاتصال", 
                                   "⚠️ لا يوجد اتصال بالإنترنت!\n\n"
                                   "يرجى التأكد من الاتصال ثم حاول مرة أخرى.")
                return
            
            # تحميل البيانات مجدداً
            self.load_data()
            
            # مسح الرسوم البيانية القديمة
            for frame in [self.operations_chart_frame, self.categories_chart_frame,
                         self.projects_chart_frame, self.inventory_chart_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()
            
            # إعادة توليد التحليلات
            self.generate_analytics()
            
            messagebox.showinfo("تم التحديث", "تم تحديث جميع التحليلات بنجاح!")
            
        except Exception as e:
            print(f"❌ خطأ في تحديث التحليلات: {e}")
            messagebox.showerror("خطأ", f"فشل في تحديث التحليلات:\n{e}")
    
    # Functions removed for simplified interface


def test_analytics():
    """اختبار نافذة التحليل"""
    try:
        # فحص الاتصال بالإنترنت أولاً
        print("🔍 فحص الاتصال بالإنترنت...")
        if not check_internet_connection():
            print("❌ لا يوجد اتصال بالإنترنت")
            show_no_internet_message()
            return
        
        print("✅ تم التأكد من وجود اتصال بالإنترنت")
        
        import sys
        sys.path.append(r'D:\StrucTech Projects\Inventory System')
        
        from config.settings import load_config
        from enhanced_sheets_manager import EnhancedSheetsManager
        
        # تحميل الإعدادات
        config = load_config()
        
        # إنشاء النافذة الجذرية
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        # إنشاء المدير المحسن
        enhanced_manager = EnhancedSheetsManager(
            credentials_file=config['credentials_file'],
            spreadsheet_name=config['spreadsheet_name'],
            worksheet_name=config['worksheet_name']
        )
        
        if not enhanced_manager.connect():
            print("❌ فشل في الاتصال")
            return
        
        # إنشاء مستخدم تجريبي
        test_user = {
            'user_id': 'ADM_001',
            'user_type': 'admin'
        }
        
        # إنشاء النافذة
        analytics_window = AnalyticsWindow(root, enhanced_manager, test_user)
        
        print("✅ تم إنشاء نافذة التحليل بنجاح")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ في اختبار نافذة التحليل: {e}")
        # عرض رسالة خطأ للمستخدم
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("خطأ في التطبيق", f"حدث خطأ في تشغيل التطبيق:\n{e}")
        root.destroy()


if __name__ == "__main__":
    test_analytics()