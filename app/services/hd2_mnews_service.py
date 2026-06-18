from app.schemas import HD2MNEWSCalculationRequest, HD2MNEWSCalculationResult, HD2MNEWSComponentScores


RISK_LABELS_AR = {
    "green": "أخضر / آمن",
    "yellow": "أصفر / مراقبة",
    "red": "أحمر / طوارئ",
    "automatic_red": "أحمر تلقائي",
}


def score_hd2_respiratory_rate(respiratory_rate: int) -> int:
    if 12 <= respiratory_rate <= 20:
        return 0
    if 9 <= respiratory_rate <= 11 or 21 <= respiratory_rate <= 24:
        return 1
    return 2


def score_hd2_spo2(oxygen_saturation: int) -> int:
    if oxygen_saturation >= 96:
        return 0
    if oxygen_saturation >= 94:
        return 1
    if oxygen_saturation >= 92:
        return 2
    return 3


def score_hd2_temperature(temperature: float) -> int:
    if 36.1 <= temperature <= 38.0:
        return 0
    if temperature <= 36.0 or 38.1 <= temperature <= 39.0:
        return 1
    return 2


def score_hd2_systolic_bp(systolic_bp: int, sbp_symptomatic_hypotension: bool = False) -> int:
    if systolic_bp <= 90 and sbp_symptomatic_hypotension:
        return 3
    if 111 <= systolic_bp <= 219:
        return 0
    if 101 <= systolic_bp <= 110 or 220 <= systolic_bp <= 229:
        return 1
    return 2


def score_hd2_heart_rate(heart_rate: int) -> int:
    if 51 <= heart_rate <= 90:
        return 0
    if 41 <= heart_rate <= 50 or 91 <= heart_rate <= 110:
        return 1
    return 2


def score_hd2_avpu(consciousness_level: str) -> int:
    return {
        "alert": 0,
        "voice": 1,
        "pain": 2,
        "unresponsive": 3,
        "new_confusion": 1,
    }[consciousness_level]


def score_hd2_vascular_access(status: str) -> int:
    return {"normal": 0, "weak": 1, "disturbed": 2, "critical": 3}[status]


def calculate_idwg_percent(pre_dialysis_weight: float, dry_weight: float) -> float:
    return round(((pre_dialysis_weight - dry_weight) / dry_weight) * 100, 2)


def score_hd2_idwg(idwg_percent: float) -> int:
    if idwg_percent < 3:
        return 0
    if idwg_percent <= 5:
        return 1
    return 2


def calculate_ufr(fluid_to_remove: float, dry_weight: float, session_duration_hours: float) -> float:
    return round(fluid_to_remove / (dry_weight * session_duration_hours), 2)


def score_hd2_ufr(ufr: float) -> int:
    if ufr <= 10:
        return 0
    if ufr <= 13:
        return 1
    return 2


def score_hd2_potassium(potassium: float) -> int:
    if 3.5 <= potassium <= 5.0:
        return 0
    if 3.0 <= potassium <= 3.4 or 5.1 <= potassium <= 5.5:
        return 1
    if 2.5 <= potassium <= 2.9 or 5.6 <= potassium <= 6.0:
        return 2
    return 3


def calculate_hd2_mnews(request: HD2MNEWSCalculationRequest) -> HD2MNEWSCalculationResult:
    idwg_percent = calculate_idwg_percent(request.pre_dialysis_weight, request.dry_weight)
    ufr = calculate_ufr(request.fluid_to_remove, request.dry_weight, request.session_duration_hours)

    component_scores = HD2MNEWSComponentScores(
        respiratory_rate_score=score_hd2_respiratory_rate(request.respiratory_rate),
        oxygen_saturation_score=score_hd2_spo2(request.oxygen_saturation),
        temperature_score=score_hd2_temperature(request.temperature),
        systolic_bp_score=score_hd2_systolic_bp(request.systolic_bp, request.sbp_symptomatic_hypotension),
        heart_rate_score=score_hd2_heart_rate(request.heart_rate),
        consciousness_score=score_hd2_avpu(request.consciousness_level),
        vascular_access_score=score_hd2_vascular_access(request.vascular_access_status),
        idwg_score=score_hd2_idwg(idwg_percent),
        ufr_score=score_hd2_ufr(ufr),
        potassium_score=score_hd2_potassium(request.potassium),
    )
    total_score = sum(component_scores.model_dump().values())
    critical_reasons = _critical_reasons(request)
    critical_trigger = bool(critical_reasons)

    if critical_trigger:
        risk_color = "red"
        risk_label_ar = RISK_LABELS_AR["automatic_red"]
    elif total_score >= 7:
        risk_color = "red"
        risk_label_ar = RISK_LABELS_AR["red"]
    elif total_score >= 5:
        risk_color = "yellow"
        risk_label_ar = RISK_LABELS_AR["yellow"]
    else:
        risk_color = "green"
        risk_label_ar = RISK_LABELS_AR["green"]

    return HD2MNEWSCalculationResult(
        **component_scores.model_dump(),
        idwg_percent=idwg_percent,
        ufr=ufr,
        hd2_mnews_total_score=total_score,
        hd2_mnews_risk_color=risk_color,
        hd2_mnews_risk_label_ar=risk_label_ar,
        hd2_mnews_critical_trigger=critical_trigger,
        hd2_mnews_critical_reasons=critical_reasons,
    )


def _critical_reasons(request: HD2MNEWSCalculationRequest) -> list[str]:
    reasons: list[str] = []
    if request.oxygen_saturation <= 91:
        reasons.append("SpO2 ≤91%")
    if request.consciousness_level == "unresponsive":
        reasons.append("AVPU unresponsive")
    if request.systolic_bp <= 90 and request.sbp_symptomatic_hypotension:
        reasons.append("Symptomatic hypotension with SBP ≤90")
    if request.potassium < 2.5 or request.potassium > 6.0:
        reasons.append("Potassium critical range")
    if request.vascular_access_status == "critical":
        reasons.append("Critical vascular access status")
    return reasons
