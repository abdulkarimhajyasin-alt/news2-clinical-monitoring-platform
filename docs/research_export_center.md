# Research Dataset & Export Center

Phase 11 adds a research dataset builder and export center for the NEWS2 hemodialysis monitoring platform.

## Dataset Row Definition

Each row represents one intradialytic measurement with its linked NEWS2 assessment. The row is enriched with downstream workflow data when available:

- Patient baseline and study group.
- Dialysis session details.
- Vascular access.
- Measurement values.
- NEWS2 component scores and total score.
- Alert details.
- Clinical deterioration event.
- Clinical response.
- Response tracking metrics.
- Clinical outcome.

## Included Variables

The dataset includes whitelisted variables only. Core variable groups are:

- Patient: `patient_code`, age, gender, dialysis vintage, comorbidities, study phase, and study group.
- Session: date, timing, prescription, ultrafiltration, and session status.
- Measurement: vital signs, oxygen therapy, consciousness, and confusion status.
- NEWS2: component scores, total score, risk level, alert flag, and trigger reason.
- Alert: status, priority, severity, trigger reason, and timestamps.
- Deterioration: event type, time, NEWS2 trigger score, and description.
- Response: response timing, delay, actions, and notes.
- Tracking: time to alert, view, response, action, and total response time.
- Outcome: outcome type, window, timestamp, and description.

## Privacy Rules

Research exports include `patient_code` and exclude direct clinical/user identifiers.

Exports do not include:

- Patient full name.
- User email.
- User phone.
- Password hash.
- Audit IP address.
- User agent.

The export service builds rows from explicit fields and never serializes ORM objects directly.

## Export Formats

Supported downloads:

- `research_dataset.csv`
- `research_dataset.xlsx`
- `spss_codebook.md`
- `spss_variable_labels.csv`

The SPSS package is SPSS-ready CSV plus metadata. It does not create a native `.sav` file.

## SPSS Preparation Approach

The codebook documents row definition, variable labels, value label examples, missing-value handling, and privacy notes.

The variable labels CSV maps dataset column names to human-readable labels for SPSS import preparation.

## Data Quality Checks

The quality endpoint reports:

- `missing_patient_code`
- `missing_session`
- `missing_measurement_time`
- `missing_news2_total_score`
- `invalid_timestamp_sequence`
- `missing_outcome_for_deterioration`
- `alert_without_response`
- `response_without_tracking`
- `duplicate_dataset_rows`

The quality score is simple and explainable: `100` minus weighted penalties for detected issues.

## API Endpoints

- `GET /api/research/dataset`: preview dataset rows with optional filters and limit.
- `GET /api/research/dataset/quality`: dataset quality report and statistics.
- `GET /api/research/export/csv`: downloadable CSV.
- `GET /api/research/export/xlsx`: downloadable Excel workbook.
- `GET /api/research/export/spss-codebook`: downloadable markdown codebook.
- `GET /api/research/export/spss-variable-labels`: downloadable variable label CSV.

## Filters

All dataset and export endpoints support optional filters:

- `start_date`
- `end_date`
- `patient_id`
- `patient_code`
- `study_phase`
- `study_group`
- `risk_level`
- `outcome_type`
- `deterioration_type`

## Frontend Behavior

The Export Center displays:

- Dataset preview.
- Filter form.
- CSV, Excel, SPSS codebook, and SPSS variable label download buttons.
- Data quality score.
- Issue counts by type.
- Quality warnings.

The Dataset Statistics screen displays research rows, measurements, NEWS2 alerts, deterioration events, responses, outcomes, and completion score.

Phase 12 builds the Research Analytics Dashboard on top of this same dataset layer, so export and analytics totals remain aligned.

Phase 14 protects dataset preview and quality endpoints with `research:view`, and protects CSV, XLSX, SPSS codebook, and SPSS variable-label downloads with `research:export`. The frontend hides export actions when the temporary development role lacks export permission.

## Research Safety Note

Exports are research datasets, not complete clinical records. They should be reviewed against study protocol, institutional privacy rules, and data governance requirements before external sharing or statistical analysis.
