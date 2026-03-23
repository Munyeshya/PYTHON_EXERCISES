import random

class NumberChallenge:
    def __init__(self):
        self.secret_value = random.randint(5, 5000)
        self.max_trials = 5

    def compare_values(self, user_value):
        if user_value == self.secret_value:
            return "equal"
        elif user_value < self.secret_value:
            return "smaller"
        else:
            return "greater"

    def play_round(self):
        remaining_trials = self.max_trials

        print("=== Number Challenge ===")
        print("Pick a number from 1 to 100")
        print(f"You can only try {self.max_trials} times\n")

        while remaining_trials > 0:
            try:
                player_input = int(input(f"Guess ({remaining_trials} left): "))

                result = self.compare_values(player_input)

                if result == "equal":
                    print("Congratulations ,You win!")
                    return
                elif result == "smaller":
                    print("Higher Please!\n")
                else:
                    print("Lower Please!\n")

                remaining_trials -= 1

            except ValueError:
                print("Enter a valid number!\n")

        self.end_game()

    def end_game(self):
        print(f"You have failed! The correct number was {self.secret_value}")


if __name__ == "__main__":
    game_app = NumberChallenge()
    game_app.play_round()