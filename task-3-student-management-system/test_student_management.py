import json

import pytest

from student_management import StudentManagementSystem


@pytest.fixture
def system(tmp_path):
    return StudentManagementSystem(tmp_path / "students.json")


def test_add_student(system):
    student = system.add_student("S001", "Asha", 20, "Python")

    assert student["student_id"] == "S001"
    assert student["name"] == "Asha"
    assert student["age"] == 20
    assert student["course"] == "Python"


def test_duplicate_student_id(system):
    system.add_student("S001", "Asha", 20, "Python")

    with pytest.raises(ValueError):
        system.add_student("S001", "Ravi", 21, "Java")


def test_reject_empty_name(system):
    with pytest.raises(ValueError):
        system.add_student("S001", " ", 20, "Python")


def test_reject_invalid_age(system):
    with pytest.raises(ValueError):
        system.add_student("S001", "Asha", 0, "Python")


def test_reject_boolean_age(system):
    with pytest.raises(ValueError):
        system.add_student("S001", "Asha", True, "Python")


def test_get_student(system):
    system.add_student("S001", "Asha", 20, "Python")

    assert system.get_student("S001")["name"] == "Asha"


def test_missing_student(system):
    with pytest.raises(KeyError):
        system.get_student("UNKNOWN")


def test_get_all_students(system):
    system.add_student("S001", "Asha", 20, "Python")
    system.add_student("S002", "Ravi", 21, "Java")

    assert len(system.get_all_students()) == 2


def test_update_student(system):
    system.add_student("S001", "Asha", 20, "Python")

    updated = system.update_student("S001", name="Asha Rao", age=21)

    assert updated["name"] == "Asha Rao"
    assert updated["age"] == 21
    assert updated["course"] == "Python"


def test_update_rejects_invalid_age(system):
    system.add_student("S001", "Asha", 20, "Python")

    with pytest.raises(ValueError):
        system.update_student("S001", age=-1)

    assert system.get_student("S001")["age"] == 20


def test_delete_student(system):
    system.add_student("S001", "Asha", 20, "Python")

    assert system.delete_student("S001") is True
    assert system.get_all_students() == []


def test_delete_missing_student(system):
    with pytest.raises(KeyError):
        system.delete_student("UNKNOWN")


def test_persistence_between_instances(tmp_path):
    file_path = tmp_path / "students.json"

    first = StudentManagementSystem(file_path)
    first.add_student("S001", "Asha", 20, "Python")

    second = StudentManagementSystem(file_path)

    assert second.get_student("S001")["name"] == "Asha"


def test_json_file_contains_student_data(system):
    system.add_student("S001", "Asha", 20, "Python")

    with system.storage_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["S001"]["course"] == "Python"


def test_get_all_students_returns_copies(system):
    system.add_student("S001", "Asha", 20, "Python")

    students = system.get_all_students()
    students[0]["name"] = "Changed"

    assert system.get_student("S001")["name"] == "Asha"


def test_student_id_is_trimmed(system):
    system.add_student(" S001 ", "Asha", 20, "Python")

    assert system.get_student("S001")["student_id"] == "S001"
