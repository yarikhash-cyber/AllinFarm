from allinfarm_engine import engine_info


def test_engine_info_reports_versions() -> None:
    assert engine_info() == {"engine": "0.1.0", "units": "0.1.0"}
