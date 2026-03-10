import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

CSV_PATH = "CodeIE/codeie_experiment_matrix.csv"
df = pd.read_csv(CSV_PATH)

# ── Compute per-class std for each config ─────────────────────────────
records = []
for (gran, style, model), subset in df.groupby(["granularity", "style", "model"]):
    f1_cols = subset[[c for c in subset.columns if c.startswith("f1_")]].dropna(axis=1, how="all").columns
    for col in f1_cols:
        records.append({
            "granularity": gran, "style": style, "model": model,
            "class": col.replace("f1_", ""), "std": subset[col].std(),
            "mean": subset[col].mean(),
        })

stats = pd.DataFrame(records)

# ── Find most sensitive class per granularity (highest mean std across configs) ──
most_sensitive = (
    stats.groupby(["granularity", "class"])["std"]
    .mean()
    .reset_index()
    .sort_values("std", ascending=False)
    .groupby("granularity")
    .first()
)

print("Most prompt-sensitive class per granularity:")
for gran, row in most_sensitive.iterrows():
    print(f"  {gran}: {row['class']} (mean std = {row['std']:.4f})")

# ====================================================================
# PLOT 1: Scatter plot (context) — top 3 + bottom 3 labeled per config
# ====================================================================
fig1, axes = plt.subplots(1, 2, figsize=(20, 9))

for ax, gran in zip(axes, ["coarse", "fine"]):
    gran_stats = stats[stats["granularity"] == gran]
    highlight_cls = most_sensitive.loc[gran, "class"]

    all_points = []
    labeled_points = []

    for (style, model), grp in gran_stats.groupby(["style", "model"]):
        grp = grp.copy()
        grp["config"] = f"{style} / {model}"
        grp = grp.dropna(subset=["mean", "std"])
        all_points.append(grp)

        top3 = grp.nlargest(min(3, len(grp)), "std")
        bot3 = grp.nsmallest(min(3, len(grp)), "std")
        labeled_points.append(pd.concat([top3, bot3]).drop_duplicates())

    all_pts = pd.concat(all_points)
    labeled = pd.concat(labeled_points)

    sns.scatterplot(data=all_pts, x="mean", y="std", hue="config",
                    s=100, alpha=0.5, ax=ax, legend=(gran == "fine"))

    # Highlight the most sensitive class with a star
    highlight = all_pts[all_pts["class"] == highlight_cls]
    ax.scatter(highlight["mean"], highlight["std"], marker="*", s=400,
               c="red", zorder=10, edgecolors="black", linewidths=0.8,
               label=f"★ {highlight_cls}")

    # Labels — only for labeled points, deduplicated by class name
    seen = set()
    texts = []
    for _, row in labeled.iterrows():
        if row["class"] not in seen:
            seen.add(row["class"])
            t = ax.text(row["mean"], row["std"], row["class"], fontsize=8, alpha=0.85)
            texts.append(t)

    # Also label the highlighted class if not already
    if highlight_cls not in seen:
        r = highlight.iloc[0]
        t = ax.text(r["mean"], r["std"], highlight_cls, fontsize=9, weight="bold", color="red")
        texts.append(t)

    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="->", color="gray", lw=0.5),
                expand=(2.5, 2.5), force_text=(1.5, 1.5),
                force_points=(0.8, 0.8), iterations=300,
                only_move={"text": "xy", "static": "xy", "explode": "xy", "pull": "xy"})

    ax.set_title(f"{gran.capitalize()} — ★ Most Sensitive: {highlight_cls}", fontsize=13)
    ax.set_xlabel("Mean F1 Score", fontsize=11)
    ax.set_ylabel("Std Dev of F1 (Sensitivity)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, title_fontsize=9, title="Config")

fig1.suptitle("Prompt Sensitivity per Entity Class (CodeIE)", fontsize=15, y=1.01)
plt.tight_layout()
fig1.savefig("CodeIE/codeie_sensitivity_scatter.png", dpi=150, bbox_inches="tight")
print("Saved scatter plot")

# ====================================================================
# PLOT 2: 2×2 grid — most sensitive class's std per config
# ====================================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

for ax, gran in zip(axes2, ["coarse", "fine"]):
    cls_name = most_sensitive.loc[gran, "class"]
    gran_data = stats[(stats["granularity"] == gran) & (stats["class"] == cls_name)]

    x_labels = []
    vals = []
    colors = []
    for model in ["qwen2.5:7b", "qwen2.5-coder:7b"]:
        for style in ["NL", "PL"]:
            row = gran_data[(gran_data["model"] == model) & (gran_data["style"] == style.lower())]
            x_labels.append(f"{style}\n{model}")
            vals.append(row["std"].values[0] if len(row) > 0 else 0)
            colors.append("#4C72B0" if style == "NL" else "#55A868")

    bars = ax.bar(x_labels, vals, color=colors, edgecolor="white", width=0.6)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f"{val:.3f}", ha="center", va="bottom", fontsize=11, weight="bold")

    ax.set_title(f"{gran.capitalize()} — class: {cls_name}", fontsize=12)
    ax.set_ylabel("Std Dev of F1" if gran == "coarse" else "", fontsize=11)
    ax.grid(axis="y", alpha=0.3)

fig2.suptitle("Prompt Sensitivity of Most Volatile Entity Class", fontsize=14)
plt.tight_layout()
fig2.savefig("CodeIE/codeie_sensitivity_bars.png", dpi=150, bbox_inches="tight")
print("Saved bar chart")
