/* ==========================================================
   AI AUDIT
   REPORT PAGE
========================================================== */

(function () {

    "use strict";


    /* ======================================================
       STATE
    ====================================================== */

    let audit = null;


    /* ======================================================
       HELPERS
    ====================================================== */

    function getElement(id) {

        return document.getElementById(id);

    }


    function getAuditId() {

        const page =
            document.getElementById(
                "auditReportPage"
            );

        return page?.dataset.auditId || null;

    }


    function getAuthToken() {

        const keys = [

            "access_token",
            "token",
            "auth_token",
            "accessToken"

        ];


        for (const key of keys) {

            const local =
                localStorage.getItem(key);

            if (local) {

                return local;

            }

        }


        for (const key of keys) {

            const session =
                sessionStorage.getItem(key);

            if (session) {

                return session;

            }

        }


        return null;

    }


    function escapeHTML(value) {

        return String(
            value ?? ""
        )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

    }


    function numericValue(value) {

        const number =
            Number(value);

        return Number.isFinite(number)
            ? number
            : 0;

    }


    function clampScore(value) {

        return Math.max(
            0,
            Math.min(
                100,
                numericValue(value)
            )
        );

    }


    function formatScore(value) {

        const number =
            numericValue(value);

        if (
            Number.isInteger(number)
        ) {

            return String(number);

        }

        return number.toFixed(1);

    }


    function formatDate(value) {

        if (!value) {

            return "—";

        }


        const date =
            new Date(value);

        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return String(value);

        }


        return new Intl.DateTimeFormat(
            "en-IN",
            {
                dateStyle: "medium",
                timeStyle: "short"
            }
        ).format(date);

    }


    function getPriorityClass(priority) {

        const value =
            String(
                priority || "Medium"
            ).toLowerCase();


        if (
            value === "high"
        ) {

            return "high";

        }

        if (
            value === "low"
        ) {

            return "low";

        }

        return "medium";

    }


    function getStatusClass(value) {

        const text =
            String(
                value ?? ""
            ).toLowerCase();


        if (
            text === "true" ||
            text === "yes" ||
            text === "pass" ||
            text === "passed" ||
            text === "secure" ||
            text === "good"
        ) {

            return "pass";

        }


        if (
            text === "false" ||
            text === "no" ||
            text === "fail" ||
            text === "failed" ||
            text === "poor"
        ) {

            return "fail";

        }


        return "neutral";

    }


    /* ======================================================
       LOAD AUDIT
    ====================================================== */

    async function loadAudit() {

        const auditId =
            getAuditId();


        if (!auditId) {

            throw new Error(
                "Audit ID is missing."
            );

        }


        const token =
            getAuthToken();


        if (!token) {

            throw new Error(
                "Your session has expired. Please log in again."
            );

        }


        const response =
            await fetch(
                `/api/audits/${encodeURIComponent(auditId)}`,
                {
                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${token}`,

                        "Accept":
                            "application/json"

                    }
                }
            );


        if (
            response.status === 401
        ) {

            throw new Error(
                "Your session has expired. Please log in again."
            );

        }


        if (
            response.status === 404
        ) {

            throw new Error(
                "This audit could not be found."
            );

        }


        if (!response.ok) {

            throw new Error(
                `Unable to load audit (${response.status}).`
            );

        }


        return await response.json();

    }


    /* ======================================================
       RENDER SCORE
    ====================================================== */

    function renderScore(
        valueId,
        barId,
        value
    ) {

        const score =
            clampScore(value);


        const valueElement =
            getElement(valueId);


        const barElement =
            getElement(barId);


        if (valueElement) {

            valueElement.textContent =
                formatScore(score);

        }


        if (barElement) {

            barElement.style.width =
                `${score}%`;

        }

    }


    function renderScores() {

        renderScore(
            "seoValue",
            "seoBar",
            audit.seo_score
        );


        renderScore(
            "performanceValue",
            "performanceBar",
            audit.performance_score
        );


        renderScore(
            "accessibilityValue",
            "accessibilityBar",
            audit.accessibility_score
        );


        renderScore(
            "securityValue",
            "securityBar",
            audit.security_score
        );


        renderScore(
            "mobileValue",
            "mobileBar",
            audit.mobile_score
        );


        renderScore(
            "overallValue",
            "overallBar",
            audit.overall_score
        );


        const circle =
            getElement(
                "overallCircleScore"
            );


        if (circle) {

            circle.textContent =
                formatScore(
                    audit.overall_score
                );

        }


        const summaryMap = {

            summarySeo:
                audit.seo_score,

            summaryPerformance:
                audit.performance_score,

            summaryAccessibility:
                audit.accessibility_score,

            summarySecurity:
                audit.security_score,

            summaryMobile:
                audit.mobile_score

        };


        Object.entries(
            summaryMap
        ).forEach(
            ([id, value]) => {

                const element =
                    getElement(id);

                if (element) {

                    element.textContent =
                        `${formatScore(value)}/100`;

                }

            }
        );

    }


    /* ======================================================
       HEADER
    ====================================================== */

    function renderHeader() {

        const url =
            getElement(
                "reportUrl"
            );


        if (url) {

            url.textContent =
                audit.website_url || "Website Audit";

        }


        const summary =
            getElement(
                "reportSummary"
            );


        if (summary) {

            summary.textContent =
                audit.summary ||
                "Audit completed successfully.";

        }


        const date =
            getElement(
                "reportDate"
            );


        if (date) {

            date.textContent =
                formatDate(
                    audit.created_at
                );

        }


        const grade =
            getElement(
                "reportGrade"
            );


        if (grade) {

            grade.textContent =
                `Grade ${audit.grade || "—"}`;

        }

    }


    /* ======================================================
       RADAR CHART
    ====================================================== */

    function renderRadar() {

        const svg =
            getElement(
                "scoreRadar"
            );


        if (!svg) {

            return;

        }


        const scores = [

            clampScore(
                audit.seo_score
            ),

            clampScore(
                audit.performance_score
            ),

            clampScore(
                audit.accessibility_score
            ),

            clampScore(
                audit.security_score
            ),

            clampScore(
                audit.mobile_score
            )

        ];


        const labels = [

            "SEO",
            "Performance",
            "Accessibility",
            "Security",
            "Mobile"

        ];


        const centerX = 210;

        const centerY = 160;

        const radius = 105;

        const count =
            labels.length;


        function point(
            index,
            scale
        ) {

            const angle =
                (
                    -Math.PI / 2
                ) +
                (
                    index *
                    2 *
                    Math.PI /
                    count
                );


            return {

                x:
                    centerX +
                    Math.cos(angle) *
                    radius *
                    scale,

                y:
                    centerY +
                    Math.sin(angle) *
                    radius *
                    scale

            };

        }


        function polygonPoints(
            scale
        ) {

            return labels
                .map(
                    (_, index) => {

                        const p =
                            point(
                                index,
                                scale
                            );

                        return `${p.x},${p.y}`;

                    }
                )
                .join(" ");

        }


        let output = "";


        /* -----------------------------------------------
           Grid
        ------------------------------------------------ */

        [
            0.25,
            0.5,
            0.75,
            1
        ].forEach(
            scale => {

                output += `
                    <polygon
                        points="${polygonPoints(scale)}"
                        class="radar-grid"
                    ></polygon>
                `;

            }
        );


        /* -----------------------------------------------
           Axis
        ------------------------------------------------ */

        labels.forEach(
            (_, index) => {

                const p =
                    point(
                        index,
                        1
                    );

                output += `
                    <line
                        x1="${centerX}"
                        y1="${centerY}"
                        x2="${p.x}"
                        y2="${p.y}"
                        class="radar-axis"
                    ></line>
                `;

            }
        );


        /* -----------------------------------------------
           Score
        ------------------------------------------------ */

        const scorePoints =
            scores
                .map(
                    (score, index) => {

                        const p =
                            point(
                                index,
                                score / 100
                            );

                        return `${p.x},${p.y}`;

                    }
                )
                .join(" ");


        output += `
            <polygon
                points="${scorePoints}"
                class="radar-score"
            ></polygon>
        `;


        /* -----------------------------------------------
           Score points
        ------------------------------------------------ */

        scores.forEach(
            (score, index) => {

                const p =
                    point(
                        index,
                        score / 100
                    );

                output += `
                    <circle
                        cx="${p.x}"
                        cy="${p.y}"
                        r="4"
                        class="radar-point"
                    ></circle>
                `;

            }
        );


        /* -----------------------------------------------
           Labels
        ------------------------------------------------ */

        labels.forEach(
            (label, index) => {

                const p =
                    point(
                        index,
                        1.18
                    );

                output += `
                    <text
                        x="${p.x}"
                        y="${p.y}"
                        class="radar-label"
                        text-anchor="middle"
                    >
                        ${escapeHTML(label)}
                    </text>
                `;

            }
        );


        svg.innerHTML =
            output;


        const legend =
            getElement(
                "radarLegend"
            );


        if (legend) {

            legend.innerHTML =
                labels
                    .map(
                        (label, index) => `
                            <span>
                                <i></i>
                                ${escapeHTML(label)}
                                <strong>
                                    ${formatScore(scores[index])}
                                </strong>
                            </span>
                        `
                    )
                    .join("");

        }

    }


    /* ======================================================
       SCREENSHOT
    ====================================================== */

    function renderScreenshot() {

        const image =
            getElement(
                "websiteScreenshot"
            );


        const loading =
            getElement(
                "screenshotLoading"
            );


        const empty =
            getElement(
                "screenshotEmpty"
            );


        const status =
            getElement(
                "screenshotStatus"
            );


        const screenshot =
            audit.screenshot_path;


        if (!screenshot) {

            loading.hidden =
                true;

            empty.hidden =
                false;

            status.textContent =
                "Unavailable";

            return;

        }


        let src =
            screenshot;


        if (
            !src.startsWith("/")
        ) {

            src =
                `/${src}`;

        }


        image.onload =
            function () {

                loading.hidden =
                    true;

                empty.hidden =
                    true;

                image.hidden =
                    false;

                status.textContent =
                    "Available";

            };


        image.onerror =
            function () {

                loading.hidden =
                    true;

                image.hidden =
                    true;

                empty.hidden =
                    false;

                status.textContent =
                    "Unavailable";

            };


        image.src =
            `${src}?audit=${audit.id}`;

    }


    /* ======================================================
       PERFORMANCE METRICS
    ====================================================== */

    function getMetric(
        object,
        keys
    ) {

        if (!object) {

            return null;

        }


        for (
            const key of keys
        ) {

            if (
                object[key] !== undefined &&
                object[key] !== null
            ) {

                return object[key];

            }

        }


        return null;

    }


    function renderPerformanceMetrics() {

        /*
         * The current AuditRead schema does not expose
         * performance_metrics yet.
         *
         * Therefore we do not invent values here.
         *
         * When the backend schema stores the real metrics,
         * this renderer will automatically use them.
         */

        const metrics =
            audit.performance_metrics || {};


        const values = {

            metricFcp:
                getMetric(
                    metrics,
                    [
                        "fcp",
                        "first_contentful_paint"
                    ]
                ),

            metricLcp:
                getMetric(
                    metrics,
                    [
                        "lcp",
                        "largest_contentful_paint"
                    ]
                ),

            metricSpeedIndex:
                getMetric(
                    metrics,
                    [
                        "speed_index",
                        "speedIndex"
                    ]
                ),

            metricTti:
                getMetric(
                    metrics,
                    [
                        "tti",
                        "time_to_interactive"
                    ]
                ),

            metricTbt:
                getMetric(
                    metrics,
                    [
                        "tbt",
                        "total_blocking_time"
                    ]
                ),

            metricCls:
                getMetric(
                    metrics,
                    [
                        "cls",
                        "cumulative_layout_shift"
                    ]
                )

        };


        Object.entries(
            values
        ).forEach(
            ([id, value]) => {

                const element =
                    getElement(id);

                if (!element) {

                    return;

                }


                element.textContent =
                    value === null
                        ? "Not stored"
                        : String(value);

            }
        );


        const status =
            getElement(
                "performanceStatus"
            );


        if (status) {

            status.textContent =
                Object.keys(metrics).length
                    ? "Available"
                    : "Metrics not stored";

        }

    }


    /* ======================================================
       GENERIC METRIC OBJECT
    ====================================================== */

    function renderObjectMetrics(
        containerId,
        metrics,
        emptyText
    ) {

        const container =
            getElement(
                containerId
            );


        if (!container) {

            return;

        }


        const entries =
            Object.entries(
                metrics || {}
            );


        if (!entries.length) {

            container.innerHTML = `
                <div class="section-empty inline">
                    <i class="bi bi-info-circle"></i>
                    <span>
                        ${escapeHTML(emptyText)}
                    </span>
                </div>
            `;

            return;

        }


        container.innerHTML =
            entries
                .map(
                    ([key, value]) => {

                        const status =
                            getStatusClass(
                                value
                            );

                        return `
                            <div class="detail-item">

                                <div class="detail-item-icon">
                                    <i class="bi bi-check2-circle"></i>
                                </div>

                                <div>

                                    <span>
                                        ${escapeHTML(
                                            key
                                                .replace(
                                                    /_/g,
                                                    " "
                                                )
                                        )}
                                    </span>

                                    <strong>
                                        ${escapeHTML(value)}
                                    </strong>

                                </div>

                                <em class="${status}">
                                    ${status === "pass"
                                        ? "Pass"
                                        : status === "fail"
                                            ? "Review"
                                            : "Info"}
                                </em>

                            </div>
                        `;

                    }
                )
                .join("");

    }


    /* ======================================================
       ACCESSIBILITY
    ====================================================== */

    function renderAccessibility() {

        renderObjectMetrics(
            "accessibilityDetails",
            audit.accessibility_metrics,
            "No accessibility metrics were stored for this audit."
        );

    }


    /* ======================================================
       SECURITY
    ====================================================== */

    function renderSecurity() {

        const container =
            getElement(
                "securityChecksContent"
            );


        if (!container) {

            return;

        }


        const metrics =
            audit.security_metrics || {};


        const entries =
            Object.entries(
                metrics
            );


        if (!entries.length) {

            container.innerHTML = `
                <div class="section-empty inline">
                    <i class="bi bi-shield-exclamation"></i>
                    <span>
                        No security metrics were stored for this audit.
                    </span>
                </div>
            `;

            return;

        }


        container.innerHTML =
            entries
                .map(
                    ([key, value]) => {

                        const status =
                            getStatusClass(
                                value
                            );


                        return `
                            <div class="security-item">

                                <div class="security-item-left">

                                    <div class="security-icon">
                                        <i class="bi bi-shield-check"></i>
                                    </div>

                                    <div>

                                        <strong>
                                            ${escapeHTML(
                                                key.replace(
                                                    /_/g,
                                                    " "
                                                )
                                            )}
                                        </strong>

                                        <span>
                                            ${escapeHTML(value)}
                                        </span>

                                    </div>

                                </div>

                                <span
                                    class="security-status ${status}"
                                >
                                    <i class="bi ${
                                        status === "pass"
                                            ? "bi-check-circle-fill"
                                            : "bi-exclamation-circle"
                                    }"></i>

                                    ${
                                        status === "pass"
                                            ? "Pass"
                                            : "Review"
                                    }

                                </span>

                            </div>
                        `;

                    }
                )
                .join("");

    }


    /* ======================================================
       MOBILE
    ====================================================== */

    function renderMobile() {

        renderObjectMetrics(
            "mobileDetails",
            audit.mobile_metrics,
            "No mobile metrics were stored for this audit."
        );

    }


    /* ======================================================
       PAGE DETAILS
    ====================================================== */

    function renderPageDetails() {

        const container =
            getElement(
                "pageDetails"
            );


        if (!container) {

            return;

        }


        const details =
            audit.page_details || {};


        const entries = [

            [
                "Page Title",
                details.title_tag
            ],

            [
                "Meta Description",
                details.meta_description
            ],

            [
                "Canonical URL",
                details.canonical_url
            ],

            [
                "Viewport",
                details.viewport
            ],

            [
                "H1 Count",
                details.h1_count
            ],

            [
                "Internal Links",
                details.internal_links
            ],

            [
                "External Links",
                details.external_links
            ],

            [
                "Broken Links",
                details.broken_links
            ],

            [
                "Images",
                details.image_count
            ],

            [
                "Structured Data",
                details.structured_data
            ],

            [
                "Open Graph Tags",
                details.open_graph_tags
            ],

            [
                "Twitter Tags",
                details.twitter_tags
            ]

        ];


        container.innerHTML =
            entries
                .map(
                    ([label, value]) => `

                        <div class="technical-item">

                            <span>
                                ${escapeHTML(label)}
                            </span>

                            <strong>
                                ${
                                    value === undefined ||
                                    value === null ||
                                    value === ""
                                        ? "—"
                                        : escapeHTML(value)
                                }
                            </strong>

                        </div>

                    `
                )
                .join("");

    }


    /* ======================================================
       AI RECOMMENDATIONS
    ====================================================== */

    function renderRecommendations() {

        const container =
            getElement(
                "aiRecommendations"
            );


        if (!container) {

            return;

        }


        const recommendations =
            Array.isArray(
                audit.recommendations
            )
                ? audit.recommendations
                : [];


        if (!recommendations.length) {

            container.innerHTML = `
                <div class="section-empty inline">
                    <i class="bi bi-stars"></i>
                    <span>
                        No AI recommendations were generated.
                    </span>
                </div>
            `;

            return;

        }


        container.innerHTML =
            recommendations
                .map(
                    recommendation => {

                        const priority =
                            recommendation.priority ||
                            "Medium";


                        return `
                            <article class="recommendation-card">

                                <div class="recommendation-icon">

                                    <i class="bi bi-stars"></i>

                                </div>

                                <div class="recommendation-body">

                                    <div class="recommendation-top">

                                        <span>
                                            AI Recommendation
                                        </span>

                                        <em
                                            class="${getPriorityClass(priority)}"
                                        >
                                            ${escapeHTML(priority)}
                                        </em>

                                    </div>

                                    <p>
                                        ${escapeHTML(
                                            recommendation.recommendation ||
                                            ""
                                        )}
                                    </p>

                                </div>

                            </article>
                        `;

                    }
                )
                .join("");

    }


    /* ======================================================
       FINDINGS
    ====================================================== */

    function renderFindings() {

        const container =
            getElement(
                "findingsTable"
            );


        const count =
            getElement(
                "findingCount"
            );


        if (!container) {

            return;

        }


        const findings =
            Array.isArray(
                audit.findings
            )
                ? audit.findings
                : [];


        if (count) {

            count.textContent =
                `${findings.length} ${
                    findings.length === 1
                        ? "finding"
                        : "findings"
                }`;

        }


        if (!findings.length) {

            container.innerHTML = `
                <div class="section-empty">
                    <i class="bi bi-check-circle"></i>

                    <h3>
                        No findings
                    </h3>

                    <p>
                        No detailed issues were returned for this audit.
                    </p>
                </div>
            `;

            return;

        }


        container.innerHTML =
            findings
                .map(
                    finding => {

                        const priority =
                            finding.priority ||
                            finding.severity ||
                            "Medium";


                        const category =
                            finding.category ||
                            "General";


                        return `
                            <article class="finding-card">

                                <div class="finding-card-top">

                                    <div class="finding-category">

                                        <i class="bi bi-search"></i>

                                        <span>
                                            ${escapeHTML(category)}
                                        </span>

                                    </div>

                                    <span
                                        class="priority-badge ${getPriorityClass(priority)}"
                                    >
                                        ${escapeHTML(priority)}
                                    </span>

                                </div>


                                <h3>
                                    ${escapeHTML(
                                        finding.issue ||
                                        finding.title ||
                                        finding.description ||
                                        "Issue detected"
                                    )}
                                </h3>


                                <p>
                                    ${escapeHTML(
                                        finding.recommendation ||
                                        "Review this finding and apply the recommended improvement."
                                    )}
                                </p>

                            </article>
                        `;

                    }
                )
                .join("");

    }


    /* ======================================================
       PDF
    ====================================================== */

    function initializePdfButton() {

        const button =
            getElement(
                "downloadPdfBtn"
            );


        if (!button) {

            return;

        }


        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();


                const auditId =
                    getAuditId();


                if (!auditId) {

                    return;

                }


                const token =
                    getAuthToken();


                if (!token) {

                    window.location.href =
                        "/login";

                    return;

                }


                /*
                 * Browser download endpoint uses the same
                 * authenticated API.
                 *
                 * Opening the endpoint directly lets the
                 * browser handle the PDF attachment.
                 */

                const url =
                    `/api/reports/${encodeURIComponent(auditId)}/pdf`;


                /*
                 * We need the Bearer token, so fetch the
                 * PDF and create a temporary download URL.
                 */

                button.classList.add(
                    "loading"
                );


                fetch(
                    url,
                    {
                        headers: {

                            "Authorization":
                                `Bearer ${token}`

                        }
                    }
                )
                .then(
                    response => {

                        if (!response.ok) {

                            throw new Error(
                                `PDF request failed: ${response.status}`
                            );

                        }

                        return response.blob();

                    }
                )
                .then(
                    blob => {

                        const blobUrl =
                            URL.createObjectURL(
                                blob
                            );


                        const link =
                            document.createElement(
                                "a"
                            );


                        link.href =
                            blobUrl;

                        link.download =
                            `audit-report-${auditId}.pdf`;


                        document.body.appendChild(
                            link
                        );


                        link.click();


                        link.remove();


                        URL.revokeObjectURL(
                            blobUrl
                        );

                    }
                )
                .catch(
                    error => {

                        console.error(
                            "[Report] PDF download failed:",
                            error
                        );

                        alert(
                            "Unable to download the PDF report."
                        );

                    }
                )
                .finally(
                    () => {

                        button.classList.remove(
                            "loading"
                        );

                    }
                );

            }
        );

    }


    /* ======================================================
       ERROR STATE
    ====================================================== */

    function renderError(
        message
    ) {

        const page =
            getElement(
                "auditReportPage"
            );


        if (!page) {

            return;

        }


        page.innerHTML = `

            <section class="report-error-shell">

                <div class="report-error-card">

                    <div class="report-error-icon">
                        <i class="bi bi-exclamation-triangle"></i>
                    </div>

                    <span class="report-eyebrow">
                        AUDIT REPORT
                    </span>

                    <h1>
                        Unable to load this report
                    </h1>

                    <p>
                        ${escapeHTML(message)}
                    </p>

                    <div class="report-error-actions">

                        <button
                            type="button"
                            class="report-primary-button"
                            onclick="window.location.reload()"
                        >
                            <i class="bi bi-arrow-clockwise"></i>
                            Try Again
                        </button>

                        <a
                            href="/dashboard"
                            class="report-secondary-button"
                        >
                            Back to Dashboard
                        </a>

                    </div>

                </div>

            </section>

        `;

    }


    /* ======================================================
       INITIALIZE
    ====================================================== */

    async function initializeReport() {

        initializePdfButton();


        try {

            audit =
                await loadAudit();


            console.info(
                "[AI Audit] Report loaded:",
                audit
            );


            renderHeader();

            renderScores();

            renderRadar();

            renderScreenshot();

            renderPerformanceMetrics();

            renderAccessibility();

            renderSecurity();

            renderMobile();

            renderPageDetails();

            renderRecommendations();

            renderFindings();

        }

        catch (error) {

            console.error(
                "[AI Audit] Report loading failed:",
                error
            );


            if (
                String(
                    error.message
                ).includes(
                    "session has expired"
                )
            ) {

                window.location.href =
                    "/login";

                return;

            }


            renderError(
                error.message ||
                "Unable to load audit report."
            );

        }

    }


    /* ======================================================
       START
    ====================================================== */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeReport,
            {
                once: true
            }
        );

    }
    else {

        initializeReport();

    }

})();