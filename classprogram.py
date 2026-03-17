class Flight:
    def __init__(self, flight_id, destination, capacity):
        self.flight_id = flight_id
        self.destination = destination
        self.capacity = capacity
        self.passengers = []
    
    def add_passenger(self, passenger_name):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger_name)
            print(f"Passenger '{passenger_name}' added successfully.")
        else:
            print(f"Flight is full. Cannot add '{passenger_name}'.")
    
    def remove_passenger(self, passenger_name):
        if passenger_name in self.passengers:
            self.passengers.remove(passenger_name)
            print(f"Passenger '{passenger_name}' removed.")
        else:
            print(f"Passenger '{passenger_name}' not found.")
    
    def display_passengers(self):
        print(f"\nFlight {self.flight_id} to {self.destination}")
        print(f"Passengers ({len(self.passengers)}/{self.capacity}):")
        for passenger in self.passengers:
            print(f"  - {passenger}")
    
    def get_available_seats(self):
        return self.capacity - len(self.passengers)


if __name__ == "__main__":
    flight = Flight("UA123", "New York", 3)
    
    flight.add_passenger("Alice")
    flight.add_passenger("Bob")
    flight.add_passenger("Charlie")
    flight.add_passenger("David")
    
    flight.display_passengers()
    print(f"Available seats: {flight.get_available_seats()}")
    
    flight.remove_passenger("Bob")
    flight.display_passengers()