"""
Assignment 1 - Reliability Engineering and Failure Analysis
"""

from collections import defaultdict

# ---------------------------------------------------------------
# Input data (as given in the assignment)
# ---------------------------------------------------------------
T = 720.0  # total operating period, hours (30 days)

# (event_no, component, failure_time_h, repair_completed_h, duration_h)
events = [
    (1, "Application Server A", 38, 40, 2),
    (2, "Primary Database", 91, 95, 4),
    (3, "Campus Network", 143, 144, 1),
    (4, "Application Server B", 201, 203, 2),
    (5, "Primary Database", 287, 291, 4),
    (6, "Load Balancer", 356, 357, 1),
    (7, "Application Server A", 411, 413, 2),
    (8, "Campus Network", 478, 480, 2),
    (9, "Primary Database", 529, 534, 5),
    (10, "Application Server B", 601, 603, 2),
    (11, "Application Server A", 654, 655, 1),
    (12, "Load Balancer", 689, 690, 1),
]

component_reliability = {
    "Load Balancer": 0.995,
    "Application Server A": 0.970,
    "Application Server B": 0.970,
    "Primary Database": 0.980,
    "Standby Database": 0.990,
    "Campus Network": 0.995,
}

# ---------------------------------------------------------------
# Part A: Reliability metrics
# ---------------------------------------------------------------
def part_a():
    n = len(events)
    total_downtime = sum(e[4] for e in events)
    total_uptime = T - total_downtime
    availability = total_uptime / T
    mttf = total_uptime / n
    mttr = total_downtime / n
    mtbf = T / n  # equivalently mttf + mttr

    print("=" * 60)
    print("PART A: RELIABILITY METRICS")
    print("=" * 60)
    print(f"Number of failures (n)        = {n}")
    print(f"Total downtime                = {total_downtime} h")
    print(f"Total uptime                  = {total_uptime} h")
    print(f"Availability                  = {availability:.4f}  ({availability*100:.2f}%)")
    print(f"MTTF (uptime / n)             = {mttf:.2f} h")
    print(f"MTTR (downtime / n)           = {mttr:.2f} h")
    print(f"MTBF (T / n = MTTF + MTTR)    = {mtbf:.2f} h")

    comp_downtime = defaultdict(float)
    comp_count = defaultdict(int)
    for e in events:
        comp_downtime[e[1]] += e[4]
        comp_count[e[1]] += 1

    print("\nDowntime and failure count by component:")
    for c, d in sorted(comp_downtime.items(), key=lambda x: -x[1]):
        print(f"  {c:<24s} downtime={d:5.1f} h   failures={comp_count[c]}")

    return dict(total_downtime=total_downtime, total_uptime=total_uptime,
                availability=availability, mttf=mttf, mttr=mttr, mtbf=mtbf)


# ---------------------------------------------------------------
# Part B: Reliability Block Diagram
# Load Balancer -> [A OR B] -> [Primary OR Standby] -> Campus Network
# ---------------------------------------------------------------
def part_b():
    r = component_reliability
    r_app = 1 - (1 - r["Application Server A"]) * (1 - r["Application Server B"])
    r_db = 1 - (1 - r["Primary Database"]) * (1 - r["Standby Database"])
    r_overall = r["Load Balancer"] * r_app * r_db * r["Campus Network"]

    print("\n" + "=" * 60)
    print("PART B: RELIABILITY BLOCK DIAGRAM")
    print("=" * 60)
    print(f"R_application (A OR B)        = 1-(1-{r['Application Server A']})"
          f"*(1-{r['Application Server B']}) = {r_app:.4f}")
    print(f"R_database (Primary OR Standby)= 1-(1-{r['Primary Database']})"
          f"*(1-{r['Standby Database']}) = {r_db:.4f}")
    print(f"R_load_balancer (single)      = {r['Load Balancer']}")
    print(f"R_network (single)            = {r['Campus Network']}")
    print(f"R_overall (series product)    = {r_overall:.4f}  ({r_overall*100:.3f}%)")
    return dict(r_app=r_app, r_db=r_db, r_overall=r_overall)


# ---------------------------------------------------------------
# Part C: FMEA - Risk Priority Number = Severity x Occurrence x Detection
# ---------------------------------------------------------------
def part_c():
    # (component, Severity 1-10, Occurrence 1-10, Detection 1-10)
    fmea = [
        ("Load Balancer", 9, 3, 4),
        ("Application Server A", 4, 6, 3),
        ("Application Server B", 4, 5, 3),
        ("Primary Database", 7, 7, 5),
        ("Standby Database", 6, 1, 8),
        ("Campus Network", 8, 4, 3),
    ]
    print("\n" + "=" * 60)
    print("PART C: FMEA - RISK PRIORITY NUMBER (RPN = S x O x D)")
    print("=" * 60)
    results = []
    for comp, s, o, d in fmea:
        rpn = s * o * d
        results.append((comp, s, o, d, rpn))
        print(f"  {comp:<22s} S={s} O={o} D={d}  RPN={rpn}")

    print("\nRanked by RPN (highest first):")
    for comp, s, o, d, rpn in sorted(results, key=lambda x: -x[4]):
        print(f"  {rpn:4d}  {comp}")
    return results


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
