def generate_recommendations(findings):
    recommendations = []
    seen = set()

    for finding in findings:
        issue = finding.get("issue", "").lower()

        recommendation = None

        if "meta description" in issue:
            recommendation = {
                "priority": "High",
                "recommendation": "Add a meta description between 150-160 characters."
            }

        elif "https" in issue:
            recommendation = {
                "priority": "Critical",
                "recommendation": "Enable SSL certificate and redirect all traffic to HTTPS."
            }

        elif "alt" in issue:
            recommendation = {
                "priority": "Medium",
                "recommendation": "Add descriptive ALT text to images."
            }

        elif "mobile" in issue:
            recommendation = {
                "priority": "High",
                "recommendation": "Improve responsive design for smaller screens."
            }

        elif "performance" in issue:
            recommendation = {
                "priority": "High",
                "recommendation": "Optimize images, CSS, JS and enable caching."
            }

        elif "accessibility" in issue:
            recommendation = {
                "priority": "Medium",
                "recommendation": "Improve contrast, labels and keyboard navigation."
            }

        if recommendation:
            key = recommendation["recommendation"]

            if key not in seen:
                seen.add(key)
                recommendations.append(recommendation)

    return recommendations