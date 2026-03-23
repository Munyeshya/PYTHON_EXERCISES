class GradeSystem:
    def __init__(self):
        self.thresholds = [40, 50, 60, 70]  
        self.classes = [
            "Fail",
            "Third Class",
            "Second Class Lower",
            "Second Class Upper",
            "First Class"
        ]

    def calculate_grade(self, score):
        for i, t in enumerate(reversed(self.thresholds)):
            if score >= t:
                return self.classes[-(i + 1)]
        return self.classes[0]

    def start(self):
        print("=== Grade Checker ===")

        while True:
            user_input = input("\nEnter your Score: ")

            if user_input.lower() == "exit":
                print("Goodbye")
                break

            try:
                marks = float(user_input)

                if marks < 0 or marks > 100:
                    print("Score must be between 0 and 100.")
                    continue

                grade = self.calculate_grade(marks)
                print(f"Grade: {grade}")

            except ValueError:
                print("Invalid input! Please enter a number.")


if __name__ == "__main__":
    app = GradeSystem()
    app.start()