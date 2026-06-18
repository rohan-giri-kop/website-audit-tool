import requests


SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "issue": "HSTS protection missing",
        "recommendation": "Add the Strict-Transport-Security header.",
        "priority": "Medium",
        "benefit": "Forces browsers to use HTTPS connections."
    },
    "Content-Security-Policy": {
        "issue": "Content Security Policy missing",
        "recommendation": "Configure a Content-Security-Policy header.",
        "priority": "High",
        "benefit": "Reduces Cross-Site Scripting (XSS) attacks."
    },
    "X-Frame-Options": {
        "issue": "Clickjacking protection missing",
        "recommendation": "Add the X-Frame-Options header.",
        "priority": "Medium",
        "benefit": "Prevents clickjacking attacks."
    },
    "X-Content-Type-Options": {
        "issue": "MIME sniffing protection missing",
        "recommendation": "Add the X-Content-Type-Options header.",
        "priority": "Medium",
        "benefit": "Stops browsers from MIME type sniffing."
    },
    "Referrer-Policy": {
        "issue": "Referrer Policy missing",
        "recommendation": "Configure a Referrer-Policy header.",
        "priority": "Low",
        "benefit": "Improves user privacy."
    }
}


def analyze_security(url: str) -> dict:
    findings = []
    score = 100

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            }
        )

        # HTTPS Check
        if not url.startswith("https://"):
            findings.append({
                "category": "Security",
                "issue": "Website is not using HTTPS",
                "recommendation": "Install an SSL certificate and redirect HTTP traffic to HTTPS.",
                "priority": "High",
                "benefit": "Protects user data and improves trust."
            })
            score -= 20

        # Security Headers Check
        for header, data in SECURITY_HEADERS.items():
            if header not in response.headers:
                findings.append({
                    "category": "Security",
                    "issue": data["issue"],
                    "recommendation": data["recommendation"],
                    "priority": data["priority"],
                    "benefit": data["benefit"]
                })
                if data["priority"] == "High":
                    score -= 10

                elif data["priority"] == "Medium":
                    score -= 5

                else:
                    score -= 2

        # Server Header Exposure
        if "Server" in response.headers:
            findings.append({
                "category": "Security",
                "issue": f"Server information exposed ({response.headers['Server']})",
                "recommendation": "Hide or minimize server version information.",
                "priority": "Low",
                "benefit": "Reduces information disclosure to attackers."
            })
            score -= 5

        # Secure Cookies Check
        cookies = response.cookies

        for cookie in cookies:
            if not cookie.secure:
                findings.append({
                    "category": "Security",
                    "issue": f"Cookie '{cookie.name}' is not marked Secure",
                    "recommendation": "Set the Secure flag on cookies.",
                    "priority": "Medium",
                    "benefit": "Protects cookies during transmission."
                })
                score -= 5

        score = max(score, 0)

        return {
            "security_score": round(score, 1),
            "findings": findings,
            "metrics": {
                "https_enabled": url.startswith("https://"),
                "hsts_enabled": "Strict-Transport-Security" in response.headers,
                "csp_present": "Content-Security-Policy" in response.headers,
                "x_frame_options": "X-Frame-Options" in response.headers,
                "x_content_type": "X-Content-Type-Options" in response.headers,
                "referrer_policy": "Referrer-Policy" in response.headers,
                "server_hidden": "Server" not in response.headers
            }
        }

    except Exception as e:
        return {
            "security_score": 0,
            "findings": [
                {
                    "category": "Security",
                    "issue": f"Security scan failed: {str(e)}",
                    "recommendation": "Verify the website URL and network connectivity.",
                    "priority": "High",
                    "benefit": "Allows accurate security analysis."
                }
            ],
            "metrics": {
                "https_enabled": False,
                "headers_checked": 0,
                "issues_found": 1
            }
        }