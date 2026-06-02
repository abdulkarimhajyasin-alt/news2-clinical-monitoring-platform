# System Architecture

The system starts with patient baseline data, including dialysis vintage, comorbidities, dry weight, functional status, study phase, and study group.

Each dialysis session records operational details such as session date, start/end time, ultrafiltration, blood flow, dialysate settings, and session status.

Intradialytic monitoring captures repeated vital sign measurements during a session. These observations feed NEWS2 assessment records.

NEWS2 assessments store component scores, total score, risk level, alert requirement, and trigger reason. The current phase stores scores but does not implement calculation logic.

Alerts connect high-risk NEWS2 findings to clinical workflow states: new, viewed, acknowledged, in progress, closed, or cancelled.

Clinical deterioration events document the type, timing, description, and triggering NEWS2 score for clinically significant deterioration.

Clinical responses record medical and nursing actions, response start time, response delay, vascular access actions, and notes.

Response tracking stores timestamps from vital sign recording through alert creation, viewing, response, action, and closure.

Clinical outcomes capture 24-72 hour outcomes such as stable completion, early stopped session, transfer, admission, ICU admission, or death.

Research analytics aggregate patients, sessions, measurements, assessments, alerts, deterioration events, and outcomes for research monitoring.

The export layer is planned for later phases and must enforce anonymization and governance rules.

Audit logs record sensitive actions across system entities for traceability.
