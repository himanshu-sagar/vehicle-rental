# Vehicle Rental

<aside>
💡 Vehicle rental Service

</aside>

### Postman

[Vehicle Rental API Doc](https://documenter.getpostman.com/view/15206589/2s8ZDa1MBG)


### Tech Stack Used

---

- Python
- Django
- Redis
- PostgreSQL
- JWT
- qrcode
- opencv

### Project Setup Steps

---

1. Clone the application using GitHub
2. `pip install pipenv`
3. `pipenv install`
4. `pipenv shell`
5. add `.env` file
    - Example env variables
        
        ```jsx
        SECRET_KEY=
        HOST=
        PORT=
        POSTGRES_USER=
        POSTGRES_PASSWORD=
        TWO_FACTOR_API_KEY=
        ```
        
6. Connect to your PostgreSQL and Redis server
7. `python manage.py makemigrations`
8. `python manage.py migrate`
9. `python manage.py runserver`

### Authentication System

---

- **Signup**
    - **POST: /api/user/send_otp/**
        - Enter the Phone number, password, etc in the body
        - Validate the User data
        - Send OTP to the phone using [2-factor](https://2fa.api-docs.io/) APIs and store user_data & session_id in the **Redis** cache temporarily till OTP verification
    - **POST: /api/user/verify_otp/**
        - Enter phone and otp
        - validate OTP
        - Create User in database
- **Authenticate**
    - POST: /api/authenticate/
        - Enter phone and password
        - Get Access and refresh token
        - Use it for every other APIs for authentication

### Vehicle Store and Booking Management

---

- **Station**
    - POST: /api/station/create/
        - Create station using name and location
        - Check If User is Admin
        - Create station in database
    - GET: /api/station/vehicles?station_id=<station_id>
        - Get all vehicles in this station
- **Vehicle**
    - POST: /api/vehicle/create/
        - Send request using company, model, status, etc.
        - Create vehicle in database
        - Generate **QR code** for the vehicle using vehicle_id
            - Package Used: `qrcode`
        - Store QR code in **static** folder
        - In real-world, print the QR code and paste it on Vehicles
- **Booking**
    - User will visit the store for booking
    - In real-world will scan the QR code of vehicle and enter booking details
    - Here I have used the following steps for booking
        - On frontend, a QR code scanner will be implemented using OpenCV library.
        - It will send the scanned QR code path or url to server
        - Server will decode the Vehicle_id from QR code
        - And then that vehicle will be booked till mentioned date
        - mark the vehicle as `in_use`
    - POST: /api/booking/book_vehicle/
        - Send qr_code_path and end_date to server
        - booking will be confirmed by server with booking id
    - GET: /api/booking/return_vehicle?booking_id=<booking_id>
        - send booking_id to server
        - server will accept the vehicle and mark the vehicle `available`
