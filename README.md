# Spatiotemporal Analysis of Insecurity in Nigeria 🇳🇬

This repository tracks the data gathering and cleaning pipeline for the CPE Club Week 09 Security Analysis project.

# Objectives🎯

The project aims to:

•Analyze the geographical distribution of insecurity incidents across Nigeria.

•Examine temporal trends in security incidents.

•Identify regions experiencing the highest levels of insecurity.

•Visualize findings using charts and graphs.

•Provide data-driven insights that support understanding of insecurity patterns.



# Team Members👥

Member| Responsibility

Chioma| Data Gathering

Anthony| Data Cleaning

Joshua| Data Analysis & Visualization

Goodluck| Documentation & GitHub

Miracle| Presentation & Social Media

Chinonso| Project Integration (Team Lead)

## Stage 3 & 4: Data Pipeline Architecture

Below is the logical flow of how we fetch the raw ACLED conflict data using the `requests` module and clean it using `pandas`.

```mermaid
graph TD
    A([Start Pipeline]) --> B[HTTP GET Request: requests.get]
    B --> C{Status Code == 200?}
    
    C -- No --> D[Log Error & Terminate Program]
    C -- Yes --> E[Save Data Locally: raw_conflict_data.csv]
    
    E --> F[Initialize Pandas: pd.read_csv]
    
    subgraph Data Cleaning Pipeline
        F --> G[1. Drop missing State/LGA rows]
        G --> H[2. Cast 'fatalities' to integers]
        H --> I[3. Standardize State names]
        I --> J[4. Parse 'event_date' to Datetime]
    end
    
    J --> K[Export Clean Data: cleaned_conflict_data.csv]
    K --> L([End Pipeline])

    %% Styling
    style A fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style L fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style C fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style D fill:#F44336,stroke:#D32F2F,stroke-width:2px,color:#fff
```