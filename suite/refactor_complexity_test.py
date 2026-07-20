from model_solution import find_duplicates

def test_dups():
    assert sorted(find_duplicates([1, 2, 3, 1])) == [1]
    assert sorted(find_duplicates([1, 1, 2, 2, 3, 3])) == [1, 2, 3]
    assert find_duplicates([1, 2, 3]) == []

if __name__ == "__main__":
    try:
        test_dups()
        print("Passed")
    except Exception as e:
        print(f"Failed: {e}")
        exit(1)
