
import unittest

from main import (
    NotificationService,
    NotificationStatus,
    EmailNotification,
    SMSNotification,
    WhatsAppNotification,
    WebhookNotification
)


class TestNotificationSystem(unittest.TestCase):

    def setUp(self):
        self.service = NotificationService()

    def test_create_email_notification(self):
        notification = self.service.create_notification(
            "email", "test@gmail.com", "Hello"
        )
        self.assertIsInstance(notification, EmailNotification)

    def test_create_sms_notification(self):
        notification = self.service.create_notification(
            "sms", "+923001234567", "Hello"
        )
        self.assertIsInstance(notification, SMSNotification)

    def test_create_whatsapp_notification(self):
        notification = self.service.create_notification(
            "whatsapp", "+923001234567", "Hello"
        )
        self.assertIsInstance(notification, WhatsAppNotification)

    def test_create_webhook_notification(self):
        notification = self.service.create_notification(
            "webhook", "https://example.com/hook", "Hello"
        )
        self.assertIsInstance(notification, WebhookNotification)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.service.create_notification(
                "email", "invalid-email", "Hello"
            )

    def test_invalid_phone(self):
        with self.assertRaises(ValueError):
            self.service.create_notification(
                "sms", "abc123", "Hello"
            )

    def test_empty_message(self):
        with self.assertRaises(ValueError):
            self.service.create_notification(
                "email", "test@gmail.com", ""
            )

    def test_invalid_channel(self):
        with self.assertRaises(ValueError):
            self.service.create_notification(
                "telegram", "test", "Hello"
            )

    def test_successful_delivery(self):
        notification = self.service.create_notification(
            "email", "test@gmail.com", "Hello"
        )
        result = self.service.send_notification(
            notification.notification_id
        )
        self.assertTrue(result)
        self.assertEqual(
            notification.status, NotificationStatus.SENT
        )

    def test_failed_delivery(self):
        notification = self.service.create_notification(
            "email", "test@gmail.com", "Hello", 1
        )
        result = self.service.send_notification(
            notification.notification_id
        )
        self.assertFalse(result)
        self.assertEqual(
            notification.status, NotificationStatus.FAILED
        )

    def test_retry_failed_notification(self):
        notification = self.service.create_notification(
            "email", "test@gmail.com", "Hello", 1
        )
        self.service.send_notification(notification.notification_id)

        result = self.service.retry_notification(
            notification.notification_id
        )

        self.assertTrue(result)
        self.assertEqual(
            notification.status, NotificationStatus.SENT
        )

    def test_notification_history(self):
        notification = self.service.create_notification(
            "email", "test@gmail.com", "Hello"
        )
        self.service.send_notification(notification.notification_id)

        history = self.service.get_history(notification.notification_id)

        self.assertGreaterEqual(len(history), 2)

    def test_notification_not_found(self):
        with self.assertRaises(ValueError):
            self.service.get_notification(999)


if __name__ == "__main__":
    unittest.main()
