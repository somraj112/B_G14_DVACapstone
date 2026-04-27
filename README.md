# NST DVA Capstone 2 - Project Repository

> **Newton School of Technology | Data Visualization & Analytics**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Identifying High-Risk Road Conditions and Geographic Hotspots to Reduce Traffic Accident Severity Across the United States |
| **Sector** | Transportation / Public Safety |
| **Team ID** | B_G14 |
| **Section** | DVA-B |
| **Faculty Mentor** | _To be filled_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _To be filled_ |

### Team Members

| Role | GitHub Username |
|---|---|
| Project Lead | `AalokeCode` |
| Data Lead | `aryankinha` |
| ETL Lead | `aryankinha` |
| Analysis Lead | `punityadavrao` |
| Visualization Lead | `somraj112` |
| Strategy Lead | `bigXalok` |
| PPT and Quality Lead | `AalokeCode` |

---

## Business Problem

Road traffic accidents cause billions of dollars in infrastructure damage, emergency response costs, and productivity loss annually across the United States. Despite vast amounts of accident data being collected, safety resource allocation — road signage, traffic signal placement, emergency staffing — remains largely reactive rather than predictive. This project serves transportation planners, state DOTs, and public safety departments who need to prioritise where and when to deploy limited resources.

**Core Business Question**

> Which geographic locations, road conditions, and temporal patterns are most strongly associated with high-severity traffic accidents, and what actionable interventions can reduce accident severity?

**Decision Supported**

> This analysis enables transportation authorities to redirect infrastructure investment and emergency response staffing toward the highest-risk corridors, time windows, and weather conditions identified in the data.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Kaggle — US Accidents (Moosavi et al.) |
| **Direct Access Link** | https://kaggle.com/datasets/sobhanmoosavi/us-accidents |
| **Row Count** | 7,728,394 |
| **Column Count** | 46 (raw) · ~34 after cleaning |
| **Time Period Covered** | Feb 2016 – Mar 2023 |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `severity` | Traffic impact score 1 (low) – 4 (critical) | Primary target variable; all KPIs and stats |
| `start_lat` / `start_lng` | Accident GPS coordinates | Geographic hotspot mapping in Tableau |
| `state` / `city` | Administrative geography | Hotspot KPIs, segmentation, filters |
| `weather_condition` | Text label of weather at event time | Weather-severity chi-square test, dashboard filter |
| `start_time` | Accident timestamp | Derives hour, day, month, season, rush-hour flag |
| `duration_min` | Minutes traffic was blocked (derived) | Severity-weighted response staffing KPI |
| `junction` / `traffic_signal` / `crossing` | Infrastructure POI flags within ~150 m | Infrastructure odds-ratio analysis (logistic regression) |
| `is_rush_hour` | True if accident fell in 7–9 AM or 4–7 PM (derived) | Peak-hour staffing KPI |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| High-Severity Rate (%) | Share of accidents with severity ≥ 3 — the primary intervention target | `df['is_high_severity'].mean() * 100` — nb04 |
| Median Accident Duration by Severity (min) | How long traffic was blocked at each severity level — proxy for emergency response load | `df.groupby('severity')['duration_min'].median()` — nb04 |
| Geographic Hotspot Concentration | Top states and cities by accident count and high-severity rate | `df.groupby('state')['is_high_severity'].agg(['count','mean'])` — nb03 |
| Rush-Hour Accident Share (%) | % of all accidents occurring during peak commute windows | `df['is_rush_hour'].mean() * 100` — nb03 |
| YoY Accident Volume Growth Rate (%) | Year-over-year change in total accident count — tracks whether risk is increasing | `df.groupby('year').size().pct_change() * 100` — nb04 |
| Adverse-Weather High-Severity Rate | % of high-severity accidents under adverse weather — quantifies weather exposure risk | Chi-square test + conditional rate — nb04 |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | https://public.tableau.com/app/profile/somraj.nandi/viz/USARoadAccidentsIntelligence/Dashboard1 |
| **Executive View** | National KPI summary — total accidents, high-severity rate, top-5 states by volume |
| **Operational View** | Regional drill-down — city-level hotspots, severity heatmap, temporal breakdown |
| **Main Filters** | State, Severity Level, Weather Condition, Year |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **21.3% of accidents are high-severity (Sev 3+4).** Severity 2 dominates at 77.7%, but the 21.3% high-severity share drives disproportionate emergency costs and road clearance time — these are the priority intervention targets.
2. **Severity-4 accidents block traffic 2.9× longer than severity-1.** Median clearance is 130 min (Sev 4) vs 44.8 min (Sev 1). Emergency teams routed by severity level — not just volume — can reclaim thousands of person-hours annually.
3. **Junctions are the single most dangerous road feature.** Accidents near junctions average 0.107 higher severity than non-junction locations (logistic OR = 1.35, p < 0.001). Junction redesign offers the highest return on infrastructure spend.
4. **Traffic signals are the most protective intervention available.** Signal-present accidents average severity 2.086 vs 2.257 where signals are absent — a 7.6% severity reduction. Logistic OR = 0.47 confirms signals nearly halve the odds of a high-severity outcome.
5. **Weather condition significantly determines severity (χ² = 3527.80, p ≈ 0).** Adverse conditions (snow, heavy rain, fog) carry systematically higher severity than clear weather — weather-responsive speed limits and variable message signs are statistically justified.
6. **Railway crossings carry the highest severity uplift of all POIs (OR = 1.44).** Despite low accident volume, railway-proximate accidents are 44% more likely to be high-severity — most are unprotected or poorly lit.
7. **Weekend accidents are 19% more likely to be high-severity (OR = 1.19, p < 0.001).** Higher-speed and off-peak driving behaviour shifts the severity profile upward on weekends, requiring weekend-specific patrol deployment.
8. **Nighttime accidents are measurably more severe (2.238) than daytime (2.227).** While the gap appears small in absolute terms, across millions of accidents this translates to thousands of additional high-severity events attributable to lighting deficit.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | Junctions = OR 1.35 for high-severity | Prioritise junction redesign (roundabouts, raised crosswalks) at top-50 high-frequency, high-severity intersections | Estimated 10–15% reduction in severe junction accidents |
| 2 | Traffic signals OR = 0.47 (protective) | Expand signal deployment at uncontrolled high-volume intersections in top-10 hotspot cities | 7–8% severity reduction per intersection; scalable across thousands of sites |
| 3 | Railway OR = 1.44, highest POI risk | Upgrade all unsignalised railway crossings in high-accident corridors with active warning systems and lighting | Targets the highest-severity-per-event POI class |
| 4 | Weather × severity: p ≈ 0 | Deploy weather-responsive variable speed limits and real-time advisory signs on high-volume corridors with frequent adverse conditions | Reduces weather-amplified severity; aligns with existing MUTCD guidance |
| 5 | Severity-4 clearance = 130 min | Implement severity-tiered emergency response staging — pre-position heavy-response units in Sev 3/4-dominant corridors during peak risk windows (rush hour, winter weekends) | Potential to cut Sev-4 clearance time by 20–30 min per event |

