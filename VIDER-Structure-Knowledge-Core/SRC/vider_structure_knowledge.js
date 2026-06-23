
/**
 * 🧠 VIDER Structure & Knowledge Core
 * - สแกนโครงสร้างแยกย่อยลงลึก
 * - จัดลำดับความรู้จากพื้นฐานสู่ซับซ้อน
 * - จำแนกประเภทการใช้งานอัตโนมัติ
 * - พร้อมเชื่อมต่อกับแกนหลัก VIDER AGI
 */

const crypto = require('crypto');

class VIDER_Structure_Knowledge {
  constructor(options = {}) {
    this.maxDepth = options.maxDepth || 15;
    this.structureDB = new Map();
    this.propertyDB = new Map();
    this.relationDB = new Map();
    this.variantDB = new Map();
    this._initBaseData();
  }

  // --- ฐานข้อมูลเริ่มต้น ---
  _initBaseData() {
    this.add("ข้าวผัดกระเพรา", ["ข้าวสวย", "เนื้อสัตว์", "ใบกระเพรา", "กระเทียม", "พริก", "น้ำมัน", "เครื่องปรุง", "กระทะ", "ความร้อน"]);
    this.add("ปากกา", ["ตัวเรือน", "แกนหมึก", "หัวเขียน", "ฝาปิด", "กลไก"]);
    this.add("มือมนุษย์", ["ฝ่ามือ", "นิ้วมือ", "ข้อมือ", "เส้นเอ็น", "กระดูก", "ผิวหนัง"]);
    this.addProperty("ข้าวสวย", "หน้าที่", "ให้พลังงาน");
    this.addProperty("ปากกา", "หน้าที่", "ใช้เขียนบันทึก");
  }

  // --- เพิ่ม/แก้ไขข้อมูล ---
  add(entity, parts) { this.structureDB.set(entity, parts); }
  addProperty(entity, key, val) {
    if (!this.propertyDB.has(entity)) this.propertyDB.set(entity, {});
    this.propertyDB.get(entity)[key] = val;
  }
  addVariant(entity, variantObj) { this.variantDB.set(entity, variantObj); }

  // --- ฟังก์ชันสแกนโครงสร้างหลัก ---
  async scan(target, visited = new Set(), depth = 0) {
    if (depth >= this.maxDepth) return { entity: target, depth, type: "พื้นฐาน", components: [] };
    if (visited.has(target)) return { entity: target, depth, type: "อ้างอิงซ้ำ", components: [] };
    visited.add(target);

    const parts = this.structureDB.get(target) || [];
    const children = [];
    for (const p of parts) children.push(await this.scan(p, new Set(visited), depth + 1));

    return {
      scanId: crypto.randomUUID(),
      entity: target,
      depth,
      type: parts.length ? "ประกอบด้วย" : "หน่วยพื้นฐาน",
      components: children,
      properties: this.propertyDB.get(target) || {},
      variants: this.variantDB.get(target) || null,
      countTotal: this._countNodes(children) + 1
    };
  }

  _countNodes(arr) {
    return arr.reduce((sum, n) => sum + 1 + this._countNodes(n.components), 0);
  }

  // --- จัดลำดับการเรียนรู้ ---
  generateLearningPath(scanResult) {
    const levels = [];
    const collect = (node) => { levels.push({ topic: node.entity, depth: node.depth }); node.components.forEach(collect); };
    collect(scanResult);
    levels.sort((a, b) => a.depth - b.depth);

    return {
      startFrom: "พื้นฐาน",
      sequence: levels.map((l, i) => ({ ลำดับ: i + 1, เรียนรู้: l.topic, ระดับ: l.depth })),
      logic: "เรียนจากส่วนประกอบเล็กสุด → รวมเป็นโครงสร้างใหญ่ → เข้าใจการทำงานทั้งระบบ"
    };
  }

  // --- จำแนกและสร้างผลลัพธ์พร้อมใช้งาน ---
  async analyze(target) {
    const scanData = await this.scan(target);
    const learning = this.generateLearningPath(scanData);

    return {
      system: "VIDER Structure+Knowledge",
      target,
      totalElements: scanData.countTotal,
      structure: scanData,
      learning_path: learning,
      summary: this._buildSummary(scanData)
    };
  }

  _buildSummary(data) {
    return {
      สรุป: `${data.entity} ประกอบด้วยทั้งหมด ${data.countTotal} ส่วน`,
      การนำไปใช้: "สามารถอธิบายโครงสร้าง วิเคราะห์ หรือจัดทำคู่มือ/คำตอบได้ตามลำดับความรู้"
    };
  }
}

// --- ส่งออกเพื่อใช้งาน ---
module.exports = VIDER_Structure_Knowledge;

// --- ทดสอบรันเมื่อเรียกใช้โดยตรง ---
if (require.main === module) {
  (async () => {
    const viderSK = new VIDER_Structure_Knowledge();
    const res = await viderSK.analyze("ข้าวผัดกระเพรา");
    console.log(JSON.stringify(res, null, 2));
  })();
}
