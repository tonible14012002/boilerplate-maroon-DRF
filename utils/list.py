def is_subset_list(superset, subset):
    """Check if all item in list is included in another list."""
    set_a = set(superset)
    set_b = set(subset)
    return set_b.issubset(set_a)
