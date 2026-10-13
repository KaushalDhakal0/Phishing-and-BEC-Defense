"""Create 240 synthetic, safe email examples for coursework. No live malicious links."""
import csv, random
from pathlib import Path

random.seed(42)
out = Path("data/dummy_emails.csv")
out.parent.mkdir(exist_ok=True)

benign = [
    ("Weekly project meeting notes", "Hi team, attached are the notes from our weekly project meeting. Please review before Thursday.", "alex@university.example", "", "SPF pass; DKIM pass; DMARC pass", "meeting-notes.pdf", "benign"),
    ("Your library book is due soon", "A friendly reminder that your library book is due next week. You can visit the library portal using your usual bookmark.", "library@university.example", "", "SPF pass; DKIM pass; DMARC pass", "", "benign"),
    ("Lunch order confirmation", "Thanks for placing your lunch order. Your pickup window is 12:15 to 12:30. Reply if you have questions.", "orders@cafeteria.example", "", "SPF pass; DKIM pass; DMARC pass", "", "benign"),
    ("Draft report for review", "Hello, could you review the attached draft report and send comments by Friday? No rush if you need more time.", "sam@company.example", "", "SPF pass; DKIM pass; DMARC pass", "draft-report.pdf", "benign"),
    ("Schedule update", "The planning meeting has moved to 2 PM tomorrow. The calendar invitation will be updated.", "coordinator@company.example", "", "SPF pass; DKIM pass; DMARC pass", "", "benign"),
]
suspicious = [
    ("Urgent: Verify your account immediately", "Your account will be suspended today. Verify your password immediately at http://login-check.example/verify.", "security@account-notice.example", "reply@unrelated-mail.example", "SPF fail; DKIM fail; DMARC fail", "login.html", "phishing"),
    ("Payment overdue - act now", "Final warning: invoice payment is overdue. Wire transfer the amount today and send bank details for confirmation.", "billing@vendor-alert.example", "finance@free-mail.example", "SPF pass; DKIM fail; DMARC fail", "invoice.xlsm", "phishing"),
    ("CEO request - gift cards", "I am in a meeting. Buy gift cards immediately and send me the codes. Keep this confidential.", "ceo@company-lookalike.example", "assistant@external-mail.example", "Not provided", "", "phishing"),
    ("Mailbox locked", "Your mailbox is locked. Sign in now to verify your credentials or access will expire within 24 hours: hxxp://mail-access.example/login", "helpdesk@company-support.example", "verify@another-domain.example", "SPF fail; DKIM pass; DMARC fail", "account.htm", "phishing"),
    ("Updated bank details", "Please change the supplier bank details before today's payment run. This is urgent; act now.", "supplier@vendor-payments.example", "supplier-update@free-mail.example", "Not provided", "payment-instructions.pdf", "phishing"),
]
rows = []
for i in range(120):
    item = benign[i % len(benign)]
    subject, body, sender, reply, auth, attach, label = item
    rows.append({"id": f"SYN-B-{i+1:03d}", "sender": sender, "reply_to": reply, "subject": subject,
                 "body": body, "auth_results": auth, "attachment_metadata": attach, "label": label})
for i in range(120):
    item = suspicious[i % len(suspicious)]
    subject, body, sender, reply, auth, attach, label = item
    # Small safe variations add diversity while preserving synthetic placeholders.
    variants = ["", " Please review carefully.", " Thank you.", " This message is intended for the recipient."]
    rows.append({"id": f"SYN-P-{i+1:03d}", "sender": sender, "reply_to": reply, "subject": subject,
                 "body": body + variants[i % len(variants)], "auth_results": auth,
                 "attachment_metadata": attach, "label": label})
random.shuffle(rows)
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","sender","reply_to","subject","body","auth_results","attachment_metadata","label"])
    writer.writeheader()
    writer.writerows(rows)
print(f"Created {len(rows)} synthetic examples at {out}")
