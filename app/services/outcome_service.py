from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    Alert,
    AuditLog,
    ClinicalDeteriorationEvent,
    ClinicalOutcome,
    DialysisSession,
    News2Assessment,
    OutcomeType,
    Patient,
)
from app.schemas import ClinicalOutcomeCreate


class OutcomeWorkflowError(Exception):
    pass


class OutcomeEventNotFoundError(OutcomeWorkflowError):
    pass


class OutcomeNotFoundError(OutcomeWorkflowError):
    pass


class OutcomeTraceabilityError(OutcomeWorkflowError):
    pass


def create_outcome(db: Session, payload: ClinicalOutcomeCreate) -> dict[str, object]:
    event = db.get(ClinicalDeteriorationEvent, payload.clinical_deterioration_event_id)
    if event is None:
        raise OutcomeEventNotFoundError("Clinical deterioration event not found")

    patient = db.get(Patient, event.patient_id)
    session = db.get(DialysisSession, event.dialysis_session_id)
    if patient is None or session is None:
        raise OutcomeTraceabilityError("Deterioration event traceability chain is incomplete")

    existing_outcome = (
        db.query(ClinicalOutcome)
        .filter(
            ClinicalOutcome.clinical_deterioration_event_id == event.id,
            ClinicalOutcome.outcome_window_hours == payload.outcome_window_hours,
        )
        .first()
    )
    if existing_outcome is not None:
        _create_audit_log(
            db,
            action="clinical_outcome_reused",
            outcome=existing_outcome,
            user_id=payload.recorded_by_user_id,
            new_value=f"Reused {payload.outcome_window_hours}h clinical outcome for deterioration event {event.id}",
        )
        db.commit()
        return {
            "outcome": _outcome_to_dict(db, existing_outcome),
            "outcome_created": False,
            "message": "Existing clinical outcome returned for this deterioration event and window",
        }

    outcome = ClinicalOutcome(
        patient_id=event.patient_id,
        dialysis_session_id=event.dialysis_session_id,
        clinical_deterioration_event_id=event.id,
        outcome_type=payload.outcome_type,
        outcome_recorded_at=datetime.now(timezone.utc).replace(microsecond=0),
        outcome_window_hours=payload.outcome_window_hours,
        description=payload.description,
        recorded_by_user_id=payload.recorded_by_user_id,
    )
    db.add(outcome)
    db.flush()

    _create_audit_log(
        db,
        action="clinical_outcome_created",
        outcome=outcome,
        user_id=payload.recorded_by_user_id,
        new_value=f"Created {payload.outcome_window_hours}h clinical outcome for deterioration event {event.id}",
    )
    db.commit()
    db.refresh(outcome)
    return {
        "outcome": _outcome_to_dict(db, outcome),
        "outcome_created": True,
        "message": "Clinical outcome created successfully",
    }


def get_outcomes(
    db: Session,
    patient_id: int | None = None,
    dialysis_session_id: int | None = None,
    clinical_deterioration_event_id: int | None = None,
    outcome_type: str | None = None,
    outcome_window_hours: int | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    query = db.query(ClinicalOutcome)
    if patient_id is not None:
        query = query.filter(ClinicalOutcome.patient_id == patient_id)
    if dialysis_session_id is not None:
        query = query.filter(ClinicalOutcome.dialysis_session_id == dialysis_session_id)
    if clinical_deterioration_event_id is not None:
        query = query.filter(ClinicalOutcome.clinical_deterioration_event_id == clinical_deterioration_event_id)
    if outcome_type is not None:
        query = query.filter(ClinicalOutcome.outcome_type == outcome_type)
    if outcome_window_hours is not None:
        query = query.filter(ClinicalOutcome.outcome_window_hours == outcome_window_hours)
    outcomes = query.order_by(ClinicalOutcome.created_at.desc()).limit(limit).all()
    return [_outcome_to_dict(db, outcome) for outcome in outcomes]


def get_outcome(db: Session, outcome_id: int) -> dict[str, object]:
    outcome = db.get(ClinicalOutcome, outcome_id)
    if outcome is None:
        raise OutcomeNotFoundError("Clinical outcome not found")
    return _outcome_to_dict(db, outcome)


def get_outcome_summary(db: Session) -> dict[str, int]:
    counts = _outcome_counts(db)
    return {
        "total_outcomes": db.query(ClinicalOutcome).count(),
        **counts,
    }


def _outcome_counts(db: Session) -> dict[str, int]:
    counts = {f"{outcome_type.value}_count": 0 for outcome_type in OutcomeType}
    rows = (
        db.query(ClinicalOutcome.outcome_type, func.count(ClinicalOutcome.id))
        .group_by(ClinicalOutcome.outcome_type)
        .all()
    )
    for outcome_type, count in rows:
        counts[f"{outcome_type}_count"] = count
    return counts


def _outcome_to_dict(db: Session, outcome: ClinicalOutcome) -> dict[str, object]:
    patient = db.get(Patient, outcome.patient_id)
    session = db.get(DialysisSession, outcome.dialysis_session_id)
    event = db.get(ClinicalDeteriorationEvent, outcome.clinical_deterioration_event_id)
    assessment = db.get(News2Assessment, event.news2_assessment_id) if event else None
    alert = db.get(Alert, event.alert_id) if event else None
    return {
        "id": outcome.id,
        "patient_id": outcome.patient_id,
        "patient_code": patient.patient_code if patient else None,
        "dialysis_session_id": outcome.dialysis_session_id,
        "session_date": session.session_date if session else None,
        "clinical_deterioration_event_id": outcome.clinical_deterioration_event_id,
        "alert_id": event.alert_id if event else None,
        "news2_assessment_id": event.news2_assessment_id if event else None,
        "news2_total_score": assessment.total_score if assessment else (event.triggering_news2_score if event else None),
        "deterioration_type": event.deterioration_type if event else None,
        "outcome_type": outcome.outcome_type,
        "outcome_recorded_at": outcome.outcome_recorded_at,
        "outcome_window_hours": outcome.outcome_window_hours,
        "description": outcome.description,
        "recorded_by_user_id": outcome.recorded_by_user_id,
        "is_locked": outcome.is_locked,
        "locked_at": outcome.locked_at,
        "locked_by_user_id": outcome.locked_by_user_id,
        "created_at": outcome.created_at,
    }


def _create_audit_log(
    db: Session,
    action: str,
    outcome: ClinicalOutcome,
    new_value: str,
    user_id: int | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type="clinical_outcome",
            entity_id=str(outcome.id),
            new_value=new_value,
        )
    )
