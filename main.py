
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re


class NotificationStatus(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


@dataclass
class Notification(ABC):
    notification_id: int
    recipient: str
    message: str
    fail_attempts: int = 0
    status: NotificationStatus = NotificationStatus.PENDING
    attempts: int = 0
    created_time: datetime = field(default_factory=datetime.now)
    history: list = field(default_factory=list)

    def __post_init__(self):
        if not self.recipient.strip():
            raise ValueError("Recipient cannot be empty")

        if not self.message.strip():
            raise ValueError("Message cannot be empty")

        if self.fail_attempts < 0:
            raise ValueError("Invalid failure count")

        self.validate_recipient()
        self.history.append("Notification created")

    @property
    @abstractmethod
    def channel_name(self):
        pass

    @abstractmethod
    def validate_recipient(self):
        pass

    def send(self):
        self.attempts += 1

        if self.attempts <= self.fail_attempts:
            self.status = NotificationStatus.FAILED
            result = "Delivery failed"
        else:
            self.status = NotificationStatus.SENT
            result = "Delivery successful"

        self.history.append(
            f"{datetime.now()} - {result}"
        )

        return self.status == NotificationStatus.SENT

    def retry(self):
        if self.status != NotificationStatus.FAILED:
            raise ValueError("Only failed notifications can be retried")

        self.history.append("Retry requested")
        return self.send()

    def get_details(self):
        return {
            "ID": self.notification_id,
            "Channel": self.channel_name,
            "Recipient": self.recipient,
            "Message": self.message,
            "Status": self.status.value,
            "Attempts": self.attempts,
            "Created": self.created_time
        }


class EmailNotification(Notification):

    @property
    def channel_name(self):
        return "Email"

    def validate_recipient(self):
        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            self.recipient.strip()
        ):
            raise ValueError("Invalid email address")


class SMSNotification(Notification):

    @property
    def channel_name(self):
        return "SMS"

    def validate_recipient(self):
        if not re.fullmatch(r"\+?[0-9]{7,15}", self.recipient.strip()):
            raise ValueError("Invalid phone number")


class WhatsAppNotification(Notification):

    @property
    def channel_name(self):
        return "WhatsApp"

    def validate_recipient(self):
        if not re.fullmatch(r"\+?[0-9]{7,15}", self.recipient.strip()):
            raise ValueError("Invalid WhatsApp number")


class WebhookNotification(Notification):

    @property
    def channel_name(self):
        return "Webhook"

    def validate_recipient(self):
        if not re.match(r"^https?://[^\s]+$", self.recipient.strip()):
            raise ValueError("Invalid webhook URL")


class NotificationService:

    CHANNELS = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "whatsapp": WhatsAppNotification,
        "webhook": WebhookNotification
    }

    def __init__(self):
        self.notifications = []
        self.next_id = 1

    def create_notification(self, channel, recipient, message,
                            fail_attempts=0):

        notification_class = self.CHANNELS.get(channel.lower().strip())

        if notification_class is None:
            raise ValueError("Invalid notification channel")

        notification = notification_class(
            self.next_id,
            recipient,
            message,
            fail_attempts
        )

        self.notifications.append(notification)
        self.next_id += 1

        return notification

    def get_notification(self, notification_id):
        for notification in self.notifications:
            if notification.notification_id == notification_id:
                return notification

        raise ValueError("Notification not found")

    def send_notification(self, notification_id):
        notification = self.get_notification(notification_id)

        if notification.status != NotificationStatus.PENDING:
            raise ValueError("Notification is not pending")

        return notification.send()

    def retry_notification(self, notification_id):
        return self.get_notification(notification_id).retry()

    def get_all_notifications(self):
        return self.notifications.copy()

    def get_history(self, notification_id):
        return self.get_notification(notification_id).history.copy()


def run_cli():

    service = NotificationService()

    while True:

        print("\n===== NOTIFICATION SYSTEM =====")
        print("1. Create and send notification")
        print("2. View all notifications")
        print("3. Check notification status")
        print("4. Retry failed notification")
        print("5. View notification history")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        try:

            if choice == "1":

                print("Channels: Email, SMS, WhatsApp, Webhook")

                channel = input("Enter channel: ")
                recipient = input("Enter recipient: ")
                message = input("Enter message: ")

                failures = int(
                    input("Simulate initial failures (0 for none): ") or "0"
                )

                if failures < 0:
                    raise ValueError("Failure count cannot be negative")

                notification = service.create_notification(
                    channel, recipient, message, failures
                )

                print("Notification ID:", notification.notification_id)

                sent = service.send_notification(notification.notification_id)

                print(
                    "Notification sent successfully"
                    if sent else
                    "Notification failed. You can retry it."
                )

                print(notification.get_details())

            elif choice == "2":

                notifications = service.get_all_notifications()

                if not notifications:
                    print("No notifications found")

                for notification in notifications:
                    print(notification.get_details())

            elif choice == "3":

                notification_id = int(input("Enter notification ID: "))

                notification = service.get_notification(notification_id)

                print(notification.get_details())

            elif choice == "4":

                notification_id = int(input("Enter failed notification ID: "))

                result = service.retry_notification(notification_id)

                print("Retry successful" if result else "Retry failed")

            elif choice == "5":

                notification_id = int(input("Enter notification ID: "))

                history = service.get_history(notification_id)

                for item in history:
                    print(item)

            elif choice == "6":

                print("Thank you for using Notification System")
                break

            else:
                print("Invalid choice. Try again.")

        except (ValueError, TypeError) as error:
            print("Error:", error)


if __name__ == "__main__":
    run_cli()
