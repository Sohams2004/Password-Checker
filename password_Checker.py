import re
import warnings
from getpass import GetPassWarning, getpass


MIN_LENGTH = 15
COMMON_PASSWORDS = {"password", "password123", "123456", "qwerty", "letmein"}
PATTERNS = ("password", "1234", "abcd", "qwerty")
SUBSTITUTIONS = str.maketrans({"@": "a", "0": "o", "$": "s", "3": "e"})


def check_password(password):
    findings = []
    lowercase = password.lower()
    simplified = lowercase.translate(SUBSTITUTIONS)

    if len(password) < MIN_LENGTH:
        findings.append(f"Use at least {MIN_LENGTH} characters.")

    if lowercase in COMMON_PASSWORDS:
        findings.append("This matches a common password in the demo list.")

    if any(pattern in lowercase or pattern in simplified for pattern in PATTERNS):
        findings.append("Avoid common words and predictable sequences.")

    if re.search(r"(.)\1{3}", lowercase):
        findings.append("Avoid repeating the same character four or more times.")

    return findings


def main():
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            password = getpass("Enter a made-up password to check: ")
    except GetPassWarning:
        print("Hidden input is unavailable. Run this from PowerShell.")
        return
    except (KeyboardInterrupt, EOFError):
        print("\nCheck cancelled.")
        return

    if not password.strip():
        print("Enter a password with at least one non-space character.")
        return

    findings = check_password(password)

    if findings:
        print("\nWeaknesses found:")
        for finding in findings:
            print(f"- {finding}")
    else:
        print("\nNo obvious weaknesses found by these checks.")


if __name__ == "__main__":
    main()