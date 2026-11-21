# Chapter 2: finished figures and tables

Open **Chapter_2_Figures_and_Tables.pdf** for the seven-page set. Each numbered item is also supplied separately as PNG, PDF and SVG. New diagrams, map, chart and tables were drawn for this chapter. Photographs were extracted from the original sources, rather than taken from the project's earlier figures.

| File | Suggested placement | Caption / source |
| --- | --- | --- |
| `01_study_regions_map` | §2.1, after defining the geographical scope | Places discussed in Chapter 2, distinguishing the Ladakh–Rupshu core from regional comparisons. Place coordinates reused from the project map; Natural Earth reference outlines. This locator map does not reconstruct historical boundaries or trading paths. |
| `02_regional_circuits` | End of §2.3, or at the transition into §2.4 | Selected arrangements of salt circulation in Garhwal, Rupshu, Kanum–Rampur and Mandi. Source-based schematics after Walton (1910), pp. 42–45; Ahmed (1999), pp. 32–36; Kanum survey, pp. 113–114; and Emerson (1920), pp. 160–164. Cases and periods are separate; arrows are not quantitative flows. |
| `03_tso_kar_extraction_and_transport` | §2.3, after the Rupshu supply-change paragraph | Salt extraction and transport at Tso Kar: carrying salt to the shore, and sheep and goats departing with salt. Reproduced from Ahmed (1999), figs 1 and 4, printed pp. 34–35; local PDF p. 2. Exact photographic dates and reproduction credit remain to be established. |
| `04_lavi_wool_and_pashm` | §2.3, beside the Lavi/Rampur discussion | Wool trading and pashm purchasing at Lavi, Rampur. Reproduced from the Kanum village survey's unnumbered plates, PDF pp. 139 and 149. Do not label these as salt transactions or identify their subjects as the chapter's named traders. Exact exposure dates and image credits are unconfirmed. |
| `05_mandi_quarry_finances` | §2.4, beside the direct-management discussion | Recorded Mandi quarry income divided into expenditure and surplus, 1915–19. Drawn from Emerson (1920), printed p. 160; local 1996 reprint, PDF p. 173. Values are nominal historical rupees, not quantities of salt. |
| `06_mandi_accounts_table` | Alternative to the chart in §2.4 | Mandi quarry income, expenditure and surplus under direct management. Transcribed from Emerson (1920), p. 160. All four surplus calculations checked. Editable values are in `mandi_quarry_accounts.csv`. |
| `07_documentary_sources_table` | End of §2.2 | Source types, uses and limits. Author's synthesis of the chapter's source discussion; this is not a list of sources already processed computationally. |

Choose either the Mandi chart or the accounts table for the chapter; the pair is supplied to give a choice of presentation. Photograph resolution is limited by the original scans. The individual extracts and their page references are preserved in `source_extracts/provenance.json`.

Kanum source: https://censusindia.gov.in/nada/index.php/catalog/31012/download/34193/23212_1961_KAN.pdf

The chapter's publication year for the Kanum survey differs from its catalogue record. Settle the edition when finalising the bibliography. The photos do not acquire an open reproduction licence through this extraction.

The thesis itself has not been changed. To regenerate the exports, run `python3 Thesis_Chapters/Chapter_2/Figures/build_figures.py` from the research root; it uses the preserved source extracts and installed Matplotlib/PyMuPDF.
