"""0/1 Knapsack using bottom-up dynamic programming."""

def solve_knapsack(parcels, capacity):
    """
    Select the parcel subset with maximum total value without exceeding capacity.
    Parcel weights and capacity must be non-negative integers.
    Returns selected_parcels, total_weight, total_value, dp_table.
    """
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("Capacity must be a non-negative integer.")

    items = [dict(p) for p in parcels]
    for p in items:
        if not isinstance(p.get("weight"), int) or p["weight"] < 0:
            raise ValueError(f"Parcel {p.get('id')} must have a non-negative integer weight.")
        if not isinstance(p.get("value"), (int, float)) or p["value"] < 0:
            raise ValueError(f"Parcel {p.get('id')} must have a non-negative value.")

    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = items[i - 1]["weight"]
        value = items[i - 1]["value"]
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                take_value = value + dp[i - 1][current_capacity - weight]
                if take_value > dp[i][current_capacity]:
                    dp[i][current_capacity] = take_value

    selected = []
    remaining = capacity
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            parcel = items[i - 1]
            selected.append(parcel)
            remaining -= parcel["weight"]

    selected.reverse()
    total_weight = sum(p["weight"] for p in selected)
    total_value = sum(p["value"] for p in selected)
    return selected, total_weight, total_value, dp
