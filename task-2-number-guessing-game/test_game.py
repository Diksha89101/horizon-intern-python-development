import pytest

from game import NumberGuessingGame


def test_easy_difficulty():
    game = NumberGuessingGame("easy")
    assert game.max_number == 10
    assert game.max_attempts == 5


def test_medium_difficulty():
    game = NumberGuessingGame("medium")
    assert game.max_number == 50
    assert game.max_attempts == 7


def test_hard_difficulty():
    game = NumberGuessingGame("hard")
    assert game.max_number == 100
    assert game.max_attempts == 10


def test_invalid_difficulty():
    with pytest.raises(ValueError):
        NumberGuessingGame("expert")


def test_correct_guess():
    game = NumberGuessingGame("easy")
    game.secret_number = 7

    assert game.make_guess(7) == "correct"
    assert game.won is True
    assert game.finished is True


def test_guess_too_low():
    game = NumberGuessingGame("easy")
    game.secret_number = 8

    assert game.make_guess(3) == "too_low"


def test_guess_too_high():
    game = NumberGuessingGame("easy")
    game.secret_number = 3

    assert game.make_guess(8) == "too_high"


def test_guess_out_of_range():
    game = NumberGuessingGame("easy")

    with pytest.raises(ValueError):
        game.make_guess(11)

    assert game.attempts == 0


def test_non_integer_guess():
    game = NumberGuessingGame("easy")

    with pytest.raises(ValueError):
        game.make_guess(2.5)


def test_invalid_guess_does_not_consume_attempt():
    game = NumberGuessingGame("easy")

    with pytest.raises(ValueError):
        game.make_guess(0)

    assert game.attempts == 0


def test_game_over_after_maximum_attempts():
    game = NumberGuessingGame("easy")
    game.secret_number = 10

    for guess in [1, 2, 3, 4]:
        assert game.make_guess(guess) == "too_low"

    assert game.make_guess(5) == "game_over"
    assert game.finished is True
    assert game.won is False


def test_cannot_guess_after_game_finishes():
    game = NumberGuessingGame("easy")
    game.secret_number = 5

    assert game.make_guess(5) == "correct"

    with pytest.raises(RuntimeError):
        game.make_guess(4)


def test_status_contains_remaining_attempts():
    game = NumberGuessingGame("medium")
    game.secret_number = 30
    game.make_guess(10)

    status = game.get_status()

    assert status["attempts"] == 1
    assert status["remaining_attempts"] == 6
    assert status["guesses"] == [10]


def test_status_returns_a_copy_of_guesses():
    game = NumberGuessingGame("easy")
    game.secret_number = 8
    game.make_guess(3)

    status = game.get_status()
    status["guesses"].clear()

    assert game.get_status()["guesses"] == [3]


def test_case_insensitive_difficulty():
    game = NumberGuessingGame("EASY")
    assert game.difficulty == "easy"
