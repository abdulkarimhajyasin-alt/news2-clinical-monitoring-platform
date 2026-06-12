from pathlib import Path


def test_rbac_permission_summary_uses_arabic_display_labels():
    source = Path("app/static/app.js").read_text(encoding="utf-8")

    assert "PERMISSION_RESOURCE_LABELS" in source
    assert "PERMISSION_ACTION_LABELS" in source
    assert "permissionResourceLabel(resource)" in source
    assert "permissionActionLabel(action)" in source
    assert "`${group} (${count})`" not in source
    assert "alerts (2)" not in source
