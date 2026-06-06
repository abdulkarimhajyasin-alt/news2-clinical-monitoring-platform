# NEWS2 Calculation Engine

## Purpose

The NEWS2 calculation engine scores vital signs for early detection of clinical deterioration in hemodialysis monitoring workflows. It is a clinical decision-support layer for API routes, seed data, future write workflows, future alert creation, and analytics.

NEWS2 does not replace clinical judgment. Final clinical decisions remain the responsibility of qualified healthcare professionals, and this implementation must be clinically reviewed before real-world deployment.

## Scored Parameters

- Respiratory rate.
- Oxygen saturation.
- Supplemental oxygen.
- Systolic blood pressure.
- Pulse rate.
- Temperature.
- Consciousness level or new confusion.

## Score Bands

Each component returns a score from 0 to 3, except supplemental oxygen which returns 0 or 2. SpO2 Scale 1 is the default path.

Risk classification:

- `0-4`: `low`.
- `5-6`: `medium`.
- `>=7`: `high`.

Alert flag:

- `alert_required = true` when total NEWS2 score is 5 or higher.

Single-parameter trigger:

- `single_parameter_trigger = true` when any component score is 3.
- This matters because a single extreme physiological parameter can be clinically important even when the total score is below the alert threshold.

## SpO2 Scale Support

`spo2_scale` defaults to `scale_1`.

`scale_2` is available only as an explicit calculation path for future patients at risk of hypercapnic respiratory failure. In this phase it uses a conservative placeholder and requires clinical review before production use.

## API Endpoint

Non-persistent calculation endpoint:

```http
POST /api/news2/calculate
```

Example request:

```json
{
  "respiratory_rate": 18,
  "spo2": 95,
  "oxygen_therapy": false,
  "systolic_bp": 125,
  "pulse_rate": 88,
  "temperature": 37.2,
  "consciousness_level": "alert",
  "spo2_scale": "scale_1"
}
```

Persistent monitoring workflow endpoint:

```http
POST /api/monitoring/measurements
```

This endpoint saves the submitted measurement, calculates NEWS2 with the same engine, saves the linked NEWS2 assessment, evaluates governed alert rules, and returns the workflow result.

Example response:

```json
{
  "respiratory_score": 0,
  "spo2_score": 1,
  "oxygen_score": 0,
  "systolic_bp_score": 0,
  "pulse_score": 0,
  "temperature_score": 0,
  "consciousness_score": 0,
  "total_score": 1,
  "risk_level": "low",
  "alert_required": false,
  "single_parameter_trigger": false,
  "trigger_reason": "NEWS2 total score below alert threshold"
}
```

## Testing Summary

Automated tests cover all requested component boundary values, total-score risk classification, single-parameter trigger behavior, Scale 2 placeholder routing, valid API calculation, invalid vital validation, and high-score alert behavior.
