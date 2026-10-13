# AGENTS.md · samd-ra-toolkit

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
Software as a Medical Device（SaMD / AIaMD）的注册与质量体系工具包：SaMD 判定树 + IEC 62304 / ISO 14971(AI) / EU AI Act 映射 + PCCP 模板骨架 + AI-CER 骨架 + **跨辖区差异表（NMPA / EU MDR / FDA / PMDA）**。（对应『跨辖区监管映射模板』能力缺口。）

## 运行
```bash
python scripts/samd_map.py --demo
python scripts/samd_map.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增辖区：在 `JURISDICTIONS` 字典加一项，跨辖区表自动扩展。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
