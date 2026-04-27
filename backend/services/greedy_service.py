import time
import copy


# ─── Fractional Knapsack ──────────────────────────────────────────────────────

def fractional_knapsack(deliveries, capacity):
    items = [(d.priority / d.weight, d.weight, d.priority, d) for d in deliveries]
    items.sort(key=lambda x: x[0], reverse=True)

    total_value = 0.0
    assigned = []
    remaining = capacity

    for ratio, weight, value, d in items:
        if remaining <= 0:
            break
        fraction = min(1.0, remaining / weight)
        taken_weight = fraction * weight
        taken_value = fraction * value
        total_value += taken_value
        remaining -= taken_weight
        assigned.append({
            "delivery": d.to_dict(),
            "fraction": round(fraction, 4),
            "weight_taken": round(taken_weight, 4),
            "value_taken": round(taken_value, 4),
        })

    return assigned, round(total_value, 4)


# ─── Job Scheduling with Deadlines ────────────────────────────────────────────

def job_scheduling(deliveries):
    jobs = sorted(deliveries, key=lambda d: d.priority, reverse=True)
    max_deadline = max(d.deadline for d in deliveries) if deliveries else 0
    slots = [None] * (max_deadline + 1)
    scheduled = []
    total_profit = 0

    for job in jobs:
        slot = min(job.deadline, max_deadline)
        while slot > 0 and slots[slot] is not None:
            slot -= 1
        if slot > 0:
            slots[slot] = job
            scheduled.append({"slot": slot, "delivery": job.to_dict()})
            total_profit += job.priority

    return scheduled, total_profit


# ─── Activity Selection ───────────────────────────────────────────────────────

def activity_selection(deliveries):
    # Treat deadline as finish time, priority as start time proxy
    acts = sorted(deliveries, key=lambda d: d.deadline)
    selected = []
    last_finish = -1

    for d in acts:
        start = max(0, d.deadline - d.priority)
        if start >= last_finish:
            selected.append(d)
            last_finish = d.deadline

    return [d.to_dict() for d in selected]


# ─── Service Entry Point ───────────────────────────────────────────────────────

def assign(deliveries, capacity=500):
    data = copy.deepcopy(deliveries)

    t0 = time.perf_counter()
    fk_assigned, fk_value = fractional_knapsack(data, capacity)
    t_fk = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    js_scheduled, js_profit = job_scheduling(data)
    t_js = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    act_selected = activity_selection(data)
    t_act = (time.perf_counter() - t0) * 1000

    return {
        "fractional_knapsack": {
            "assigned": fk_assigned,
            "total_value": fk_value,
            "count": len(fk_assigned),
            "time_ms": round(t_fk, 4),
        },
        "job_scheduling": {
            "scheduled": js_scheduled,
            "total_profit": js_profit,
            "count": len(js_scheduled),
            "time_ms": round(t_js, 4),
        },
        "activity_selection": {
            "selected": act_selected,
            "count": len(act_selected),
            "time_ms": round(t_act, 4),
        },
        "comparison": {
            "fractional_knapsack_ms": round(t_fk, 4),
            "job_scheduling_ms": round(t_js, 4),
            "activity_selection_ms": round(t_act, 4),
        },
    }
