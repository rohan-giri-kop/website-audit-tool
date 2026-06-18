from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import requests

from bs4 import BeautifulSoup
from backend.app.utils.grades import score_to_grade

from backend.app.analyzers.seo_analyzer import analyze_seo
from backend.app.analyzers.performance_analyzer import analyze_performance
from backend.app.analyzers.accessibility_analyzer import analyze_accessibility
from backend.app.analyzers.security_analyzer import analyze_security
from backend.app.analyzers.mobile_analyzer import analyze_mobile
from backend.app.utils.screenshot import capture_screenshot
from backend.app.analyzers.uiux_analyzer import analyze_uiux
from backend.app.services.gemini_service import generate_recommendations

@dataclass
class FindingDraft:
    category: str
    issue: str
    recommendation: str
    priority: str
    benefit: str


def _safe_get(url: str):
    try:
        response = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            }
        )

        print("STATUS:", response.status_code)

        if response.status_code >= 400:
            return None

        return response

    except Exception as e:
        print("ERROR:", e)
        return None    
     
    
def _check_link(url: str) -> bool:
    try:
        response = requests.head(url, timeout=8, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        return response.status_code < 400
    except requests.RequestException:
        return False


def analyze_website(url: str) -> dict:
    response = _safe_get(url)

    screenshot_path = None

    try:
        screenshot_path = capture_screenshot(url)
    except Exception as e:
        print("Screenshot Error:", e)

    if response is None:
        return _offline_result(url)

    soup = BeautifulSoup(response.text, "html.parser")
    seo_result = analyze_seo(url)

    seo_score = seo_result["seo_score"]

    findings: list[FindingDraft] = []

    for item in seo_result["findings"]:
        findings.append(
            FindingDraft(
                category=item["category"],
                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"],
            )
        )
            
    parsed = urlparse(url)
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    canonical = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    robots = soup.find("meta", attrs={"name": "robots"})
    viewport = soup.find("meta", attrs={"name": "viewport"})
    h1_tags = soup.find_all("h1")
    images = soup.find_all("img")
    internal_links = 0
    external_links = 0
    broken_links = 0

    for anchor in soup.find_all("a", href=True)[:30]:
        target = urljoin(url, anchor["href"])
        if urlparse(target).netloc == parsed.netloc:
            internal_links += 1
        else:
            external_links += 1
        if not _check_link(target):
            broken_links += 1

    performance_result = analyze_performance(url)

    performance_score = performance_result["performance_score"]
    performance_metrics = performance_result.get("metrics", {})

    for item in performance_result["findings"]:
        findings.append(
            FindingDraft(
                category=item["category"],
                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"]
            )
        )
        
        
    accessibility_result = analyze_accessibility(soup)

    accessibility_score = accessibility_result["accessibility_score"]
    
    accessibility_metrics = accessibility_result.get(
        "metrics",
        {}
    )

    for item in accessibility_result["findings"]:
        findings.append(
            FindingDraft(
                category=item["category"],
                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"]
            )
        )
        
    security_result = analyze_security(url)
    
    security_metrics = security_result.get("metrics", {})

    security_score = security_result["security_score"]

    for item in security_result["findings"]:        
        findings.append(
            FindingDraft(
                category=item["category"],
                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"]
            )
        )      
    
    mobile_result = analyze_mobile(url)

    mobile_score = mobile_result["score"]
    
    mobile_metrics = mobile_result.get(
        "metrics",
        {}
    )

    for item in mobile_result["findings"]:
        findings.append(
            FindingDraft(
                category="Mobile",
                issue=item["issue"],
                recommendation="Improve mobile responsiveness.",
                priority=item["severity"].capitalize(),
                benefit="Better experience for mobile visitors."
            )
        )
        
    uiux_findings = analyze_uiux(response.text)

    for item in uiux_findings:
        findings.append(
            FindingDraft(
                category=item["category"],
                issue=item["issue"],
                recommendation=item["recommendation"],
                priority=item["priority"],
                benefit=item["benefit"]
            )
        )    

    # Overall Score
    overall_score = round(
        (
            seo_score +
            performance_score +
            accessibility_score +
            security_score +
            mobile_score
        ) / 5,
        1
    )
    
    scores = {
        "SEO": seo_score,
        "Performance": performance_score,
        "Accessibility": accessibility_score,
        "Security": security_score,
        "Mobile": mobile_score
    }

    weakest_area = min(scores, key=scores.get)

    summary = (
        f"{url} scored {overall_score}/100 overall. "
        f"The biggest improvement opportunity is "
        f"{weakest_area} with a score of "
        f"{scores[weakest_area]:.1f}."
    )     
     
     
    if not findings:
        findings.append(FindingDraft("SEO", "No major issues detected", "Maintain content quality and performance monitoring.", "Low", "Helps preserve strong baseline health."))

    recommendations = generate_recommendations(
            [finding.__dict__ for finding in findings]
        )
    
    print(type(recommendations))
    print("TYPE =", type(recommendations))
    print("VALUE =", recommendations)
    
    print("AI RECOMMENDATIONS:")
    print(recommendations)
    
    return {
        "seo_score": round(seo_score, 1),
        "performance_score": round(performance_score, 1),
        "screenshot_path": screenshot_path,
        "accessibility_score": round(accessibility_score, 1),
        "security_score": round(security_score, 1),
        "accessibility_metrics": accessibility_metrics,
        "security_metrics": security_metrics,
        "mobile_score": round(mobile_score, 1),
        "mobile_metrics": mobile_metrics,
        "overall_score": overall_score,
        "grade": score_to_grade(overall_score),
        "summary": summary,
        "performance_metrics": performance_metrics,
        "findings": [finding.__dict__ for finding in findings],
        "recommendations": recommendations,
        "page_details": {
            "title_tag": title,
            "meta_description": meta_description.get("content") if meta_description else "",
            "meta_keywords": meta_keywords.get("content") if meta_keywords else "",
            "canonical_url": canonical.get("href") if canonical else "",
            "robots_meta": robots.get("content") if robots else "",
            "viewport": viewport.get("content") if viewport else "",
            "h1_count": len(h1_tags),
            "internal_links": internal_links,
            "external_links": external_links,
            "broken_links": broken_links,
            "image_count": len(images),
            "structured_data": bool(soup.find_all("script", attrs={"type": "application/ld+json"})),
            "open_graph_tags": len(soup.find_all("meta", attrs={"property": lambda value: value and value.startswith("og:")})),
            "twitter_tags": len(soup.find_all("meta", attrs={"name": lambda value: value and value.startswith("twitter:")})),
        },
    }


def _offline_result(url: str):
    performance_result = analyze_performance(url)

    performance_score = performance_result.get(
        "performance_score",
        0
    )

    return {
        "seo_score": 0,
        "performance_score": performance_score,
        "accessibility_score": 0,
        "security_score": 0,
        "mobile_score": 0,
        "overall_score": performance_score / 5,
        "grade": "F",
        "summary": "Website could not be accessed.",
        "performance_metrics": performance_result.get("metrics", {}),
        "accessibility_metrics": {},
        "security_metrics": {},
        "mobile_metrics": {},
        "findings": [
            {
                "category": "Website",
                "issue": "Website could not be accessed",
                "recommendation": "Verify URL and server availability.",
                "priority": "High",
                "benefit": "Allows complete audit analysis."
            }
        ],
        "page_details": {}
    }