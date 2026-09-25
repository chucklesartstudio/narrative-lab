from backend.app.evaluation.screenplay_alignment import evaluate_dataset


def test_synthetic_alignment_dataset_matches_expected_labels_and_spans():
    report = evaluate_dataset()

    assert report["case_count"] == 8
    assert report["all_cases_pass"] is True
    assert report["block_classification"]["micro_precision"] == 1.0
    assert report["block_classification"]["micro_recall"] == 1.0
    assert report["scene_boundary"]["precision"] == 1.0
    assert report["scene_boundary"]["recall"] == 1.0
    assert report["span_round_trip"]["rate"] == 1.0
    assert all(report["source_revision_identity_stability"].values())


def test_review_cases_and_diagnostic_counts_are_reported():
    report = evaluate_dataset()

    assert report["cases_requiring_human_review"] == [
        "odd_indentation",
        "missing_heading",
        "malformed_heading",
    ]
    assert report["diagnostics_by_type"] == {
        "ambiguous_character_cue": 1,
        "missing_scene_heading": 2,
        "pre_scene_text": 4,
        "suspicious_scene_heading": 1,
    }
