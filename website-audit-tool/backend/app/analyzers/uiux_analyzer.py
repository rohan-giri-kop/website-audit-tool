from bs4 import BeautifulSoup


def analyze_uiux(html_content):
    """
    Analyze UI/UX issues from page HTML
    """

    findings = []

    soup = BeautifulSoup(html_content, "html.parser")

    # -------------------------
    # Images without alt
    # -------------------------
    images = soup.find_all("img")

    missing_alt = [
        img for img in images
        if not img.get("alt")
    ]

    if missing_alt:
        findings.append({
            "category": "UI/UX",
            "title": "Images missing alt text",
            "severity": "Medium",
            "issue": f"{len(missing_alt)} image(s) missing alt text.",
            "recommendation": "Add meaningful alt text to all images.",
            "priority": "Medium",
            "benefit": "Improves usability and accessibility."
        })

    # -------------------------
    # Missing H1
    # -------------------------
    h1_tags = soup.find_all("h1")

    if len(h1_tags) == 0:
        findings.append({
            "category": "UI/UX",
            "title": "Missing H1 heading",
            "severity": "High",
            "issue": "No H1 heading found.",
            "recommendation": "Add a clear page title using H1.",
            "priority": "High",
            "benefit": "Improves page hierarchy and user understanding."
        })

    # -------------------------
    # Too many H1 tags
    # -------------------------
    elif len(h1_tags) > 1:
        findings.append({
            "category": "UI/UX",
            "title": "Multiple H1 headings",
            "severity": "Low",
            "issue": f"{len(h1_tags)} H1 tags found.",
            "recommendation": "Use a single primary H1 heading.",
            "priority": "Low",
            "benefit": "Improves structure and readability."
        })

    # -------------------------
    # Missing buttons
    # -------------------------
    buttons = soup.find_all("button")

    if len(buttons) == 0:
        findings.append({
            "category": "UI/UX",
            "title": "No buttons detected",
            "severity": "Low",
            "issue": "No button elements found.",
            "recommendation": "Provide clear call-to-action buttons.",
            "priority": "Medium",
            "benefit": "Improves user engagement."
        })

    # -------------------------
    # Missing forms
    # -------------------------
    forms = soup.find_all("form")

    if len(forms) == 0:
        findings.append({
            "category": "UI/UX",
            "title": "No forms detected",
            "severity": "Low",
            "issue": "No forms found on the page.",
            "recommendation": "Add contact or inquiry forms where appropriate.",
            "priority": "Low",
            "benefit": "Improves user interaction."
        })

    # -------------------------
    # Broken links
    # -------------------------
    links = soup.find_all("a")

    empty_links = [
        link for link in links
        if not link.get("href")
        or link.get("href") == "#"
    ]

    if empty_links:
        findings.append({
            "category": "UI/UX",
            "title": "Empty links found",
            "severity": "Medium",
            "issue": f"{len(empty_links)} empty links detected.",
            "recommendation": "Replace placeholder links with valid destinations.",
            "priority": "Medium",
            "benefit": "Improves navigation."
        })

    return findings