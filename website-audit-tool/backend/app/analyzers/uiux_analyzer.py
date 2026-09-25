from bs4 import BeautifulSoup


def analyze_uiux(html_content: str):
    """
    Perform a real UI/UX analysis from the downloaded HTML.

    The score is derived from actual page checks.
    """

    findings = []

    soup = BeautifulSoup(
        html_content,
        "html.parser"
    )

    # =====================================================
    # PAGE ELEMENTS
    # =====================================================

    images = soup.find_all("img")

    missing_alt = [
        image
        for image in images
        if not image.get("alt")
        or not image.get("alt").strip()
    ]

    h1_tags = soup.find_all("h1")

    buttons = soup.find_all("button")

    forms = soup.find_all("form")

    links = soup.find_all("a")

    empty_links = [
        link
        for link in links
        if not link.get("href")
        or link.get("href").strip() == "#"
    ]

    # =====================================================
    # REAL METRICS
    # =====================================================

    metrics = {
        "image_count": len(images),

        "images_missing_alt":
            len(missing_alt),

        "images_with_alt":
            max(
                len(images) - len(missing_alt),
                0
            ),

        "h1_count":
            len(h1_tags),

        "button_count":
            len(buttons),

        "form_count":
            len(forms),

        "link_count":
            len(links),

        "empty_link_count":
            len(empty_links),
    }

    # =====================================================
    # SCORE
    #
    # Start at 100 and deduct only for issues that were
    # actually detected.
    # =====================================================

    score = 100

    # -----------------------------------------------------
    # Images
    # -----------------------------------------------------

    if missing_alt:

        score -= min(
            len(missing_alt) * 3,
            15
        )

        findings.append({
            "category": "UI/UX",
            "title": "Images missing alt text",
            "severity": "Medium",
            "issue": (
                f"{len(missing_alt)} image(s) "
                "missing alt text."
            ),
            "recommendation": (
                "Add meaningful alt text "
                "to informative images."
            ),
            "priority": "Medium",
            "benefit": (
                "Improves usability and accessibility."
            )
        })

    # -----------------------------------------------------
    # H1
    # -----------------------------------------------------

    if len(h1_tags) == 0:

        score -= 15

        findings.append({
            "category": "UI/UX",
            "title": "Missing H1 heading",
            "severity": "High",
            "issue": "No H1 heading found.",
            "recommendation": (
                "Add a clear primary H1 heading."
            ),
            "priority": "High",
            "benefit": (
                "Improves page hierarchy "
                "and content understanding."
            )
        })

    elif len(h1_tags) > 1:

        score -= 5

        findings.append({
            "category": "UI/UX",
            "title": "Multiple H1 headings",
            "severity": "Low",
            "issue": (
                f"{len(h1_tags)} H1 headings found."
            ),
            "recommendation": (
                "Use a single primary H1 heading."
            ),
            "priority": "Low",
            "benefit": (
                "Improves content structure."
            )
        })

    # -----------------------------------------------------
    # Buttons
    # -----------------------------------------------------

    if len(buttons) == 0:

        score -= 5

        findings.append({
            "category": "UI/UX",
            "title": "No buttons detected",
            "severity": "Low",
            "issue": (
                "No button elements were detected."
            ),
            "recommendation": (
                "Provide clear action controls "
                "where appropriate."
            ),
            "priority": "Low",
            "benefit": (
                "Improves user interaction."
            )
        })

    # -----------------------------------------------------
    # Forms
    # -----------------------------------------------------

    if len(forms) == 0:

        score -= 3

        findings.append({
            "category": "UI/UX",
            "title": "No forms detected",
            "severity": "Low",
            "issue": (
                "No form elements were detected."
            ),
            "recommendation": (
                "Add forms when user input "
                "is required by the page."
            ),
            "priority": "Low",
            "benefit": (
                "Supports user interaction "
                "where applicable."
            )
        })

    # -----------------------------------------------------
    # Empty links
    # -----------------------------------------------------

    if empty_links:

        score -= min(
            len(empty_links) * 4,
            15
        )

        findings.append({
            "category": "UI/UX",
            "title": "Empty links found",
            "severity": "Medium",
            "issue": (
                f"{len(empty_links)} empty "
                "or placeholder links detected."
            ),
            "recommendation": (
                "Replace placeholder links "
                "with valid destinations."
            ),
            "priority": "Medium",
            "benefit": (
                "Improves navigation clarity."
            )
        })

    return {
        "uiux_score": round(
            max(0, min(100, score)),
            1
        ),

        "uiux_metrics": metrics,

        "findings": findings
    }