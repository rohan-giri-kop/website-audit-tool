/**
 * ==========================================================
 * AI WEBSITE AUDIT TOOL
 * DASHBOARD JAVASCRIPT
 * ==========================================================
 *
 * Responsibilities:
 * - Load real dashboard data
 * - Load dashboard summary
 * - Load chart data
 * - Load recent audits
 * - Render KPI cards
 * - Render website health scores
 * - Render Score Performance chart
 * - Handle chart period changes
 * - Handle empty states
 * - Handle API errors
 *
 * API:
 * /api/dashboard/summary
 * /api/dashboard/charts
 * /api/dashboard/recent-audits
 *
 * ==========================================================
 */

(function () {
    "use strict";


    // ======================================================
    // CONFIGURATION
    // ======================================================

    const API_BASE = "/api/dashboard";

    const DEFAULT_PERIOD = "30d";

    let scoreChart = null;

    let currentPeriod = DEFAULT_PERIOD;


    // ======================================================
    // DOM HELPERS
    // ======================================================

    function getElement(id) {
        return document.getElementById(id);
    }


    function setText(id, value) {
        const element = getElement(id);

        if (!element) {
            return;
        }

        element.textContent = value;
    }


    function setHidden(id, hidden) {
        const element = getElement(id);

        if (!element) {
            return;
        }

        element.hidden = hidden;
    }


    // ======================================================
    // AUTHENTICATION
    // ======================================================

    function getAccessToken() {

        const possibleKeys = [
            "access_token",
            "token",
            "auth_token",
            "accessToken"
        ];


        // ======================================================
        // CHECK LOCAL STORAGE
        // ======================================================

        for (const key of possibleKeys) {

            const token =
                localStorage.getItem(key);

            if (token) {

                return token;

            }

        }


        // ======================================================
        // CHECK SESSION STORAGE
        // ======================================================

        for (const key of possibleKeys) {

            const token =
                sessionStorage.getItem(key);

            if (token) {

                return token;

            }

        }



    // ======================================================
    // CHECK SESSION STORAGE
    // ======================================================

    for (const key of possibleKeys) {

        const token =
            sessionStorage.getItem(key);

        if (token) {

            return token;

        }

    }


    // ======================================================
    // TOKEN NOT FOUND
    // ======================================================

    console.warn(
        "[AI Audit] Dashboard authentication token not found."
    );

    return null;
}


    // ======================================================
    // API REQUEST
    // ======================================================

    async function apiRequest(
        endpoint,
        options = {}
    ) {

        const token = getAccessToken();


        const headers = {
            "Accept": "application/json",
            ...(options.headers || {})
        };


        if (token) {
            headers["Authorization"] =
                `Bearer ${token}`;
        }


        const response = await fetch(
            endpoint,
            {
                ...options,
                headers
            }
        );


        /*
         * Authentication failure.
         */

        if (response.status === 401) {

            console.error(
                "Dashboard authentication failed."
            );

            throw new Error(
                "Your session has expired. Please log in again."
            );
        }


        /*
         * Other HTTP errors.
         */

        if (!response.ok) {

            let message =
                `Dashboard request failed (${response.status})`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    message = errorData.detail;
                }

            } catch (error) {
                /*
                 * Keep the default message.
                 */
            }


            throw new Error(message);
        }


        return response.json();
    }


    // ======================================================
    // EXTRACT API DATA
    // ======================================================

    function extractData(response) {

        /*
         * Current dashboard API returns:
         *
         * {
         *   success: true,
         *   message: "...",
         *   timestamp: "...",
         *   data: {...}
         * }
         */

        if (
            response &&
            Object.prototype.hasOwnProperty.call(
                response,
                "data"
            )
        ) {
            return response.data;
        }


        return response;
    }


    // ======================================================
    // FORMAT SCORE
    // ======================================================

    function formatScore(value) {

        const number = Number(value);


        if (!Number.isFinite(number)) {
            return "0";
        }


        /*
         * Keep whole numbers clean.
         *
         * Example:
         * 85     → 85
         * 85.5   → 85.5
         */

        return Number.isInteger(number)
            ? String(number)
            : number.toFixed(1);
    }


    // ======================================================
    // FORMAT DATE
    // ======================================================

    function formatDate(value) {

        if (!value) {
            return "—";
        }


        const date = new Date(value);


        if (Number.isNaN(date.getTime())) {
            return "—";
        }


        return date.toLocaleDateString(
            undefined,
            {
                day: "2-digit",
                month: "short",
                year: "numeric"
            }
        );
    }


    // ======================================================
    // GET GRADE
    // ======================================================

    function getGrade(score, providedGrade) {

        if (providedGrade) {
            return String(
                providedGrade
            ).toUpperCase();
        }


        const value = Number(score);


        if (!Number.isFinite(value)) {
            return "F";
        }


        if (value >= 90) {
            return "A";
        }

        if (value >= 80) {
            return "B";
        }

        if (value >= 70) {
            return "C";
        }

        if (value >= 60) {
            return "D";
        }


        return "F";
    }


    // ======================================================
    // DASHBOARD SUMMARY
    // ======================================================

    async function loadDashboardSummary() {

        const response = await apiRequest(
            `${API_BASE}/summary`
        );


        const summary =
            extractData(response);


        if (!summary) {
            throw new Error(
                "Dashboard summary data is empty."
            );
        }


        /*
         * KPI CARDS
         */

        setText(
            "dashboardTotalAudits",
            summary.total_audits ?? 0
        );


        setText(
            "dashboardAverageScore",
            formatScore(
                summary.average_score
            )
        );


        setText(
            "dashboardAverageSeo",
            formatScore(
                summary.average_seo
            )
        );


        setText(
            "dashboardAveragePerformance",
            formatScore(
                summary.average_performance
            )
        );


        /*
         * WEBSITE HEALTH
         */

        updateHealthScore(
            "healthSeoScore",
            "healthSeoBar",
            summary.average_seo
        );


        updateHealthScore(
            "healthPerformanceScore",
            "healthPerformanceBar",
            summary.average_performance
        );


        updateHealthScore(
            "healthAccessibilityScore",
            "healthAccessibilityBar",
            summary.average_accessibility
        );


        updateHealthScore(
            "healthSecurityScore",
            "healthSecurityBar",
            summary.average_security
        );


        updateHealthScore(
            "healthMobileScore",
            "healthMobileBar",
            summary.average_mobile
        );


        return summary;
    }


    // ======================================================
    // UPDATE HEALTH SCORE
    // ======================================================

    function updateHealthScore(
        scoreId,
        barId,
        value
    ) {

        const score = Number(value);


        const safeScore =
            Number.isFinite(score)
                ? Math.max(
                    0,
                    Math.min(100, score)
                )
                : 0;


        setText(
            scoreId,
            formatScore(safeScore)
        );


        const bar = getElement(barId);


        if (!bar) {
            return;
        }


        bar.style.width =
            `${safeScore}%`;


        /*
         * Accessibility state.
         */

        bar.setAttribute(
            "aria-valuenow",
            String(safeScore)
        );

        bar.setAttribute(
            "aria-valuemin",
            "0"
        );

        bar.setAttribute(
            "aria-valuemax",
            "100"
        );
    }


    // ======================================================
    // DASHBOARD CHART
    // ======================================================

    async function loadDashboardChart(
        period = DEFAULT_PERIOD
    ) {

        currentPeriod = period;


        const response = await apiRequest(
            `${API_BASE}/charts?period=${encodeURIComponent(
                period
            )}`
        );


        const chartData =
            extractData(response);


        if (!chartData) {
            throw new Error(
                "Dashboard chart data is empty."
            );
        }


        renderScoreChart(
            chartData
        );


        return chartData;
    }


    // ======================================================
    // LOAD CHART.JS
    // ======================================================

    function ensureChartJs() {

        if (
            typeof window.Chart !==
            "undefined"
        ) {
            return Promise.resolve();
        }


        return new Promise(
            (resolve, reject) => {

                const existingScript =
                    document.querySelector(
                        'script[src*="chart.js"]'
                    );


                if (existingScript) {

                    existingScript.addEventListener(
                        "load",
                        () => resolve()
                    );

                    existingScript.addEventListener(
                        "error",
                        () => reject(
                            new Error(
                                "Chart.js failed to load."
                            )
                        )
                    );

                    return;
                }


                const script =
                    document.createElement(
                        "script"
                    );


                script.src =
                    "https://cdn.jsdelivr.net/npm/chart.js";


                script.async = true;


                script.onload =
                    () => resolve();


                script.onerror =
                    () => reject(
                        new Error(
                            "Unable to load Chart.js."
                        )
                    );


                document.head.appendChild(
                    script
                );
            }
        );
    }


    // ======================================================
    // RENDER SCORE CHART
    // ======================================================

    async function renderScoreChart(
        chartData
    ) {

        const canvas =
            getElement(
                "dashboardScoreChart"
            );


        const emptyState =
            getElement(
                "dashboardChartEmpty"
            );


        if (!canvas) {
            return;
        }


        const labels =
            Array.isArray(
                chartData.labels
            )
                ? chartData.labels
                : [];


        const datasets =
            chartData.datasets || {};


        /*
         * No audit history.
         */

        if (labels.length === 0) {

            if (scoreChart) {
                scoreChart.destroy();
                scoreChart = null;
            }


            if (canvas) {
                canvas.hidden = true;
            }


            if (emptyState) {
                emptyState.hidden = false;
            }


            return;
        }


        /*
         * Audit history exists.
         */

        canvas.hidden = false;


        if (emptyState) {
            emptyState.hidden = true;
        }


        await ensureChartJs();


        if (
            typeof window.Chart ===
            "undefined"
        ) {
            throw new Error(
                "Chart.js is unavailable."
            );
        }


        const context =
            canvas.getContext("2d");


        if (!context) {
            throw new Error(
                "Unable to initialize chart."
            );
        }


        /*
         * Destroy previous chart instance.
         */

        if (scoreChart) {
            scoreChart.destroy();
            scoreChart = null;
        }


        /*
         * Use the existing dashboard visual
         * direction.
         *
         * No new colors are introduced.
         */

        scoreChart = new Chart(
            context,
            {
                type: "line",

                data: {
                    labels,

                    datasets: [
                        {
                            label: "Overall",

                            data:
                                Array.isArray(
                                    datasets.overall
                                )
                                    ? datasets.overall
                                    : [],

                            borderColor:
                                "#2563EB",

                            backgroundColor:
                                "rgba(37, 99, 235, 0.08)",

                            borderWidth: 2,

                            pointRadius: 3,

                            pointHoverRadius: 5,

                            fill: true,

                            tension: 0.35
                        },

                        {
                            label: "SEO",

                            data:
                                Array.isArray(
                                    datasets.seo
                                )
                                    ? datasets.seo
                                    : [],

                            borderColor:
                                "#4F46E5",

                            backgroundColor:
                                "transparent",

                            borderWidth: 1.5,

                            pointRadius: 2,

                            pointHoverRadius: 4,

                            fill: false,

                            tension: 0.35
                        },

                        {
                            label: "Performance",

                            data:
                                Array.isArray(
                                    datasets.performance
                                )
                                    ? datasets.performance
                                    : [],

                            borderColor:
                                "#16A34A",

                            backgroundColor:
                                "transparent",

                            borderWidth: 1.5,

                            pointRadius: 2,

                            pointHoverRadius: 4,

                            fill: false,

                            tension: 0.35
                        }
                    ]
                },


                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    interaction: {
                        mode: "index",
                        intersect: false
                    },


                    plugins: {

                        legend: {
                            display: true,

                            position: "top",

                            align: "end"
                        },


                        tooltip: {
                            callbacks: {

                                label: function (
                                    context
                                ) {

                                    return (
                                        `${context.dataset.label}: ` +
                                        `${formatScore(
                                            context.parsed.y
                                        )}/100`
                                    );
                                }
                            }
                        }
                    },


                    scales: {

                        y: {
                            min: 0,
                            max: 100,

                            ticks: {
                                stepSize: 20
                            },

                            grid: {
                                color:
                                    "rgba(226, 232, 240, 0.8)"
                            }
                        },


                        x: {

                            grid: {
                                display: false
                            }
                        }
                    }
                }
            }
        );
    }


    // ======================================================
    // RECENT AUDITS
    // ======================================================

    async function loadRecentAudits() {

        showRecentLoading();


        const response =
            await apiRequest(
                `${API_BASE}/recent-audits?page=1&limit=10`
            );


        const data =
            extractData(response);


        if (!data) {
            throw new Error(
                "Recent audit data is empty."
            );
        }


        renderRecentAudits(
            data
        );


        return data;
    }


    // ======================================================
    // RECENT AUDITS UI STATES
    // ======================================================

    function showRecentLoading() {

        setHidden(
            "dashboardRecentLoading",
            false
        );

        setHidden(
            "dashboardRecentTableWrapper",
            true
        );

        setHidden(
            "dashboardRecentEmpty",
            true
        );

        setHidden(
            "dashboardRecentError",
            true
        );
    }


    function showRecentError() {

        setHidden(
            "dashboardRecentLoading",
            true
        );

        setHidden(
            "dashboardRecentTableWrapper",
            true
        );

        setHidden(
            "dashboardRecentEmpty",
            true
        );

        setHidden(
            "dashboardRecentError",
            false
        );
    }


    // ======================================================
    // RENDER RECENT AUDITS
    // ======================================================

    function renderRecentAudits(
        data
    ) {

        const tableBody =
            getElement(
                "dashboardRecentAudits"
            );


        if (!tableBody) {
            return;
        }


        const items =
            Array.isArray(
                data.items
            )
                ? data.items
                : [];


        /*
         * Clear previous rows.
         */

        tableBody.innerHTML = "";


        /*
         * No audits.
         */

        if (items.length === 0) {

            setHidden(
                "dashboardRecentLoading",
                true
            );

            setHidden(
                "dashboardRecentTableWrapper",
                true
            );

            setHidden(
                "dashboardRecentEmpty",
                false
            );

            setHidden(
                "dashboardRecentError",
                true
            );

            return;
        }


        /*
         * Audits exist.
         */

        setHidden(
            "dashboardRecentLoading",
            true
        );

        setHidden(
            "dashboardRecentTableWrapper",
            false
        );

        setHidden(
            "dashboardRecentEmpty",
            true
        );

        setHidden(
            "dashboardRecentError",
            true
        );


        for (const audit of items) {

            const row =
                createAuditRow(
                    audit
                );


            tableBody.appendChild(
                row
            );
        }
    }


    // ======================================================
    // CREATE AUDIT TABLE ROW
    // ======================================================

    function createAuditRow(
        audit
    ) {

        const row =
            document.createElement(
                "tr"
            );


        const websiteCell =
            document.createElement(
                "td"
            );


        const websiteLink =
            document.createElement(
                "a"
            );


        websiteLink.href =
            `/reports/${encodeURIComponent(
                audit.id
            )}`;


        websiteLink.textContent =
            getDisplayDomain(
                audit.website_url
            );


        websiteLink.title =
            audit.website_url || "";


        websiteLink.className =
            "dashboard-website-link";


        websiteCell.appendChild(
            websiteLink
        );


        /*
         * Overall
         */

        const overallCell =
            createScoreCell(
                audit.overall_score
            );


        /*
         * SEO
         */

        const seoCell =
            createScoreCell(
                audit.seo_score
            );


        /*
         * Performance
         */

        const performanceCell =
            createScoreCell(
                audit.performance_score
            );


        /*
         * Grade
         */

        const gradeCell =
            document.createElement(
                "td"
            );


        const grade =
            getGrade(
                audit.overall_score,
                audit.grade
            );


        const gradeBadge =
            document.createElement(
                "span"
            );


        gradeBadge.className =
            `dashboard-grade-badge grade-${grade.toLowerCase()}`;


        gradeBadge.textContent =
            grade;


        gradeCell.appendChild(
            gradeBadge
        );


        /*
         * Date
         */

        const dateCell =
            document.createElement(
                "td"
            );


        dateCell.textContent =
            formatDate(
                audit.created_at
            );


        /*
         * Action
         */

        const actionCell =
            document.createElement(
                "td"
            );


        const actionLink =
            document.createElement(
                "a"
            );


        actionLink.href =
            `/reports/${encodeURIComponent(
                audit.id
            )}`;


        actionLink.className =
            "dashboard-audit-action";


        actionLink.innerHTML =
            `
                View
                <i class="bi bi-arrow-right"></i>
            `;


        actionCell.appendChild(
            actionLink
        );


        /*
         * Build row.
         */

        row.appendChild(
            websiteCell
        );

        row.appendChild(
            overallCell
        );

        row.appendChild(
            seoCell
        );

        row.appendChild(
            performanceCell
        );

        row.appendChild(
            gradeCell
        );

        row.appendChild(
            dateCell
        );

        row.appendChild(
            actionCell
        );


        return row;
    }


    // ======================================================
    // SCORE TABLE CELL
    // ======================================================

    function createScoreCell(
        value
    ) {

        const cell =
            document.createElement(
                "td"
            );


        const score =
            Number(value);


        const scoreValue =
            Number.isFinite(score)
                ? score
                : 0;


        const scoreElement =
            document.createElement(
                "span"
            );


        scoreElement.className =
            "dashboard-table-score";


        scoreElement.textContent =
            formatScore(
                scoreValue
            );


        cell.appendChild(
            scoreElement
        );


        return cell;
    }


    // ======================================================
    // WEBSITE DOMAIN
    // ======================================================

    function getDisplayDomain(
        url
    ) {

        if (!url) {
            return "Unknown website";
        }


        try {

            const normalized =
                url.match(
                    /^https?:\/\//i
                )
                    ? url
                    : `https://${url}`;


            const parsed =
                new URL(
                    normalized
                );


            return parsed.hostname
                .replace(
                    /^www\./i,
                    ""
                );

        } catch (error) {

            return String(url)
                .replace(
                    /^https?:\/\//i,
                    ""
                )
                .replace(
                    /^www\./i,
                    ""
                )
                .split("/")[0];
        }
    }


    // ======================================================
    // CHART PERIOD
    // ======================================================

    function setupChartPeriod() {

        const selector =
            getElement(
                "dashboardChartPeriod"
            );


        if (!selector) {
            return;
        }


        selector.addEventListener(
            "change",
            async function () {

                const period =
                    selector.value ||
                    DEFAULT_PERIOD;


                try {

                    await loadDashboardChart(
                        period
                    );

                } catch (error) {

                    console.error(
                        "Unable to update dashboard chart:",
                        error
                    );
                }
            }
        );
    }


    // ======================================================
    // RETRY BUTTON
    // ======================================================

    function setupRetryButton() {

        const button =
            getElement(
                "dashboardRetryButton"
            );


        if (!button) {
            return;
        }


        button.addEventListener(
            "click",
            async function () {

                await loadDashboard();
            }
        );
    }

    /* ==========================================================
   DASHBOARD RETURN REFRESH
   ----------------------------------------------------------
   Refresh dashboard data when the user returns to the
   dashboard after creating/viewing an audit.
========================================================== */

