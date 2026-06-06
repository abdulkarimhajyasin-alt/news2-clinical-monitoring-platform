# System Architecture

The system starts with patient baseline data, including dialysis vintage, comorbidities, dry weight, functional status, study phase, and study group.

Each dialysis session records operational details such as session date, start/end time, ultrafiltration, blood flow, dialysate settings, and session status.

Intradialytic monitoring captures repeated vital sign measurements during a session. These observations feed NEWS2 assessment records.

The NEWS2 calculation engine scores respiratory rate, SpO2, supplemental oxygen, systolic blood pressure, pulse rate, temperature, and consciousness/new confusion. It returns component scores, total score, risk level, alert requirement, single-parameter trigger status, and trigger reason.

The monitoring write workflow persists a new intradialytic measurement, calculates NEWS2, persists the linked NEWS2 assessment, and evaluates governed alert creation in one transaction. The standalone NEWS2 calculation endpoint remains non-persistent.

NEWS2 assessments store component scores, total score, risk level, alert requirement, and trigger reason. The alert engine creates or reuses one active alert for a patient/session when NEWS2 is 5 or higher or when a single parameter scores 3.

Alerts connect high-risk NEWS2 findings to clinical workflow states: new, viewed, acknowledged, in progress, closed, or cancelled.

Clinical deterioration events are created from active alerts and document the type, timing, description, triggering NEWS2 score, and time from dialysis session start when calculable. The event workflow prevents duplicate events for the same alert.

Clinical responses are created from deterioration events and record medical and nursing actions, response start time, response delay from digital alert creation, vascular access actions, responding user, and notes.

Response tracking stores timestamps from vital sign recording through alert creation, viewing, response, action, and closure. Phase 09 calculates one tracking record per alert, prevents duplicate tracking rows, keeps optional missing timestamps nullable, and exposes list, detail, recalculation, and summary APIs for research dashboards.

Clinical outcomes capture 24, 48, and 72 hour outcomes such as stable completion, early stopped session, transfer, admission, ICU admission, or death. Outcomes are created only from an existing deterioration event, derive patient/session IDs from that event, and prevent duplicate records for the same event/window.

Research analytics aggregate patients, sessions, measurements, assessments, alerts, deterioration events, response timing, and outcomes for research monitoring. Phase 10 exposes outcome counts for stable completion, early session stop, hospital admission, emergency transfer, ICU admission, and death.

The Phase 11 research export layer builds a privacy-protected flat dataset from measurement-linked NEWS2 assessments. It enriches each row with patient baseline, session, vascular access, alert, deterioration, response, tracking, and outcome data when available. The export layer is read-only and uses explicit field whitelisting to avoid leaking patient names, user emails, phones, password hashes, IP addresses, or user agents.

The Phase 12 research analytics layer consumes the same research dataset and derives descriptive KPIs, NEWS2 distributions, risk-level analysis, outcome analysis, response-time analysis, deterioration analysis, and group comparisons. It deliberately avoids inferential statistics and predictive analytics.

The Phase 13 study management layer sits above the dataset and analytics layers. It stores formal study registry records in `research_studies`, including protocol configuration, study periods, study groups, target sample size, status, and research notes. The readiness engine checks whether the study definition, dataset, analytics, exports, outcomes, and response tracking are operationally available.

The Phase 14 RBAC layer centralizes role labels, permission strings, and the permission matrix in `app/rbac.py`. Sensitive research, study, alert-management, and clinical write endpoints depend on reusable permission checks. The temporary development resolver reads `X-Dev-Role` and defaults to `admin` only until Phase 15 authentication replaces it.

Deployment startup initializes the database before requests are served. The startup helper creates missing tables with SQLAlchemy metadata, never drops existing tables, and optionally seeds demo/research data only when the users/patients tables are empty.

Later export phases should add governed dataset approvals, richer analysis outputs, and institution-specific review controls.

Audit logs record sensitive actions across system entities for traceability.
