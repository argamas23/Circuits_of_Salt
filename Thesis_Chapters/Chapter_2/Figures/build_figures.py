"""Export Chapter 2 figures from the source extracts and checked historical accounts."""

import ast
import csv
import json
import textwrap
from pathlib import Path

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import FuncFormatter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
EXTRACTS = OUT / "source_extracts"
INK, BLUE, PALE, RUST = "#242424", "#294d60", "#e8eff2", "#945234"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "pdf.fonttype": 42, "svg.fonttype": "none", "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.facecolor": "white"})
exports = []


def sheet(title, subtitle, source, size=(10, 7)):
    fig = plt.figure(figsize=size)
    fig.text(.065, .94, title, fontsize=18, weight="bold", color=INK, va="top")
    fig.text(.065, .882, subtitle, fontsize=10.5, color="#555555", va="top")
    fig.text(.065, .045, source, fontsize=8.5, color="#505050", va="bottom", linespacing=1.5)
    return fig


def save(fig, stem):
    for ext in ("png", "pdf", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}", dpi=300)
    exports.append(stem)
    plt.close(fig)


def box(ax, x, y, width, height, text, color=PALE):
    ax.add_patch(Rectangle((x, y), width, height, facecolor=color,
                           edgecolor="#8d9ca4", linewidth=.8))
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=11)


def arrow(ax, a, b, label="", both=False, offset=.017):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="<->" if both else "->",
                                mutation_scale=13, linewidth=1.3, color=BLUE))
    if label:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + offset, label,
                ha="center", va="bottom", fontsize=9, color=BLUE)


# Reuse the project's place coordinates without executing its plotting script.
tree = ast.parse((ROOT / "Bibliography/Diagrams/maps/build_himalayan_salt_trade_map.py").read_text())
places = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
                              and any(isinstance(t, ast.Name) and t.id == "PLACES" for t in n.targets)))
geo = json.loads((ROOT / "Bibliography/Diagrams/maps/ne_110m_admin_0_countries.geojson").read_text())
fig = sheet("Places and regions discussed in Chapter 2",
            "Ladakh–Rupshu core and the Mandi, Kinnaur and Garhwal comparisons",
            "Source: project place coordinates; Natural Earth 1:110m basemap.\n"
            "Modern outlines provide orientation. No historical routes or trade volumes are represented.", (10, 8))
ax = fig.add_axes([.09, .16, .82, .65])
for feature in geo["features"]:
    geometry = feature["geometry"]
    if geometry["type"] not in ("Polygon", "MultiPolygon"):
        continue
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    for polygon in polygons:
        xs, ys = zip(*polygon[0])
        if max(xs) < 74.7 or min(xs) > 82.5 or max(ys) < 29.7 or min(ys) > 35.2:
            continue
        ax.fill(xs, ys, facecolor="#f4f3ed", edgecolor="#c4c4bc", linewidth=.75)
labels = {
    "Leh": (.15, .17), "Padum / Zanskar": (-1.13, .05), "Tso Kar": (.16, -.05),
    "Mandi": (-.65, -.16), "Rampur Bushahr": (-1.10, -.28), "Joshimath": (-.1, -.25),
    "Mana Pass": (-.98, .15), "Niti Pass": (.15, -.02), "Shipki La": (.14, .08),
    "Gartok": (.14, -.04), "Srinagar": (.14, -.10),
}
for name, (dx, dy) in labels.items():
    lon, lat, kind = places[name]
    marker = "^" if kind == "pass" else "D" if kind == "salt" else "o"
    ax.scatter(lon, lat, marker=marker, s=42, color=RUST if name == "Tso Kar" else BLUE, zorder=4)
    ax.annotate(name.replace("Padum / Zanskar", "Padum"), (lon, lat),
                xytext=(lon + dx, lat + dy), fontsize=10, color=INK,
                bbox={"facecolor": "white", "alpha": .83, "edgecolor": "none", "pad": 1}, zorder=5)
