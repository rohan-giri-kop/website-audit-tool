/**
 * ==========================================================
 * AI WEBSITE AUDIT TOOL
 * AUDIT HISTORY
 * ==========================================================
 *
 * Loads the authenticated user's audit history.
 *
 * API:
 *
 * GET /api/audits
 *
 * Authentication:
 *
 * Authorization: Bearer <access_token>
 *
 * ==========================================================
 */

(function () {

    "use strict";


    // ======================================================
    // CONFIGURATION
    // ======================================================

    const API_ENDPOINT = "/api/audits";

    const LOGIN_URL = "/login";


    // ======================================================
    // DOM HELPER
    // ======================================================

    function getElement(id) {

        return document.getElementById(id);

    }


    // ======================================================
    // GET AUTH TOKEN
    // ======================================================

    function getAuthToken() {

        const possibleKeys = [
            "access_token",
            "token",
            "auth_token",
            "accessToken"
        ];


        // --------------------------------------------------
        // LOCAL STORAGE
        // --------------------------------------------------

        for (const key of possibleKeys) {

            const token =
                localStorage.getItem(key);

            if (token) {

                return token;

            }

        }


        // --------------------------------------------------
        // SESSION STORAGE
        // --------------------------------------------------

        for (const key of possibleKeys) {

            const token =
                sessionStorage.getItem(key);

            if (token) {

                return token;

            }

        }


        return null;

    }


    // ======================================================
    // CLEAR AUTHENTICATION
    // ======================================================

    function clearAuth() {

        const keys = [
            "access_token",
            "token",
            "auth_token",
            "accessToken",
            "audit_token"
        ];


        keys.forEach(function (key) {

            localStorage.removeItem(key);

            sessionStorage.removeItem(key);

        });

    }


    // ======================================================
    // LOAD HISTORY
    // ======================================================

    async function loadHistory() {

        const tableBody =
            getElement("historyTable");


        if (!tableBody) {

            console.error(
                "[Audit History] historyTable not found."
            );

            return;

        }


        console.log(
            "[Audit History] Loading..."
        );


        const token =
            getAuthToken();


        console.log(
            "[Audit History] Token:",
            token ? "FOUND" : "NOT FOUND"
        );


        // --------------------------------------------------
        // TOKEN CHECK
        // --------------------------------------------------

        if (!token) {

            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Your session has expired.
                        Please log in again.
                    </td>
                </tr>
            `;

            window.setTimeout(
                function () {

                    window.location.replace(
                        LOGIN_URL
                    );

                },
                800
            );

            return;

        }


        // --------------------------------------------------
        // API REQUEST
        // --------------------------------------------------

        let response;


        try {

            response = await fetch(
                API_ENDPOINT,
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

        }

        catch (error) {

            console.error(
                "[Audit History] Request failed:",
                error
            );


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Unable to connect to the audit service.
                    </td>
                </tr>
            `;

            return;

        }


        console.log(
            "[Audit History] Status:",
            response.status
        );


        // --------------------------------------------------
        // AUTHENTICATION ERROR
        // --------------------------------------------------

        if (response.status === 401) {

            let errorData = null;

            try {

                errorData =
                    await response.json();

            }

            catch (_) {

                // Response may not contain JSON.

            }


            console.error(
                "[Audit History] Authentication failed:",
                errorData
            );


            clearAuth();


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Your session has expired.
                        Please log in again.
                    </td>
                </tr>
            `;


            window.setTimeout(
                function () {

                    window.location.replace(
                        LOGIN_URL
                    );

                },
                800
            );


            return;

        }


        // --------------------------------------------------
        // OTHER API ERROR
        // --------------------------------------------------

        if (!response.ok) {

            let message =
                `Unable to load audit history (${response.status}).`;


            try {

                const errorData =
                    await response.json();


                if (
                    errorData &&
                    errorData.detail
                ) {

                    message =
                        errorData.detail;

                }

            }

            catch (_) {

                // Keep default message.

            }


            console.error(
                "[Audit History] API error:",
                message
            );


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        ${message}
                    </td>
                </tr>
            `;


            return;

        }


        // --------------------------------------------------
        // READ RESPONSE
        // --------------------------------------------------

        let audits;


        try {

            audits =
                await response.json();

        }

        catch (error) {

            console.error(
                "[Audit History] Invalid JSON:",
                error
            );


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Invalid response from the server.
                    </td>
                </tr>
            `;


            return;

        }


        console.log(
            "[Audit History] Audits:",
            audits
        );


        // --------------------------------------------------
        // NORMALIZE RESPONSE
        // --------------------------------------------------

        if (
            audits &&
            Array.isArray(audits.data)
        ) {

            audits =
                audits.data;

        }


        if (
            !Array.isArray(audits)
        ) {

            console.error(
                "[Audit History] Unexpected response:",
                audits
            );


            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-danger py-4"
                    >
                        Unexpected audit history response.
                    </td>
                </tr>
            `;


            return;

        }


        // --------------------------------------------------
        // EMPTY STATE
        // --------------------------------------------------

        if (audits.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="8"
                        class="text-center text-muted py-4"
                    >
                        No audits have been performed yet.
                    </td>
                </tr>
            `;

            return;

        }


        // --------------------------------------------------
        // RENDER AUDITS
        // --------------------------------------------------

        tableBody.innerHTML = "";


        audits.forEach(function (audit) {

            const row =
                document.createElement("tr");


            const website =
                audit.website_url ||
                audit.url ||
                "—";


            const seo =
                audit.seo_score ??
                0;


            const performance =
                audit.performance_score ??
                0;


            const security =
                audit.security_score ??
                0;


            const overall =
                audit.overall_score ??
                0;


            const grade =
                audit.grade ||
                getGrade(overall);


            const date =
                formatDate(
                    audit.created_at ||
                    audit.completed_at ||
                    audit.updated_at
                );


            row.innerHTML = `

                <td>
                    <a
                        href="/audits/${audit.id}"
                        class="text-decoration-none"
                    >
                        ${escapeHtml(website)}
                    </a>
                </td>

                <td>
                    ${formatScore(seo)}
                </td>

                <td>
                    ${formatScore(performance)}
                </td>

                <td>
                    ${formatScore(security)}
                </td>

                <td>
                    <strong>
                        ${formatScore(overall)}
                    </strong>
                </td>

                <td>
                    ${escapeHtml(grade)}
                </td>

                <td>
                    ${escapeHtml(date)}
                </td>

                <td>

                    <a
                        href="/audits/${audit.id}"
                        class="btn btn-sm btn-primary"
                    >
                        View
                    </a>

                </td>

            `;


            tableBody.appendChild(row);

        });

    }


    // ======================================================
    // SCORE FORMAT
    // ======================================================

    function formatScore(value) {

        const number =
            Number(value);


        if (
            !Number.isFinite(number)
        ) {

            return "0";

        }


        return Number.isInteger(number)
            ? String(number)
            : number.toFixed(1);

    }


    // ======================================================
    // GRADE
    // ======================================================

    function getGrade(score) {

        const value =
            Number(score);


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
    // DATE FORMAT
    // ======================================================

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

            return "—";

        }


        return date.toLocaleDateString(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                year: "numeric"
            }
        );

    }


    // ======================================================
    // HTML ESCAPE
    // ======================================================

    function escapeHtml(value) {

        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");

    }


    // ======================================================
    // INITIALIZE
    // ======================================================

    document.addEventListener(
        "DOMContentLoaded",
        function () {

            loadHistory();

        }
    );

})();