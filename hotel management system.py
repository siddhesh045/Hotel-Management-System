rooms={
    101:{"type":"Single","price":1200,"booked":False,"customer":None},
    102:{"type":"Single","price":1200,"booked":False,"customer":None},
    201:{"type":"Double","price":2200,"booked":False,"customer":None},
    202:{"type":"Double","price":2200,"booked":False,"customer":None},
    301:{"type":"Deluxe","price":4000,"booked":False,"customer":None},
    302:{"type":"Deluxe","price":4000,"booked":False,"customer":None}
}

def show_available_rooms():
    print("\n===== AVAILABLE ROOMS =====")
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
    phone=input("enter phone no:")
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

             

