"""
إدارة جلسة المستخدم وصلاحياته
"""

class UserSession:
    """كلاس لإدارة جلسة المستخدم الحالي"""
    
    def __init__(self):
        self.username = None
        self.project_number = None
        self.is_admin = False
        self.is_logged_in = False
        self.login_time = None
    
    def login(self, username, project_number, is_admin=False):
        """تسجيل دخول المستخدم"""
        from datetime import datetime
        
        self.username = username
        self.project_number = project_number
        self.is_admin = is_admin
        self.is_logged_in = True
        self.login_time = datetime.now()
        
        print(f"✅ تم تسجيل دخول المستخدم: {username}")
        print(f"   رقم المشروع: {project_number}")
        print(f"   نوع المستخدم: {'مدير' if is_admin else 'مستخدم عادي'}")
    
    def logout(self):
        """تسجيل خروج المستخدم"""
        print(f"👋 تم تسجيل خروج المستخدم: {self.username}")
        
        self.username = None
        self.project_number = None
        self.is_admin = False
        self.is_logged_in = False
        self.login_time = None
    
    def has_admin_access(self):
        """التحقق من صلاحيات المدير"""
        return self.is_logged_in and self.is_admin
    
    def can_access_project(self, project_number):
        """التحقق من إمكانية الوصول للمشروع"""
        if not self.is_logged_in:
            return False
        
        # المدير يمكنه الوصول لجميع المشاريع
        if self.is_admin:
            return True
        
        # المستخدم العادي يمكنه الوصول فقط لمشروعه
        return str(self.project_number) == str(project_number)
    
    def can_access_user_data(self, username):
        """التحقق من إمكانية الوصول لبيانات المستخدم"""
        if not self.is_logged_in:
            return False
        
        # المدير يمكنه الوصول لجميع المستخدمين
        if self.is_admin:
            return True
        
        # المستخدم العادي يمكنه الوصول فقط لبياناته
        return self.username == username
    
    def get_accessible_projects(self):
        """الحصول على قائمة المشاريع المتاحة للمستخدم"""
        if not self.is_logged_in:
            return []
        
        if self.is_admin:
            # المدير يرى جميع المشاريع - يمكن تحديث هذا لاحقاً
            return ['الكل']  # سيتم تحديثها من قاعدة البيانات
        else:
            # المستخدم العادي يرى مشروعه فقط
            return [str(self.project_number)]
    
    def get_accessible_users(self):
        """الحصول على قائمة المستخدمين المتاحة"""
        if not self.is_logged_in:
            return []
        
        if self.is_admin:
            # المدير يرى جميع المستخدمين - يمكن تحديث هذا لاحقاً
            return ['الكل']  # سيتم تحديثها من قاعدة البيانات
        else:
            # المستخدم العادي يرى نفسه فقط
            return [self.username]
    
    def __str__(self):
        """تمثيل نصي للجلسة"""
        if not self.is_logged_in:
            return "غير مسجل دخول"
        
        return f"{self.username} - مشروع {self.project_number} ({'مدير' if self.is_admin else 'مستخدم'})"

# متغير عام للجلسة الحالية
current_session = UserSession()