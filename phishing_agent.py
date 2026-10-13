"""Explainable, offline-first email triage rules. Never opens URLs or downloads files."""
import re
from urllib.parse import urlparse

URL_RE = re.compile(r"""(?i)\b(?:https?://|hxxps?://|www\.)[^\s<>"']+""")
URGENCY_TERMS = [
    "urgent", "immediately", "act now", "within 24 hours", "today", "suspended",
    "expire", "final warning", "verify now", "account locked"
]
CREDENTIAL_TERMS = ["password", "sign in", "log in", "verify your account", "mailbox", "credentials"]
PAYMENT_TERMS = ["wire transfer", "bank details", "payment", "gift card", "invoice", "pay immediately", "change of bank"]
SUSPICIOUS_EXTENSIONS = [".html", ".htm", ".iso", ".js", ".vbs", ".exe", ".scr", ".docm", ".xlsm", ".zip"]

def _text(value):
    return str(value or "").strip()

def extract_urls(text):
    # This extracts strings only. It does not request, resolve, or open them.
    return [u.rstrip(".,);]") for u in URL_RE.findall(_text(text))]

def defang_url(url):
    """Render URLs non-clickably for safe display."""
    return _text(url).replace("https://", "hxxps://").replace("http://", "hxxp://").replace(".", "[.]")

def _domain_from_address(address):
    match = re.search(r'@([A-Za-z0-9.-]+\.[A-Za-z]{2,})', _text(address))
    return match.group(1).lower().strip(".") if match else ""

def _domain_from_url(url):
    candidate = _text(url)
    if candidate.lower().startswith("hxxp"):
        candidate = candidate.replace("hxxps://", "https://", 1).replace("hxxp://", "http://", 1)
    if candidate.lower().startswith("www."):
        candidate = "http://" + candidate
    try:
        return (urlparse(candidate).hostname or "").lower()
    except Exception:
        return ""

def normalize_email_row(row):
    aliases = {
        "sender": ["sender", "from", "from_address"],
        "reply_to": ["reply_to", "reply-to"],
        "subject": ["subject"],
        "body": ["body", "text", "email_body"],
        "auth_results": ["auth_results", "authentication", "authentication_results"],
        "attachment_metadata": ["attachment_metadata", "attachments", "attachment"]
    }
    lower = {str(k).strip().lower(): v for k, v in row.items()}
    out = {}
    for target, names in aliases.items():
        for name in names:
            if name in lower:
                out[target] = _text(lower[name])
                break
        out.setdefault(target, "")
    return out

def analyze_email(email):
    email = normalize_email_row(email)
    sender, reply_to = email["sender"], email["reply_to"]
    subject, body = email["subject"], email["body"]
    auth, attachments = email["auth_results"], email["attachment_metadata"]
    combined = f"{subject}\n{body}"
    lower = combined.lower()
    urls = extract_urls(combined)
    score, evidence = 0, []

    def add(points, message):
        nonlocal score
        score += points
        evidence.append(message)

    urgency_hits = sorted({term for term in URGENCY_TERMS if term in lower})
    if urgency_hits:
        add(min(18, 6 + 3 * len(urgency_hits)), "Urgency or pressure language: " + ", ".join(urgency_hits[:5]) + ".")

    credential_hits = sorted({term for term in CREDENTIAL_TERMS if term in lower})
    if credential_hits:
        add(min(18, 6 + 3 * len(credential_hits)), "Credential/account language: " + ", ".join(credential_hits[:5]) + ".")

    payment_hits = sorted({term for term in PAYMENT_TERMS if term in lower})
    if payment_hits:
        add(min(24, 8 + 4 * len(payment_hits)), "Payment or financial-change language: " + ", ".join(payment_hits[:5]) + ".")

    if urls:
        add(min(18, 4 + 4 * len(urls)), f"Contains {len(urls)} URL(s): " + ", ".join(defang_url(u) for u in urls[:4]) + ".")
    for url in urls:
        domain = _domain_from_url(url)
        if domain and domain.endswith(".example"):
            # Synthetic reserved domains are not inherently malicious.
            continue
        if domain and any(ch.isdigit() for ch in domain.split(".")[0]) and domain.count(".") >= 2:
            add(8, f"URL uses an unusual numeric subdomain: {defang_url(url)}.")
            break
        if domain and ("-" in domain or domain.count(".") >= 3):
            add(4, f"URL domain has a potentially deceptive structure: {defang_url(url)}.")
            break

    sender_domain, reply_domain = _domain_from_address(sender), _domain_from_address(reply_to)
    if sender_domain and reply_domain and sender_domain != reply_domain:
        add(16, f"Reply-To domain differs from sender domain ({sender_domain} vs. {reply_domain}).")

    auth_lower = auth.lower()
    if auth and any(f"{proto} fail" in auth_lower for proto in ("spf", "dkim", "dmarc")):
        failed = [p.upper() for p in ("spf", "dkim", "dmarc") if f"{p} fail" in auth_lower]
        add(min(24, 8 * len(failed)), "Email authentication failure reported: " + ", ".join(failed) + ".")
    elif auth and all(f"{proto} pass" in auth_lower for proto in ("spf", "dkim", "dmarc")):
        evidence.append("SPF, DKIM, and DMARC are reported as passing; this does not by itself prove the email is safe.")

    if attachments:
        attach_lower = attachments.lower()
        risky = [ext for ext in SUSPICIOUS_EXTENSIONS if ext in attach_lower]
        if risky:
            add(16, "Attachment metadata includes potentially risky file type(s): " + ", ".join(risky) + ".")
        else:
            add(3, "Attachment metadata was provided; inspect it in a controlled environment.")

    score = min(100, score)
    if score >= 60:
        label = "High"
    elif score >= 30:
        label = "Medium"
    else:
        label = "Low"

    if label == "High":
        actions = [
            "Do not click links, open attachments, reply, or provide credentials.",
            "Report the message to the organization's security/IT team and preserve it for investigation.",
            "Verify any payment or account request through a separate, trusted channel."
        ]
    elif label == "Medium":
        actions = [
            "Do not use links in the message until the sender and request are independently verified.",
            "Check the sender and Reply-To details, authentication results, and attachment type.",
            "Escalate to IT/security if the request is unexpected or involves credentials or money."
        ]
    else:
        actions = [
            "No strong phishing indicators were detected by these baseline rules; this is not a guarantee of safety.",
            "Verify unexpected requests through a trusted channel and follow your organization's reporting policy."
        ]

    summary = (
        f"The baseline rules assigned **{label.lower()} risk** ({score}/100). "
        + (f"Detected {len(evidence)} indicator(s). " if evidence else "No strong indicators were detected. ")
        + "This is a triage aid, not a definitive verdict; a human analyst should review consequential cases."
    )
    return {
        "risk_label": label,
        "risk_score": score,
        "summary": summary,
        "evidence": evidence,
        "recommended_actions": actions,
        "features": {
            "url_count": len(urls),
            "urls_defanged": [defang_url(u) for u in urls],
            "sender_domain": sender_domain,
            "reply_to_domain": reply_domain,
            "urgency_terms": urgency_hits,
            "credential_terms": credential_hits,
            "payment_terms": payment_hits,
            "authentication_results_provided": bool(auth),
            "attachment_metadata_provided": bool(attachments)
        },
        "limitations": [
            "Rules can produce false positives and false negatives.",
            "No live URL reputation lookup, DNS lookup, attachment inspection, or email-header parsing is performed.",
            "Domains ending in .example are reserved placeholders for training."
        ]
    }
