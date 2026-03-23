class SmartCalc:
    def __init__(self):
        self.actions = {
            "1": ("Addition", self._sum),
            "2": ("Subtraction", self._difference),
            "3": ("Multiplication", self._product),
            "4": ("Division", self._quotient)
        }

    def _sum(self, a, b):
        return a + b

    def _difference(self, a, b):
        return a - b

    def _product(self, a, b):
        return a * b

    def _quotient(self, a, b):
        if b == 0:
            return "Cannot divide by zero!"
        return a / b

    def run(self):
        print("=== Smart Calculator ===")

        while True:
            print("\nChoose operation:")
            for key, (name, _) in self.actions.items():
                print(f"{key}: {name}")
            print("0: Exit")

            choice = input("Choose operation: ").strip()

            if choice == "0":
                print("Goodbye")
                break

            if choice not in self.actions:
                print("Invalid choice. Try again.")
                continue

            try:
                x = float(input("Number 1: "))
                y = float(input("Number 2: "))

                operation_name, func = self.actions[choice]
                result = func(x, y)

                print(f"{operation_name} Result = {result}")

            except ValueError:
                print("Please enter valid numbers.")


if __name__ == "__main__":
    calc_app = SmartCalc()
    calc_app.run()