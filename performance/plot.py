# -*- coding: utf-8 -*-
"""Generate per-security-level performance figures.

Usage:  python plot.py
Output: figures/levels/level-{128,160,192,256,384,512}.png
Requires: matplotlib (pip install matplotlib)
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator, NullLocator, LogLocator, NullFormatter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "pkc", "ref")
OUT = os.path.join(HERE, "figures", "levels")

TRACKS = {
    "KEM": {
        "ops": ["keygen", "encap", "decap"],
        "primary": ("encap", "decap"),
        "primary_label": "encap + decap",
        "size": ("pk_bytes", "ct_bytes"),
        "size_label": "pk + ct",
    },
    "DSA": {
        "ops": ["keygen", "sign", "verify"],
        "primary": ("sign",),
        "primary_label": "sign",
        "size": ("pk_bytes", "sn_bytes"),
        "size_label": "pk + sn",
    },
    "KEX": {
        "ops": ["init_a", "init_b", "exchange_total"],
        "primary": ("exchange_total",),
        "primary_label": "exchange",
        "size": ("pk_bytes", "total_msg_bytes"),
        "size_label": "pk + total_msg",
    },
}
TRACK_COLORS = {"KEM": "#0072B2", "DSA": "#D55E00", "KEX": "#009E73"}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#999999",
    "axes.grid": True,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
})


def load(track):
    rows = []
    with open(os.path.join(REF, track + ".csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r["level"] = r.get("classical_security_level", "")
            try:
                r["samples_n"] = int(r.get("samples", "0") or 0)
            except ValueError:
                r["samples_n"] = 0
            rows.append(r)
    return rows


def time_unit(vmax):
    if vmax >= 1e9:
        return 1e9, "s"
    if vmax >= 1e6:
        return 1e6, "ms"
    if vmax >= 1e3:
        return 1e3, "µs"
    return 1.0, "ns"


def size_unit(vmax):
    if vmax >= 1e6:
        return 1e6, "MB"
    if vmax >= 1e3:
        return 1e3, "KB"
    return 1.0, "B"


def fmt_tick(v, div):
    x = v / div
    if x == 0:
        return "0"
    if x >= 1000:
        return f"{x:,.0f}"
    if x >= 10:
        return f"{x:.0f}"
    if x >= 1:
        return f"{x:g}"
    if x >= 0.001:
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return f"{x:.1e}"


def fmt_value(x):
    if x >= 100:
        return f"{x:,.0f}"
    if x >= 1:
        return f"{x:.1f}"
    if x >= 0.01:
        return f"{x:.3f}".rstrip("0").rstrip(".")
    return f"{x:.4f}"


def metric(r, cfg):
    return sum(float(r[o + "_median_ns"]) for o in cfg["primary"])


def size_of(r, cfg):
    return sum(float(r[f]) for f in cfg["size"])


def rank(rows, track, level, kind):
    cfg = TRACKS[track]
    sub = [r for r in rows if r["level"] == str(level)]
    if kind == "perf":
        sub = [r for r in sub if r["samples_n"] >= 3
               and all(r.get(o + "_median_ns") for o in cfg["primary"])]
        value = lambda r: metric(r, cfg)
    else:
        sub = [r for r in sub if all(r.get(f) for f in cfg["size"])]
        value = lambda r: size_of(r, cfg)
    best = {}
    for r in sub:
        pkg = r["package"]
        if pkg not in best or value(r) < value(best[pkg]):
            best[pkg] = r
    data = sorted(best.values(), key=value)[:10]
    return data, [value(r) for r in data]


def draw_rank(ax, data, vals, title, kind, color, cfg):
    if not data:
        ax.axis("off")
        ax.text(0.5, 0.5, "no data", ha="center", va="center", fontsize=9, color="#777777")
        return
    has_outlier = len(vals) > 1 and vals[-1] > 10 * vals[-2]
    labels = []
    for r in data:
        lab = f"{r['package']} / {r['param_set']}"
        if len(lab) > 26:
            lab = lab[:23] + "…"
        labels.append(lab)
    y = np.arange(len(data))
    bar_h = 0.22 if len(data) <= 3 else 0.6
    vmax = max(vals)
    if kind == "perf":
        div, unit = time_unit(vmax)
        xlabel = f"Median time ({unit})"
    else:
        div, unit = size_unit(vmax)
        xlabel = f"{title.split(' — ')[-1]} ({unit})"

    if has_outlier:
        lo = min(vals) * 0.3
        ax.set_xscale("log")
        ax.barh(y, [v - lo for v in vals], left=lo, height=bar_h,
                color=color, edgecolor="white", linewidth=0.5, zorder=3)
        ax.set_xlim(lo, vmax * 1.8)
        ax.set_xlabel(xlabel + ", log scale")
        ax.xaxis.set_major_locator(LogLocator(base=10, numticks=6))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _, d=div: fmt_tick(v, d)))
        ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
        ax.xaxis.set_minor_formatter(NullFormatter())
        for yi, v in zip(y, vals):
            ax.text(v * 1.07, yi, f"{fmt_value(v / div)} {unit}",
                    va="center", fontsize=7.2, color="#333333")
    else:
        ax.barh(y, vals, height=bar_h, color=color, edgecolor="white",
                linewidth=0.5, zorder=3)
        ax.set_xscale("linear")
        ax.set_xlim(0, vmax * (2.5 if len(data) == 1 else 1.15))
        ax.set_xlabel(xlabel)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _, d=div: fmt_tick(v, d)))
        ax.xaxis.set_minor_locator(NullLocator())
        for yi, v in zip(y, vals):
            ax.text(v + vmax * 0.015, yi, f"{fmt_value(v / div)} {unit}",
                    va="center", fontsize=7.2, color="#333333")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.5)
    ax.invert_yaxis()
    if len(data) <= 3:
        ax.set_ylim(len(data) - 0.3, -0.7)
    ax.set_title(title, loc="left", fontweight="bold")
    ax.grid(which="major", axis="x")


def by_level(rows_by_track):
    os.makedirs(OUT, exist_ok=True)
    levels = sorted({int(r["level"]) for rows in rows_by_track.values()
                     for r in rows if r["level"] and int(r["level"]) >= 128})
    for level in levels:
        perf_tracks = []
        size_tracks = []
        for track in ("KEM", "DSA", "KEX"):
            data, _ = rank(rows_by_track[track], track, level, "perf")
            if data:
                perf_tracks.append(track)
            cfg = TRACKS[track]
            if cfg["size"]:
                data, _ = rank(rows_by_track[track], track, level, "size")
                if data:
                    size_tracks.append(track)
        ncols = max(len(perf_tracks), len(size_tracks), 1)
        fig = plt.figure(figsize=((7.0 if ncols == 1 else 5.4 * ncols), 8.2))
        gs = fig.add_gridspec(2, ncols, hspace=0.55, wspace=0.42)
        for i, track in enumerate(perf_tracks):
            ax = fig.add_subplot(gs[0, i])
            data, vals = rank(rows_by_track[track], track, level, "perf")
            cfg = TRACKS[track]
            draw_rank(ax, data, vals, f"{track} — {cfg['primary_label']}", "perf", TRACK_COLORS[track], cfg)
        for i, track in enumerate(size_tracks):
            ax = fig.add_subplot(gs[1, i])
            data, vals = rank(rows_by_track[track], track, level, "size")
            cfg = TRACKS[track]
            draw_rank(ax, data, vals, f"{track} — {cfg['size_label']}", "size", TRACK_COLORS[track], cfg)
        fig.suptitle(f"Classical security level: {level} bits", fontsize=15, fontweight="bold", y=0.98)
        fig.text(0.5, 0.015,
                 "Top: fastest. Bottom: smallest combined size. "
                 "One parameter set per algorithm; 1–2 sample probes excluded.",
                 ha="center", fontsize=6.8, color="#555555")
        fig.subplots_adjust(left=(0.30 if ncols == 1 else 0.12), right=0.985,
                            top=0.90, bottom=0.10, wspace=0.62, hspace=0.55)
        path = os.path.join(OUT, f"level-{level}.png")
        fig.savefig(path, dpi=220, facecolor="white")
        plt.close(fig)
        print("wrote", path)


def main():
    rows_by_track = {track: load(track) for track in TRACKS}
    by_level(rows_by_track)


if __name__ == "__main__":
    main()
