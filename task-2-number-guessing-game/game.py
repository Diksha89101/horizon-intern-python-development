import random


class NumberGuessingGame:
    """A number guessing game with three difficulty levels."""

    DIFFICULTIES = {
        "easy": {"max_number": 10, "max_attempts": 5},
        "medium": {"max_number": 50, "max_attempts": 7},
        "hard": {"max_number": 100, "max_attempts": 10},
    }

    def __init__(self, difficulty="medium"):
        difficulty = difficulty.lower()

        if difficulty not in self.DIFFICULTIES:
            raise ValueError(
                "Invalid difficulty. Choose easy, medium, or hard."
            )

        self.difficulty = difficulty
        settings = self.DIFFICULTIES[difficulty]

        self.max_number = settings["max_number"]
        self.max_attempts = settings["max_attempts"]
        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        self.guesses = []
        self.finished = False
        self.won = False

    def make_guess(self, guess):
        """Process a guess and return feedback."""

        if self.finished:
            raise RuntimeError("The game has already finished.")

        if not isinstance(guess, int) or isinstance(guess, bool):
            raise ValueError("Guess must be an integer.")

        if not 1 <= guess <= self.max_number:
            raise ValueError(
                f"Guess must be between 1 and {self.max_number}."
            )

        self.attempts += 1
        self.guesses.append(guess)

        if guess == self.secret_number:
            self.finished = True
            self.won = True
            return "correct"

        if self.attempts >= self.max_attempts:
            self.finished = True
            return "game_over"

        if guess < self.secret_number:
            return "too_low"

        return "too_high"

    def get_status(self):
        """Return the current game status."""

        return {
            "difficulty": self.difficulty,
            "max_number": self.max_number,
            "max_attempts": self.max_attempts,
            "attempts": self.attempts,
            "remaining_attempts": self.max_attempts - self.attempts,
            "guesses": self.guesses.copy(),
            "finished": self.finished,
            "won": self.won,
        }


def main():
    print("\n========== NUMBER GUESSING GAME ==========")
    print("Choose your difficulty:")
    print("1. Easy   (1-10, 5 attempts)")
    print("2. Medium (1-50, 7 attempts)")
    print("3. Hard   (1-100, 10 attempts)")

    difficulty_options = {
        "1": "easy",
        "2": "medium",
        "3": "hard",
    }

    while True:
        choice = input("Enter your choice (1-3): ").strip()

        if choice in difficulty_options:
            difficulty = difficulty_options[choice]
            break

        print("Invalid choice. Please enter 1, 2, or 3.")

    game = NumberGuessingGame(difficulty)

    print(
        f"\nI'm thinking of a number between 1 and {game.max_number}."
    )
    print(f"You have {game.max_attempts} attempts. Good luck!")

    while not game.finished:
        raw_guess = input("\nEnter your guess: ").strip()

        try:
            guess = int(raw_guess)
            result = game.make_guess(guess)

            if result == "correct":
                print(
                    f"Congratulations! You guessed {game.secret_number} "
                    f"in {game.attempts} attempt(s)."
                )
            elif result == "too_low":
                print("Too low! Try a higher number.")
            elif result == "too_high":
                print("Too high! Try a lower number.")
            elif result == "game_over":
                print("Game over! You've used all your attempts.")
                print(f"The correct number was {game.secret_number}.")

            if not game.finished:
                print(
                    f"Attempts remaining: "
                    f"{game.max_attempts - game.attempts}"
                )

        except ValueError as error:
            print(f"Invalid input: {error}")

    print("\n========== GAME SUMMARY ==========")
    print(f"Difficulty: {game.difficulty.title()}")
    print(f"Attempts used: {game.attempts}")
    print(f"Result: {'Won' if game.won else 'Lost'}")
    print(f"Your guesses: {game.guesses}")


if __name__ == "__main__":
    main()
