"""
tests/test_bayes.py
-------------------
Test cases for the Bayesian Network implementation.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bayesian_network import (
    query_pass_probability, joint_probability,
    enumerate_all, P_STUDY, P_ATTEND, P_DIFF, CPT_PASSES
)


def test_prior_probabilities_sum_to_one():
    """Prior probabilities must sum to 1."""
    assert abs(P_STUDY[True] + P_STUDY[False] - 1.0) < 1e-9
    assert abs(P_ATTEND[True] + P_ATTEND[False] - 1.0) < 1e-9
    assert abs(P_DIFF[True] + P_DIFF[False] - 1.0) < 1e-9
    print("PASS: test_prior_probabilities_sum_to_one")


def test_all_joint_probabilities_sum_to_one():
    """Sum of all 16 joint probabilities must equal 1."""
    rows = enumerate_all()
    total = sum(jp for *_, jp in rows)
    assert abs(total - 1.0) < 1e-9, f"Total joint P = {total}, expected 1.0"
    print("PASS: test_all_joint_probabilities_sum_to_one")


def test_pass_probability_between_0_and_1():
    """All queried probabilities must be in [0, 1]."""
    evidences = [
        {},
        {'study': True},
        {'study': False},
        {'attend': True},
        {'difficulty': True},
        {'study': True, 'attend': True, 'difficulty': False},
        {'study': False, 'attend': False, 'difficulty': True},
    ]
    for ev in evidences:
        p = query_pass_probability(ev)
        assert 0.0 <= p <= 1.0, f"P={p} out of range for evidence {ev}"
    print("PASS: test_pass_probability_between_0_and_1")


def test_studying_increases_pass_rate():
    """P(Pass|Study=T) must be greater than P(Pass|Study=F)."""
    p_study   = query_pass_probability({'study': True})
    p_no_study = query_pass_probability({'study': False})
    assert p_study > p_no_study, (
        f"Expected P(Pass|Study=T)={p_study} > P(Pass|Study=F)={p_no_study}"
    )
    print(f"PASS: test_studying_increases_pass_rate "
          f"({p_study:.3f} > {p_no_study:.3f})")


def test_hard_exam_reduces_pass_rate():
    """P(Pass|Hard=T) must be less than P(Pass|Hard=F)."""
    p_easy = query_pass_probability({'difficulty': False})
    p_hard = query_pass_probability({'difficulty': True})
    assert p_hard < p_easy, (
        f"Expected P(Pass|Hard=T)={p_hard} < P(Pass|Hard=F)={p_easy}"
    )
    print(f"PASS: test_hard_exam_reduces_pass_rate "
          f"({p_hard:.3f} < {p_easy:.3f})")


def test_best_case_scenario():
    """Study + Attend + Easy should yield very high pass probability."""
    p = query_pass_probability({'study': True, 'attend': True, 'difficulty': False})
    assert p > 0.90, f"Expected >0.90 for best-case, got {p:.4f}"
    print(f"PASS: test_best_case_scenario (P={p:.4f})")


def test_worst_case_scenario():
    """No study + No attend + Hard should yield very low pass probability."""
    p = query_pass_probability({'study': False, 'attend': False, 'difficulty': True})
    assert p < 0.15, f"Expected <0.15 for worst-case, got {p:.4f}"
    print(f"PASS: test_worst_case_scenario (P={p:.4f})")


def test_joint_probability_is_non_negative():
    """All joint probabilities must be >= 0."""
    rows = enumerate_all()
    for row in rows:
        assert row[-1] >= 0, f"Negative joint probability: {row}"
    print("PASS: test_joint_probability_is_non_negative")


if __name__ == "__main__":
    print("Running Bayesian Network Tests...\n")
    test_prior_probabilities_sum_to_one()
    test_all_joint_probabilities_sum_to_one()
    test_pass_probability_between_0_and_1()
    test_studying_increases_pass_rate()
    test_hard_exam_reduces_pass_rate()
    test_best_case_scenario()
    test_worst_case_scenario()
    test_joint_probability_is_non_negative()
    print("\nAll Bayesian Network tests passed!")
