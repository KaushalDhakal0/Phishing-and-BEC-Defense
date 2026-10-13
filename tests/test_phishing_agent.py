import unittest
from phishing_agent import analyze_email, defang_url

class AgentTests(unittest.TestCase):
    def test_high_risk_email(self):
        result = analyze_email({
            "sender": "security@sender.example",
            "reply_to": "reply@other.example",
            "subject": "Urgent verify your account",
            "body": "Your password will expire today. Sign in immediately at http://login.example/verify",
            "auth_results": "SPF fail; DKIM fail; DMARC fail",
            "attachment_metadata": "account.html"
        })
        self.assertEqual(result["risk_label"], "High")
        self.assertGreaterEqual(result["risk_score"], 60)

    def test_benign_email_low(self):
        result = analyze_email({
            "sender": "alex@university.example",
            "subject": "Meeting notes",
            "body": "Here are the notes from the project meeting. Please review when convenient."
        })
        self.assertEqual(result["risk_label"], "Low")

    def test_url_defanged(self):
        self.assertEqual(defang_url("https://example.com/path"), "hxxps://example[.]com/path")

if __name__ == "__main__":
    unittest.main()
