from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

import requests
from bs4 import BeautifulSoup

from backend.app.utils.grades import score_to_grade

from backend.app.analyzers.seo_analyzer import analyze_seo
from backend.app.analyzers.performance_analyzer import analyze_performance
from backend.app.analyzers.accessibility_analyzer import analyze_accessibility
from backend.app.analyzers.security_analyzer import analyze_security
from backend.app.analyzers.mobile_analyzer import analyze_mobile
from backend.app.analyzers.uiux_analyzer import analyze_uiux

from backend.app.utils.screenshot import capture_screenshot

from backend.app.services.gemini_service import (
    generate_recommendations
)


# ==========================================================
# FINDING MODEL
# ==========================================================

@dataclass
class FindingDraft:

    category: str
    issue: str
    recommendation: str
    priority: str
    benefit: str


# ==========================================================
# COMMON USER AGENT
# ==========================================================

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)


# ==========================================================
# SAFE HTTP GET
# ==========================================================

def _safe_get(url: str):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": USER_AGENT
            }
        )

        print(
            f"[AUDIT] HTTP STATUS: "
            f"{response.status_code}"
        )

        if response.status_code >= 400:

            return None

        return response

    except requests.RequestException as e:

        print(
            f"[AUDIT] HTTP ERROR: {e}"
        )

        return None

    except Exception as e:

        print(
            f"[AUDIT] Unexpected HTTP ERROR: {e}"
        )

        return None


# ==========================================================
# BROKEN LINK CHECK
# ==========================================================

def _check_link(url: str) -> bool:

    try:

        response = requests.head(
            url,
            timeout=3,
            allow_redirects=True,
            headers={
                "User-Agent": USER_AGENT
            }
        )

        # Some websites reject HEAD requests.
        # In that case try a lightweight GET.
        if response.status_code >= 400:

            try:

                response = requests.get(
                    url,
                    timeout=3,
                    allow_redirects=True,
                    headers={
                        "User-Agent": USER_AGENT
                    },
                    stream=True
                )

            except Exception:

                return False

        return response.status_code < 400

    except requests.RequestException:

        return False

    except Exception:

        return False


# ==========================================================
# SAFE ANALYZER WRAPPERS
# ==========================================================

def _run_seo(url: str):

    started = time.perf_counter()

    try:

        result = analyze_seo(url)

        print(
            f"[AUDIT] SEO complete: "
            f"{time.perf_counter() - started:.2f}s"
        )

        return result

    except Exception as e:

        print(
            f"[AUDIT] SEO ERROR: {e}"
        )

        return {
            "seo_score": 0,
            "findings": [
                {
                    "category": "SEO",
                    "issue": f"SEO audit failed: {str(e)}",
                    "recommendation": (
                        "Verify the website is accessible "
                        "and try the audit again."
                    ),
                    "priority": "High",
                    "benefit": (
                        "Allows the website to be "
                        "properly analyzed."
                    )
                }
            ]
        }


# ==========================================================
# PERFORMANCE
# ==========================================================

def _run_performance(url: str):

    started = time.perf_counter()

    try:

        result = analyze_performance(url)

        print(
            f"[AUDIT] Performance complete: "
            f"{time.perf_counter() - started:.2f}s"
        )

        return result

    except Exception as e:

        print(
            f"[AUDIT] Performance ERROR: {e}"
        )

        return {
            "performance_score": 0,
            "metrics": {},
            "findings": [
                {
                    "category": "Performance",
                    "issue": (
                        f"Performance audit failed: {str(e)}"
                    ),
                    "recommendation": (
                        "Verify Lighthouse installation "
                        "and website accessibility."
                    ),
                    "priority": "High",
                    "benefit": (
                        "Allows accurate performance analysis."
                    )
                }
            ]
        }


# ==========================================================
# SECURITY
# ==========================================================

