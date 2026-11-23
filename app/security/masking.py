
import re


PATTERNS = [
    # Authorization headers
    (
        re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
        "Bearer [REDACTED]",
    ),
    (
        re.compile(r"(?i)\bBasic\s+[A-Za-z0-9+/=]+"),
        "Basic [REDACTED]",
    ),

    # Sensitive key-value pairs
    (
        re.compile(
            r"""(?i)\b(password|passwd|pwd|api[_-]?key|"""
            r"""access[_-]?token|refresh[_-]?token|auth[_-]?token|"""
            r"""client[_-]?secret|secret[_-]?key|secret|"""
            r"""token|credential)\b(["']?\s*[:=]\s*["']?)([^\s,"';}]+)"""
        ),
        r"\1\2[REDACTED]",
    ),

    # JWT tokens
    (
        re.compile(
            r"\beyJ[A-Za-z0-9_-]+\."
            r"[A-Za-z0-9_-]+\."
            r"[A-Za-z0-9_-]+\b"
        ),
        "[REDACTED_JWT]",
    ),

    # Common provider tokens
    (
        re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
        "[REDACTED_API_KEY]",
    ),
    (
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "[REDACTED_AWS_KEY]",
    ),
    (
        re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        "[REDACTED_GITHUB_TOKEN]",
    ),

    # Private key blocks
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?"
            r"-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),

    # URL credentials
    (
        re.compile(
            r"(?i)(https?://)[^/\s:@]+:[^@\s/]+@"
        ),
        r"\1[REDACTED]@",
    ),

    # Email addresses
    (
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        "[REDACTED_EMAIL]",
    ),

    # Phone numbers (basic international/local format)
    (
        re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)"),
        "[REDACTED_PHONE]",
    ),
]


def mask_sensitive_data(text: str) -> str:
    """
    Mask common secrets and personal data.
    This is basic regex-based masking, not complete DLP.
    """
    if not isinstance(text, str):
        return text

    masked = text

    for pattern, replacement in PATTERNS:
        masked = pattern.sub(replacement, masked)

    return masked
