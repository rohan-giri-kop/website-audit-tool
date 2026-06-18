import requests
from bs4 import BeautifulSoup


def analyze_seo(url: str):
    findings = []
    score = 100
    
    # Auto-fix URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        
        if response.status_code != 200:
            findings.append({
                "category": "SEO",
                "issue": f"Website returned HTTP {response.status_code}",
                "recommendation": "Ensure the website returns HTTP 200 OK.",
                "priority": "High",
                "benefit": "Allows search engines to properly crawl the website."
            })
            score -= 20

        soup = BeautifulSoup(response.text, "html.parser")
        
        # HTTPS Check
        if not url.startswith("https://"):
            findings.append({
                "category": "SEO",
                "issue": "Website is not using HTTPS",
                "recommendation": "Install an SSL certificate and redirect HTTP to HTTPS.",
                "priority": "High",
                "benefit": "Improves SEO, trust, and security."
            })

            score -= 15
        
        # Meta Description Check
        meta_description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if not meta_description:
            findings.append({
                "category": "SEO",
                "issue": "Missing meta description",
                "recommendation": "Add a meta description between 120-160 characters.",
                "priority": "High",
                "benefit": "Improves click-through rates from search engines."
            })
            score -= 15


        # H1 Check
        h1_tags = soup.find_all("h1")

        if len(h1_tags) == 0:
            findings.append({
                "category": "SEO",
                "issue": "Missing H1 heading",
                "recommendation": "Add a primary H1 heading to the page.",
                "priority": "High",
                "benefit": "Helps search engines understand page content."
            })
            score -= 10

        elif len(h1_tags) > 1:
            findings.append({
                "category": "SEO",
                "issue": "Multiple H1 headings found",
                "recommendation": "Use only one main H1 heading per page.",
                "priority": "Medium",
                "benefit": "Improves content hierarchy and SEO."
            })
            score -= 5
            
                
        # Image ALT Check
        images = soup.find_all("img")

        missing_alt = 0

        for img in images:
            if not img.get("alt"):
                missing_alt += 1

        if missing_alt > 0:
            findings.append({
                "category": "SEO",
                "issue": f"{missing_alt} image(s) missing ALT text",
                "recommendation": "Add descriptive ALT text to all images.",
                "priority": "Medium",
                "benefit": "Improves accessibility and image SEO."
            })

            score -= min(missing_alt * 2, 10) 
            
        # Viewport Check
        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        if not viewport:
            findings.append({
                "category": "SEO",
                "issue": "Missing viewport meta tag",
                "recommendation": "Add a responsive viewport meta tag.",
                "priority": "High",
                "benefit": "Improves mobile usability and SEO."
            })

            score -= 10      
            
        # Robots.txt Check
        try:
            robots_url = url.rstrip("/") + "/robots.txt"

            robots_response = requests.get(
                robots_url,
                timeout=5
            )

            if robots_response.status_code != 200:
                findings.append({
                    "category": "SEO",
                    "issue": "robots.txt file not found",
                    "recommendation": "Create a robots.txt file.",
                    "priority": "Medium",
                    "benefit": "Helps search engines crawl your website."
                })

                score -= 5

        except Exception:
            pass     
        
        # Sitemap Check
        try:
            sitemap_url = url.rstrip("/") + "/sitemap.xml"

            sitemap_response = requests.get(
                sitemap_url,
                timeout=5
            )

            if sitemap_response.status_code != 200:
                findings.append({
                    "category": "SEO",
                    "issue": "sitemap.xml not found",
                    "recommendation": "Generate and submit a sitemap.xml file.",
                    "priority": "Medium",
                    "benefit": "Improves search engine indexing."
                })

                score -= 5

        except Exception:
            pass     
        
        canonical = soup.find(
            "link",
            attrs={"rel": "canonical"}
        )

        if not canonical:
            findings.append({
                "category": "SEO",
                "issue": "Canonical tag missing",
                "recommendation": "Add a canonical URL.",
                "priority": "Medium",
                "benefit": "Avoids duplicate content issues."
            })

            score -= 5 

        # Title Check
        title = soup.title.string.strip() if soup.title else ""

        if not title:
            findings.append({
                "category": "SEO",
                "issue": "Missing title tag",
                "recommendation": "Add a title tag",
                "priority": "High",
                "benefit": "Improves search ranking"
            })
            score -= 20

        return {
            "seo_score": max(score, 0),
            "findings": findings
        }

    except Exception as e:
        return {
            "seo_score": 0,
            "findings": [{
                "category": "SEO",
                "issue": str(e),
                "recommendation": "Check website accessibility",
                "priority": "High",
                "benefit": "Allow SEO scanning"
            }]
        }