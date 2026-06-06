# Research Workflow

```text
Patient Baseline
↓
Dialysis Session
↓
Repeated Monitoring
↓
NEWS2 Calculation
↓
Alert if NEWS2 >= 5 or sudden deterioration
↓
Deterioration Log
↓
Medical/Nursing Response
↓
Response Time Tracking
↓
Outcome within 24-72h
↓
Research Dataset
```

Phase 04 adds the validated NEWS2 calculation engine and `POST /api/news2/calculate` endpoint. The endpoint calculates scores without saving records.

Phase 05 adds `POST /api/monitoring/measurements`, which saves a new intradialytic measurement, calculates NEWS2, and saves the linked assessment.

Phase 06 adds governed alert creation after persisted NEWS2 assessments. Alerts are created for NEWS2 5 or higher, or for a single NEWS2 component score of 3, with duplicate prevention for active patient/session alert chains. Later phases should implement clinical deterioration workflows, export controls, and expanded analytics.

Phase 07 adds clinical deterioration events created from active alerts. Events preserve the patient/session/measurement/NEWS2/alert traceability chain and prevent duplicate events for the same alert. Later phases should implement medical and nursing response workflows, export controls, and expanded analytics.

Phase 08 adds the primary medical and nursing response record for each deterioration event. It stores patient actions, vascular access actions, response start time, response delay, responder, and notes.

Phase 09 adds persisted response time tracking for the full monitoring-to-response chain. It calculates time to alert, time to view, time to response, time to action, and total response time; updates records after lifecycle changes and response creation; and exposes research summary fields for average, fastest, slowest, and missing response metrics.

Phase 10 adds clinical outcome tracking for 24, 48, and 72 hour windows after deterioration events. Outcomes are linked to the event, derive patient/session traceability from that event, prevent duplicate event/window records, and add stable completion, early stop, hospital admission, emergency transfer, ICU admission, and death metrics to the research summary.

Phase 11 adds the Research Dataset & Export Center. It builds one flat row per intradialytic measurement with linked NEWS2 assessment, enriches rows with downstream workflow data, validates dataset quality, exports CSV/XLSX, and prepares SPSS-ready codebook and variable label files. Later phases should implement deeper analytics, inferential comparison, and governed export approvals.

Phase 12 adds the Research Analytics Dashboard. It uses the research dataset layer to calculate descriptive study KPIs, NEWS2 distributions, risk-level summaries, outcome rates, response-time metrics, deterioration summaries, and study group/phase comparisons. Inferential pre/post analysis remains intentionally out of scope.

Phase 13 adds Study Management and the Research Protocol Center. It defines the study registry, protocol configuration, baseline/intervention timeline, readiness checks, and audit trail for research-governance activities. Authentication, RBAC, publication generation, and inferential statistics remain out of scope.
