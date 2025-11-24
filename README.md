# Hotel-Management-System
1. PROJECT OBJECTIVE
• To design and implement a simple, reliable hotel management system.
• To allow room management, check■ins, check■outs, customer data storage, and billing.
• To follow modular and maintainable software engineering practices.


2. FUNCTIONAL REQUIREMENTS
Room Management
- FR1: Display available rooms.
- FR2: Admin can add rooms.
- FR3: Admin can remove rooms.
 
Booking Management
- FR4: Perform check■in.
- FR5: Prevent booking an occupied room.
- FR6: Store customer details.
 
Checkout & Billing
- FR7: Perform checkout.
- FR8: Calculate billing.
- FR9: Free room after checkout.
 
Data Persistence
- FR10: Save data to JSON.
- FR11: Load default rooms when file missing.

 
3. NON■FUNCTIONAL REQUIREMENTS
Usability
- NFR1: Must be user■friendly.
- NFR2: Clear prompts.
 
Performancement
NFR3: Operations complete within 1 second.
- NFR4: Efficient for < 50 rooms.
 
Reliability
- NFR5: Prevent invalid operations.
- NFR6: Handle incorrect input gracefully.
 
Maintainability
- NFR7: Modular code.
- NFR8: Good naming conventions.
 
Portability
- NFR9: Runs on Python 3.10+


4.CASE DIAGRAM
  %%{init: { 'theme': 'base', 'themeVariables': {} }}%%
usecaseDiagram
    actor Staff as S
    actor Admin as A

    S --> (View Available Rooms)
    S --> (Check In Customer)
    S --> (Check Out Customer)

    A --> (Add Room)
    A --> (Remove Room)
    A --> (View Available Rooms)

  5.flowchart TD
    Console["Console UI"] -->|commands| App["Application (main.py)"]
    App --> BookingSvc["BookingService"]
    BookingSvc --> RoomMgr["RoomManager"]
    RoomMgr --> Storage["Storage (rooms.json)"]
    BookingSvc --> Billing["Billing Module"]
    Billing --> App