def _run_security(url: str):

    started = time.perf_counter()

    try:

        result = analyze_security(url)

        print(
            f"[AUDIT] Security complete: "
            f"{time.perf_counter() - started:.2f}s"
        )

        return result

    except Exception as e:

        print(
            f"[AUDIT] Security ERROR: {e}"
        )

        return {
            "security_score": 0,
            "metrics": {},
            "findings": [
                {
                    "category": "Security",
                    "issue": (
                        f"Security audit failed: {str(e)}"
                    ),
                    "recommendation": (
                        "Verify the website URL "
                        "and network connectivity."
                    ),
                    "priority": "High",
                    "benefit": (
                        "Allows accurate security analysis."
                    )
                }
            ]
        }


# ==========================================================
# MOBILE
# ==========================================================

def _run_mobile(url: str):

    started = time.perf_counter()

    try:

        result = analyze_mobile(url)

        print(
            f"[AUDIT] Mobile complete: "
            f"{time.perf_counter() - started:.2f}s"
        )

        return result

    except Exception as e:

        print(
            f"[AUDIT] Mobile ERROR: {e}"
        )

        return {
            "score": 0,
            "metrics": {},
            "findings": [
                {
                    "severity": "high",
                    "issue": (
                        f"Mobile audit failed: {str(e)}"
                    )
                }
            ]
        }


# ==========================================================
# SCREENSHOT
# ==========================================================

def _run_screenshot(url: str):

    started = time.perf_counter()

    try:

        result = capture_screenshot(url)

        print(
            f"[AUDIT] Screenshot complete: "
            f"{time.perf_counter() - started:.2f}s"
        )

        return result

    except Exception as e:

        print(
            f"[AUDIT] Screenshot ERROR: {e}"
        )

        return None


# ==========================================================
# ANALYZE WEBSITE
# ==========================================================

