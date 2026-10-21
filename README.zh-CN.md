# NGCC Round 1 —— 密码算法评估数据

**维护者**：苏宇凡、李兆轩 · **最后更新**：2026-10-21

[English](README.md) | **中文**

本仓库收录中国 NGCC（新一代商用密码）第一轮密码算法征集提交的评估数据：
**84 个公钥算法**（签名 34 / KEM 41 / KEX 9）与 **35 个哈希算法**。

> **说明**：本仓库为独立第三方评估。

目录按评估类型（`performance` / `correctness` / `consistency`）、
再按算法类别（`pkc` / `crypthash`）组织。

```
evaluation/
├── README.md           # 英文说明
├── README.zh-CN.md     # 中文说明（本文件）
├── LICENSE             # CC BY 4.0（数据、文档、图表）
├── performance/
│   ├── README.md       # 性能列与测量说明
│   ├── figures/
│   │   └── levels/     # 按安全档位的对比图
│   ├── pkc/
│   │   ├── ref/        # DSA.csv、KEM.csv、KEX.csv（已发布）
│   │   ├── opt/        # 预留，暂空
│   │   └── add/        # 预留，暂空
│   └── crypthash/
│       ├── ref/        # 预留，哈希性能暂未支持
│       ├── opt/        # 预留，暂空
│       └── add/        # 预留，暂空
├── correctness/
│   ├── README.md       # 正确性列与失败说明
│   ├── pkc/
│   │   ├── ref/        # DSA.csv、KEM.csv、KEX.csv（已发布）
│   │   ├── opt/        # 预留，暂空
│   │   └── add/        # 预留，暂空
│   └── crypthash/
│       ├── ref/        # 预留，哈希正确性暂未支持
│       ├── opt/        # 预留，暂空
│       └── add/        # 预留，暂空
└── consistency/
    ├── README.md       # 一致性（文档与代码）
    ├── pkc/            # 预留，结果整理中
    └── crypthash/      # 预留，结果整理中
```

## 数据来源

- **代码来源**：被测实现来自 NGCC 官方征集页公布的提交包
  （<https://www.niccs.org.cn/niccs/Proposal/pc/list.html>），
  该页同时列出公钥与哈希第一轮候选。
- **公钥算法**：84 个提交算法（DSA 34 / KEM 41 / KEX 9），均为参考（`ref`）实现；
  共 **396 条性能记录**（DSA 170 / KEM 168 / KEX 58）与 **396 条正确性记录**
  （DSA 170 / KEM 168 / KEX 58）。**全部 396 个提交参数集都有覆盖**。
- **哈希算法**：35 个提交算法。一致性评估已完成，结果正在整理、尚未入库；
  性能与正确性暂未支持。
- **性能与正确性相互独立**：性能覆盖全部公钥参数集，包括 6 个未通过正确性测试
  （外部向量检查）、但流程能跑完的参数集。

## 文档

- [performance/README.md](performance/README.md) —— 性能列、测量说明、排序、图表。
- [correctness/README.md](correctness/README.md) —— 正确性列、判词、失败说明。
- [consistency/README.md](consistency/README.md) —— 一致性（文档与代码）。

## 公共列

性能表与正确性表共有：

| 列 | 含义 |
| --- | --- |
| `ngcc_id` | [ngcc.dev](https://ngcc.dev/) 上的候选编号（如 `sign-01`） |
| `track` | `DSA` / `KEM` / `KEX` |
| `package` | 提交包名（如 `Aigis-Sig+`） |
| `param_set` | 参数集名称（包内唯一，如 `Aigis-Sig+-I`、`Amoeba-576`） |
| `classical_security_level` | 提交文档声明的经典安全档位（位：128/160/192/256/384/512）；无依据时留空 |
| `implementation` | 本版均为 `ref` |
| `family` | 算法族，[ngcc.dev](https://ngcc.dev/) 使用的标签（英文） |

`ngcc_id` 沿用 [ngcc.dev](https://ngcc.dev/) 公开安全报告的“类型-编号”顺序
（`sign-01`…`sign-34`、`kem-01`…`kem-41`、`kex-01`…`kex-09`），
`family` 采用该站点的算法族标签；两者均用于交叉检索。

## 状态

`performance/pkc/ref/` 与 `correctness/pkc/ref/` 已发布。
`performance/pkc/{opt,add}/`、全部 `crypthash/` 目录、
`consistency/{pkc,crypthash}/` 为预留，暂空。

## 方法局限

- **单机、单编译器基线。** 耗时为单机原始中位数，未按 CPU 频率归一化。
  锁频、绑核、预热不在已公布的测量协议内；相近条目的差异可能是噪声。
- **样本数不均。** 慢参数集只有 1–2 次采样（见 `samples`），耗时仅作方向性参考。

## 权利与许可

版权所有 (c) 2026 The Authors。

本评估由作者在自有设备上独立完成，为独立第三方评估。

数据、文档与图表采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可：
允许共享、改编，包括商业使用；但需署名、附许可链接，如作修改需注明修改。

如对数据或方法有疑问，或需进一步讨论，请联系 syf962812003@gmail.com。

## 后续计划

1. 入库一致性（文档与代码）评估结果。
2. 加入正确性测试的边界、异常等情况。
3. 加入 35 个哈希算法（先 ref 实现）的性能与正确性结果。
4. 补充全部 `opt/`、`add/` 实现的正确性与性能结果。
5. 加入内存与栈占用测量。
6. 加入计时控制（CPU 锁频、绑核、预热）并写入测量说明。
