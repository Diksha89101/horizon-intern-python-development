import math


class AdvancedCalculator:
    """Calculator with arithmetic and advanced mathematical operations."""

    def __init__(self):
        self.history = []

    def _record(self, operation, result):
        self.history.append({"operation": operation, "result": result})
        return result

    def add(self, a, b):
        return self._record(f"{a} + {b}", a + b)

    def subtract(self, a, b):
        return self._record(f"{a} - {b}", a - b)

    def multiply(self, a, b):
        return self._record(f"{a} * {b}", a * b)

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return self._record(f"{a} / {b}", a / b)

    def power(self, base, exponent):
        result = base ** exponent

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")

        if isinstance(result, float) and not math.isfinite(result):
            raise OverflowError("The result is too large.")

        return self._record(f"{base} ** {exponent}", result)

    def modulus(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot calculate modulus with zero.")
        return self._record(f"{a} % {b}", a % b)

    def square_root(self, number):
        if number < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return self._record(f"sqrt({number})", math.sqrt(number))

    def factorial(self, number):
        if not isinstance(number, int) or isinstance(number, bool):
            raise ValueError("Factorial requires an integer.")

        if number < 0:
            raise ValueError("Factorial requires a non-negative integer.")

        return self._record(f"{number}!", math.factorial(number))

    def sine(self, degrees):
        result = math.sin(math.radians(degrees))
        return self._record(f"sin({degrees} degrees)", result)

    def cosine(self, degrees):
        result = math.cos(math.radians(degrees))
        return self._record(f"cos({degrees} degrees)", result)

    def tangent(self, degrees):
        radians = math.radians(degrees)

        if math.isclose(math.cos(radians), 0.0, abs_tol=1e-12):
            raise ValueError("Tangent is undefined at this angle.")

        return self._record(
            f"tan({degrees} degrees)",
            math.tan(radians),
        )

    def natural_log(self, number):
        if number <= 0:
            raise ValueError("Natural logarithm requires a positive number.")
        return self._record(f"ln({number})", math.log(number))

    def log10(self, number):
        if number <= 0:
            raise ValueError("Base-10 logarithm requires a positive number.")
        return self._record(f"log10({number})", math.log10(number))

    def show_history(self):
        return self.history.copy()


def main():
    calculator = AdvancedCalculator()

    operations = {
        "1": ("Addition", calculator.add, 2),
        "2": ("Subtraction", calculator.subtract, 2),
        "3": ("Multiplication", calculator.multiply, 2),
        "4": ("Division", calculator.divide, 2),
        "5": ("Power", calculator.power, 2),
        "6": ("Modulus", calculator.modulus, 2),
        "7": ("Square root", calculator.square_root, 1),
        "8": ("Factorial", calculator.factorial, 1),
        "9": ("Sine (degrees)", calculator.sine, 1),
        "10": ("Cosine (degrees)", calculator.cosine, 1),
        "11": ("Tangent (degrees)", calculator.tangent, 1),
        "12": ("Natural logarithm", calculator.natural_log, 1),
        "13": ("Base-10 logarithm", calculator.log10, 1),
    }

    while True:
        print("\n========== ADVANCED CALCULATOR ==========")

        for key, (name, _, _) in operations.items():
            print(f"{key}. {name}")

        print("14. View calculation history")
        print("0. Exit")

        choice = input("\nChoose an operation: ").strip()

        if choice == "0":
            print("Thank you for using Advanced Calculator!")
            break

        if choice == "14":
            history = calculator.show_history()

            if not history:
                print("No calculations yet.")
            else:
                print("\nCalculation History:")
                for item in history:
                    print(f"{item['operation']} = {item['result']}")
            continue

        if choice not in operations:
            print("Invalid choice. Please select a listed option.")
            continue

        name, function, argument_count = operations[choice]

        try:
            if argument_count == 2:
                a = float(input("Enter the first number: "))
                b = float(input("Enter the second number: "))
                result = function(a, b)
            else:
                value = input("Enter a number: ").strip()

                if choice == "8":
                    if not value.lstrip("+-").isdigit():
                        raise ValueError("Please enter an integer.")
                    result = function(int(value))
                else:
                    result = function(float(value))

            print(f"Result ({name}): {result}")

        except (ValueError, ZeroDivisionError, OverflowError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()

