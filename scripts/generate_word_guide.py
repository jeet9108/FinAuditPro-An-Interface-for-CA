import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_guide():
    doc = docx.Document()

    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Styles helper
    def set_para_font(p, name='Calibri', size=11, color=None, bold=False, italic=False, space_after=6):
        p.paragraph_format.space_after = Pt(space_after)
        for run in p.runs:
            run.font.name = name
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
            if color:
                run.font.color.rgb = color

    def set_cell_shading(cell, color_hex):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_section_header(title, level=1):
        p = doc.add_paragraph()
        p.add_run(title)
        if level == 1:
            set_para_font(p, size=15, bold=True, color=RGBColor(16, 75, 140), space_after=8)
        elif level == 2:
            set_para_font(p, size=12.5, bold=True, color=RGBColor(35, 100, 160), space_after=6)
        else:
            set_para_font(p, size=11, bold=True, color=RGBColor(50, 70, 90), space_after=4)

    # Document Header
    p_title = doc.add_paragraph()
    p_title.add_run('FinAuditPro — Internal System Architecture & Code Execution Blueprint')
    set_para_font(p_title, size=22, bold=True, color=RGBColor(24, 43, 73), space_after=2)

    p_sub = doc.add_paragraph()
    p_sub.add_run('Comprehensive Technical Reference for External Viva, Presentation, and Code Walkthrough\nAuthor: Jeet Shah (jeet9108) | Version: 1.2.0 | Offline-First Audit Operating System')
    set_para_font(p_sub, size=11, italic=True, color=RGBColor(80, 90, 105), space_after=16)

    # Executive Summary Box
    p_box = doc.add_paragraph()
    p_box.add_run('📋 Executive Summary for Examiners & Reviewers:\nThis document details the exact runtime lifecycle of FinAuditPro: from initial CLI launch (run.py), database bootstrap and immutability triggers (database.py), HTTP request lifecycle (main.py), 24 REST API Routers, forensic statutory calculation engines, Scikit-Learn outlier algorithms, local RAG LLM integration, to the Vanilla JS Single-Page Application (SPA) frontend.')
    set_para_font(p_box, size=10.5, color=RGBColor(30, 45, 65), space_after=16)

    # Section 1
    add_section_header('1. The Complete High-Level Execution Chain (Step-by-Step Flow)')
    steps = [
        ('Step 1: Environment Auto-Detection (run.py)', 'Inspects whether Python is running inside a virtual environment (sys.base_prefix != sys.prefix). If not, it automatically discovers venv/ or .venv/ on Windows/macOS/Linux and re-executes itself inside the isolated virtual environment using os.execv.'),
        ('Step 2: Database Initialization & Trigger Seeding (backend/app/database.py)', 'Executes init_db(). Connects to backend/finauditpro.db under SQLite WAL (Write-Ahead Logging) mode. Creates 25 relational tables, compound indices, and installs SQLite BEFORE UPDATE and BEFORE DELETE triggers that block tampering on audit_events. Seeds default audit checklists and default users.'),
        ('Step 3: Background Browser Dispatcher (run.py)', 'Spawns a background Python daemon thread (threading.Thread) that sleeps for 1.5 seconds and opens the default web browser targeting http://127.0.0.1:8000.'),
        ('Step 4: FastAPI Server Ignition (backend/app/main.py)', 'Uvicorn launches the FastAPI ASGI application on port 8000. It attaches CORS middleware (restricted to localhost/127.0.0.1), registers 24 modular API routers, and mounts frontend/ as a static directory (/static).'),
        ('Step 5: Client SPA Bootstrap (frontend/index.html & frontend/js/app.js)', 'The browser loads the Single-Page Application. app.js runs initApp(): checks for an existing JWT token in localStorage, calls GET /api/auth/me, verifies user permissions, and renders the initial view (Login Screen or Executive Dashboard).'),
        ('Step 6: Data Ingestion & Forensic Processing', 'Auditors upload CSV/Excel ledgers. import_data.py isolates files via UUIDs, parses data, sanitizes rows, and transactions enter the SQLite database. The Tri-Engine (Deterministic Rules, Scikit-Learn Anomaly Detection, BRS/GST Reconciliation) executes automatically.'),
        ('Step 7: Local AI Copilot & Working Papers (backend/app/ai/)', 'Auditor queries trigger AIGateway. The AIContextBoundary extracts relevant financial slices, strips PII (PAN, GSTIN, Bank A/C), and queries LM Studio locally (http://localhost:1234). Findings are persisted into SA 230 Electronic Working Papers and exported to ReportLab PDFs with SHA-256 verification QR codes.')
    ]
    for title, desc in steps:
        p = doc.add_paragraph()
        r1 = p.add_run(f'• {title}: ')
        r1.bold = True
        p.add_run(desc)
        set_para_font(p, size=10.5, space_after=4)

    # Section 2
    add_section_header('2. File-by-File Technical Anatomy (Which File Does What)')
    p_table_intro = doc.add_paragraph('Below is the canonical catalog of all critical files, their exact functions, invocation triggers, and internal dependencies:')
    set_para_font(p_table_intro, size=10.5, space_after=6)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    headers = ['File Path', 'Triggered By / Entry', 'Core Functions & Classes', 'Key Role & Explanation']
    for idx, text in enumerate(headers):
        hdr_cells[idx].text = text
        set_cell_shading(hdr_cells[idx], '1E3A5F')
        set_cell_margins(hdr_cells[idx], 120, 120, 150, 150)
        for p in hdr_cells[idx].paragraphs:
            set_para_font(p, size=9.5, bold=True, color=RGBColor(255, 255, 255), space_after=0)

    files_data = [
        ('run.py', 'CLI / User Start', 'open_browser(), init_db(), uvicorn.run()', 'Root bootstrap script. Auto-detects virtual environment, launches background browser thread, initializes DB, and starts FastAPI server.'),
        ('backend/app/main.py', 'run.py (uvicorn)', 'lifespan(), serve_index(), health_check()', 'FastAPI application factory. Configures CORS, mounts 24 router modules, serves frontend SPA at `/`, and manages app lifecycle.'),
        ('backend/app/database.py', 'main.py / run.py', 'get_db_connection(), init_db(), execute_query()', 'Database foundation layer. Manages SQLite connection pooling, WAL mode, foreign keys, table creation, and immutable triggers on audit_events.'),
        ('backend/app/auth.py', 'auth.py router / API requests', 'hash_password(), verify_password(), create_access_token(), get_current_user()', 'Cryptographic security core. Implements PBKDF2-HMAC-SHA256 (100,000 iterations) salted hashing, JWT generation, and RBAC token decoding.'),
        ('backend/app/ai/gateway.py', 'assistant.py router', 'AIGateway.generate_advisory_analysis(), check_health()', 'Central AI coordinator. Enforces context boundary, manages fallback to BuiltinDeterministicAIProvider if LM Studio daemon is offline.'),
        ('backend/app/ai/context_builder.py', 'AIGateway', 'AIContextBoundary.build_engagement_context()', 'Local RAG pipeline engine. Queries SQLite for sampled transactions/findings, sanitizes PII (PAN/GSTIN), and caps tokens to prevent context explosion.'),
        ('backend/app/services/local_ai_provider.py', 'gateway.py', 'LMStudioProvider, BuiltinDeterministicAIProvider, sanitize_audit_text()', 'Provider implementations. Communicates via HTTP to LM Studio (http://localhost:1234/v1/chat/completions) or runs zero-daemon rule-based synthesis.'),
        ('backend/app/services/anomaly_detection_engine.py', 'anomalies.py router', 'run_all_anomaly_checks(), detect_benford_anomalies(), detect_isolation_forest_anomalies()', 'Statistical ML engine. Computes Benford First-Digit MAD, Scikit-Learn Isolation Forest multi-variate scores, 3-sigma Z-scores, and weekend spikes.'),
        ('backend/app/services/bank_reconciliation_engine.py', 'reconciliation.py router', 'reconcile_bank_statement(), auto_match_records()', 'BRS engine. Segregates book vs bank datasets, executes exact amount+date matching, fuzzy reference matching, and calculates unreconciled balances.'),
        ('backend/app/services/gst_reconciliation_engine.py', 'gst_reconciliation.py router', 'reconcile_gst_records(), compute_itc_mismatches()', 'GST statutory engine. Compares Purchase Register against GSTR-2B portal data, identifies eligible vs ineligible ITC under Sec 16(2)(aa).'),
        ('backend/app/services/centralized_findings_engine.py', 'audit_findings.py router', 'aggregate_all_findings(), compute_risk_score()', 'Central findings aggregator. Ingests exceptions from all engines, calculates multi-dimensional risk scores (0-10), and tracks review statuses.'),
        ('backend/app/services/checklist_generator.py', 'checklist.py router', 'generate_engagement_checklist()', 'Dynamic workprogram engine. Spawns SA 200/CARO 2020/Form 3CD checklist procedures tailored to legal entity type and risk findings.'),
        ('backend/app/services/backup_service.py', 'settings.py router', 'create_encrypted_backup(), restore_encrypted_backup()', 'Air-gapped security vault. Packs DB, evidence, and indices into ZIPs encrypted with Fernet (AES-128-CBC + HMAC) and PBKDF2 with unique salts.'),
        ('frontend/js/api.js', 'frontend/js/app.js', 'FinAuditAPI client object (100+ API methods)', 'Client HTTP communication layer. Intercepts JWT tokens, manages Bearer authorization headers, error handling, and file upload progress.'),
        ('frontend/js/app.js', 'frontend/index.html', 'initApp(), renderView(), renderDashboard(), etc.', 'Desktop SPA orchestrator (17,000+ lines). Manages client-side routing, tab switching across 21 screens, reactive state, and modal dialogues.')
    ]
    for row in files_data:
        r_cells = table.add_row().cells
        for i, val in enumerate(row):
            r_cells[i].text = val
            set_cell_margins(r_cells[i], 80, 80, 100, 100)
            p = r_cells[i].paragraphs[0]
            set_para_font(p, size=9, space_after=0)
            if i == 0:
                for run in p.runs:
                    run.bold = True

    # Section 3
    add_section_header('3. The 24 REST API Routers (backend/app/routers/)')
    router_categories = [
        ('Authentication & RBAC (auth.py)', 'Handles POST /api/auth/login, POST /api/auth/refresh, GET /api/auth/me, and password changes. Enforces exponential lockout on brute force attacks and logs immutable authentication events.'),
        ('Client & Engagement Scoping (clients.py, engagements.py)', 'Manages client master directory, legal structure (Pvt Ltd, LLP, Partnership), PAN/GSTIN registration, and fiscal year engagement periods. All transactional queries are scoped to an engagement_id to prevent cross-client leakage.'),
        ('Data Ingestion & Cleaning (import_data.py, data_cleaning.py)', 'Accepts CSV/XLSX/PDF uploads. Performs auto-column detection (matching "Voucher No" or "Vch No" to voucher_no), detects invalid dates or missing debit/credit balances, and writes sanitized rows to transactions.'),
        ('General Ledger & Financial Statements (transactions.py, trial_balance.py, financial_statements.py, yoy_comparison.py)', 'Computes Trial Balance mathematical equality (Total Dr == Total Cr), generates Schedule III Balance Sheet and Profit & Loss statements, and runs SA 520 analytical variance tests comparing prior vs current years.'),
        ('Statutory Rules & Reconciliations (reconciliation.py, gst_reconciliation.py, duplicates_and_gaps.py)', 'Executes Section 40A(3) cash disallowances (>Rs 10,000/day), Section 269ST cash receipts (>=Rs 2,00,000), BRS 3-way matching, GSTR-2B ITC verification, and fuzzy duplicate detection using sequence pattern matching.'),
        ('Forensic Anomaly Detection (anomalies.py)', 'Executes Benford\'s Law 1-9 digit distribution analysis against Nigrini forensic benchmarks, Isolation Forest multi-variate outlier scoring, and 3-sigma Z-scores.'),
        ('Audit Evidence & Working Papers (audit_findings.py, checklist.py, working_papers.py, evidence.py)', 'Allows auditors to add SA 230 review comments, attach evidentiary documents, track checklist sign-offs (with strict human auditor completion boundaries), and assemble final working paper bundles.'),
        ('Reports & Audit Trail (reports.py, audit_trail.py)', 'Generates master statutory audit PDF reports via ReportLab with embedded SHA-256 verification QR codes, and exposes the tamper-evident hash-chained audit event trail required under Companies Act 2013 Rule 11(g).'),
        ('System Administration & AI Gateway (settings.py, ai_manager.py, assistant.py, system.py, jobs.py)', 'Configures retention periods, verifies system health, tests LM Studio loopback connection, and monitors background job execution.')
    ]
    for title, desc in router_categories:
        p = doc.add_paragraph()
        r1 = p.add_run(f'• {title}: ')
        r1.bold = True
        p.add_run(desc)
        set_para_font(p, size=10, space_after=4)

    # Section 4
    add_section_header('4. Forensic Engines & Mathematical Algorithms')
    math_points = [
        ('Deterministic Integer-Paise Precision', 'All financial monetary values are converted to and processed as integer paise (1 INR = 100 paise). This eliminates IEEE-754 binary floating-point representation drift during bulk ledger aggregations.'),
        ('Benford’s Law First-Digit Analysis (Nigrini Standard)', 'Forensic accounting standard testing digit frequencies (d in {1..9}) using formula P(d) = log10(1 + 1/d). Compares actual digit distribution against theoretical expectation via Mean Absolute Deviation (MAD). Values exceeding MAD threshold (> 0.015) trigger forensic review for manufactured figures.'),
        ('Scikit-Learn Isolation Forest', 'Unsupervised anomaly detection isolating outlier transactions based on multi-dimensional features: amount, debit/credit ratio, day-of-week, day-of-month, and velocity. Outliers receive an anomaly score from -1.0 to +1.0.'),
        ('3-Sigma Univariate Z-Score', 'Calculates Z = (x - mean) / std across ledger heads. Flags high-value entries booked more than 2.8 to 3.0 standard deviations away from historical baseline means.'),
        ('Fuzzy Levenshtein & Token Duplication', 'Flags duplicate postings sharing similar invoice patterns (e.g. INV-001 vs INV/001) or vendor alias names with >= 85% string similarity and identical financial figures.')
    ]
    for title, desc in math_points:
        p = doc.add_paragraph()
        r1 = p.add_run(f'• {title}: ')
        r1.bold = True
        p.add_run(desc)
        set_para_font(p, size=10, space_after=4)

    # Section 5
    add_section_header('5. Local RAG & AI Copilot Integration (LM Studio / Qwen 2.5)')
    ai_steps = [
        ('Host Server', 'LM Studio runs locally at http://localhost:1234, serving qwen2.5-coder-14b-instruct (14.7B parameters, 128K context window) via an OpenAI-compatible /v1/chat/completions REST endpoint.'),
        ('Scoped RAG Pipeline (AIContextBoundary)', 'When a user inquires about an anomaly or tax rule, the backend executes a scoped database lookup for relevant transaction records and findings. It limits context to ~3,000 tokens to prevent context dilution.'),
        ('Privacy & Regex Redaction Barrier', 'Before context leaves the database slice, sanitize_audit_text() strips client names, PAN numbers ([PAN_REDACTED]), GSTINs ([GSTIN_REDACTED]), Bank Account numbers, and email/phones. No PII enters the model.'),
        ('Advisory-Only Safety Barrier', 'The AI engine is strictly read-only and advisory. In adherence to SA 200/SA 230, the model can NEVER mark a checklist item "Completed" or modify financial numbers. Every finding requires human auditor sign-off.'),
        ('Built-in Zero-Daemon Fallback', 'If LM Studio is closed or the user lacks an NVIDIA/Apple GPU, the backend routes queries to BuiltinDeterministicAIProvider, generating statutory rule explanations purely via compiled Python logic.')
    ]
    for title, desc in ai_steps:
        p = doc.add_paragraph()
        r1 = p.add_run(f'• {title}: ')
        r1.bold = True
        p.add_run(desc)
        set_para_font(p, size=10, space_after=4)

    # Section 6
    add_section_header('6. Viva & External Examination Q&A Guide')
    viva_qa = [
        ('Q: What happens when you run `python run.py`?', 
         'A: run.py first detects the virtual environment and restarts inside it if necessary. Then it triggers init_db() in database.py to create the SQLite tables and append-only triggers. Next, it spawns a background thread to launch the browser at 127.0.0.1:8000, and starts the Uvicorn ASGI server with FastAPI serving the backend and static SPA frontend.'),
        
        ('Q: How is client data privacy guaranteed for Indian CAs?', 
         'A: FinAuditPro is 100% offline with zero cloud telemetry. The database is a local SQLite file protected by host OS encryption. All AI queries run against a local LM Studio server with an automatic regex redaction boundary masking PAN, GSTIN, and bank accounts.'),
         
        ('Q: How does the system prevent tampering with audit logs?', 
         'A: Under Companies Act 2013 Rule 11(g), audit logs must be immutable. We enforce this at the database engine level using SQLite BEFORE UPDATE and BEFORE DELETE triggers on audit_events that abort any modification attempt. Additionally, events are linked in a sequential SHA-256 cryptographic hash chain verified at application startup.'),
         
        ('Q: Why use RAG instead of fine-tuning the LLM?', 
         'A: Indian tax audit clauses (Form 3CD, CARO 2020) and MCA notifications change frequently. Fine-tuning causes catastrophic forgetting, risks memorizing sensitive client data, and hallucinates figures. RAG dynamically injects verified, current ledger records and statutory rules into the prompt context, guaranteeing 100% mathematical provenance.')
    ]
    for q, a in viva_qa:
        p = doc.add_paragraph()
        r_q = p.add_run(f'{q}\n')
        r_q.bold = True
        r_q.font.color.rgb = RGBColor(16, 75, 140)
        p.add_run(a)
        set_para_font(p, size=10, space_after=6)

    out_dir = r'c:\Users\Jeet Shah\OneDrive\Desktop\FinAuditPro_CA_AuditInterface\TempAudit-main\Documentation'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'FinAuditPro_Code_Working_and_Architecture_Guide.docx')
    doc.save(out_path)
    print("SUCCESS: File generated at", out_path)

if __name__ == '__main__':
    create_guide()