for label, lon, lat in [("LADAKH", 77.3, 34.82), ("RUPSHU", 78.15, 32.92),
                        ("ZANSKAR", 75.95, 33.05), ("KINNAUR", 77.75, 32.40),
                        ("GARHWAL", 79.25, 30.05), ("WESTERN TIBET", 80.8, 33.0)]:
    ax.text(lon, lat, label, fontsize=10, color="#777368", fontstyle="italic", zorder=3)
ax.set(xlim=(74.7, 82.5), ylim=(29.7, 35.2), xlabel="Longitude (°E)", ylabel="Latitude (°N)")
ax.set_aspect(1 / .845)
ax.grid(color="#deded8", linewidth=.5, alpha=.6)
ax.annotate("N", xy=(82.03, 34.60), xytext=(82.03, 34.15), ha="center",
            arrowprops={"arrowstyle": "->", "color": INK}, weight="bold")
ax.plot([75.03, 76.09], [30.10, 30.10], color=INK, linewidth=2)
ax.text(75.56, 30.18, "≈100 km at 32°N", ha="center", fontsize=8)
save(fig, "01_study_regions_map")


fig = sheet("Salt circulation took different regional forms",
            "Source-based schematics: cases and periods remain separate",
            "Sources: Walton (1910), pp. 42–45; Ahmed (1999), pp. 32–36; Kanum survey, pp. 113–114;\n"
            "Emerson (1920), pp. 160–164. Arrows show selected relations, not measured trade volumes.", (11, 9))
ax = fig.add_axes([.065, .12, .87, .69]); ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
rows = [(.80, "GARHWAL", "Walton’s 1910 account"), (.55, "RUPSHU", "Earlier journeys / later supply change"),
        (.30, "KANUM–RAMPUR", "Household accounts; 1964 revisit"), (.05, "MANDI", "Quarry and fiscal administration")]
for y, title, period in rows:
    ax.text(0, y + .165, title, weight="bold", fontsize=11, color=RUST)
    ax.text(.25, y + .165, period, fontsize=9.5, color="#666666")
    ax.axhline(y + .20, color="#cccccc", linewidth=.6)
box(ax, .00, .83, .19, .09, "Tibetan marts")
box(ax, .30, .83, .18, .09, "Mana / Niti")
box(ax, .60, .83, .18, .09, "Upper Garhwal")
box(ax, .83, .83, .17, .09, "Southern\nmarkets")
arrow(ax, (.195, .875), (.295, .875), "seasonal access", both=True)
arrow(ax, (.485, .875), (.595, .875), "local distribution", both=True)
arrow(ax, (.785, .875), (.825, .875), both=True)
ax.text(0, .792, "Salt/borax imports; grain exchange; sheep/goat transport and winter selling", fontsize=9.5)
box(ax, 0, .58, .20, .09, "Tibetan lakes")
box(ax, .35, .58, .18, .09, "Rupshu")
box(ax, .75, .58, .25, .09, "Zanskar")
arrow(ax, (.205, .625), (.345, .625), "salt")
arrow(ax, (.535, .625), (.745, .625), "salt / barley", both=True)
ax.text(0, .542, "Later: reliance shifted towards Tso Kar after the early 1960s; routes changed unevenly.", fontsize=9.5)
box(ax, 0, .33, .22, .09, "Rampur merchants")
box(ax, .39, .33, .23, .09, "Kanum trading\nhouseholds")
box(ax, .79, .33, .21, .09, "Tibetan markets")
arrow(ax, (.225, .400), (.385, .400), "credit / supplies")
arrow(ax, (.385, .350), (.225, .350), "return sales", offset=-.034)
arrow(ax, (.625, .400), (.785, .400), "outward goods")
arrow(ax, (.785, .350), (.625, .350), "wool / pashm / salt", offset=-.034)
ax.text(0, .292, "Return goods included wool, pashm and salt; hired labour and creditor ties shaped journeys.", fontsize=9.5)
box(ax, 0, .08, .20, .09, "Salt quarries")
box(ax, .36, .08, .24, .09, "Weighing and\nconsignment records")
box(ax, .79, .08, .21, .09, "Traders")
arrow(ax, (.205, .125), (.355, .125), "supply")
arrow(ax, (.605, .125), (.785, .125), "salt consignments")
ax.text(0, .041, "Distinct fiscal relation: receipts divided between Mandi and British authorities.", fontsize=9.5)
save(fig, "02_regional_circuits")


