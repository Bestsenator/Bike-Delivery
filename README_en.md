# Bike-Devliery

**Bike-Delivery** is a backend project developed using the Django framework, designed for managing and coordinating the activities of Bike-Devliery. This system helps in managing orders, drivers, customers, addresses, and various statuses of Bike-Devliery. It also includes functionalities for order registration and tracking, managing driver and customer information, and monitoring driver attendance.

## Related Projects

This backend project is connected to two mobile applications developed using the Flutter framework. One of the applications allows users to place and track their orders, while the other is designed for drivers to receive and manage orders. For more information about the Flutter projects, please refer to the following links:

- [Customer Mobile Application](#)
- [Driver Mobile Application](#)

## Features

- **Order Management:** Ability to register and track orders, view their status and details.
- **Driver Management:** Management of driver information, statuses, and courier types.
- **Customer and Address Management:** Registration and management of customer information and addresses.
- **Status and Attendance Management:** Monitoring of various courier statuses and managing attendance.
- **Mobile Application Integration:** Capability to connect with mobile applications for direct interaction with users and drivers.

## Models (Tables)

### Delivery

The `Delivery` class is used to store information related to Bike-Devliery. This model includes details such as name, surname, contact number, date of birth, national code, personal code, current status, membership date, courier type (with box, without box, passenger), and vehicle license plate numbers.

### Customer

The `Customer` class is designed to store customer information in the system. This model includes name, surname, contact number, gender, subscription number, active status, membership date, and the last update date of customers.

### CustomerAddresses

The `CustomerAddresses` class is used for managing customer addresses. This model includes address code, customer subscription number, address name and description, and its main status.

### Orders

The `Orders` class is designed for registering and managing motorbike orders. This model includes delivery type, route type, route number, source and destination addresses, subscription number, receiver's name and contact number, order registration and completion dates, order amount, delivery code, order status, and related descriptions.

### CustomerSessions

The `CustomerSessions` class is used to store information related to customer sessions. This model includes subscription number and current customer session.

### DeliverySessions

The `DeliverySessions` class is designed for managing driver sessions. This model includes personal code and current driver session.

### VerifyCode

The `VerifyCode` class is used to generate and store verification codes. This model includes usage status, contact number, verification code, code generation time and date, and code usage type.

### API_KEYS

The `API_KEYS` class is designed for managing API keys. This model includes API key, hash, and additional permissions and API listing.

### Station

The `Station` class is used to manage motorbike courier stations. This model includes station code, name, code, description, number of orders, and number of couriers.

### AttendanceDelivery

The `AttendanceDelivery` class is designed for recording driver attendance. This model includes delivery code, attendance status, date, start time, leave duration, and end status.

### Events

The `Events` class is used for recording and managing events. This model includes code, name, time, date, description, guests, and event location.

### RegisterRequest

The `RegisterRequest` class is designed for managing driver registration requests. This model includes code, name, national code, father's name, contact number, address, military service status, and registration time.

## Prerequisites

To run this project, you need to install the following software and tools:

- [Python](https://www.python.org/downloads/) version 3.8 or higher
- [Django](https://www.djangoproject.com/) version 3.2 or higher
- [PostgreSQL](https://www.postgresql.org/) or [SQLite](https://www.sqlite.org/) (based on your choice)
  

## Project Dependencies

The following packages are used in this project:

- `Django==5.0.1`
- `django-jalali==6.0.1`
- `djangorestframework==3.14.0`
- `jdatetime==5.0.0`

  ## Installation and Setup

Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bestsenator/Bike-Delivery.git
   ```

3. **Navigate to the project directory:**
   ```bash
   cd Bike-Delivery
   ```

5. **Create a Python virtual environment:**
   ```bash
   python -m venv venv
   ```

7. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS or Linux:
     ```bash
     source venv/bin/activate
     ```

8. **Install the project dependencies:**
   ```bash
   pip install -r requ.txt
   ```

10. **Configure the `.env` file based on the `.env.example` template.**

11. **Apply the database migrations:**
   ```bash
python manage.py migrate
```

13. **Run the server:**
   ```bash
python manage.py runserver
```

15. The project is now available at `http://localhost:8000`.

## Contributing

If you would like to contribute to this project, you can:

1. Fork this repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push your branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Special Thanks

[Ali Najafzadeh](https://github.com/AliNajafzadeh7916)

Special thanks to the Flutter app developer who has developed this app with great skill and effort and connected it to this backend project. Without his efforts, the creation of this integrated system would not have been possible.


