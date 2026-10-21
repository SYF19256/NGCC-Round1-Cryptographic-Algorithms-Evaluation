# NGCC Round 1 — Cryptographic Algorithms Evaluation

**Maintainer:** Yufan Su, Zhaoxuan Li · **Last updated:** 2026-10-21

[中文说明](README.zh-CN.md) | **English**

Evaluation data for China's NGCC (Next Generation Commercial Cryptography)
Round 1 cryptographic algorithm submissions: **84 public-key algorithms**
(DSA 34 / KEM 41 / KEX 9) and **35 hash algorithms**.

> **Note:** This repository contains an independent third-party evaluation.

This repository is organized by evaluation type (`performance`, `correctness`,
`consistency`), then by algorithm class (`pkc`, `crypthash`).

```
evaluation/
├── README.md           # English (this file)
├── README.zh-CN.md     # Chinese
├── LICENSE             # CC BY 4.0 (data, docs, figures)
├── performance/
│   ├── README.md       # performance columns and measurement notes
│   ├── figures/
│   │   └── levels/     # per-level comparison figures
│   ├── pkc/
│   │   ├── ref/        # DSA.csv, KEM.csv, KEX.csv (published)
│   │   ├── opt/        # reserved, empty
│   │   └── add/        # reserved, empty
│   └── crypthash/
│       ├── ref/        # reserved, hash performance not yet supported
│       ├── opt/        # reserved, empty
│       └── add/        # reserved, empty
├── correctness/
│   ├── README.md       # correctness columns and failure details
│   ├── pkc/
│   │   ├── ref/        # DSA.csv, KEM.csv, KEX.csv (published)
│   │   ├── opt/        # reserved, empty
│   │   └── add/        # reserved, empty
│   └── crypthash/
│       ├── ref/        # reserved, hash correctness not yet supported
│       ├── opt/        # reserved, empty
│       └── add/        # reserved, empty
└── consistency/
    ├── README.md       # specification-vs-code consistency
    ├── pkc/            # reserved, results being prepared
    └── crypthash/      # reserved, results being prepared
```

## Data source

- **Code source**: the tested implementations are the submission packages
  published on the official NGCC proposal page
  (<https://www.niccs.org.cn/niccs/Proposal/pc/list.html>), which lists both
  the public-key and hash Round 1 candidates.
- **Public-key algorithms**: 84 submitted algorithms (DSA 34 / KEM 41 / KEX 9),
  evaluated as reference (`ref`) implementations. **396 performance records**
  (DSA 170 / KEM 168 / KEX 58) and **396 correctness records**
  (DSA 170 / KEM 168 / KEX 58). All 396 submitted parameter sets are covered.
- **Hash algorithms**: 35 submitted algorithms. Consistency evaluation has been
  performed; results are being prepared for inclusion. Performance and
  correctness are not yet supported.
- **Performance and correctness are independent datasets**: timing covers all
  public-key parameter sets, including the six that fail the correctness suite
  (external-vector checks) but still run to completion.

## Documentation

- [performance/README.md](performance/README.md) — performance columns,
  measurement notes, sorting, figures.
- [correctness/README.md](correctness/README.md) — correctness columns,
  verdicts, failure details.
- [consistency/README.md](consistency/README.md) — specification-vs-code
  consistency.

## Common columns

Common to performance and correctness CSVs:

| Column | Meaning |
| --- | --- |
| `ngcc_id` | candidate identifier used on [ngcc.dev](https://ngcc.dev/) (e.g. `sign-01`) |
| `track` | `DSA` / `KEM` / `KEX` |
| `package` | submission package name (e.g. `Aigis-Sig+`) |
| `param_set` | parameter-set label (unique within a package, e.g. `Aigis-Sig+-I`, `Amoeba-576`) |
| `classical_security_level` | declared classical security level in bits (128/160/192/256/384/512); empty when not documented |
| `implementation` | `ref` (this release) |
| `family` | algorithm family label used on [ngcc.dev](https://ngcc.dev/) (English) |

`ngcc_id` follows the type/number order in the public security reports on
[ngcc.dev](https://ngcc.dev/) (`sign-01`…`sign-34`, `kem-01`…`kem-41`,
`kex-01`…`kex-09`); `family` uses the site's family labels. Both are kept for
cross-reference.

## Status

`performance/pkc/ref/` and `correctness/pkc/ref/` are published.
`performance/pkc/{opt,add}/`, all `crypthash/` directories, and
`consistency/{pkc,crypthash}/` are reserved and currently empty.

## Methodological limitations

- **Single host and compiler baseline.** Timings are raw medians from one
  machine and are not normalized for CPU frequency. Frequency locking, core
  pinning, and warm-up are not part of the published measurement protocol;
  small differences between close entries may be noise.
- **Uneven sample counts.** Slow parameter sets use 1–2 samples (see `samples`);
  those timings are directional only.

## Rights and license

Copyright (c) 2026 The Authors.

This evaluation was carried out independently by the authors on their own
equipment. It is an independent third-party evaluation.

Data, documentation, and figures are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): you may share and
adapt them for any purpose, including commercial use, provided you give
appropriate credit, link to the license, and indicate if changes were made.

For questions about the data or methodology, or for further discussion, please
contact syf962812003@gmail.com.

## Roadmap

1. Add the consistency (specification-vs-code) results.
2. Extend the correctness tests with boundary and abnormal-case coverage.
3. Add performance and correctness results for the 35 hash algorithms
   (reference implementations first).
4. Add correctness and performance results for all `opt/` and `add/`
   implementations.
5. Add memory and stack-usage measurements.
6. Add timing controls (CPU frequency locking, core pinning, warm-up) and
   document them in the measurement notes.
