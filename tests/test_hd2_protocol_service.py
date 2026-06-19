from app.services.hd2_protocol_service import build_hd2_nursing_protocol


def test_green_score_returns_sixty_minute_routine_protocol():
    protocol = build_hd2_nursing_protocol(4, "green")

    assert protocol["risk_color"] == "green"
    assert protocol["risk_label_ar"] == "ط£ط®ط¶ط± - ط¢ظ…ظ†"
    assert protocol["reassessment_interval_minutes_min"] == 60
    assert protocol["reassessment_interval_minutes_max"] == 60
    assert protocol["requires_physician_call"] is False


def test_yellow_score_returns_fifteen_to_thirty_minute_protocol():
    protocol = build_hd2_nursing_protocol(5, "yellow")

    assert protocol["risk_color"] == "yellow"
    assert protocol["risk_label_ar"] == "ط£طµظپط± - ظ…ط±ط§ظ‚ط¨ط©"
    assert protocol["reassessment_interval_minutes_min"] == 15
    assert protocol["reassessment_interval_minutes_max"] == 30
    assert protocol["requires_machine_settings_review"] is True
    assert protocol["requires_symptom_assessment"] is True


def test_red_score_returns_emergency_protocol():
    protocol = build_hd2_nursing_protocol(7, "red")

    assert protocol["risk_color"] == "red"
    assert protocol["risk_label_ar"] == "ط£ط­ظ…ط± - ط·ظˆط§ط±ط¦"
    assert protocol["required_response_time_minutes"] == 5
    assert protocol["requires_physician_call"] is True
    assert protocol["requires_emergency_preparation"] is True
    assert protocol["requires_close_monitoring"] is True


def test_critical_trigger_forces_red_protocol_when_score_is_lower():
    protocol = build_hd2_nursing_protocol(2, "green", ["SpO2 <=91%"])

    assert protocol["risk_color"] == "red"
    assert protocol["required_response_time_minutes"] == 5