fig = sheet("Salt extraction and pack-animal transport at Tso Kar",
            "Two photographs from Ahmed’s study of Rupshu",
            "Source: Ahmed (1999), figs 1 and 4, printed pp. 34–35; local PDF p. 2.\n"
            "Original photographs cropped from the page scan; no image reconstruction. Exposure dates unconfirmed.", (10, 6))
for pos, filename, title in [([.065, .22, .415, .54], "ahmed_salt_extraction.png", "(a) Carrying salt to the shore"),
                             ([.52, .22, .415, .54], "ahmed_salt_caravan.png", "(b) Sheep and goats carrying salt")]:
    ax = fig.add_axes(pos); ax.imshow(plt.imread(EXTRACTS / filename), cmap="gray"); ax.axis("off")
    ax.text(0, -.08, title, transform=ax.transAxes, fontsize=10, va="top")
save(fig, "03_tso_kar_extraction_and_transport")


fig = sheet("Trading at Lavi, Rampur",
            "Wool and pashm transactions in the Kanum village survey’s photographic plates",
            "Source: Census of India, Kanum village survey, unnumbered plates, PDF pp. 139 and 149.\n"
            "Embedded photographs extracted unchanged. Exact exposure dates and individual image credits unconfirmed.", (10, 8))
for pos, filename, title in [([.065, .23, .49, .57], "kanum_wool_trading.jpeg", "(a) Wool trading"),
                             ([.60, .20, .335, .61], "kanum_pashm_purchase.jpeg", "(b) Pashm purchasing")]:
    ax = fig.add_axes(pos); ax.imshow(plt.imread(EXTRACTS / filename), cmap="gray"); ax.axis("off")
    ax.text(0, -.065, title, transform=ax.transAxes, fontsize=10, va="top")
save(fig, "04_lavi_wool_and_pashm")


accounts = [("1915–16", 67799, 12303, 55496), ("1916–17", 96606, 22463, 74143),
            ("1917–18", 101839, 19157, 82682), ("1918–19", 96385, 21904, 74481)]
assert all(income - expense == surplus for _, income, expense, surplus in accounts)
with (OUT / "mandi_quarry_accounts.csv").open("w", newline="") as handle:
    writer = csv.writer(handle); writer.writerow(["Financial year", "Income (Rs)", "Expenditure (Rs)", "Surplus (Rs)"])
    writer.writerows(accounts)
fig = sheet("Mandi salt-quarry accounts, 1915–19",
            "Recorded income divided into expenditure and surplus under direct state management",
            "Source: Emerson (1920), p. 160; local 1996 reprint, PDF p. 173. Nominal historical rupees.\n"
            "These are official financial accounts, not production volumes or measures of workers’ welfare.")
ax = fig.add_axes([.12, .20, .80, .60])
x = list(range(4)); expenditure = [r[2] for r in accounts]; surplus = [r[3] for r in accounts]
ax.bar(x, expenditure, color="#bac6cc", width=.55, label="Expenditure")
ax.bar(x, surplus, bottom=expenditure, color=BLUE, width=.55, label="Surplus")
for i, (_, income, expense, remainder) in enumerate(accounts):
    ax.text(i, income + 2000, f"{income:,}", ha="center", fontsize=11, weight="bold")
    ax.text(i, expense / 2, f"{expense:,}", ha="center", va="center", fontsize=10)
    ax.text(i, expense + remainder / 2, f"{remainder:,}", ha="center", va="center", fontsize=10, color="white")
