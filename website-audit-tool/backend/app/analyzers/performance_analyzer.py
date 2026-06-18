from backend.app.utils.lighthouse import run_lighthouse


def _to_seconds(value):
    try:
        return float(
            str(value)
            .replace(" s", "")
            .replace("\xa0s", "")
        )
    except (ValueError, TypeError):
        return 0.0


def analyze_performance(url: str):
    try:
        lighthouse = run_lighthouse(url)
    except Exception as e:
        return {
            "performance_score": 0,
            "metrics": {},
            "findings": [{
                "category": "Performance",
                "issue": f"Performance audit failed: {str(e)}",
                "recommendation": "Verify Lighthouse installation and website accessibility.",
                "priority": "High",
                "benefit": "Allows accurate performance analysis."
            }]
        }

    findings = []

    score = float(lighthouse["performance_score"])

    fcp = _to_seconds(
        lighthouse["first_contentful_paint"]
    )

    lcp = _to_seconds(
        lighthouse["largest_contentful_paint"]
    )

    speed_index = _to_seconds(
        lighthouse["speed_index"]
    )

    tti = _to_seconds(
        lighthouse["time_to_interactive"]
    )

    tbt = float(
        lighthouse["total_blocking_time"]
    )

    cls = float(
        lighthouse["cls"]
    )

    # LCP
    if lcp > 2.5:
        findings.append({
            "category": "Performance",
            "issue": f"Large Contentful Paint is {lcp:.2f}s",
            "recommendation": "Optimize images and server response.",
            "priority": "High",
            "benefit": "Improves loading performance."
        })

    # FCP
    if fcp > 1.8:
        findings.append({
            "category": "Performance",
            "issue": f"First Contentful Paint is {fcp:.2f}s",
            "recommendation": "Reduce render-blocking resources.",
            "priority": "Medium",
            "benefit": "Displays content faster."
        })

    # Speed Index
    if speed_index > 3:
        findings.append({
            "category": "Performance",
            "issue": f"Speed Index is {speed_index:.2f}s",
            "recommendation": "Optimize critical rendering path.",
            "priority": "Medium",
            "benefit": "Improves perceived speed."
        })

    # TTI
    if tti > 3.8:
        findings.append({
            "category": "Performance",
            "issue": f"Time To Interactive is {tti:.2f}s",
            "recommendation": "Reduce JavaScript execution.",
            "priority": "High",
            "benefit": "Improves responsiveness."
        })

    # TBT
    if tbt > 200:
        findings.append({
            "category": "Performance",
            "issue": f"Total Blocking Time is {tbt}ms",
            "recommendation": "Break large JavaScript tasks.",
            "priority": "High",
            "benefit": "Improves interactivity."
        })

    # CLS
    if cls > 0.1:
        findings.append({
            "category": "Performance",
            "issue": f"Cumulative Layout Shift is {cls:.3f}",
            "recommendation": "Reserve image and ad space.",
            "priority": "Medium",
            "benefit": "Improves visual stability."
        })

    return {
        "performance_score": score,
        "metrics": lighthouse,
        "findings": findings
    }