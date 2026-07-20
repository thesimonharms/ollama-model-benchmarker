from model_solution import find_max

def test_max():
    assert find_max([1, 2, 3]) == 3
    assert find_max([-10, -5, -20]) == -5
    assert find_max([0]) == 0

if __name__ == "__main__":
    try:
        test_max()
        print("Passed")
    except Exception as e:
        print(f"Failed: {e}")
        exit(1)
