try:
    year_of_birth = int(input("Enter the year of birth: "))
    age = 2023 - year_of_birth

    if age >= 18:
        print("You are allowed to drink alcohol.")

    else:
        print("You are not allowed to drink alcohol.")

except (ValueError,TypeError):
    print("Invalid input. Please enter a valid year of birth.")
    

try:
    age = int(input("Age: "))

    if int(age) >= 18:
        print("You are an adult.")

    else:
        print("You are not an adult.")

except (ValueError,TypeError):
    print("Invalid input. Please enter a valid age.")
