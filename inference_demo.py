"""
inference_demo.py
-----------------
Extended Inference Demo for Bayesian Network
Author: Student Submission

This file demonstrates:
  1. Sensitivity analysis — how each variable affects pass probability
  2. Most likely explanation — which combination has highest joint prob
  3. Comparison table of all CPT entries with inferred probabilities
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BayesianNetworks'))
sys.path.insert(0, os.path.dirname(__file__))

from bayesian_network import (
    query_pass_probability, joint_probability, enumerate_all,
    CPT_PASSES, P_STUDY, P_ATTEND, P_DIFF
)


def sensitivity_analysis():
    """
    Shows how much each individual variable changes the pass probability.
    """
    print("─── Sensitivity Analysis ───────────────────────────────────")
    base = query_pass_probability()
    print(f"  Base P(Pass) = {base:.4f}\n")

    variables = {
        'study': [True, False],
        'attend': [True, False],
        'difficulty': [True, False],
    }

    for var, values in variables.items():
        for val in values:
            p = query_pass_probability({var: val})
            delta = p - base
            direction = "↑" if delta > 0 else "↓"
            print(f"  {var}={str(val):<5}  → P(Pass)={p:.4f}  (Δ={delta:+.4f} {direction})")
        print()


def most_likely_explanation():
    """
    Find the combination of (study, attend, difficulty) that
    maximizes joint probability of passing.
    """
    print("─── Most Likely Passing Scenario ────────────────────────────")
    rows = [(s, a, d, jp)
            for s, a, d, passes, jp in enumerate_all() if passes]
    rows.sort(key=lambda x: x[3], reverse=True)

    print("  Top 3 scenarios with highest P(Study, Attend, Difficulty, Pass=T):\n")
    for s, a, d, jp in rows[:3]:
        print(f"  Study={str(s):<5} Attend={str(a):<5} Hard={str(d):<5} "
              f"→ Joint P = {jp:.6f}")
    print()


def full_cpt_with_inference():
    """
    Print the full CPT alongside the inferred conditional probabilities.
    Verifies the CPT values match direct queries.
    """
    print("─── Full CPT Verification ───────────────────────────────────")
    print(f"  {'Study':<7} {'Attend':<8} {'Hard':<7} {'CPT P(Pass)':<15} {'Inferred':<10}")
    print("  " + "-" * 55)

    for (s, a, d), cpt_val in CPT_PASSES.items():
        inferred = query_pass_probability({'study': s, 'attend': a, 'difficulty': d})
        match = "✓" if abs(cpt_val - inferred) < 0.001 else "✗"
        print(f"  {str(s):<7} {str(a):<8} {str(d):<7} {cpt_val:<15.3f} {inferred:.3f}  {match}")
    print()


def scenario_comparison():
    """
    Simulate two student profiles and compare their pass probabilities.
    """
    print("─── Student Profile Comparison ──────────────────────────────")

    profiles = {
        "Dedicated Student (studies + attends)": {"study": True, "attend": True},
        "Lazy Student (no study + skips class)": {"study": False, "attend": False},
        "Crammer (studies but skips class)":     {"study": True, "attend": False},
        "Lucky Student (attends, doesn't study)":{"study": False, "attend": True},
    }

    for name, evidence in profiles.items():
        p_easy = query_pass_probability({**evidence, "difficulty": False})
        p_hard = query_pass_probability({**evidence, "difficulty": True})
        print(f"  {name}")
        print(f"    Easy exam: {p_easy*100:.1f}%  |  Hard exam: {p_hard*100:.1f}%\n")


if __name__ == "__main__":
    print("=" * 60)
    print("  BAYESIAN NETWORK: Extended Inference Demo")
    print("  Problem: Student Exam Performance Prediction")
    print("=" * 60)
    print()

    sensitivity_analysis()
    most_likely_explanation()
    full_cpt_with_inference()
    scenario_comparison()
