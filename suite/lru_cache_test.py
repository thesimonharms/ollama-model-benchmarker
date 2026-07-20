from model_solution import LRUCache # Assume the model names the class LRUCache

def test_lru():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3) # evicts key 2
    assert cache.get(2) == -1 or cache.get(2) is None
    assert cache.get(3) == 3

if __name__ == "__main__":
    try:
        test_lru()
        print("Passed")
    except Exception as e:
        print(f"Failed: {e}")
        exit(1)
