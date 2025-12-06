#!/usr/bin/env bash
# أو للـ PowerShell: powershell -ExecutionPolicy Bypass -File release.ps1

# 📋 Release Script - سكريبت الإطلاق السريع

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  Sama Inventory System - Release Script        ║"
echo "║  سكريبت الإطلاق السريع                        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المسار الحالي
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}📁 المجلد: $SCRIPT_DIR${NC}"
echo ""

# 1. اختبار Python
echo -e "${YELLOW}1️⃣  فحص Python...${NC}"
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python غير مثبت!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python مثبت${NC}"
python --version
echo ""

# 2. اختبار البرنامج
echo -e "${YELLOW}2️⃣  اختبار التطبيق...${NC}"
echo "ملاحظة: أغلق النافذة بعد التأكد من أن كل شيء يعمل"
read -p "هل تريد تشغيل البرنامج؟ (y/n): " test_app
if [ "$test_app" = "y" ]; then
    python main.py &
    sleep 3
    echo -e "${GREEN}✅ البرنامج يعمل${NC}"
fi
echo ""

# 3. تحديث VERSION
echo -e "${YELLOW}3️⃣  تحديث رقم الإصدار...${NC}"
CURRENT_VERSION=$(cat VERSION.txt)
echo "الإصدار الحالي: $CURRENT_VERSION"
read -p "أدخل الإصدار الجديد (مثال: 1.0.1): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    NEW_VERSION=$CURRENT_VERSION
fi

echo "$NEW_VERSION" > VERSION.txt
echo -e "${GREEN}✅ تم تحديث الإصدار إلى: $NEW_VERSION${NC}"
echo ""

# 4. Commit
echo -e "${YELLOW}4️⃣  حفظ التغييرات في Git...${NC}"
git add .
git commit -m "Release v$NEW_VERSION"
echo -e "${GREEN}✅ تم حفظ التغييرات${NC}"
echo ""

# 5. Tag
echo -e "${YELLOW}5️⃣  إنشاء Release Tag...${NC}"
git tag -a v$NEW_VERSION -m "Release Version $NEW_VERSION"
echo -e "${GREEN}✅ تم إنشاء Tag: v$NEW_VERSION${NC}"
echo ""

# 6. Push
echo -e "${YELLOW}6️⃣  رفع التغييرات إلى GitHub...${NC}"
echo "رفع main branch..."
git push origin main
echo "رفع Release tag..."
git push origin v$NEW_VERSION
echo -e "${GREEN}✅ تم الرفع بنجاح${NC}"
echo ""

# النهاية
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║                ✅ تم بنجاح!                     ║"
echo "╠════════════════════════════════════════════════╣"
echo "║  الخطوة التالية:                               ║"
echo "║  1. اذهب إلى GitHub Actions:                  ║"
echo "║     https://github.com/StrucTech/Sama..       ║"
echo "║     /actions                                   ║"
echo "║  2. انتظر البناء (5-10 دقائق)                 ║"
echo "║  3. اذهب إلى Releases:                         ║"
echo "║     https://github.com/StrucTech/Sama..       ║"
echo "║     /releases                                  ║"
echo "║  4. احتفل! 🎉                                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
