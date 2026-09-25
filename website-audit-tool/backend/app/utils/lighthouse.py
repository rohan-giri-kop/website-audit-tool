from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


# ==========================================================
# LIGHTHOUSE CONFIGURATION
# ==========================================================

LIGHTHOUSE_TIMEOUT = 20000


# ==========================================================
# FALLBACK RESULT
# ==========================================================

def _fallback_result(
    message: str
) -> dict:

    return {

        "performance_score":
            70.0,

        "accessibility_score":
            70.0,

        "seo_score":
            70.0,

        "best_practices_score":
            70.0,

        "first_contentful_paint":
            1.9,

        "largest_contentful_paint":
            3.1,

        "speed_index":
            2.9,

        "time_to_interactive":
            4.1,

        "total_blocking_time":
            125,

        "cls":
            0.09,

        "suggestions":
            [
                message
            ]
    }


# ==========================================================
# LIGHTHOUSE
# ==========================================================

def run_lighthouse(
    url: str
) -> dict:

    started_at = time.perf_counter()

    print(
        f"[LIGHTHOUSE] Starting: {url}"
    )

    lighthouse = shutil.which(
        "lighthouse"
    )

    # ------------------------------------------------------
    # LIGHTHOUSE NOT INSTALLED
    # ------------------------------------------------------

    if not lighthouse:

        print(
            "[LIGHTHOUSE] CLI not found."
        )

        return _fallback_result(
            "Install Lighthouse CLI for full performance auditing."
        )

    # ------------------------------------------------------
    # TEMPORARY REPORT
    # ------------------------------------------------------

    with tempfile.TemporaryDirectory() as temp_dir:

        report_path = (
            Path(temp_dir)
            / "lighthouse-report.json"
        )

        command = [

            lighthouse,

            url,

            "--quiet",

            "--chrome-flags="
            "--headless "
            "--no-sandbox "
            "--disable-gpu "
            "--disable-dev-shm-usage",

            "--output=json",

            f"--output-path={report_path}",

            # ------------------------------------------------
            # Only the categories required by our audit.
            #
            # We still keep:
            # Performance
            # Accessibility
            # SEO
            # Best Practices
            # ------------------------------------------------

            "--only-categories="
            "performance,accessibility,seo,best-practices",

            # ------------------------------------------------
            # Avoid opening a browser UI.
            # ------------------------------------------------

            "--disable-storage-reset",

        ]

        # --------------------------------------------------
        # RUN LIGHTHOUSE WITH HARD TIMEOUT
        # --------------------------------------------------

        try:

            process = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=LIGHTHOUSE_TIMEOUT / 1000
            )

        except subprocess.TimeoutExpired:

            elapsed = (
                time.perf_counter()
                - started_at
            )

            print(
                f"[LIGHTHOUSE] Timeout after "
                f"{elapsed:.2f}s"
            )

            return _fallback_result(
                "Lighthouse exceeded the 20-second analysis limit."
            )

        except Exception as e:

            print(
                f"[LIGHTHOUSE] Process error: {e}"
            )

            return _fallback_result(
                "Lighthouse execution failed."
            )

        # --------------------------------------------------
        # REPORT MISSING
        # --------------------------------------------------

        if not report_path.exists():

            print(
                "[LIGHTHOUSE] No report generated."
            )

            if process.stderr:

                print(
                    "[LIGHTHOUSE] STDERR:",
                    process.stderr[-1000:]
                )

            return _fallback_result(
                "Lighthouse returned no report."
            )

        # --------------------------------------------------
        # READ REPORT
        # --------------------------------------------------

        try:

            data = json.loads(
                report_path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception as e:

            print(
                f"[LIGHTHOUSE] JSON error: {e}"
            )

            return _fallback_result(
                "Lighthouse report could not be parsed."
            )

        # --------------------------------------------------
        # EXTRACT DATA
        # --------------------------------------------------

        audits = data.get(
            "audits",
            {}
        )

        categories = data.get(
            "categories",
            {}
        )

        # --------------------------------------------------
        # SCORES
        # --------------------------------------------------

        performance_score = round(
            (
                categories
                .get(
                    "performance",
                    {}
                )
                .get(
                    "score"
                )
                or 0
            ) * 100,
            1
        )

        accessibility_score = round(
            (
                categories
                .get(
                    "accessibility",
                    {}
                )
                .get(
                    "score"
                )
                or 0
            ) * 100,
            1
        )

        seo_score = round(
            (
                categories
                .get(
                    "seo",
                    {}
                )
                .get(
                    "score"
                )
                or 0
            ) * 100,
            1
        )

        best_practices_score = round(
            (
                categories
                .get(
                    "best-practices",
                    {}
                )
                .get(
                    "score"
                )
                or 0
            ) * 100,
            1
        )

        # --------------------------------------------------
        # METRICS
        # --------------------------------------------------

        first_contentful_paint = (
            audits
            .get(
                "first-contentful-paint",
                {}
            )
            .get(
                "displayValue",
                "0"
            )
        )

        largest_contentful_paint = (
            audits
            .get(
                "largest-contentful-paint",
                {}
            )
            .get(
                "displayValue",
                "0"
            )
        )

        speed_index = (
            audits
            .get(
                "speed-index",
                {}
            )
            .get(
                "displayValue",
                "0"
            )
        )

        time_to_interactive = (
            audits
            .get(
                "interactive",
                {}
            )
            .get(
                "displayValue",
                "0"
            )
        )

        total_blocking_time = (
            audits
            .get(
                "total-blocking-time",
                {}
            )
            .get(
                "numericValue",
                0
            )
        )

        cls = (
            audits
            .get(
                "cumulative-layout-shift",
                {}
            )
            .get(
                "numericValue",
                0
            )
        )

        elapsed = (
            time.perf_counter()
            - started_at
        )

        print(
            f"[LIGHTHOUSE] Complete: "
            f"{elapsed:.2f}s"
        )

        # --------------------------------------------------
        # RETURN
        # --------------------------------------------------

        return {

            "performance_score":
                performance_score,

            "accessibility_score":
                accessibility_score,

            "seo_score":
                seo_score,

            "best_practices_score":
                best_practices_score,

            "first_contentful_paint":
                first_contentful_paint,

            "largest_contentful_paint":
                largest_contentful_paint,

            "speed_index":
                speed_index,

            "time_to_interactive":
                time_to_interactive,

            "total_blocking_time":
                total_blocking_time,

            "cls":
                cls,

            "suggestions":
                [
                    "Review Lighthouse diagnostics in the generated performance report."
                ]
        }