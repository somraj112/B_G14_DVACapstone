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
| Visualization Lead | `somraj` _(username TBD)_ |
| Strategy Lead | `alok` _(username TBD)_ |
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
| **Dashboard URL** | _To be published_ |
| **Executive View** | _To be filled_ |
| **Operational View** | _To be filled_ |
| **Main Filters** | _To be filled_ |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

_To be filled after analysis is complete._

1. _Insight 1_
2. _Insight 2_
3. _Insight 3_
4. _Insight 4_
5. _Insight 5_
6. _Insight 6_
7. _Insight 7_
8. _Insight 8_

---

## Recommendations

_To be filled after analysis is complete._

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 2 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 3 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |

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

- [ ] Public repository created with the correct naming convention (`SectionName_TeamID_ProjectName`)
- [ ] All notebooks committed in `.ipynb` format
- [ ] `data/raw/` contains the original, unedited dataset
- [ ] `data/processed/` contains the cleaned pipeline output
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains the Tableau Public URL
- [ ] `docs/data_dictionary.md` is complete
- [ ] `README.md` explains the project, dataset, and team
- [ ] All members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] Cover page, executive summary, sector context, problem statement
- [ ] Data description, cleaning methodology, KPI framework
- [ ] EDA with written insights, statistical analysis results
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
| somraj _(TBD)_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| alok _(TBD)_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** AalokeCode

**Date:** _To be filled_

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
