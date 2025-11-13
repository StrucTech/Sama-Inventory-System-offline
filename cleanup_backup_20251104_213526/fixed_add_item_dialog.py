#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخة محدثة من add_item_dialog مع إصلاحات شاملة
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FixedAddItemDialog:
    def __init__(self, parent, sheets_manager):
        self.parent = parent
        self.sheets_manager = sheets_manager
        self.result = None
        self.unique_items = {}
        self.unique_categories = set()
        self.is_new_item_mode = True
        
        # جلب البيانات
        self.load_data()
        
        # إنشاء النافذة
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة عنصر للمخزون")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # متغير الوضع مع trace
        self.mode_var = tk.StringVar(value="")
        self.mode_var.trace_add("write", self.on_mode_change_trace)
        
        self.setup_ui()
        
        # وضع النافذة في المنتصف
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # انتظار إغلاق النافذة
        self.dialog.wait_window()
        
    def load_data(self):
        """جلب البيانات من الشيت"""
        try:
            print("📊 جلب البيانات من Google Sheets...")
            all_items = self.sheets_manager.get_all_items()
            
            for item in all_items:
                if len(item) >= 2:
                    item_name = item[0].strip()
                    category = item[1].strip() if item[1] else "غير محدد"
                    
                    if item_name:
                        self.unique_items[item_name] = category
                        self.unique_categories.add(category)
            
            print(f"✅ تم جلب {len(self.unique_items)} عنصر و {len(self.unique_categories)} تصنيف")
            
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات: {e}")
            messagebox.showerror("خطأ", f"فشل في جلب البيانات: {str(e)}")
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        print("🔧 إعداد واجهة المستخدم...")
        
        # الإطار الرئيسي
        self.main_frame = ttk.Frame(self.dialog, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # العنوان
        title_label = ttk.Label(self.main_frame, text="إضافة عنصر للمخزون", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # إطار اختيار الوضع
        mode_frame = ttk.LabelFrame(self.main_frame, text="اختر طريقة الإضافة", padding="15")
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        # أزرار الاختيار
        existing_radio = ttk.Radiobutton(mode_frame, text="اختيار عنصر موجود", 
                                        variable=self.mode_var, value="existing")
        existing_radio.pack(anchor=tk.W, pady=5)
        
        new_radio = ttk.Radiobutton(mode_frame, text="إضافة عنصر جديد", 
                                   variable=self.mode_var, value="new")
        new_radio.pack(anchor=tk.W, pady=5)
        
        # إطار المحتوى
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # إطار الأزرار
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # زر الإلغاء
        cancel_btn = ttk.Button(self.buttons_frame, text="إلغاء", command=self.cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # زر الإضافة (مخفي في البداية)
        self.add_btn = ttk.Button(self.buttons_frame, text="إضافة", command=self.add_item)
        
        # عرض رسالة الاختيار الأولية
        self.show_selection_prompt()
        
        print("✅ تم إعداد واجهة المستخدم")
    
    def on_mode_change_trace(self, *args):
        """معالج تغيير الوضع"""
        mode = self.mode_var.get()
        print(f"🎯 تغيير الوضع إلى: '{mode}'")
        
        # مسح المحتوى الحالي
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # إخفاء زر الإضافة
        self.add_btn.pack_forget()
        
        # إعداد واجهة حسب الوضع
        if mode == "existing":
            print("📋 إعداد واجهة العناصر الموجودة")
            self.is_new_item_mode = False
            self.setup_existing_items_ui()
        elif mode == "new":
            print("➕ إعداد واجهة العنصر الجديد")
            self.is_new_item_mode = True
            self.setup_new_item_ui()
        else:
            print("❓ عرض رسالة الاختيار")
            self.show_selection_prompt()
    
    def show_selection_prompt(self):
        """عرض رسالة اختيار الوضع"""
        prompt_frame = ttk.LabelFrame(self.content_frame, text="يرجى الاختيار", padding="20")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        prompt_text = ("يرجى اختيار طريقة الإضافة من الأعلى:\n\n"
                      "• اختيار عنصر موجود: لإضافة كمية لعنصر موجود\n"
                      "• إضافة عنصر جديد: لإضافة عنصر جديد للمخزون")
        
        prompt_label = ttk.Label(prompt_frame, text=prompt_text,
                                font=("Arial", 12), justify=tk.CENTER)
        prompt_label.pack(expand=True)
    
    def setup_existing_items_ui(self):
        """إعداد واجهة العناصر الموجودة"""
        if not self.unique_items:
            no_items_label = ttk.Label(self.content_frame, 
                                      text="لا توجد عناصر موجودة، يرجى اختيار 'إضافة عنصر جديد'",
                                      font=("Arial", 12))
            no_items_label.pack(pady=20)
            return
        
        # إطار النموذج
        form_frame = ttk.LabelFrame(self.content_frame, text="اختيار عنصر موجود", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # اختيار العنصر
        ttk.Label(form_frame, text="اختر العنصر:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.item_combobox = ttk.Combobox(form_frame, width=35, font=("Arial", 12))
        self.item_combobox['values'] = list(self.unique_items.keys())
        self.item_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.item_combobox.bind('<<ComboboxSelected>>', self.on_item_selected)
        
        # عرض التصنيف
        ttk.Label(form_frame, text="التصنيف:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.category_display = ttk.Label(form_frame, text="", font=("Arial", 12), 
                                         background="white", relief="sunken")
        self.category_display.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # الكمية
        ttk.Label(form_frame, text="الكمية:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.quantity_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.quantity_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.quantity_entry.focus()
        
        form_frame.columnconfigure(1, weight=1)
        
        # إظهار زر الإضافة
        self.add_btn.pack(side=tk.RIGHT)
        print("✅ تم إعداد واجهة العناصر الموجودة")
    
    def setup_new_item_ui(self):
        """إعداد واجهة العنصر الجديد"""
        # إطار النموذج
        form_frame = ttk.LabelFrame(self.content_frame, text="إضافة عنصر جديد", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # اسم العنصر
        ttk.Label(form_frame, text="اسم العنصر:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.new_item_name_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.new_item_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        self.new_item_name_entry.focus()
        
        # التصنيف
        ttk.Label(form_frame, text="التصنيف:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.new_category_entry = ttk.Entry(form_frame, width=30, font=("Arial", 12))
        self.new_category_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # زر اختيار التصنيف
        category_btn = ttk.Button(form_frame, text="اختر من القائمة", 
                                 command=self.show_category_list)
        category_btn.grid(row=1, column=2, pady=8, padx=(5, 0))
        
        # الكمية
        ttk.Label(form_frame, text="الكمية:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.quantity_entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
        self.quantity_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # إظهار زر الإضافة
        self.add_btn.pack(side=tk.RIGHT)
        print("✅ تم إعداد واجهة العنصر الجديد")
    
    def on_item_selected(self, event=None):
        """معالج اختيار العنصر"""
        selected_item = self.item_combobox.get()
        if selected_item in self.unique_items:
            category = self.unique_items[selected_item]
            self.category_display.config(text=category)
            print(f"📝 تم اختيار العنصر: {selected_item}, التصنيف: {category}")
    
    def show_category_list(self):
        """عرض قائمة التصنيفات"""
        if not self.unique_categories:
            messagebox.showinfo("تنبيه", "لا توجد تصنيفات محفوظة")
            return
        
        # نافذة اختيار التصنيف
        category_dialog = tk.Toplevel(self.dialog)
        category_dialog.title("اختيار التصنيف")
        category_dialog.geometry("300x400")
        category_dialog.transient(self.dialog)
        category_dialog.grab_set()
        
        # قائمة التصنيفات
        listbox = tk.Listbox(category_dialog, font=("Arial", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for category in sorted(self.unique_categories):
            listbox.insert(tk.END, category)
        
        # أزرار
        btn_frame = ttk.Frame(category_dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def select_category():
            selection = listbox.curselection()
            if selection:
                selected_category = listbox.get(selection[0])
                self.new_category_entry.delete(0, tk.END)
                self.new_category_entry.insert(0, selected_category)
                category_dialog.destroy()
        
        ttk.Button(btn_frame, text="اختيار", command=select_category).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="إلغاء", command=category_dialog.destroy).pack(side=tk.RIGHT)
    
    def add_item(self):
        """إضافة العنصر"""
        try:
            mode = self.mode_var.get()
            print(f"🔄 محاولة إضافة عنصر، الوضع: {mode}")
            
            if not mode:
                messagebox.showerror("خطأ", "يرجى اختيار طريقة الإضافة")
                return
            
            # التحقق من الكمية
            quantity_text = self.quantity_entry.get().strip()
            if not quantity_text:
                messagebox.showerror("خطأ", "يرجى إدخال الكمية")
                return
            
            try:
                quantity = float(quantity_text)
                if quantity <= 0:
                    messagebox.showerror("خطأ", "يجب أن تكون الكمية أكبر من صفر")
                    return
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
                return
            
            if mode == "existing":
                # إضافة لعنصر موجود
                selected_item = self.item_combobox.get().strip()
                if not selected_item:
                    messagebox.showerror("خطأ", "يرجى اختيار العنصر")
                    return
                
                category = self.unique_items[selected_item]
                success = self.sheets_manager.add_item(selected_item, category, quantity)
                
            else:  # new
                # إضافة عنصر جديد
                item_name = self.new_item_name_entry.get().strip()
                category = self.new_category_entry.get().strip()
                
                if not item_name:
                    messagebox.showerror("خطأ", "يرجى إدخال اسم العنصر")
                    return
                
                if not category:
                    messagebox.showerror("خطأ", "يرجى إدخال التصنيف")
                    return
                
                success = self.sheets_manager.add_item(item_name, category, quantity)
            
            if success:
                messagebox.showinfo("نجح", "تم إضافة العنصر بنجاح!")
                self.result = "success"
                self.dialog.destroy()
            else:
                messagebox.showerror("خطأ", "فشل في إضافة العنصر")
                
        except Exception as e:
            print(f"❌ خطأ في إضافة العنصر: {e}")
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
    
    def cancel(self):
        """إلغاء"""
        print("❌ تم إلغاء العملية")
        self.result = "cancelled"
        self.dialog.destroy()

def show_dialog(parent, sheets_manager):
    """عرض نافذة إضافة العنصر"""
    dialog = FixedAddItemDialog(parent, sheets_manager)
    return dialog.result