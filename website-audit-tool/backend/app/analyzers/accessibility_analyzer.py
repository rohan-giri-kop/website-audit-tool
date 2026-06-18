from bs4 import BeautifulSoup


def analyze_accessibility(soup: BeautifulSoup):
    score = 100.0
    findings = []

    images = soup.find_all("img")

    # Missing ALT text
    missing_alt = sum(
        1 for img in images
        if not img.get("alt")
    )

    if missing_alt:
        score -= min(20, missing_alt * 2)

        findings.append({
            "category": "Accessibility",
            "issue": f"{missing_alt} image(s) missing ALT text",
            "recommendation": "Add descriptive ALT text to images.",
            "priority": "High",
            "benefit": "Improves screen reader support."
        })

    # ARIA labels
    aria_labels = (
        soup.find_all(attrs={"aria-label": True})
        + soup.find_all(attrs={"aria-labelledby": True})
    )

    if not aria_labels:
        score -= 8

        findings.append({
            "category": "Accessibility",
            "issue": "Limited ARIA support",
            "recommendation": "Add ARIA labels where appropriate.",
            "priority": "Medium",
            "benefit": "Improves accessibility navigation."
        })

    # Form labels
    forms = soup.find_all("input")

    unlabeled = 0

    for field in forms:
        if (
            not field.get("aria-label")
            and not field.get("id")
        ):
            unlabeled += 1

    if unlabeled:
        score -= min(15, unlabeled * 2)

        findings.append({
            "category": "Accessibility",
            "issue": f"{unlabeled} form field(s) lack labels",
            "recommendation": "Add labels or aria-label attributes.",
            "priority": "Medium",
            "benefit": "Improves form usability."
        })

    headings = soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    )

    if len(headings) < 2:
        score -= 5

        findings.append({
            "category": "Accessibility",
            "issue": "Weak heading structure",
            "recommendation": "Use structured heading hierarchy.",
            "priority": "Low",
            "benefit": "Improves navigation for screen readers."
        })

    score = max(0, score)
    
    return {
        "accessibility_score": round(score, 1),
        "findings": findings,
        "metrics": {
            "missing_alt_images": missing_alt,
            "unlabeled_inputs": unlabeled,
            "has_aria_support": bool(aria_labels)
        }
    }   