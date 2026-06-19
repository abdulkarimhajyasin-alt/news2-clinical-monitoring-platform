from __future__ import annotations


GREEN_ACTIONS_AR = [
    "ط§ظ„ظ…طھط§ط¨ط¹ط© ط§ظ„ط±ظˆطھظٹظ†ظٹط©",
    "ظ‚ظٹط§ط³ ط§ظ„ط¹ظ„ط§ظ…ط§طھ ط§ظ„ط­ظٹظˆظٹط© ظƒظ„ 60 ط¯ظ‚ظٹظ‚ط©",
    "طھط³ط¬ظٹظ„ ط§ظ„ط¨ظٹط§ظ†ط§طھ ظپظٹ ط§ظ„ظ…ظ†طµط©",
    "ط§ط³طھظ…ط±ط§ط± ط§ظ„ط¬ظ„ط³ط© ط­ط³ط¨ ط§ظ„ط®ط·ط©",
]
GREEN_ACTIONS_EN = [
    "Routine follow-up",
    "Measure vital signs every 60 minutes",
    "Record data in the platform",
    "Continue the session as scheduled",
]

YELLOW_ACTIONS_AR = [
    "ط¥ط¹ط§ط¯ط© ظ‚ظٹط§ط³ ط§ظ„ط¹ظ„ط§ظ…ط§طھ ط§ظ„ط­ظٹظˆظٹط© ط®ظ„ط§ظ„ 15-30 ط¯ظ‚ظٹظ‚ط©",
    "ظ…ط±ط§ط¬ط¹ط© ط¥ط¹ط¯ط§ط¯ط§طھ ط¬ظ‡ط§ط² ط§ظ„ط؛ط³ظٹظ„ ط®ط§طµط© ظ…ط¹ط¯ظ„ ط³ط­ط¨ ط§ظ„ط³ظˆط§ط¦ظ„ ظˆط§ظ„ط­ط±ط§ط±ط©",
    "طھظ‚ظٹظٹظ… ط§ظ„ط£ط¹ط±ط§ط¶ ط§ظ„ظ…طµط§ط­ط¨ط©",
    "طھظˆط«ظٹظ‚ ظ…ظ„ط§ط­ط¸ط§طھ ط§ظ„طھظ…ط±ظٹط¶ ظپظٹ ط§ظ„ظ…ظ†طµط©",
]
YELLOW_ACTIONS_EN = [
    "Repeat vital signs within 15-30 minutes",
    "Review dialysis machine settings, especially fluid removal rate and temperature",
    "Assess associated symptoms",
    "Document nursing notes in the platform",
]

RED_ACTIONS_AR = [
    "ط§ط³طھط¯ط¹ط§ط، ط§ظ„ط·ط¨ظٹط¨ ط§ظ„ظ…ط³ط¤ظˆظ„ ظپظˆط±ط§",
    "طھظ‚ظٹظٹظ… ظ…ط¬ط±ظ‰ ط§ظ„ظ‡ظˆط§ط، ظˆط¯ط±ط¬ط© ط§ظ„ظˆط¹ظٹ",
    "ط¥ط¹ط§ط¯ط© ظ‚ظٹط§ط³ ط§ظ„ط¹ظ„ط§ظ…ط§طھ ط§ظ„ط­ظٹظˆظٹط© ط®ظ„ط§ظ„ 5 ط¯ظ‚ط§ط¦ظ‚",
    "طھط­ط¶ظٹط± ظ…ط¹ط¯ط§طھ ط§ظ„ط·ظˆط§ط±ط¦: ط§ظ„ط£ظˆظƒط³ط¬ظٹظ†طŒ ط§ظ„ط³ظˆط§ط¦ظ„طŒ ط£ط¯ظˆظٹط© ط§ظ„ط·ظˆط§ط±ط¦",
    "ط§ظ„ظ†ط¸ط± ظپظٹ ط¥ظٹظ‚ط§ظپ ط§ظ„ط؛ط³ظٹظ„ ظ…ط¤ظ‚طھط§",
    "طھط³ط¬ظٹظ„ ط§ظ„ط­ط¯ط« ظپظٹ ط§ظ„ظ…ظ†طµط© ظˆط§ظ„ظ…ظ„ظپ ط§ظ„ط·ط¨ظٹ",
    "ط§ط³طھظ…ط±ط§ط± ط§ظ„ظ…ط±ط§ظ‚ط¨ط© ط§ظ„ظ„طµظٹظ‚ط© ظƒظ„ 5-10 ط¯ظ‚ط§ط¦ظ‚",
]
RED_ACTIONS_EN = [
    "Call the responsible physician immediately",
    "Assess airway and consciousness",
    "Repeat vital signs within 5 minutes",
    "Prepare emergency equipment: oxygen, fluids, emergency medications",
    "Consider temporary dialysis interruption",
    "Record the event in the platform and medical file",
    "Continue close monitoring every 5-10 minutes",
]


