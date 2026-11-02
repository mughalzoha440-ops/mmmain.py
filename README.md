# OOP Notification Management System

A Python-based Notification Management System developed using Object-Oriented Programming (OOP). This application manages notifications through multiple communication channels, including Email, SMS, WhatsApp, and Webhooks.

## Project Overview

The system provides a simple command-line interface to create, send, track, and manage notifications. It includes input validation, delivery status tracking, failure handling, retry functionality, and notification history.

## Key Features

- Support for Email, SMS, WhatsApp, and Webhook notifications
- Unique Notification IDs
- Recipient and message validation
- Notification status tracking (Pending, Sent, Failed)
- Failure handling and retry mechanism
- Notification history tracking
- Command-Line Interface (CLI)
- Unit testing using Python unittest

## Technologies Used

- Python 3
- Object-Oriented Programming
- Abstract Base Classes
- Dataclasses
- Enums
- Regular Expressions
- Unittest Framework

## OOP Concepts Implemented

**Abstraction:** Defines a common notification structure.

**Inheritance:** Different notification channels inherit from the base Notification class.

**Encapsulation:** Notification data and related operations are organized within classes.

**Polymorphism:** Each notification channel implements its own validation behavior.

## Project Structure

```text
OOP-Notification-System/
│
├── main.py
├── test_main.py
└── README.md
```

## Installation

1. Install Python 3.
2. Clone or download this repository.
3. Open the project folder in your terminal.

## How to Run

Start the application:

```bash
python main.py
```

## Running Unit Tests

Execute the following command:

```bash
python -m unittest -v
```

The project includes 13 unit test cases covering notification creation, validation, delivery, failure handling, retries, and history.

## Notification Delivery

Notification delivery is simulated for demonstration and testing purposes. External Email, SMS, WhatsApp, and Webhook services are not connected.

## Project Purpose

This project was developed as part of a Python programming assessment to demonstrate practical knowledge of Object-Oriented Programming, software design, validation, exception handling, and unit testing.

## Author

Developed as a Python programming assessment project.
