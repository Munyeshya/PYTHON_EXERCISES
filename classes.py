
# class Person():
#     input1 =int(input("Enter your first name: "))
#     input2 =int(input("Enter your last name: "))

#     def __init__(self, input1, input2):
#         self.first_name = input1
#         self.last_name = input2

# o = Person("Beni", "Obed")
# m = Person("Gilbert", "Muzehe")

# print(f"{o.first_name} {o.last_name}")
# print(f"{m.first_name} {m.last_name}")

class Flight:
    def __init__ (self,capacity):
        self.capacity = capacity
       
        self.passengers = []

    def add_passenger(self, passenger_name):
        if not self.open_seats():
            return False
        self.passengers.append(passenger_name)
        return True
    def open_seats(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)
# people = ["Harry", "Ron","Herminoe","Beni","Obed","Gilbert"]

people = []
num_people = int(input("How many people do you want to register on this flight ? "))
for i in range(num_people):
    name = input(f"Enter Passenger {i+1}: ")
    people.append(name)


for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Added {person} to flight successfully. Remaining seats: {flight.open_seats()}") 
    else:
        print(f"No available seats for {person}.")