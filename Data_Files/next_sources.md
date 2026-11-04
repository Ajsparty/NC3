# Priority Next Data Sources

Short notes on high-value sources flagged in partner discussions and notebooks. Add extracts to `Data_Files/` and update `source_catalog.csv` when acquired.

## Quarterly Workforce Indicators (QWI)

- **Publisher:** Census LEHD  
- **Use:** More granular or more recent job-flow and wage data by industry and firm age; complements QCEW and LODES.  
- **Access:** https://lehd.ces.census.gov/data/qwi/  
- **Geography:** County (Ingham, Eaton, Clinton)  
- **Notes:** Michigan coverage may lag; check latest available vintage before download.

## Post-Secondary Employment Outcomes (PSEO)

- **Publisher:** Census (via LEHD)  
- **Use:** MSU graduate employment and earnings outcomes; addresses local hiring / retention for the university.  
- **Access:** https://lehd.ces.census.gov/data/pseo/  
- **Notes:** Institution-level; useful stand-in for MSU local employment contribution beyond IPEDS headcount.

## USASpending.gov

- **Publisher:** U.S. Treasury  
- **Use:** Federal awards footprint for MSU, state agencies, and local entities (contracts, grants, loans).  
- **Access:** https://www.usaspending.gov/  
- **Notes:** Filter by recipient location (Ingham/Eaton/Clinton) or recipient name (Michigan State University, etc.). Export CSV; document fiscal year.

## HUD CHAS

- **Publisher:** HUD (Comprehensive Housing Affordability Strategy)  
- **Use:** Housing cost burden and affordability detail to complement ACS rent burden (B25070).  
- **Access:** https://www.huduser.gov/portal/datasets/cp.html  
- **Geography:** County / place  
- **Notes:** 5-year periods; useful for neighborhood mismatch framing.

## Opportunity Atlas

- **Publisher:** Opportunity Insights / Census  
- **Use:** Tract-level mobility measures (childhood income rank → adult outcomes) for mismatch analysis.  
- **Access:** https://www.opportunityatlas.org/  
- **Notes:** Download tract CSV; join to `acs_tract_2020_2024.csv` on GEOID.
