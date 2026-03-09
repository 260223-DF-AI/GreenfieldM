import pytest
from generators import read_lines, batch, filter_by, process_files_parallel

def test_batch_correct_sizes():
    """Batch should yield correct batch sizes."""
    result = list(batch(range(7), 3))
    assert len(result) == 3
    assert len(result[0]) == 3
    assert len(result[2]) == 1

def test_filter_by_predicate():
    """Filter should only yield matching items."""
    result = list(filter_by(range(10), lambda x: x % 2 == 0))
    assert result == [0, 2, 4, 6, 8]

def test_read_lines_skips_empty(tmp_path):
    """Read lines should skip empty lines."""
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello\n\nworld\n   \npython\n", encoding="utf-8")

    result = list(read_lines(file_path))
    assert result == ["hello", "world", "python"]

def test_batch_raises_for_invalid_size():
    with pytest.raises(ValueError):
        list(batch([1, 2, 3], 0))

def test_process_files_parallel(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("one\ntwo\n", encoding="utf-8")
    file2.write_text("three\n", encoding="utf-8")

    def count_lines(path):
        with open(path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    results = list(process_files_parallel([str(file1), str(file2)], count_lines, max_workers=2))

    assert sorted(results) == [1, 2]
