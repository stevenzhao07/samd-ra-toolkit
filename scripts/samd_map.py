#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
samd_map.py — SaMD / AIaMD 跨辖区法规映射
==========================================
把分散在 NMPA / EU MDR / FDA / PMDA 的 SaMD 要求聚到一张可检索表，
并按风险类别给出落地建议。零依赖（仅 Python 3.8+ 标准库）。
（对应『跨辖区监管映射模板』能力缺口。）

法规锚点已 web 一手核实（2026-10-12，多来源交叉）：
- NMPA：AI 注册审查指导原则=器审中心通告 2022年第8号（2022-03-07）；
  AI 医用软件分类界定=NMPA 通告 2021年第47号（2022年第9号是软件注册
  审查指导原则修订版，勿混）。
- FDA：分类程序=21 CFR 860；矫形器械=21 CFR 888；21 CFR 861 实为
  "Procedures for Performance Standards Development"（性能标准制定程序）。
- EU：AI Act=Regulation (EU) 2024/1689；器械 Annex I 高风险义务已由
  Regulation (EU) 2026/1744 推迟至 2028-08-02。
- PMDA：无单一"AI 指导原则"文件；可引用薬生機審発0523第2号（2019）。
"""
from __future__ import annotations
import sys
import argparse

# --- 辖区别名归一化（2026-10-14 跨模块统一词表）---
# 目标：同一句话在医疗线各模块间通用——既接受 ISO 国家码，也接受监管机构缩写。
# 注意：东盟(ASEAN) / 拉美(LATAM) 尚无实现，仍会被下方校验明确拒绝。
_JURIS_ALIAS = {
    "CN": "CN", "NMPA": "CN", "CHINA": "CN",
    "US": "US", "USA": "US", "FDA": "US",
    "EU": "EU", "MDR": "EU", "CE": "EU",
    "JP": "JP", "JAPAN": "JP", "PMDA": "JP",
}
_JURIS_LOCAL = {"CN": "NMPA", "US": "FDA", "EU": "EU", "JP": "PMDA"}


def _norm_juris(j):
    """把用户输入归一化到本模块内部键；未知值原样返回，交由原校验明确拒绝。"""
    s = (j or "").strip().upper()
    c = _JURIS_ALIAS.get(s)
    if c is None:
        return s
    return _JURIS_LOCAL.get(c, c)


JURISDICTIONS = {
    "NMPA": {
        "region": "中国",
        "agency": "国家药监局 (NMPA)",
        "framework": "《人工智能医疗器械注册审查指导原则》（国家药监局器审中心通告 2022年第8号，2022-03-07）+《人工智能医用软件产品分类界定指导原则》（NMPA 通告 2021年第47号）+ 医疗器械软件注册技术审查指导原则",
        "classification": "按《医疗器械分类规则》+ 软件风险（预期用途/重要程度）",
        "pathway": "注册申报（二类/三类审评，AI 多走三类）",
        "key_docs": "软件描述文档 / 需求 / 算法 / 更新 / 网络安全",
        "typical_timeline": "审评 12–24 月（三类）",
    },
    "EU": {
        "region": "欧盟",
        "agency": "公告机构 (Notified Body) + MDCG 协调；AI Act 由 AI Office / 成员国主管机关负责",
        "framework": "EU MDR 2017/745 + EU AI Act（Regulation (EU) 2024/1689；器械相关 Annex I 高风险义务 2028-08-02 起适用，经 Regulation (EU) 2026/1744 Digital Omnibus 推迟）",
        "classification": "MDR 基于风险(I/IIa/IIb/III) + AI Act 风险分级（注意：EMA 管药品不管器械）",
        "pathway": "CE 认证（III 类 / IIb 植入需 NB 介入）+ AI Act 合规",
        "key_docs": "Technical File / CER / 临床证据 / AI 系统风险自评",
        "typical_timeline": "CE 9–18 月 + AI Act 义务",
    },
    "FDA": {
        "region": "美国",
        "agency": "FDA (CDRH)",
        "framework": "SaMD 框架 + Predetermined Change Control Plan (PCCP)",
        "classification": "按 21 CFR 860 分类程序 (Class I–III；矫形器械目录见 21 CFR 888) + 软件宣称",
        "pathway": "510(k) / De Novo / PMA（AI 多走 510(k)+PCCP）",
        "key_docs": "Software Documentation / Clinical / PCCP / 算法变更协议",
        "typical_timeline": "510(k) 3–12 月；PMA 更长",
    },
    "PMDA": {
        "region": "日本",
        "agency": "PMDA / MHLW",
        "framework": "PMDA プログラム医療機器（SaMD）审查指南 +《人工知能技術を利用した医用画像診断支援システムに関する評価指標》（薬生機審発0523第2号，2019-05-23）",
        "classification": "基于对人体风险(Ⅰ–Ⅳ类)",
        "pathway": "上市许可申请（外国制造须指定 MAH）",
        "key_docs": "程序描述 / 算法 / 验证 / 网络安全",
        "typical_timeline": "审查 9–18 月",
    },
}

# 注意：RISK_ADVICE 的 I–IV 是「内部统一风险刻度」（序数），并非任一辖区的法定分类。
# 真实辖区档位不同：NMPA/FDA 为 I/II/III（3 类），EU MDR 为 I/IIa/IIb/III，PMDA 为 Ⅰ–Ⅳ。
# 映射时以各辖区 classification 字段为准，本刻度仅用于跨辖区相对高低排序。
RISK_ADVICE = {
    "I": "最低风险：文档化 + 基本 QMS（ISO 13485）即可。",
    "II": "中风险：需临床证据 + 变更控制；考虑 PCCP/AI Act 透明义务。",
    "III": "高风险：独立审评/公告机构介入 + 充分临床 + 人因/网络安全。",
    "IV": "最高风险：最严临床 + 持续监测(PMS/PMCF) + 人类监督强约束。",
}


def print_jurisdiction(j: str) -> None:
    d = JURISDICTIONS[j]
    print(f"### {j}（{d['region']}）")
    for k in ("agency", "framework", "classification", "pathway", "key_docs", "typical_timeline"):
        print(f"  - {k}: {d[k]}")
    print()


def _demo() -> int:
    for j in JURISDICTIONS:
        print_jurisdiction(j)
    print("[注] 下方 I–IV 为内部统一风险刻度（序数），非任一辖区法定分类；"
          "NMPA/FDA 为 I/II/III，EU MDR 为 I/IIa/IIb/III，PMDA 为 Ⅰ–Ⅳ。")
    print(f"[风险 III] {RISK_ADVICE['III']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="SaMD 跨辖区法规映射")
    ap.add_argument("--demo", action="store_true", help="打印全部辖区 + 风险 III 建议")
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--jurisdiction", default="ALL", help="CN|NMPA | US|FDA | EU|MDR | JP|PMDA | ALL（别名互通；ASEAN/LATAM 未实现）")
    ap.add_argument("--risk-class", help="I/II/III/IV 给出落地建议")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()

    if args.demo:
        return _demo()

    if args.risk_class:
        if args.risk_class not in RISK_ADVICE:
            print("[err] risk-class 须为 I/II/III/IV")
            return 2
        print(f"[风险 {args.risk_class}] {RISK_ADVICE[args.risk_class]}\n")

    js = JURISDICTIONS.keys() if args.jurisdiction.upper() == "ALL" else [_norm_juris(args.jurisdiction)]
    for j in js:
        if j not in JURISDICTIONS:
            print(f"[err] 未知辖区: {j}")
            return 2
        print_jurisdiction(j)
    return 0


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, [], [], None), (['--jurisdiction', 'FDA', '--risk-class', 'II'], 0, [], [], None), (['--risk-class', 'IX'], 2, [], [], None), (['--jurisdiction', 'US', '--risk-class', 'II'], 0, [], [], '跨模块辖区命名不一致：pms-vigilance 用 CN/US/EU，本模块用 NMPA/FDA/EU/PMDA，US 被拒')]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
