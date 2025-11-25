HOTEL MANAGEMENT SYSTEM

1. PROJECT OBJECTIVE
•  Designed and implemented a simple, reliable hotel management system.
•  Allowed room management, check-ins, check-outs, customer data storage, and billing.
•  Follow modular and maintainable software engineering practices.

2.FEATURES
- 1)Room Managment System:-
- View all available rooms
- Add new rooms
- Remove existing rooms

- 2)Customer check-in:-
- Assign a customer to a selected room
- Prevent booking an already booked room

- 3)Customer check-out:-
- Release the room
- Generate billing details
- Calculate total payable amount

- 4)Billing system:-
- Automatic calculation of charges
- Display full bill breakdown
- Ensures accurate invoicing

- 5)Data persistence
- Saves room and customer data to a JSON file
- Automatic loads data when system starts
- Generates default data if no file exists

- 6)Error handling and validation
- Handles invalid inputs gracefully
- Validates room numbers
- Prevents double booking

INPUT:-
  ![input 1](https://github.com/user-attachments/assets/8149abdd-af9c-4ca5-b041-a74f7d8b02d9)
  ![input 2](https://github.com/user-attachments/assets/55dd7cd4-9053-4c1c-a78b-079e2f21606b)

OUTPUT:-
  ![output 1](https://github.com/user-attachments/assets/81e9fb1f-00f2-48b0-9fd6-bf5c1bd15872)
  ![output 2](https://github.com/user-attachments/assets/aab807ca-081c-4947-a8a7-f4be4ebe1ae7)


CODE:-
rooms={
    101:{"type":"Single","price":1200,"booked":False,"customer":None},
    102:{"type":"Single","price":1200,"booked":False,"customer":None},
    201:{"type":"Double","price":2200,"booked":False,"customer":None},
    202:{"type":"Double","price":2200,"booked":False,"customer":None},
    301:{"type":"Deluxe","price":4000,"booked":False,"customer":None},
    302:{"type":"Deluxe","price":4000,"booked":False,"customer":None}
}

def show_available_rooms():
    print("\n===== AVAILAIBLE ROOMS =====")
    for r_no , details in rooms.items():
        if not details["booked"]:
            print(f"{r_no} - {details['type']} - ₹{details['price']} per day")
    print("===========================\n") 


def check_in():
    show_available_rooms()
    room_no = int(input("enter room number to book:"))

    if room_no not in rooms:
        print("invalid room number")
        return

    if rooms[room_no]["booked"]:
        print("room already booked")
        return

    name=input("enter name:")
    phone=("enter phone no:")
    days=int(input("enter no of days to stay:"))

    rooms[room_no]["customer"]={
        "name":name,
        "phone":phone,
        "days":days
    }

    rooms[room_no]["booked"]=True
    print(f"\nroom{room_no} succesfully booked for you")

def check_out():
    room_no=int(input("enter room no for checkout:"))

    if room_no not in rooms:
        print("invalid room no")
        return

    if not rooms[room_no]["booked"]:
        print("room is not booked")
        return

    customer = rooms[room_no]["customer"]
    price = rooms[room_no]["price"]
    days = customer["days"] 
    total_bill = price*days

    print("\n=======BILL DETAILS=======") 
    print(f"customer name : {customer['name']}")
    print(f"room no : {room_no}") 
    print(f"phone number : {customer['phone']}")
    print(f"room type : {rooms[room_no]['type']}")
    print(f"price/day : {price}")
    print(f"total days : {days}") 
    print(f"total bill : {total_bill}") 

    rooms[room_no]["booked"]=False
    rooms[room_no]["customer"]=None
    print("checkout successfull. Thank you for staying")

def menu():
    while True:
        print("======= HOTEL MANAGEMENT SYSTEM =======")
        print("1.show available rooms")     
        print("2.check in")  
        print("3.check out")
        print("4.exit")  

        choice = input("enter your choice:")

        if choice == "1":
            show_available_rooms()
        elif choice == "2":
            check_in()     
        elif choice == "3":
            check_out()
        elif choice == "4":
            print("Thank you visit again")
            break
        else:
            print("invalid choice, try again") 

menu()


  


  
