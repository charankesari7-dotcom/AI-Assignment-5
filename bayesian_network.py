"""
bayesian_network.py
-------------------
Bayesian Network Implementation — Student Exam Performance
Author: Student Submission

PROBLEM: Predict whether a student passes their exam based on:
  - StudyHours  : Did the student study enough? (True/False)
  - Attendance  : Did the student have good attendance? (True/False)
  - Difficulty  : Is the exam hard? (True/False)
  - Passes      : Does the student pass? (True/False)

NETWORK STRUCTURE (DAG):
  StudyHours ─────────┐
                       ▼
  Attendance ────────► Passes
                       ▲
  Difficulty ──────────┘

So the conditional probability is: P(Passes | StudyHours, Attendance, Difficulty)

HOW A BAYESIAN NETWORK WORKS:
  1. Each node has a prior probability (if no parents) or a
     Conditional Probability Table (CPT) given its parents.
  2. Inference computes the probability of a query variable
     given observed evidence, using Bayes' theorem and
     marginalization.
"""


# ─── Prior Probabilities ──────────────────────────────────────────────────────

P_STUDY = {True: 0.60, False: 0.40}   # P(StudyHours=T) = 60%
P_ATTEND = {True: 0.70, False: 0.30}  # P(Attendance=T) = 70%
P_DIFF = {True: 0.40, False: 0.60}    # P(Difficulty=T) = 40%

# ─── Conditional Probability Table for Passes ────────────────────────────────
# P(Passes=True | StudyHours, Attendance, Difficulty)
# Keys: (study, attend, difficulty)

CPT_PASSES = {
    # (study, attend, difficulty) → P(Pass=True)
    (True,  True,  False): 0.95,   # studied, attended, easy   → very likely
    (True,  True,  True):  0.80,   # studied, attended, hard   → likely
    (True,  False, False): 0.70,   # studied, missed, easy     → moderate
    (True,  False, True):  0.50,   # studied, missed, hard     → 50/50
    (False, True,  False): 0.50,   # didn't study, attended, easy  → 50/50
    (False, True,  True):  0.25,   # didn't study, attended, hard  → unlikely
    (False, False, False): 0.20,   # didn't study, missed, easy    → low
    (False, False, True):  0.05,   # didn't study, missed, hard    → very low
}


# ─── Inference Engine ─────────────────────────────────────────────────────────

def p_passes(study, attend, difficulty):
    """P(Passes=True | study, attend, difficulty) from CPT."""
    return CPT_PASSES[(study, attend, difficulty)]


def p_not_passes(study, attend, difficulty):
    """P(Passes=False | study, attend, difficulty)."""
    return 1 - p_passes(study, attend, difficulty)


def joint_probability(study, attend, difficulty, passes):
    """
    Compute the joint probability:
    P(Study, Attend, Difficulty, Passes) =
      P(Study) × P(Attend) × P(Difficulty) × P(Passes | Study, Attend, Difficulty)
    """
    p_s = P_STUDY[study]
    p_a = P_ATTEND[attend]
    p_d = P_DIFF[difficulty]
    p_p = p_passes(study, attend, difficulty) if passes else p_not_passes(study, attend, difficulty)
    return p_s * p_a * p_d * p_p


def enumerate_all():
    """
    Enumerate all combinations of variables.
    Returns a list of (study, attend, difficulty, passes, joint_prob).
    """
    rows = []
    for study in [True, False]:
        for attend in [True, False]:
            for diff in [True, False]:
                for passes in [True, False]:
                    jp = joint_probability(study, attend, diff, passes)
                    rows.append((study, attend, diff, passes, jp))
    return rows


def query_pass_probability(evidence=None):
    """
    Compute P(Passes=True | evidence) using enumeration inference.

    evidence : dict with optional keys 'study', 'attend', 'difficulty'
               mapping to True/False.
               If a variable is not in evidence, it is marginalized out.

    Returns: float — probability of passing given evidence
    """
    if evidence is None:
        evidence = {}

    total_pass = 0.0
    total = 0.0

    for study in [True, False]:
        if 'study' in evidence and study != evidence['study']:
            continue
        for attend in [True, False]:
            if 'attend' in evidence and attend != evidence['attend']:
                continue
            for diff in [True, False]:
                if 'difficulty' in evidence and diff != evidence['difficulty']:
                    continue

                jp_pass = joint_probability(study, attend, diff, True)
                jp_fail = joint_probability(study, attend, diff, False)

                total_pass += jp_pass
                total      += jp_pass + jp_fail

    if total == 0:
        return 0.0
    return total_pass / total


def query_marginal(variable):
    """
    Compute the marginal probability of a root variable.
    Returns {True: p, False: 1-p}
    """
    if variable == 'study':
        return P_STUDY
    elif variable == 'attend':
        return P_ATTEND
    elif variable == 'difficulty':
        return P_DIFF
    else:
        p_true = query_pass_probability()
        return {True: p_true, False: 1 - p_true}


# ─── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Bayesian Network: Student Exam Performance")
    print("=" * 60)

    print("\nPrior Probabilities:")
    print(f"  P(StudyHours=T)  = {P_STUDY[True]:.2f}")
    print(f"  P(Attendance=T)  = {P_ATTEND[True]:.2f}")
    print(f"  P(Difficulty=T)  = {P_DIFF[True]:.2f}")

    print("\nSample CPT entries for P(Pass=True | ...):")
    for key, val in CPT_PASSES.items():
        s, a, d = key
        print(f"  Study={str(s):<5} Attend={str(a):<5} Difficult={str(d):<5}  →  {val:.2f}")

    print("\n─── Inference Results ───")

    p1 = query_pass_probability()
    print(f"\n1. P(Pass) [no evidence]                     = {p1:.4f} ({p1*100:.1f}%)")

    p2 = query_pass_probability({'study': True})
    print(f"2. P(Pass | Studied=True)                    = {p2:.4f} ({p2*100:.1f}%)")

    p3 = query_pass_probability({'study': False})
    print(f"3. P(Pass | Studied=False)                   = {p3:.4f} ({p3*100:.1f}%)")

    p4 = query_pass_probability({'study': True, 'attend': True, 'difficulty': False})
    print(f"4. P(Pass | Study=T, Attend=T, Hard=F)       = {p4:.4f} ({p4*100:.1f}%)")

    p5 = query_pass_probability({'study': False, 'attend': False, 'difficulty': True})
    print(f"5. P(Pass | Study=F, Attend=F, Hard=T)       = {p5:.4f} ({p5*100:.1f}%)")

    p6 = query_pass_probability({'difficulty': True})
    print(f"6. P(Pass | Exam is Hard)                    = {p6:.4f} ({p6*100:.1f}%)")

    p7 = query_pass_probability({'attend': True, 'difficulty': False})
    print(f"7. P(Pass | Attend=T, Hard=F)                = {p7:.4f} ({p7*100:.1f}%)")
