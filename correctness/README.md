# Correctness data

[中文](#中文)

Correctness evaluation of the NGCC Round 1 public-key reference
implementations. Hash correctness is not yet supported; `crypthash/` is
reserved.

## Scope

- `pkc/ref/{KEM,DSA,KEX}.csv`: 396 records, **390 pass** and **6 fail**
  (KEM 168 / DSA 170 / KEX 58).
- `pkc/opt/`, `pkc/add/`, and `crypthash/`: reserved.

## Columns

Common columns are defined in the [root README](../README.md#common-columns).
Correctness CSVs add:

| Column | Meaning |
| --- | --- |
| `cases_total` | number of KAT cases executed |
| `cases_passed` | number of cases that passed |
| `cases_failed` | number of cases that failed |
| `verdict` | `pass` / `fail` |
| `failure_type` | evaluator's failure classification, English (empty when `pass`) |
| `failure_detail` | concrete cause for a failing row (empty when `pass`) |

Most rows execute **8 cases**; a few submissions ship vector blocks that yield
fewer usable cases (1, 3, 4 or 6) — the exact count is in `cases_total`.

## Failures

The six failures are four `SQIsign2D-push12` sets and two `Tins` sets:

- `SQIsign2D-push12` Level-1/2/4: `sig_sign` only accepts in-process registry
  keys, so external KAT `sk` is rejected.
- `SQIsign2D-push12` Level-3: same registry limitation; in addition the KAT
  has `SK_Len=676` while the implementation generates `900`.
- `Tins-128`: verification compares against uninitialized `test_h_piop`.
- `Tins-512`: verification overwrites the caller's signature buffer and
  decodes uninitialized bytes.

`failure_detail` states the cause for each failing row. The three `CS` rows use
the public build recipe described in the
[performance README](../performance/README.md#measurement-notes).

Verdicts refer to the 2026-10-21 evaluation batch and may differ from earlier
releases.

---

## 中文

NGCC 第一轮公钥参考实现的正确性评估数据。哈希正确性暂未支持，`crypthash/`
为预留目录。

### 范围

- `pkc/ref/{KEM,DSA,KEX}.csv`：396 条，**通过 390 条**、**未通过 6 条**
  （KEM 168 / DSA 170 / KEX 58）。
- `pkc/opt/`、`pkc/add/`、`crypthash/`：预留。

### 列

公共列见[根 README](../README.md#common-columns)。正确性表另有：

| 列 | 含义 |
| --- | --- |
| `cases_total` | 实际执行的 KAT 用例数 |
| `cases_passed` | 通过的用例数 |
| `cases_failed` | 未通过的用例数 |
| `verdict` | `pass` / `fail` |
| `failure_type` | 评估侧的失败分类（英文；`pass` 时为空） |
| `failure_detail` | 失败行的具体原因（`pass` 时为空） |

多数行执行 **8 个用例**；少数提交的向量块可用用例更少（1、3、4 或 6 个），
确切数字见 `cases_total`。

### 失败说明

6 条失败为 `SQIsign2D-push12` 四组与 `Tins` 两组：

- `SQIsign2D-push12` Level-1/2/4：`sig_sign` 只认进程内注册表，
  外部 KAT `sk` 被拒。
- `SQIsign2D-push12` Level-3：同上；另加 KAT `SK_Len=676` vs 实现 `900`。
- `Tins-128`：验签与未初始化 `test_h_piop` 比较。
- `Tins-512`：验签覆盖调用者签名缓冲、解码未初始化字节。

具体原因见 `failure_detail`。三条 `CS` 使用
[性能 README](../performance/README.md#测量说明) 中说明的配方档构建。

判词对应 2026-10-21 批次，可能与更早版本不同。
