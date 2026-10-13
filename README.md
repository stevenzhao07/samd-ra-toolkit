# samd-ra-toolkit

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

Software as a Medical Device（SaMD / AIaMD）的注册与质量体系工具包：SaMD 判定树 + IEC 62304 / ISO 14971(AI) / EU AI Act 映射 + PCCP 模板骨架 + AI-CER 骨架 + **跨辖区差异表（NMPA / EU MDR / FDA / PMDA）**。（对应『跨辖区监管映射模板』能力缺口。）

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增辖区：在 `JURISDICTIONS` 字典加一项，跨辖区表自动扩展。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 跨辖区矩阵：NMPA / EU MDR / FDA / PMDA 的分类、路径、主管/公告机构、关键文档、典型周期
- SaMD 判定树：按风险类别（I–IV）给出辖区落地建议
- 模板骨架：PCCP（ Predetermined Change Control Plan）、AI-CER 章节占位
- 零依赖 + CLI：`python scripts/samd_map.py --jurisdiction EU`

**上游投稿目标**：OpenRegulatory/templates

## 内容说明

本仓定位为「法规工程师的工作台」，把分散在各辖区的 SaMD 要求聚到一张可检索的表。自创内容 CC BY 4.0；投向上游 OpenRegulatory/templates。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/samd_map.py --jurisdiction ALL
python scripts/samd_map.py --risk-class III --jurisdiction FDA
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/samd-ra-toolkit.git && cd samd-ra-toolkit
python scripts/samd_map.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/samd-ra-toolkit/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [ai-governance-checklist](https://github.com/stevenzhao07/ai-governance-checklist)
- [ml-validation-toolkit](https://github.com/stevenzhao07/ml-validation-toolkit)
- [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)

## 许可

CC-BY-4.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