def build_hd2_nursing_protocol(score: int, risk_color: str, critical_triggers: list[str] | None = None) -> dict[str, object]:
    critical_triggers = critical_triggers or []
    normalized_color = "red" if risk_color == "red" or critical_triggers or score >= 7 else risk_color
    if normalized_color == "red":
        return _protocol(
            risk_color="red",
            risk_label_ar="ط£ط­ظ…ط± - ط·ظˆط§ط±ط¦",
            risk_label_en="Red - High Risk / Emergency",
            risk_level="high",
            actions_ar=RED_ACTIONS_AR,
            actions_en=RED_ACTIONS_EN,
            reassessment_min=5,
            reassessment_max=5,
            response_time=5,
            follow_up_min=5,
            follow_up_max=10,
            physician_call=True,
            emergency_preparation=True,
            machine_review=False,
            symptom_assessment=True,
            close_monitoring=True,
            summary_ar="ط®ط·ظˆط±ط© ط­ظ…ط±ط§ط،: ط§ط³طھط¯ط¹ط§ط، ط§ظ„ط·ط¨ظٹط¨ ظپظˆط±ط§ ظˆط¥ط¹ط§ط¯ط© ط§ظ„طھظ‚ظٹظٹظ… ط®ظ„ط§ظ„ 5 ط¯ظ‚ط§ط¦ظ‚.",
            summary_en="Red risk: call physician immediately and reassess within 5 minutes.",
        )
    if normalized_color == "yellow" or 5 <= score <= 6:
        return _protocol(
            risk_color="yellow",
            risk_label_ar="ط£طµظپط± - ظ…ط±ط§ظ‚ط¨ط©",
            risk_label_en="Yellow - Moderate Risk",
            risk_level="moderate",
            actions_ar=YELLOW_ACTIONS_AR,
            actions_en=YELLOW_ACTIONS_EN,
            reassessment_min=15,
            reassessment_max=30,
            response_time=None,
            follow_up_min=15,
            follow_up_max=30,
            physician_call=False,
            emergency_preparation=False,
            machine_review=True,
            symptom_assessment=True,
            close_monitoring=False,
            summary_ar="ط®ط·ظˆط±ط© طµظپط±ط§ط،: ط¥ط¹ط§ط¯ط© ط§ظ„ظ‚ظٹط§ط³ ط®ظ„ط§ظ„ 15-30 ط¯ظ‚ظٹظ‚ط© ظˆظ…ط±ط§ط¬ط¹ط© ط¥ط¹ط¯ط§ط¯ط§طھ ط§ظ„ط¬ظ‡ط§ط².",
            summary_en="Yellow risk: repeat vital signs within 15-30 minutes and review dialysis settings.",
        )
    return _protocol(
        risk_color="green",
        risk_label_ar="ط£ط®ط¶ط± - ط¢ظ…ظ†",
        risk_label_en="Green - Low Risk",
        risk_level="low",
        actions_ar=GREEN_ACTIONS_AR,
        actions_en=GREEN_ACTIONS_EN,
        reassessment_min=60,
        reassessment_max=60,
        response_time=None,
        follow_up_min=60,
        follow_up_max=60,
        physician_call=False,
        emergency_preparation=False,
        machine_review=False,
        symptom_assessment=False,
        close_monitoring=False,
        summary_ar="ط®ط·ظˆط±ط© ط®ط¶ط±ط§ط،: ظ…طھط§ط¨ط¹ط© ط±ظˆطھظٹظ†ظٹط© ظˆظ‚ظٹط§ط³ ط§ظ„ط¹ظ„ط§ظ…ط§طھ ظƒظ„ 60 ط¯ظ‚ظٹظ‚ط©.",
        summary_en="Green risk: routine follow-up and vital signs every 60 minutes.",
    )


def reassessment_interval_label_ar(protocol: dict[str, object]) -> str:
    min_value = protocol.get("reassessment_interval_minutes_min")
    max_value = protocol.get("reassessment_interval_minutes_max")
    if min_value == max_value:
        return f"ظƒظ„ {min_value} ط¯ظ‚ظٹظ‚ط©"
    return f"ط®ظ„ط§ظ„ {min_value}-{max_value} ط¯ظ‚ظٹظ‚ط©"


def required_response_time_label_ar(protocol: dict[str, object]) -> str:
    minutes = protocol.get("required_response_time_minutes")
    if minutes is None:
        return "ط؛ظٹط± ظ…ط·ظ„ظˆط¨ ط§ط³طھط¬ط§ط¨ط© ط·ط§ط±ط¦ط©"
    return f"ط®ظ„ط§ظ„ {minutes} ط¯ظ‚ط§ط¦ظ‚"


def _protocol(
    *,
    risk_color: str,
    risk_label_ar: str,
    risk_label_en: str,
    risk_level: str,
    actions_ar: list[str],
    actions_en: list[str],
    reassessment_min: int,
    reassessment_max: int,
    response_time: int | None,
    follow_up_min: int,
    follow_up_max: int,
    physician_call: bool,
    emergency_preparation: bool,
    machine_review: bool,
    symptom_assessment: bool,
    close_monitoring: bool,
    summary_ar: str,
    summary_en: str,
) -> dict[str, object]:
    return {
        "risk_color": risk_color,
        "risk_label_ar": risk_label_ar,
        "risk_label_en": risk_label_en,
        "risk_level": risk_level,
        "required_actions_ar": actions_ar,
        "required_actions_en": actions_en,
        "reassessment_interval_minutes_min": reassessment_min,
        "reassessment_interval_minutes_max": reassessment_max,
        "required_response_time_minutes": response_time,
        "follow_up_interval_minutes_min": follow_up_min,
        "follow_up_interval_minutes_max": follow_up_max,
        "requires_physician_call": physician_call,
        "requires_emergency_preparation": emergency_preparation,
        "requires_machine_settings_review": machine_review,
        "requires_symptom_assessment": symptom_assessment,
        "requires_close_monitoring": close_monitoring,
        "protocol_summary_ar": summary_ar,
        "protocol_summary_en": summary_en,
    }
