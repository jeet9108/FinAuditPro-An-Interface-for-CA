# 📊 FinAuditPro — System Architecture, DFD & Presentation Diagrams

This document contains all architectural diagrams, Data Flow Diagrams (DFD Level 0 & Level 1), physical deployment topology, and core workflow diagrams extracted directly from the official project presentation ([`FinAuditPro_FY_Presentation.pptx`](../../FinAuditPro_FY_Presentation.pptx)).

---

## 📑 Table of Contents
1. [Core Audit Pipeline Flow (Slide 5)](#1-core-audit-pipeline-flow)
2. [High-Level Layered Architecture (Slide 11)](#2-high-level-layered-architecture)
3. [System Design & Component Architecture (Slide 7)](#3-system-design--component-architecture)
4. [Data Flow Diagram (DFD Level 0) (Slide 8)](#4-data-flow-diagram-dfd-level-0)
5. [Data Flow Diagram (DFD Level 1) (Slide 9)](#5-data-flow-diagram-dfd-level-1)
6. [Deployment Topology Diagram (Slide 10)](#6-deployment-topology-diagram)
7. [Implemented Modules Catalog (Slide 13)](#7-implemented-modules-catalog)
8. [Module Screen Gallery (Slides 14–22)](#8-module-screen-gallery)

---

## 1. Core Audit Pipeline Flow

The end-to-end journey from raw financial records to signed statutory audit reports:

```mermaid
flowchart LR
    A["1. Ingest<br/>• CSV / XLSX / PDF<br/>• Validate & Classify<br/>• Local Parser"] --> B["2. Extract & Index<br/>• OCR & Table Extraction<br/>• Evidence Indexing<br/>• FAISS Vector Store"]
    B --> C["3. Analyse<br/>• Deterministic Rules<br/>• BRS & GST Recon<br/>• ML Anomaly Engine"]
    C --> D["4. AI Copilot<br/>• Local RAG Pipeline<br/>• LM Studio / Ollama<br/>• Risk Context & Notes"]
    D --> E["5. Report<br/>• Working Papers (SA 230)<br/>• Master PDF / Excel<br/>• QR Verification & Hash"]

    style A fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    style B fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    style C fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    style D fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    style E fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
```

* **Zero Data Leaks:** Everything stays on the local machine in SQLite. Zero cloud analytics.
* **Faster Audits:** Auditors skip manual ledger cross-checking and focus on professional judgment.
* **Balanced Workload:** Engagement planning, risk findings, and working paper sign-offs unified in one workspace.

---

## 2. High-Level Layered Architecture

```mermaid
flowchart TD
    subgraph PresentationLayer["Presentation Layer (HTML5 / CSS3 / ES6 Vanilla SPA)"]
        UI_Dash["Executive Dashboards"]
        UI_Forms["Data Grid & Ingestion Forms"]
        UI_Viewer["Report Viewer & Working Papers"]
    end

    subgraph AppLayer["Application Layer (Python / FastAPI / Uvicorn)"]
        Eng_Rule["Deterministic Statutory Rule Engine"]
        Eng_OCR["OCR & File Parsing Service"]
        Eng_Report["ReportLab PDF & Excel Generator"]
        Eng_Jobs["Background Task Scheduler"]
    end

    subgraph IntelLayer["Intelligence Layer (100% Local Offline AI)"]
        AI_Gate["Local AI Gateway & Context Boundary"]
        AI_Hybrid["Hybrid Audit Analysis & ML Outlier Scoring"]
        AI_Local["LM Studio / Local LLM Server (:1234)"]
    end

    subgraph DataLayer["Data Layer (Local Storage Only)"]
        DB_SQL[("SQLite 3 with WAL Mode")]
        DB_Audit[("SHA-256 Hash Chained Audit Trail")]
        Files_Evidence["Local Evidence Files & FAISS Store"]
    end

    PresentationLayer -->|REST JSON / Localhost| AppLayer
    AppLayer --> IntelLayer
    AppLayer --> DataLayer
    IntelLayer --> DataLayer

    style PresentationLayer fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px;
    style AppLayer fill:#e0f2f1,stroke:#00897b,stroke-width:2px;
    style IntelLayer fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px;
    style DataLayer fill:#fff8e1,stroke:#ffa000,stroke-width:2px;
```

---

## 3. System Design & Component Architecture

Comprehensive system components, micro-services, data flow, and audit intelligence layers:

![System Design Architecture](assets/presentation_diagrams/01_system_design_architecture.png)

```mermaid
flowchart TD
    Auditor["Chartered Accountant / Engagement Team"] -->|Desktop Browser| ClientApp["FinAuditPro Desktop Client"]
    
    subgraph CoreFrontend["Client Workspace"]
        ClientApp --> ViewAuth["Authentication & User Session"]
        ClientApp --> ViewClient["Client & Engagement Master"]
        ClientApp --> ViewLedgers["General Ledger & Trial Balance"]
        ClientApp --> ViewRecon["Bank Reconciliation & GST Portal"]
        ClientApp --> ViewFindings["Findings & Risk Scoring"]
        ClientApp --> ViewWP["Working Papers (SA 230)"]
    end

    CoreFrontend -->|HTTP / Localhost:8000| BackendFastAPI["FastAPI Backend Core"]

    subgraph BackendCore["FastAPI Backend Services"]
        BackendFastAPI --> AuthMiddleware["RBAC & Token Gatekeeper"]
        AuthMiddleware --> ParserService["File Parser & Data Cleaner"]
        AuthMiddleware --> TriEngine["Tri-Engine Forensic Core"]
        AuthMiddleware --> ReconService["Bank & GST Reconciliation"]
        AuthMiddleware --> PDFService["ReportLab PDF & QR Code Generator"]
    end

    subgraph StorageSecurity["Persistence & Audit Trail"]
        BackendCore --> LocalDB[("SQLite 3 WAL Engine")]
        BackendCore --> HashTrail[("Append-Only SHA-256 Audit Events")]
        BackendCore --> EncBackups["AES-128 Portable Encrypted Backups"]
    end

    BackendCore -.->|Local IPC / HTTP :1234| LocalLLM["LM Studio / Local AI LLM"]
```

---

## 4. Data Flow Diagram (DFD Level 0)

Context-level data flow between the external entity (Auditor/CA) and the FinAuditPro operating system:

![DFD Level 0](assets/presentation_diagrams/02_dfd_level_0.png)

```mermaid
flowchart LR
    Auditor["Chartered Accountant / Auditor"]

    subgraph System["FinAuditPro System (0.0)"]
        FAP["FinAuditPro<br/>Audit Operating System"]
    end

    Auditor -->|1. Credentials & Auth Request| FAP
    Auditor -->|2. Client Info & Engagement Scope| FAP
    Auditor -->|3. Trial Balances, Ledgers, Bank Stmts, GST Files| FAP
    Auditor -->|4. Audit Inquiries & Verification Notes| FAP

    FAP -->|5. Authentication Token & Session| Auditor
    FAP -->|6. Exception Registers & Anomaly Alerts| Auditor
    FAP -->|7. Bank & GST Reconciliation Summaries| Auditor
    FAP -->|8. AI Advisory Insights & Evidence Citations| Auditor
    FAP -->|9. Final Signed Audit Reports & Working Papers (PDF/XLSX)| Auditor
```

---

## 5. Data Flow Diagram (DFD Level 1)

Detailed breakdown of sub-processes, data stores, and intermediate flows:

![DFD Level 1](assets/presentation_diagrams/03_dfd_level_1.png)

```mermaid
flowchart TD
    Auditor(["Auditor / Article Assistant"])

    subgraph Process1["1.0 Authentication & Access Control"]
        P1["Verify Credentials & Role"]
    end

    subgraph Process2["2.0 Engagement & Client Management"]
        P2["Create & Scope Engagements"]
    end

    subgraph Process3["3.0 Ingestion & Data Sanitation"]
        P3["Ingest, Validate & Clean Files"]
    end

    subgraph Process4["4.0 Forensic Analysis & Rules Engine"]
        P4["Run Sec 40A(3), 269ST, Benford, ML Outliers"]
    end

    subgraph Process5["5.0 Reconciliation Engine"]
        P5["Reconcile Books vs Bank & GST 2B/3B"]
    end

    subgraph Process6["6.0 Local AI Copilot & Working Papers"]
        P6["Query Offline LLM & Draft SA 230 Notes"]
    end

    subgraph Process7["7.0 Reporting & Audit Trail"]
        P7["Generate PDF/Excel Reports & Log SHA-256 Event"]
    end

    %% Stores
    D1[("D1: Users & Permissions")]
    D2[("D2: Clients & Engagements")]
    D3[("D3: Transactions & Ledgers")]
    D4[("D4: Audit Findings & Exceptions")]
    D5[("D5: Working Papers & Sign-offs")]
    D6[("D6: Cryptographic Audit Trail")]

    %% Flows
    Auditor -->|Login Request| P1
    P1 <--> D1
    P1 -->|Session Token| Auditor

    Auditor -->|Client & Period Setup| P2
    P2 <--> D2

    Auditor -->|Upload Raw Excel/CSV/PDF| P3
    P3 --> D3

    D3 --> P4
    P4 --> D4
    D4 -->|Exceptions & Anomaly Flags| Auditor

    D3 --> P5
    P5 --> D4
    P5 -->|BRS / GST Variances| Auditor

    Auditor -->|Natural Language Inquiries| P6
    D4 --> P6
    P6 <--> D5
    P6 -->|Redacted Context Query| OfflineLLM["Local LM Studio (:1234)"]
    OfflineLLM -->|Advisory Explanation| P6

    D5 --> P7
    D4 --> P7
    P7 --> D6
    P7 -->|Master Audit PDF with QR Code| Auditor
```

---

## 6. Deployment Topology Diagram

Physical workstation deployment architecture showing local execution boundaries:

![Deployment Diagram](assets/presentation_diagrams/04_deployment_diagram.png)

```mermaid
flowchart TD
    subgraph Host["Auditor Host Workstation (Windows / macOS / Linux)"]
        subgraph BrowserEnv["User Workspace"]
            Browser["Default Web Browser<br/>(Chrome / Edge / Safari / Firefox)"]
        end

        subgraph RuntimeEnv["Python Runtime Environment (Port :8000)"]
            FastAPI["FastAPI / Uvicorn Server"]
            DomainLogic["Domain Logic & Statutory Rules"]
            MLCore["Scikit-Learn ML Anomaly Engine"]
            ReportGen["ReportLab PDF Engine"]
        end

        subgraph LocalAIServer["Local AI Service (Port :1234)"]
            LMStudio["LM Studio Daemon / Local Inference"]
            LocalModel["Loaded LLM: Qwen 2.5 Coder 14B / Llama 3.1 8B"]
        end

        subgraph LocalDisk["Host Filesystem Storage"]
            SQLiteFile[("finauditpro.db (SQLite WAL Mode)")]
            EvidenceFolder["Evidence Uploads & PDF Working Papers"]
            BackupsFolder["AES-128 Encrypted Backup Archives"]
        end
    end

    Browser <-->|HTTP / WebSocket (127.0.0.1:8000)| FastAPI
    FastAPI <--> DomainLogic
    DomainLogic <--> MLCore
    DomainLogic <--> ReportGen
    DomainLogic <-->|Loopback REST (127.0.0.1:1234)| LMStudio
    LMStudio <--> LocalModel
    DomainLogic <--> LocalDisk

    style Host fill:#fafafa,stroke:#37474f,stroke-width:2px;
    style BrowserEnv fill:#e3f2fd,stroke:#1976d2,stroke-width:1px;
    style RuntimeEnv fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px;
    style LocalAIServer fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px;
    style LocalDisk fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;
```

---

## 7. Implemented Modules Catalog

From Slide 13 of the Presentation:

| Cluster | Implemented Module | Description |
| :--- | :--- | :--- |
| **Core & Administration** | **Dashboard** | Executive financial metrics, risk breakdown & health scorecards |
| | **Clients** | Master client directory, PAN/GSTIN registration, legal entity structure |
| | **Engagements** | Fiscal year audit scoping, statutory mandate selection & assignments |
| | **Users & RBAC** | Role-based accounts (Admin, Auditor, Staff) with session protection |
| | **Settings** | Retention policies, local AI endpoints, and backup configurations |
| **Data & Ledgers** | **Import & Cleaning** | Multi-format CSV/Excel parser, column mapping, and error reporting |
| | **General Ledger** | Full transactional ledger viewer with filtering and sorting |
| | **Trial Balance** | Real-time mathematical debit-credit balance verification |
| | **Parties & Volumes** | Counterparty risk aggregation and transaction velocity tracking |
| **Analytics & Checks** | **Reconciliation** | Automated BRS (Bank Reconciliation) and GSTR-2B vs 3B comparisons |
| | **YoY Comparison** | Multi-period trend and analytical procedures (SA 520) |
| | **Duplicates & Gaps** | Exact/fuzzy duplicate detection and cheque/invoice sequence gaps |
| | **Anomaly Detection** | Benford's Law (MAD), Isolation Forest ML, and 3-Sigma Z-Scores |
| | **Financial Statements** | Balance Sheet, Profit & Loss, and Cash Flow statement synthesis |
| **Audit Output & AI** | **Findings** | Central exception register with quantified risk scores and remediation |
| | **Working Papers** | Electronic SA 230 workpapers with evidence attachments & maker-checker |
| | **Checklist** | 15-category dynamic workprograms tailored to legal entity & risk |
| | **Reports** | Master statutory PDF report generation with verification QR codes |
| | **AI Assistant** | Air-gapped natural language auditor Q&A assistant |
| | **Audit Trail** | Append-only sequential SHA-256 hash chained event log |

---

## 8. Module Screen Gallery

High-resolution visual representations of the application views:

| Module View | Presentation Slide | Screenshot Artifact |
| :--- | :---: | :--- |
| **Executive Audit Dashboard** | Slide 14 | ![Dashboard](assets/presentation_diagrams/05_ui_module_01.png) |
| **Client & Engagement Master** | Slide 15 | ![Clients](assets/presentation_diagrams/06_ui_module_02.png) |
| **Trial Balance & Ledger Verification** | Slide 16 | ![Trial Balance](assets/presentation_diagrams/07_ui_module_03.png) |
| **Bank Reconciliation (BRS)** | Slide 17 | ![BRS](assets/presentation_diagrams/08_ui_module_04.png) |
| **Duplicate & Gap Detection** | Slide 18 | ![Duplicates](assets/presentation_diagrams/09_ui_module_05.png) |
| **Anomaly Detection (Benford & ML)** | Slide 19 | ![Anomalies](assets/presentation_diagrams/10_ui_module_06.png) |
| **Working Papers (SA 230)** | Slide 20 | ![Working Papers](assets/presentation_diagrams/11_ui_module_07.png) |
| **AI Assistant & Copilot** | Slide 21 | ![AI Assistant](assets/presentation_diagrams/12_ui_module_08.png) |
| **Report Generation & Verification** | Slide 22 | ![Reports](assets/presentation_diagrams/13_ui_module_09.png) |
