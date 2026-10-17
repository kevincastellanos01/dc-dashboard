# Data

La visión general del proyecto está en [README.es.md](../README.es.md).

These tables are the dashboard's source of truth. Nothing in this folder is queried from a live API at runtime. Pages read the CSVs through `utils/data_loader.py`, and `data/sources.csv` is what each page prints under Sources.

Two kinds of files live here:

- **Case study.** Incident log, move/add/change requests, and the security checklist. These describe the fictional operator YucaCore.
- **Published snapshot.** Outage shares, the 2024 PUE average, Mexico facility counts, LATAM indicators, and the capacity outlook. The numbers are copied from the reports in `sources.csv`.

## Files

| File | Kind | What a row is |
| --- | --- | --- |
| `operations_benchmarks.csv` | Published | One cited outage statistic. `key` is the lookup id, `value` is the display text (`54%`, `Power issues`). |
| `operations_incidents.csv` | Case study | Incident count by category in the YucaCore log. |
| `operations_mac.csv` | Case study | One move, add, or change request. |
| `energy_reference.csv` | Published | PUE definition and the 2024 industry average. The average is the number the calculator compares against. |
| `security_checklist.csv` | Case study | One physical or governance control and a status of `Implemented` or `In Progress`. |
| `security_layers.csv` | Case study | One security layer, its primary control, and a qualitative risk level. |
| `market_mexico.csv` | Published snapshot | Facility count for one Mexico market. The page total is `sum(data_centers)`, 173 in this snapshot. Querétaro is 28. |
| `market_latam.csv` | Published snapshot | One 2025 LATAM indicator. `percent` is the unit for every row, which is why those three can share a chart. |
| `market_focus.csv` | Published snapshot | Country group named in the JLL Latin America report. |
| `emerging_capacity.csv` | Published snapshot | Global data-center capacity in GW for one year. Years are categories, not a continuous axis. |
| `emerging_signals.csv` | Published snapshot | One outlook figure. `unit` is `%`, `GW`, or `ratio`. Mixed units are why this file is a table, not a bar chart. |
| `sources.csv` | Citations | `page` is `operations`, `energy`, `market`, or `emerging`. The security page is a case checklist and has no external statistic. |

## Citations

| Page | Source | URL |
| --- | --- | --- |
| Operations | Uptime Institute, Annual Outage Analysis 2025 | https://intelligence.uptimeinstitute.com/resource/annual-outage-analysis-2025 |
| Operations | Uptime Institute, Annual Outage Analysis 2024 | https://uptimeinstitute.com/resources/research-and-reports/annual-outage-analysis-2024 |
| Energy | The Green Grid, Power Usage Effectiveness (PUE) | https://www.thegreengrid.org/node/372 |
| Energy, emerging tech | Uptime Institute, Global Data Center Survey 2024 | https://datacenter.uptimeinstitute.com/rs/711-RIA-145/images/2024.GlobalDataCenterSurvey.Report.pdf?version=0 |
| Market | JLL, Latin America Data Center Report, year-end 2025 | https://www.jll.com/en-us/insights/latin-america-data-center-report-year-end-2025 |
| Market | Cloudscene, Mexico market overview | https://cloudscene.com/market/data-centers-in-mexico/all |
| Emerging tech | JLL, 2026 Global Data Center Outlook | https://www.jll.com/en-us/insights/market-outlook/data-center-outlook |
| Emerging tech | JLL newsroom, sector outlook to about 200 GW | https://www.jll.com/en-us/newsroom/global-data-center-sector-to-nearly-double-to-200gw-amid-ai-infrastructure-boom |

Cloudscene is a live directory. The Mexico counts in git are the snapshot this dashboard ships, and they can drift from the live site. When you refresh `market_mexico.csv`, update the 173-facility assertion in `tests/test_data.py` in the same change. The same rule applies to the other published figures locked in that file.

The security checklist uses the vocabulary of ISO/IEC 27001 and ANSI/TIA-942. It is not a certification and it is not an audit result.
