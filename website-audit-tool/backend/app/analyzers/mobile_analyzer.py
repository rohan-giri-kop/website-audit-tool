from bs4 import BeautifulSoup
import requests

def analyze_mobile(url):
    findings = []
    score = 100

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
                )
            }
        )

        soup = BeautifulSoup(response.text, "html.parser")

        # Viewport Check
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        if not viewport:
            findings.append({
                "issue": "Viewport meta tag missing",
                "severity": "high"
            })
            score -= 20

        # Image Responsiveness
        images = soup.find_all("img")

        responsive_images = 0

        for img in images:
            if (
                img.get("width") is None or
                "img-fluid" in img.get("class", [])
            ):
                responsive_images += 1

        if images and responsive_images < len(images) * 0.5:
            findings.append({
                "issue": "Many images may not be mobile responsive",
                "severity": "medium"
            })
            score -= 10

        # Media Query Detection
        stylesheets = soup.find_all("link", rel="stylesheet")
        
        buttons = soup.find_all(
            ["button", "a"]
        )

        if len(buttons) < 2:
            findings.append({
                "issue": "Few touch-friendly controls detected",
                "severity": "low"
            })

            score -= 5

        if len(stylesheets) == 0:
            findings.append({
                "issue": "No external CSS found",
                "severity": "medium"
            })
            score -= 10

        return {
            "score": max(score, 0),
            "metrics": {
                "viewport_present": viewport is not None,
                "image_count": len(images),
                "responsive_images": responsive_images
            },
            "findings": findings
        }
        
    except Exception as e:
        return {
            "score": 0,
            "findings": [{
                "issue": str(e),
                "severity": "high"
            }]
        }