def analyze_website(url: str) -> dict:

    audit_started_at = time.perf_counter()

    print("")
    print("=" * 70)
    print(
        f"[AUDIT] Starting audit: {url}"
    )
    print("=" * 70)

    # ======================================================
    # STEP 1 — INITIAL WEBSITE FETCH
    # ======================================================

    response = _safe_get(url)

    print(
        f"[AUDIT] Initial HTTP fetch: "
        f"{time.perf_counter() - audit_started_at:.2f}s"
    )

    # ======================================================
    # WEBSITE UNAVAILABLE
    # ======================================================

    if response is None:

        print(
            "[AUDIT] Website could not be accessed."
        )

        return _offline_result(url)

    # ======================================================
    # STEP 2 — PARSE HTML
    # ======================================================

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # ======================================================
    # STEP 3 — BASIC PAGE INFORMATION
    # ======================================================

    parsed = urlparse(url)

    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else ""
    )

    meta_description = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )

    meta_keywords = soup.find(
        "meta",
        attrs={
            "name": "keywords"
        }
    )

    canonical = soup.find(
        "link",
        attrs={
            "rel": lambda value:
                value and "canonical" in value
        }
    )

    robots = soup.find(
        "meta",
        attrs={
            "name": "robots"
        }
    )

    viewport = soup.find(
        "meta",
        attrs={
            "name": "viewport"
        }
    )

    h1_tags = soup.find_all("h1")

    images = soup.find_all("img")

    # ======================================================
    # STEP 4 — PARALLEL ANALYZERS
    # ======================================================
    #
    # These operations are independent:
    #
    # SEO
    # Performance / Lighthouse
    # Security
    # Mobile
    # Screenshot
    #
    # Running them together prevents:
    #
    # 16 sec screenshot
    # + 24 sec Lighthouse
    # + security
    # + mobile
    #
    # from becoming 40+ seconds.
    #
    # ======================================================

    print(
        "[AUDIT] Starting parallel analysis..."
    )

    parallel_started_at = time.perf_counter()

    parallel_results = {}

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = {

            executor.submit(
                _run_seo,
                url
            ): "seo",

            executor.submit(
                _run_performance,
                url
            ): "performance",

            executor.submit(
                _run_security,
                url
            ): "security",

            executor.submit(
                _run_mobile,
                url
            ): "mobile",

            executor.submit(
                _run_screenshot,
                url
            ): "screenshot"

        }

        for future in as_completed(futures):

            name = futures[future]

            try:

                parallel_results[name] = (
                    future.result()
                )

            except Exception as e:

                print(
                    f"[AUDIT] {name} "
                    f"unexpected ERROR: {e}"
                )

    print(
        f"[AUDIT] Parallel analysis complete: "
        f"{time.perf_counter() - parallel_started_at:.2f}s"
    )

    # ======================================================
    # GET PARALLEL RESULTS
    # ======================================================

    seo_result = parallel_results.get(
        "seo",
        {
            "seo_score": 0,
            "findings": []
        }
    )

    performance_result = parallel_results.get(
        "performance",
        {
            "performance_score": 0,
            "metrics": {},
            "findings": []
        }
    )

    security_result = parallel_results.get(
        "security",
        {
            "security_score": 0,
            "metrics": {},
            "findings": []
        }
    )

    mobile_result = parallel_results.get(
        "mobile",
        {
            "score": 0,
            "metrics": {},
            "findings": []
        }
    )

    screenshot_path = parallel_results.get(
        "screenshot"
    )

    # ======================================================
    # STEP 5 — ACCESSIBILITY
    # ======================================================
    #
    # This analyzer works directly on the already downloaded
    # HTML. No additional website request is required.
    #
    # ======================================================

    accessibility_started_at = time.perf_counter()

    try:

        accessibility_result = (
            analyze_accessibility(soup)
        )

    except Exception as e:

        print(
            f"[AUDIT] Accessibility ERROR: {e}"
        )

        accessibility_result = {
            "accessibility_score": 0,
            "metrics": {},
            "findings": [
                {
                    "category": "Accessibility",
                    "issue": (
                        f"Accessibility audit failed: {str(e)}"
                    ),
                    "recommendation": (
                        "Review accessibility manually."
                    ),
                    "priority": "High",
                    "benefit": (
                        "Improves accessibility for users."
                    )
                }
            ]
        }

    print(
        f"[AUDIT] Accessibility complete: "
        f"{time.perf_counter() - accessibility_started_at:.2f}s"
    )

    # ======================================================
    # STEP 6 — FINDINGS
    # ======================================================

    findings: list[FindingDraft] = []

    # ------------------------------------------------------
    # SEO FINDINGS
    # ------------------------------------------------------

    for item in seo_result.get(
        "findings",
        []
    ):

        findings.append(
            FindingDraft(
                category=item.get(
                    "category",
                    "SEO"
                ),
                issue=item.get(
                    "issue",
                    "SEO issue detected."
                ),
                recommendation=item.get(
                    "recommendation",
                    "Review SEO configuration."
                ),
                priority=item.get(
                    "priority",
                    "Medium"
                ),
                benefit=item.get(
                    "benefit",
                    "Improves website SEO."
                )
            )
        )

    # ------------------------------------------------------
    # PERFORMANCE FINDINGS
    # ------------------------------------------------------

    for item in performance_result.get(
        "findings",
        []
    ):

        findings.append(
            FindingDraft(
                category=item.get(
                    "category",
                    "Performance"
                ),
                issue=item.get(
                    "issue",
                    "Performance issue detected."
                ),
                recommendation=item.get(
                    "recommendation",
                    "Improve website performance."
                ),
                priority=item.get(
                    "priority",
                    "Medium"
                ),
                benefit=item.get(
                    "benefit",
                    "Improves website speed."
                )
            )
        )

    # ------------------------------------------------------
    # ACCESSIBILITY FINDINGS
    # ------------------------------------------------------

    for item in accessibility_result.get(
        "findings",
        []
    ):

        findings.append(
            FindingDraft(
                category=item.get(
                    "category",
                    "Accessibility"
                ),
                issue=item.get(
                    "issue",
                    "Accessibility issue detected."
                ),
                recommendation=item.get(
                    "recommendation",
                    "Improve accessibility."
                ),
                priority=item.get(
                    "priority",
                    "Medium"
                ),
                benefit=item.get(
                    "benefit",
                    "Improves accessibility."
                )
            )
        )

    # ------------------------------------------------------
    # SECURITY FINDINGS
    # ------------------------------------------------------

    for item in security_result.get(
        "findings",
        []
    ):

        findings.append(
            FindingDraft(
                category=item.get(
                    "category",
                    "Security"
                ),
                issue=item.get(
                    "issue",
                    "Security issue detected."
                ),
                recommendation=item.get(
                    "recommendation",
                    "Improve website security."
                ),
                priority=item.get(
                    "priority",
                    "Medium"
                ),
                benefit=item.get(
                    "benefit",
                    "Improves website security."
                )
            )
        )

    # ------------------------------------------------------
    # MOBILE FINDINGS
    # ------------------------------------------------------

    for item in mobile_result.get(
        "findings",
        []
    ):

        severity = item.get(
            "severity",
            "medium"
        )

        findings.append(
            FindingDraft(
                category="Mobile",
                issue=item.get(
                    "issue",
                    "Mobile usability issue detected."
                ),
                recommendation=(
                    item.get(
                        "recommendation",
                        "Improve mobile responsiveness."
                    )
                ),
                priority=str(
                    severity
                ).capitalize(),
                benefit=(
                    item.get(
                        "benefit",
                        "Improves mobile experience."
                    )
                )
            )
        )

    # ======================================================
    # STEP 7 — UI / UX
    # ======================================================

    uiux_started_at = time.perf_counter()

    try:

        uiux_result = analyze_uiux(
            response.text
        )

        if not isinstance(uiux_result, dict):
            raise TypeError(
                "UI/UX analyzer must return a dictionary."
            )

    except Exception as e:

        print(
            f"[AUDIT] UI/UX ERROR: {e}"
        )

        uiux_result = {
            "uiux_score": None,
            "uiux_metrics": {
                "error": str(e)
            },
            "findings": []
        }

    print(
        f"[AUDIT] UI/UX complete: "
        f"{time.perf_counter() - uiux_started_at:.2f}s"
    )

    # ------------------------------------------------------
    # REAL UI/UX SCORE
    # ------------------------------------------------------

    uiux_score = uiux_result.get(
        "uiux_score"
    )

    if uiux_score is not None:

        try:
            uiux_score = round(
                float(uiux_score),
                1
            )

        except (
            TypeError,
            ValueError
        ):

            uiux_score = None

    # ------------------------------------------------------
    # REAL UI/UX METRICS
    # ------------------------------------------------------

    uiux_metrics = uiux_result.get(
        "uiux_metrics",
        {}
    )

    if not isinstance(
        uiux_metrics,
        dict
    ):

        uiux_metrics = {}

    # ------------------------------------------------------
    # REAL UI/UX FINDINGS
    # ------------------------------------------------------

    uiux_findings = uiux_result.get(
        "findings",
        []
    )

    if not isinstance(
        uiux_findings,
        list
    ):

        uiux_findings = []

    for item in uiux_findings:

        # Ignore malformed entries rather than
        # crashing the complete audit.

        if not isinstance(
            item,
            dict
        ):
            print(
                "[AUDIT] Ignoring malformed "
                f"UI/UX finding: {item!r}"
            )
            continue

        findings.append(
            FindingDraft(
                category=item.get(
                    "category",
                    "UI/UX"
                ),

                issue=item.get(
                    "issue",
                    item.get(
                        "title",
                        "UI/UX issue detected."
                    )
                ),

                recommendation=item.get(
                    "recommendation",
                    "Improve user experience."
                ),

                priority=item.get(
                    "priority",
                    item.get(
                        "severity",
                        "Medium"
                    )
                ),

                benefit=item.get(
                    "benefit",
                    "Improves usability."
                )
            )
        )
        
    # ======================================================
    # STEP 8 — BROKEN LINKS
    # ======================================================

    broken_links_started_at = time.perf_counter()

    internal_links = 0
    external_links = 0
    broken_links = 0

    audit_links = []

    for anchor in soup.find_all(
        "a",
        href=True
    )[:20]:

        target = urljoin(
            url,
            anchor["href"]
        )

        parsed_target = urlparse(
            target
        )

        if parsed_target.scheme not in (
            "http",
            "https"
        ):

            continue

        if parsed_target.netloc == parsed.netloc:

            internal_links += 1

        else:

            external_links += 1

        audit_links.append(
            target
        )

    if audit_links:

        try:

            with ThreadPoolExecutor(
                max_workers=min(
                    8,
                    len(audit_links)
                )
            ) as executor:

                results = list(
                    executor.map(
                        _check_link,
                        audit_links
                    )
                )

            broken_links = sum(
                1
                for result in results
                if not result
            )

        except Exception as e:

            print(
                f"[AUDIT] Broken link ERROR: {e}"
            )

            broken_links = 0

    print(
        f"[AUDIT] Broken links complete: "
        f"{time.perf_counter() - broken_links_started_at:.2f}s"
    )

    # ======================================================
    # STEP 9 — SCORES
    # ======================================================

    seo_score = float(
        seo_result.get(
            "seo_score",
            0
        )
    )

    performance_score = float(
        performance_result.get(
            "performance_score",
            0
        )
    )

    accessibility_score = float(
        accessibility_result.get(
            "accessibility_score",
            0
        )
    )

    security_score = float(
        security_result.get(
            "security_score",
            0
        )
    )

    mobile_score = float(
        mobile_result.get(
            "score",
            0
        )
    )

    # ======================================================
    # METRICS
    # ======================================================

    performance_metrics = (
        performance_result.get(
            "metrics",
            {}
        )
    )

    accessibility_metrics = (
        accessibility_result.get(
            "metrics",
            {}
        )
    )

    security_metrics = (
        security_result.get(
            "metrics",
            {}
        )
    )

    mobile_metrics = (
        mobile_result.get(
            "metrics",
            {}
        )
    )

    # ======================================================
    # STEP 10 — OVERALL SCORE
    # ======================================================

    overall_score = round(
        (
            seo_score
            + performance_score
            + accessibility_score
            + security_score
            + mobile_score
        ) / 5,
        1
    )

    scores = {

        "SEO":
            seo_score,

        "Performance":
            performance_score,

        "Accessibility":
            accessibility_score,

        "Security":
            security_score,

        "Mobile":
            mobile_score

    }

    weakest_area = min(
        scores,
        key=scores.get
    )

    summary = (
        f"{url} scored "
        f"{overall_score}/100 overall. "
        f"The biggest improvement opportunity "
        f"is {weakest_area} with a score of "
        f"{scores[weakest_area]:.1f}."
    )

    # ======================================================
    # FALLBACK FINDING
    # ======================================================

    if not findings:

        findings.append(
            FindingDraft(
                category="General",
                issue="No major issues detected.",
                recommendation=(
                    "Maintain current website quality "
                    "and continue regular monitoring."
                ),
                priority="Low",
                benefit=(
                    "Helps preserve strong website health."
                )
            )
        )

    # ======================================================
    # STEP 11 — AI RECOMMENDATIONS
    # ======================================================

    ai_started_at = time.perf_counter()

    try:

        recommendations = generate_recommendations(
            [
                finding.__dict__
                for finding in findings
            ]
        )

        if not isinstance(
            recommendations,
            list
        ):

            recommendations = []

    except Exception as e:

        print(
            f"[AUDIT] AI recommendation ERROR: {e}"
        )

        recommendations = []

    print(
        f"[AUDIT] AI recommendations complete: "
        f"{time.perf_counter() - ai_started_at:.2f}s"
    )

    print(
        f"[AUDIT] AI recommendations generated: "
        f"{len(recommendations)}"
    )

    # ======================================================
    # STEP 12 — PAGE DETAILS
    # ======================================================

    page_details = {

        "title_tag":
            title,

        "meta_description":
            (
                meta_description.get("content")
                if meta_description
                else ""
            ),

        "meta_keywords":
            (
                meta_keywords.get("content")
                if meta_keywords
                else ""
            ),

        "canonical_url":
            (
                canonical.get("href")
                if canonical
                else ""
            ),

        "robots_meta":
            (
                robots.get("content")
                if robots
                else ""
            ),

        "viewport":
            (
                viewport.get("content")
                if viewport
                else ""
            ),

        "h1_count":
            len(h1_tags),

        "internal_links":
            internal_links,

        "external_links":
            external_links,

        "broken_links":
            broken_links,

        "image_count":
            len(images),

        "structured_data":
            bool(
                soup.find_all(
                    "script",
                    attrs={
                        "type":
                            "application/ld+json"
                    }
                )
            ),

        "open_graph_tags":
            len(
                soup.find_all(
                    "meta",
                    attrs={
                        "property":
                            lambda value:
                                value
                                and value.startswith(
                                    "og:"
                                )
                    }
                )
            ),

        "twitter_tags":
            len(
                soup.find_all(
                    "meta",
                    attrs={
                        "name":
                            lambda value:
                                value
                                and value.startswith(
                                    "twitter"
                                )
                    }
                )
            )
    }

    # ======================================================
    # FINAL RESULT
    # ======================================================

    total_time = (
        time.perf_counter()
        - audit_started_at
    )

    print("")
    print("=" * 70)

    print(
        f"[AUDIT] COMPLETE: "
        f"{total_time:.2f}s"
    )

    print(
        f"[AUDIT] Overall Score: "
        f"{overall_score}/100"
    )

    print(
        f"[AUDIT] Grade: "
        f"{score_to_grade(overall_score)}"
    )

    print(
        f"[AUDIT] Findings: "
        f"{len(findings)}"
    )

    print(
        f"[AUDIT] AI Recommendations: "
        f"{len(recommendations)}"
    )

    print("=" * 70)
    print("")

    return {
        "status": "completed",

        "error_message": None,

        "duration_seconds": round(
            total_time,
            2,
        ),

        "seo_score": round(
            seo_score,
            1,
        ),

        "seo_metrics": (
            seo_result.get(
                "metrics",
                {},
            )
            if isinstance(seo_result, dict)
            else {}
        ),

        "performance_score": round(
            performance_score,
            1,
        ),

        "performance_metrics": performance_metrics,

        "screenshot_path": screenshot_path,

        "accessibility_score": round(
            accessibility_score,
            1,
        ),

        "accessibility_metrics": accessibility_metrics,

        "security_score": round(
            security_score,
            1,
        ),

        "security_metrics": security_metrics,

        "mobile_score": round(
            mobile_score,
            1,
        ),

        "mobile_metrics": mobile_metrics,

        "uiux_score": uiux_score,

        "uiux_metrics": uiux_metrics,

        "overall_score": overall_score,

        "grade": score_to_grade(
            overall_score
        ),

        "summary": summary,

        "findings": [
            finding.__dict__
            for finding in findings
        ],

        "recommendations": recommendations,

        "page_details": page_details,
    }

# ==========================================================
# OFFLINE RESULT
# ==========================================================

def _offline_result(
    url: str
) -> dict:

    print(
        "[AUDIT] Creating offline result."
    )

    return {
        "status": "failed",

        "error_message": (
            f"Website could not be accessed: {url}"
        ),

        "duration_seconds": None,

        "seo_score": None,

        "seo_metrics": {},

        "performance_score": None,

        "performance_metrics": {},

        "accessibility_score": None,

        "accessibility_metrics": {},

        "security_score": None,

        "security_metrics": {},

        "mobile_score": None,

        "mobile_metrics": {},

        "uiux_score": None,

        "uiux_metrics": {},

        "overall_score": None,

        "grade": None,

        "summary": (
            "The website could not be accessed, "
            "so a complete audit could not be performed."
        ),

        "findings": [
            {
                "category": "Website",
                "issue": "Website could not be accessed.",
                "recommendation": (
                    "Verify the URL and confirm that "
                    "the website is publicly reachable."
                ),
                "priority": "High",
                "benefit": (
                    "Allows the complete website audit "
                    "to run successfully."
                ),
            }
        ],

        "recommendations": [],

        "page_details": {},
    }