"""Stable parcel sorting algorithms: insertion sort and bubble sort."""

def _parcel_key(parcel, sort_by="priority"):
    """Return a key that sorts highest priority first or earliest deadline first."""
    if sort_by == "priority":
        return (-int(parcel["priority"]), int(parcel["deadline"]), str(parcel["id"]))
    if sort_by == "deadline":
        return (int(parcel["deadline"]), -int(parcel["priority"]), str(parcel["id"]))
    raise ValueError("sort_by must be 'priority' or 'deadline'")

def insertion_sort_parcels(parcels, sort_by="priority"):
    """Return a new list sorted using insertion sort. Original list is not changed."""
    result = [dict(p) for p in parcels]
    for i in range(1, len(result)):
        key_parcel = result[i]
        key = _parcel_key(key_parcel, sort_by)
        j = i - 1
        while j >= 0 and _parcel_key(result[j], sort_by) > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key_parcel
    return result

def bubble_sort_parcels(parcels, sort_by="priority"):
    """Return a new list sorted using optimized bubble sort."""
    result = [dict(p) for p in parcels]
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if _parcel_key(result[j], sort_by) > _parcel_key(result[j + 1], sort_by):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result
