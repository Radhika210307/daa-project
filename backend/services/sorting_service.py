import heapq
import time
import copy


# ─── Merge Sort (stable, sorts by deadline) ───────────────────────────────────

def merge_sort(arr, key_fn):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_fn)
    right = merge_sort(arr[mid:], key_fn)
    return _merge(left, right, key_fn)


def _merge(left, right, key_fn):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_fn(left[i]) <= key_fn(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ─── Quick Sort (sorts by priority) ───────────────────────────────────────────

def quick_sort(arr, key_fn, low=None, high=None):
    arr = list(arr)
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1
    _quick_sort_inplace(arr, key_fn, low, high)
    return arr


def _quick_sort_inplace(arr, key_fn, low, high):
    if low < high:
        pi = _partition(arr, key_fn, low, high)
        _quick_sort_inplace(arr, key_fn, low, pi - 1)
        _quick_sort_inplace(arr, key_fn, pi + 1, high)


def _partition(arr, key_fn, low, high):
    pivot = key_fn(arr[high])
    i = low - 1
    for j in range(low, high):
        if key_fn(arr[j]) >= pivot:  # descending: highest priority first
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ─── Heap-based Priority Queue (real-time scheduling) ─────────────────────────

class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, delivery):
        # Min-heap by (deadline, -priority) for scheduling
        heapq.heappush(self._heap, (delivery.deadline, -delivery.priority, self._counter, delivery))
        self._counter += 1

    def pop(self):
        _, _, _, delivery = heapq.heappop(self._heap)
        return delivery

    def peek(self):
        return self._heap[0][3] if self._heap else None

    def __len__(self):
        return len(self._heap)

    def to_sorted_list(self):
        temp = list(self._heap)
        temp.sort()
        return [item[3] for item in temp]


# ─── Service Functions ─────────────────────────────────────────────────────────

def run_merge_sort(deliveries):
    data = copy.deepcopy(deliveries)
    start = time.perf_counter()
    sorted_list = merge_sort(data, key_fn=lambda d: d.deadline)
    elapsed = (time.perf_counter() - start) * 1000
    return sorted_list, elapsed


def run_quick_sort(deliveries):
    data = copy.deepcopy(deliveries)
    start = time.perf_counter()
    sorted_list = quick_sort(data, key_fn=lambda d: d.priority)
    elapsed = (time.perf_counter() - start) * 1000
    return sorted_list, elapsed


def run_heap_sort(deliveries):
    data = copy.deepcopy(deliveries)
    start = time.perf_counter()
    pq = PriorityQueue()
    for d in data:
        pq.push(d)
    sorted_list = pq.to_sorted_list()
    elapsed = (time.perf_counter() - start) * 1000
    return sorted_list, elapsed


def prioritize(deliveries):
    merge_sorted, t_merge = run_merge_sort(deliveries)
    quick_sorted, t_quick = run_quick_sort(deliveries)
    heap_sorted, t_heap = run_heap_sort(deliveries)

    return {
        "merge_sort": {
            "sorted_by": "deadline",
            "result": [d.to_dict() for d in merge_sorted],
            "time_ms": round(t_merge, 4),
        },
        "quick_sort": {
            "sorted_by": "priority (desc)",
            "result": [d.to_dict() for d in quick_sorted],
            "time_ms": round(t_quick, 4),
        },
        "heap_sort": {
            "sorted_by": "deadline + priority",
            "result": [d.to_dict() for d in heap_sorted],
            "time_ms": round(t_heap, 4),
        },
        "comparison": {
            "merge_sort_ms": round(t_merge, 4),
            "quick_sort_ms": round(t_quick, 4),
            "heap_sort_ms": round(t_heap, 4),
        },
    }
