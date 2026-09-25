import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)


def analyze_seo(url: str):
    """
    Perform a real SEO analysis.

    Returns:
        seo_score
        metrics
        findings

    A failed analysis returns seo_score=None.
    It is NOT converted into a fake score of 0.
    """

    findings = []

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": USER_AGENT
            },
            allow_redirects=True,
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # =====================================================
        # BASIC PAGE DATA
        # =====================================================

        title_tag = soup.title

        title = (
            title_tag.get_text(strip=True)
            if title_tag
            else ""
        )

        meta_description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        meta_description_content = (
            meta_description.get("content", "").strip()
            if meta_description
            else ""
        )

        h1_tags = soup.find_all("h1")

        images = soup.find_all("img")

        missing_alt = sum(
            1
            for image in images
            if not image.get("alt")
            or not image.get("alt").strip()
        )

        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        canonical = soup.find(
            "link",
            attrs={"rel": "canonical"}
        )

        # =====================================================
        # ROBOTS
        # =====================================================

        robots_status = None

        try:
            robots_response = requests.get(
                url.rstrip("/") + "/robots.txt",
                timeout=5,
                headers={
                    "User-Agent": USER_AGENT
                }
            )

            robots_status = robots_response.status_code

        except requests.RequestException:
            robots_status = None

        # =====================================================
        # SITEMAP
        # =====================================================

        sitemap_status = None

        try:
            sitemap_response = requests.get(
                url.rstrip("/") + "/sitemap.xml",
                timeout=5,
                headers={
                    "User-Agent": USER_AGENT
                }
            )

            sitemap_status = sitemap_response.status_code

        except requests.RequestException:
            sitemap_status = None

        # =====================================================
        # STRUCTURED DATA
        # =====================================================

        structured_data = soup.find_all(
            "script",
            attrs={
                "type": "application/ld+json"
            }
        )

        # =====================================================
        # SOCIAL META
        # =====================================================

        open_graph_tags = soup.find_all(
            "meta",
            attrs={
                "property": lambda value:
                    value and value.startswith("og:")
            }
        )

        twitter_tags = soup.find_all(
            "meta",
            attrs={
                "name": lambda value:
                    value and value.startswith("twitter:")
            }
        )

        # =====================================================
        # METRICS
        # =====================================================

        metrics = {
            "http_status": response.status_code,

            "final_url": response.url,

            "uses_https": response.url.startswith(
                "https://"
            ),

            "title": title,

            "title_length": len(title),

            "has_title": bool(title),

            "meta_description":
                meta_description_content,

            "meta_description_length":
                len(meta_description_content),

            "has_meta_description":
                bool(meta_description_content),

            "h1_count":
                len(h1_tags),

            "image_count":
                len(images),

            "images_missing_alt":
                missing_alt,

            "images_with_alt":
                max(
                    len(images) - missing_alt,
                    0
                ),

            "has_viewport":
                viewport is not None,

            "has_canonical":
                canonical is not None,

            "robots_status":
                robots_status,

            "robots_available":
                robots_status == 200,

            "sitemap_status":
                sitemap_status,

            "sitemap_available":
                sitemap_status == 200,

            "structured_data_count":
                len(structured_data),

            "open_graph_count":
                len(open_graph_tags),

            "twitter_card_count":
                len(twitter_tags),
        }

        # =====================================================
        # SCORING
        #
        # This score is derived ONLY from checks actually
        # performed above.
        # =====================================================

        score = 100

        # HTTP status
        if response.status_code != 200:
            findings.append({
                "category": "SEO",
                "issue": (
                    f"Website returned HTTP "
                    f"{response.status_code}"
                ),
                "recommendation": (
                    "Ensure the main page returns "
                    "HTTP 200 OK."
                ),
                "priority": "High",
                "benefit": (
                    "Allows search engines to "
                    "crawl the page correctly."
                )
            })

            score -= 20

        # HTTPS
        if not response.url.startswith("https://"):

            findings.append({
                "category": "SEO",
                "issue": "Website is not using HTTPS.",
                "recommendation": (
                    "Install an SSL certificate and "
                    "redirect HTTP traffic to HTTPS."
                ),
                "priority": "High",
                "benefit": (
                    "Improves security, trust, "
                    "and search visibility."
                )
            })

            score -= 15

        # Title
        if not title:

            findings.append({
                "category": "SEO",
                "issue": "Missing title tag.",
                "recommendation": (
                    "Add a descriptive HTML title."
                ),
                "priority": "High",
                "benefit": (
                    "Helps search engines and users "
                    "understand the page."
                )
            })

            score -= 15

        elif len(title) < 30 or len(title) > 60:

            findings.append({
                "category": "SEO",
                "issue": (
                    f"Title length is {len(title)} "
                    "characters."
                ),
                "recommendation": (
                    "Use a concise title, "
                    "ideally around 30-60 characters."
                ),
                "priority": "Medium",
                "benefit": (
                    "Improves search-result presentation."
                )
            })

            score -= 5

        # Meta description
        if not meta_description_content:

            findings.append({
                "category": "SEO",
                "issue": "Missing meta description.",
                "recommendation": (
                    "Add a descriptive meta description."
                ),
                "priority": "High",
                "benefit": (
                    "Improves search-result "
                    "click-through potential."
                )
            })

            score -= 15

        elif (
            len(meta_description_content) < 120
            or len(meta_description_content) > 160
        ):

            findings.append({
                "category": "SEO",
                "issue": (
                    "Meta description length is "
                    f"{len(meta_description_content)} "
                    "characters."
                ),
                "recommendation": (
                    "Aim for approximately "
                    "120-160 characters."
                ),
                "priority": "Medium",
                "benefit": (
                    "Provides a clearer search-result "
                    "description."
                )
            })

            score -= 5

        # H1
        if len(h1_tags) == 0:

            findings.append({
                "category": "SEO",
                "issue": "Missing H1 heading.",
                "recommendation": (
                    "Add one primary H1 heading."
                ),
                "priority": "High",
                "benefit": (
                    "Improves content hierarchy."
                )
            })

            score -= 10

        elif len(h1_tags) > 1:

            findings.append({
                "category": "SEO",
                "issue": (
                    f"{len(h1_tags)} H1 headings found."
                ),
                "recommendation": (
                    "Use one primary H1 heading."
                ),
                "priority": "Medium",
                "benefit": (
                    "Improves document structure."
                )
            })

            score -= 5

        # Images
        if missing_alt > 0:

            deduction = min(
                missing_alt * 2,
                10
            )

            findings.append({
                "category": "SEO",
                "issue": (
                    f"{missing_alt} image(s) "
                    "missing ALT text."
                ),
                "recommendation": (
                    "Add meaningful ALT text "
                    "to informative images."
                ),
                "priority": "Medium",
                "benefit": (
                    "Improves accessibility "
                    "and image search."
                )
            })

            score -= deduction

        # Viewport
        if viewport is None:

            findings.append({
                "category": "SEO",
                "issue": (
                    "Missing viewport meta tag."
                ),
                "recommendation": (
                    "Add a responsive viewport "
                    "meta tag."
                ),
                "priority": "High",
                "benefit": (
                    "Improves mobile rendering."
                )
            })

            score -= 10

        # Robots
        if robots_status != 200:

            findings.append({
                "category": "SEO",
                "issue": "robots.txt not found.",
                "recommendation": (
                    "Provide a valid robots.txt "
                    "where appropriate."
                ),
                "priority": "Medium",
                "benefit": (
                    "Provides crawler instructions."
                )
            })

            score -= 5

        # Sitemap
        if sitemap_status != 200:

            findings.append({
                "category": "SEO",
                "issue": "sitemap.xml not found.",
                "recommendation": (
                    "Provide an XML sitemap "
                    "where appropriate."
                ),
                "priority": "Medium",
                "benefit": (
                    "Helps search engines discover URLs."
                )
            })

            score -= 5

        # Canonical
        if canonical is None:

            findings.append({
                "category": "SEO",
                "issue": "Canonical tag missing.",
                "recommendation": (
                    "Add a canonical URL when "
                    "duplicate URL variants exist."
                ),
                "priority": "Medium",
                "benefit": (
                    "Helps control duplicate URL signals."
                )
            })

            score -= 5

        return {
            "seo_score": round(
                max(0, min(100, score)),
                1
            ),

            "metrics": metrics,

            "findings": findings
        }

    except requests.RequestException as exc:

        return {
            "seo_score": None,

            "metrics": {
                "error": str(exc)
            },

            "findings": [{
                "category": "SEO",
                "issue": (
                    f"SEO analysis could not "
                    f"complete: {exc}"
                ),
                "recommendation": (
                    "Verify that the website "
                    "is reachable."
                ),
                "priority": "High",
                "benefit": (
                    "Allows the SEO analyzer "
                    "to inspect the page."
                )
            }]
        }

    except Exception as exc:

        return {
            "seo_score": None,

            "metrics": {
                "error": str(exc)
            },

            "findings": [{
                "category": "SEO",
                "issue": (
                    f"SEO analysis failed: {exc}"
                ),
                "recommendation": (
                    "Review the website response "
                    "and analyzer configuration."
                ),
                "priority": "High",
                "benefit": (
                    "Allows accurate SEO analysis."
                )
            }]
        }