function refreshDashboardAfterAudit() {

    if (
        typeof loadDashboardData === "function"
    ) {

        loadDashboardData();

        return;

    }


    if (
        typeof loadDashboardSummary === "function"
    ) {

        loadDashboardSummary();

    }


    if (
        typeof loadDashboardCharts === "function"
    ) {

        loadDashboardCharts();

    }


    if (
        typeof loadRecentAudits === "function"
    ) {

        loadRecentAudits();

    }

}


/* ==========================================================
   PAGE VISIBILITY
========================================================== */

document.addEventListener(
    "visibilitychange",
    () => {

        if (
            document.visibilityState !== "visible"
        ) {

            return;

        }


        /*
         * Only run when we are actually on
         * the dashboard page.
         */

        if (
            !document.getElementById(
                "dashboardOverview"
            )
        ) {

            return;

        }


        refreshDashboardAfterAudit();

    }
);


    // ======================================================
    // LOAD DASHBOARD
    // ======================================================

    async function loadDashboard() {

        /*
         * Reset error state.
         */

        setHidden(
            "dashboardRecentError",
            true
        );


        try {

            /*
             * Load summary first.
             */

            await loadDashboardSummary();


            /*
             * Load chart and recent audits
             * independently.
             */

            const chartPromise =
                loadDashboardChart(
                    currentPeriod
                );


            const recentPromise =
                loadRecentAudits();


            await Promise.all([
                chartPromise,
                recentPromise
            ]);


        } catch (error) {

            console.error(
                "Dashboard loading failed:",
                error
            );


            /*
             * If recent audits failed,
             * show the dashboard error state.
             */

            showRecentError();
        }
    }


    // ======================================================
    // INITIALIZE
    // ======================================================

    function initializeDashboard() {

        setupChartPeriod();

        setupRetryButton();

        loadDashboard();
    }


    // ======================================================
    // PAGE READY
    // ======================================================

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeDashboard
        );

    } else {

        initializeDashboard();
    }


    // ======================================================
    // OPTIONAL GLOBAL ACCESS
    // ======================================================

    window.dashboardOverview = {
        reload: loadDashboard,

        reloadChart:
            loadDashboardChart,

        reloadRecentAudits:
            loadRecentAudits
    };

})();