---

## Repository Structure

```text
B_G14_DVACapstone/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   |-- 04_statistical_analysis.ipynb
|   `-- 05_final_load_prep.ipynb
|
|-- scripts/
|   `-- etl_pipeline.py
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- README.md
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Recommended Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Is the business question clear and well-scoped? |
| Data Quality and ETL | 15 | Is the cleaning pipeline thorough and documented? |
| Analysis Depth | 25 | Are statistical methods applied correctly with insight? |
| Dashboard and Visualization | 20 | Is the Tableau dashboard interactive and decision-relevant? |
| Business Recommendations | 20 | Are insights actionable and well-reasoned? |
| Storytelling and Clarity | 10 | Is the presentation professional and coherent? |
| **Total** | **100** | |

> Marks are awarded for analytical thinking and decision relevance, not chart quantity, visual decoration, or code length.

---

## Submission Checklist

**GitHub Repository**

- [x] Public repository created with the correct naming convention (`B_G14_DVACapstone`)
- [x] All notebooks committed in `.ipynb` format
- [x] `data/raw/` contains the original, unedited dataset (`US_Accidents_March23.csv`)
- [x] `data/processed/` contains the cleaned pipeline output (`cleaned_dataset.csv`)
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains the Tableau Public URL
- [x] `docs/data_dictionary.md` is complete
- [x] `README.md` explains the project, dataset, and team
- [x] All members have visible commits and pull requests

**Tableau Dashboard**

- [x] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] Cover page, executive summary, sector context, problem statement
- [ ] Data description, cleaning methodology, KPI framework
- [x] EDA with written insights, statistical analysis results (notebooks 03 and 04 complete)
- [ ] Dashboard screenshots and explanation
- [ ] 8-12 key insights in decision language
- [ ] 3-5 actionable recommendations with impact estimates
- [ ] Contribution matrix matches GitHub history

**Presentation Deck**

- [ ] Final presentation exported as PDF into `reports/`
- [ ] Title slide through recommendations, impact, limitations, and next steps

**Individual Assets**

- [ ] DVA-oriented resume updated to include this capstone
- [ ] Portfolio link or project case study added

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| AalokeCode | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| aryankinha | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| punityadavrao | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| somraj112 | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| bigXalok | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** AalokeCode

**Date:** _To be filled_

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
