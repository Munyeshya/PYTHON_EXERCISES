# person = {"name": "Beni", "age": 20}
# print(person["name"])
# print(person["age"])

# student ={
#     "name": "John",
#     "age": 25,
#     "courses":"Math"
#     }
# print(student["name"])
# print(student["age"])
# print(student["courses"])

product = [
    {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "in_stock": True
    },
    {
    "id": 2,
    "name": "Smartphone",
    "price": 499.99,
    "in_stock": False
    }
]
for item in product:
    if item["id"] == 1:
        print("A " + str(item["name"]) + " costs $" + str(item["price"]))
        

