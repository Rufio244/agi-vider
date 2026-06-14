# unlock_system_v2.py
# ระบบปลดล็อกและจัดการสิทธิ์ แบบรองรับการขยายในอนาคต
# AGI VIDER v2.0.0

MASTER_KEY = "ViderThanva244"  # รหัสหลักเดิม
LEVEL_CODES = {
    "Chani": 1,   # พื้นฐาน
    "Prosc": 2,   # ขั้นสูง
    "SC": 3       # สูงสุด Qvnt‑SC 7.5.0 MAX
}
DEFAULT_QVNT = "Qvnt‑SC 1.7.1 Basic"
QVNT_BY_LEVEL = {
    1: "Qvnt‑SC 1.7.1 Basic",
    2: "Qvnt‑SC 5.0.0 Advanced",
    3: "Qvnt‑SC 7.5.0 MAX"
}

class AccessControl:
    def __init__(self):
        self.access_level = 0
        self.is_unlocked = False
        self.active_qvnt = DEFAULT_QVNT
        # ทะเบียนระบบ/โมดูลทั้งหมด สามารถเพิ่มได้ตลอด
        self.module_permissions = {
            # แกนหลัก
            "AGI_Core": {"min_level": 3, "description": "แกนกลางสูงสุด"},
            # ระบบย่อยปัจจุบัน
            "Vider_PranAI": {"min_level": 1, "description": "ค้นหาและออกแบบตามหลักการ"},
            "Vider_AI_Research": {"min_level": 1, "description": "วิเคราะห์ระดับโมเลกุล พันธุกรรม"},
            "Vider_Lakon": {"min_level": 1, "description": "สร้างสรรค์เนื้อหาและเรื่องราว"},
            "Vider_Office": {"min_level": 1, "description": "จัดการเอกสารและงานทั่วไป"},
            # 📌 เตรียมช่องว่างสำหรับเพิ่มในอนาคต
            # "Vider_NewModule": {"min_level": 2, "description": "ระบบใหม่ที่จะสร้างภายหลัง"}
        }

    def verify_access(self, input_master: str, input_level: str) -> dict:
        """ตรวจสอบรหัสและปลดล็อกระบบ"""
        if input_master != MASTER_KEY:
            return {"success": False, "message": "❌ รหัสหลักไม่ถูกต้อง"}
        if input_level not in LEVEL_CODES:
            return {"success": False, "message": "❌ รหัสระดับไม่ถูกต้อง"}

        self.access_level = LEVEL_CODES[input_level]
        self.is_unlocked = True
        self.active_qvnt = QVNT_BY_LEVEL.get(self.access_level, DEFAULT_QVNT)

        return {
            "success": True,
            "message": f"✅ ปลดล็อกสำเร็จ | ระดับ: {input_level} | Qvnt: {self.active_qvnt}",
            "level": input_level,
            "level_num": self.access_level,
            "qvnt": self.active_qvnt
        }

    def register_new_module(self, module_name: str, min_access_level: int, description: str = "") -> dict:
        """📌 เพิ่มระบบ/โมดูลใหม่ในอนาคตได้เลย"""
        if module_name in self.module_permissions:
            return {"success": False, "message": "⚠️ โมดูลนี้มีอยู่แล้ว"}
        if min_access_level not in QVNT_BY_LEVEL:
            return {"success": False, "message": "❌ ระดับสิทธิ์ไม่ถูกต้อง"}

        self.module_permissions[module_name] = {
            "min_level": min_access_level,
            "description": description
        }
        return {
            "success": True,
            "message": f"✅ ลงทะเบียนโมดูล {module_name} เรียบร้อย",
            "require_level": min_access_level
        }

    def check_module_access(self, module_name: str) -> dict:
        """ตรวจสอบว่ามีสิทธิ์ใช้งานระบบนี้หรือไม่"""
        if not self.is_unlocked:
            return {"allowed": False, "reason": "🔒 ระบบยังไม่ได้รับการปลดล็อก"}
        if module_name not in self.module_permissions:
            return {"allowed": False, "reason": "❌ ไม่พบข้อมูลระบบนี้"}

        req_level = self.module_permissions[module_name]["min_level"]
        if self.access_level >= req_level:
            return {
                "allowed": True,
                "message": f"✅ ใช้งาน {module_name} ได้",
                "active_qvnt": self.active_qvnt
            }
        else:
            return {
                "allowed": False,
                "reason": f"⚠️ ต้องการระดับสิทธิ์อย่างน้อย {req_level} จึงจะใช้งานได้"
            }

    def list_all_modules(self) -> dict:
        """แสดงรายการระบบทั้งหมดที่มี"""
        return {
            "total": len(self.module_permissions),
            "modules": self.module_permissions
        }