ax.set(xticks=x, xticklabels=[r[0] for r in accounts], ylim=(0, 118000), ylabel="Rupees", xlabel="Financial year")
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.set_axisbelow(True); ax.grid(axis="y", color="#dddddd", linewidth=.6)
ax.legend(frameon=False, loc="upper left", ncols=2)
save(fig, "05_mandi_quarry_finances")


fig = sheet("Mandi salt-quarry income, expenditure and surplus",
            "Four financial years under direct state management",
            "Source: Emerson (1920), printed p. 160; local 1996 reprint, PDF p. 173.\n"
            "Transcribed from the page image. Original account categories retained; digit grouping standardised.", (10, 5.3))
ax = fig.add_axes([.065, .25, .87, .48]); ax.axis("off")
table = ax.table(cellText=[[year, f"{inc:,}", f"{exp:,}", f"{sur:,}"] for year, inc, exp, sur in accounts],
                 colLabels=["Financial year", "Income (Rs)", "Expenditure (Rs)", "Surplus (Rs)"],
                 cellLoc="right", colLoc="right", bbox=[0, 0, 1, 1])
table.auto_set_font_size(False); table.set_fontsize(12)
for (r, c), cell in table.get_celld().items():
    cell.set_linewidth(.5); cell.set_edgecolor("#c5ced2")
    if r == 0: cell.set_facecolor(BLUE); cell.set_text_props(color="white", weight="bold")
    elif r % 2: cell.set_facecolor("#f0f4f5")
    if c == 0: cell.set_text_props(ha="left")
save(fig, "06_mandi_accounts_table")


sources = [
    ("Gazetteers", "Routes, commodities, labour and fiscal arrangements", "Administrative priorities; publication date differs from event date"),
    ("Travel accounts", "Landscape, accessibility and observations along journeys", "An observed resource does not establish its market destination"),
    ("Treaty reproductions", "Prescribed privileges and obligations", "Prescription differs from practice; cited clauses do not name salt"),
    ("Village surveys", "Households, credit, occupations and local changes", "Selected cases; distinguish survey and revisit dates"),
    ("Fair accounts", "Participants and goods at a particular gathering", "A fair observation is not a regional trade census"),
    ("Ethnography", "Extraction, transport, memories and interpretations", "Separate field observation from recollection and disputed accounts"),
]
fig = sheet("Reading the chapter’s documentary evidence",
            "What each source type contributes, and what it cannot establish alone",
            "Author’s synthesis of §2.2: Walton; Emerson; Mamgain; Thomson; Tingmosgang treaty reproduction;\n"
            "Kanum and Nachar surveys; Lavi fair account; Ahmed. This is not the computational corpus inventory.", (11, 8))
ax = fig.add_axes([.065, .16, .87, .64]); ax.axis("off")
widths = [.20, .38, .42]
wrapped = [[textwrap.fill(row[0], 17), textwrap.fill(row[1], 33), textwrap.fill(row[2], 37)] for row in sources]
table = ax.table(cellText=wrapped, colLabels=["Source type", "Useful evidence", "Limit to preserve"],
                 colWidths=widths, cellLoc="left", colLoc="left", bbox=[0, 0, 1, 1])
table.auto_set_font_size(False); table.set_fontsize(10.5)
for (r, c), cell in table.get_celld().items():
    cell.set_linewidth(.5); cell.set_edgecolor("#c5ced2"); cell.PAD = .06
    if r == 0: cell.set_facecolor(BLUE); cell.set_text_props(color="white", weight="bold")
    elif r % 2: cell.set_facecolor("#f0f4f5")
save(fig, "07_documentary_sources_table")


with fitz.open() as pack:
    for stem in exports:
        with fitz.open(OUT / f"{stem}.pdf") as document:
            assert len(document) == 1
            pack.insert_pdf(document)
    pack.save(OUT / "Chapter_2_Figures_and_Tables.pdf")
assert len(exports) == 7
print("Exported seven items as PNG, PDF and SVG, plus a seven-page combined PDF.")
print("Mandi accounts: all four income − expenditure = surplus checks passed.")
