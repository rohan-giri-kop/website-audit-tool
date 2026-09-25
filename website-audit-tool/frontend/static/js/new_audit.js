/**
 * ==========================================================
 * AI WEBSITE AUDIT TOOL
 * NEW WEBSITE AUDIT
 * ==========================================================
 *
 * STEP 11C
 *
 * Responsibilities:
 * - Handle New Audit form
 * - Validate website URL
 * - Normalize website URL
 * - Get authentication token
 * - Submit POST /api/audits
 * - Handle loading state
 * - Handle API errors
 * - Handle validation errors
 * - Redirect to audit report
 *
 * Existing backend:
 *
 * POST /api/audits
 *
 * Request:
 *
 * {
 *     "website_url": "https://example.com"
 * }
 *
 * Response:
 *
 * AuditRead
 *
 * Redirect:
 *
 * /audits/{audit_id}
 *
 * ==========================================================
 */

(function () {

    "use strict";


    // ======================================================
    // CONFIGURATION
    // ======================================================

    const API_ENDPOINT =
        "/api/audits";


    const REPORT_BASE_URL =
        "/audits";


    const LOGIN_URL =
        "/login";


    const REQUEST_TIMEOUT = 90000;
        


    // ======================================================
    // DOM HELPERS
    // ======================================================

    function getElement(id) {

        return document.getElementById(id);

    }


    function setHidden(
        element,
        hidden
    ) {

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


        // --------------------------------------------------
        // LOCAL STORAGE
        // --------------------------------------------------

        for (
            const key
            of possibleKeys
        ) {

            const token =
                localStorage.getItem(key);

            if (token) {

                return token;

            }

        }


        // --------------------------------------------------
        // SESSION STORAGE
        // --------------------------------------------------

        for (
            const key
            of possibleKeys
        ) {

            const token =
                sessionStorage.getItem(key);

            if (token) {

                return token;

            }

        }


        return null;

    }


    // ======================================================
    // URL NORMALIZATION
    // ======================================================

    function normalizeWebsiteUrl(
        value
    ) {

        let url =
            String(value || "")
                .trim();


        if (!url) {

            return "";

        }


        /*
         * Remove accidental spaces.
         */

        url =
            url.replace(
                /\s+/g,
                ""
            );


        /*
         * Add HTTPS when the user enters:
         *
         * example.com
         * www.example.com
         */

        if (
            !/^https?:\/\//i.test(url)
        ) {

            url =
                `https://${url}`;

        }


        return url;

    }


    // ======================================================
    // URL VALIDATION
    // ======================================================

    function validateWebsiteUrl(
        value
    ) {

        const normalized =
            normalizeWebsiteUrl(value);


        if (!normalized) {

            return {
                valid: false,
                message:
                    "Please enter a website URL."
            };

        }


        let parsedUrl;


        try {

            parsedUrl =
                new URL(normalized);

        }

        catch (error) {

            return {
                valid: false,
                message:
                    "Please enter a valid website URL."
            };

        }


        /*
         * Only HTTP and HTTPS websites
         * should be submitted to the audit engine.
         */

        if (
            parsedUrl.protocol !== "http:" &&
            parsedUrl.protocol !== "https:"
        ) {

            return {
                valid: false,
                message:
                    "Please enter an HTTP or HTTPS website URL."
            };

        }


        /*
         * A hostname is required.
         */

        if (!parsedUrl.hostname) {

            return {
                valid: false,
                message:
                    "Please enter a valid website hostname."
            };

        }


        /*
         * Reject obvious local/file targets.
         *
         * This is a frontend validation layer only.
         * Backend/network security remains authoritative.
         */

        const hostname =
            parsedUrl.hostname
                .toLowerCase();


        const blockedHosts = [

            "localhost",
            "127.0.0.1",
            "0.0.0.0",
            "::1"

        ];


        if (
            blockedHosts.includes(
                hostname
            )
        ) {

            return {
                valid: false,
                message:
                    "Please enter a public website URL."
            };

        }


        return {
            valid: true,
            url: parsedUrl.toString()
        };

    }


    // ======================================================
    // FIELD ERROR
    // ======================================================

    function clearFieldError() {

        const wrapper =
            getElement(
                "websiteUrlWrapper"
            );


        const errorElement =
            getElement(
                "websiteUrlError"
            );


        if (wrapper) {

            wrapper.classList.remove(
                "has-error"
            );

        }


        if (errorElement) {

            errorElement.textContent =
                "";

            errorElement.hidden =
                true;

        }

    }


    function showFieldError(
        message
    ) {

        const wrapper =
            getElement(
                "websiteUrlWrapper"
            );


        const errorElement =
            getElement(
                "websiteUrlError"
            );


        if (wrapper) {

            wrapper.classList.add(
                "has-error"
            );

        }


        if (errorElement) {

            errorElement.textContent =
                message;

            errorElement.hidden =
                false;

        }

    }


    // ======================================================
    // GLOBAL MESSAGE
    // ======================================================

    function clearGlobalMessage() {

        const messageElement =
            getElement(
                "auditGlobalMessage"
            );


        if (!messageElement) {
            return;
        }


        messageElement.textContent =
            "";


        messageElement.hidden =
            true;


        messageElement.className =
            "audit-global-message";

    }


    function showGlobalMessage(
        message,
        type = "error"
    ) {

        const messageElement =
            getElement(
                "auditGlobalMessage"
            );


        if (!messageElement) {
            return;
        }


        messageElement.textContent =
            message;


        messageElement.className =
            `audit-global-message ${type}`;


        messageElement.hidden =
            false;


        messageElement.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    }


    // ======================================================
    // LOADING STATE
    // ======================================================

    function setLoadingState(
        loading
    ) {

        const page =
            document.querySelector(
                ".new-audit-page"
            );


        const form =
            getElement(
                "newAuditForm"
            );


        const input =
            getElement(
                "websiteUrl"
            );


        const button =
            getElement(
                "startAuditButton"
            );


        const buttonContent =
            getElement(
                "startAuditButtonContent"
            );


        const buttonLoading =
            getElement(
                "startAuditButtonLoading"
            );


        if (loading) {

            page?.classList.add(
                "is-loading"
            );


            form?.setAttribute(
                "aria-busy",
                "true"
            );


            input?.setAttribute(
                "disabled",
                "disabled"
            );


            button?.setAttribute(
                "disabled",
                "disabled"
            );


            button?.setAttribute(
                "aria-busy",
                "true"
            );


            setHidden(
                buttonContent,
                true
            );


            setHidden(
                buttonLoading,
                false
            );

        }

        else {

            page?.classList.remove(
                "is-loading"
            );


            form?.removeAttribute(
                "aria-busy"
            );


            input?.removeAttribute(
                "disabled"
            );


            button?.removeAttribute(
                "disabled"
            );


            button?.removeAttribute(
                "aria-busy"
            );


            setHidden(
                buttonContent,
                false
            );


            setHidden(
                buttonLoading,
                true
            );

        }

    }


    // ======================================================
    // CLEAR URL BUTTON
    // ======================================================

    function updateClearButton() {

        const input =
            getElement(
                "websiteUrl"
            );


        const clearButton =
            getElement(
                "clearWebsiteUrl"
            );


        if (!input || !clearButton) {
            return;
        }


        clearButton.hidden =
            !input.value.trim();

    }


    function clearWebsiteUrl() {

        const input =
            getElement(
                "websiteUrl"
            );


        if (!input) {
            return;
        }


        input.value =
            "";


        clearFieldError();

        clearGlobalMessage();

        updateClearButton();

        input.focus();

    }


    // ======================================================
    // API ERROR MESSAGE
    // ======================================================

    async function getApiErrorMessage(
        response
    ) {

        let message =
            "";


        try {

            const data =
                await response.json();


            /*
             * FastAPI usually returns:
             *
             * {
             *     "detail": "..."
             * }
             *
             * or validation errors:
             *
             * {
             *     "detail": [...]
             * }
             */

            if (
                typeof data.detail ===
                "string"
            ) {

                message =
                    data.detail;

            }


            else if (
                Array.isArray(
                    data.detail
                )
            ) {

                const messages =
                    data.detail
                        .map(
                            item => {

                                if (
                                    typeof item ===
                                    "string"
                                ) {

                                    return item;

                                }


                                return (
                                    item?.msg ||
                                    "Invalid request."
                                );

                            }
                        )
                        .filter(Boolean);


                message =
                    messages.join(
                        " "
                    );

            }


            else if (
                typeof data.message ===
                "string"
            ) {

                message =
                    data.message;

            }

        }

        catch (error) {

            /*
             * Response may not contain JSON.
             */

        }


        if (message) {

            return message;

        }


        switch (
            response.status
        ) {

            case 400:

                return (
                    "The website URL could not be processed."
                );


            case 401:

                return (
                    "Your session has expired. Please log in again."
                );


            case 403:

                return (
                    "You are not allowed to run this audit."
                );


            case 404:

                return (
                    "The audit service could not be found."
                );


            case 408:

                return (
                    "The audit request timed out."
                );


            case 422:

                return (
                    "Please check the website URL and try again."
                );


            case 429:

                return (
                    "Too many audit requests. Please try again later."
                );


            case 500:

                return (
                    "The website audit service encountered an internal error."
                );


            case 502:

            case 503:

                return (
                    "The audit service is temporarily unavailable."
                );


            default:

                return (
                    `Audit request failed (${response.status}).`
                );

        }

    }


    // ======================================================
    // FETCH WITH TIMEOUT
    // ======================================================

    async function fetchWithTimeout(
        url,
        options = {},
        timeout = REQUEST_TIMEOUT
    ) {

        const controller =
            new AbortController();


        const timeoutId =
            setTimeout(
                () => {

                    controller.abort();

                },
                timeout
            );


        try {

            return await fetch(
                url,
                {
                    ...options,
                    signal:
                        controller.signal
                }
            );

        }

        finally {

            clearTimeout(
                timeoutId
            );

        }

    }


    // ======================================================
    // SUBMIT AUDIT
    // ======================================================

    async function submitAudit(
        websiteUrl
    ) {

        const token =
            getAccessToken();


        if (!token) {

            showGlobalMessage(
                "Your session has expired. Please log in again.",
                "error"
            );


            window.setTimeout(
                () => {

                    window.location.replace(
                        LOGIN_URL
                    );

                },
                900
            );


            return;

        }


        const payload = {

            website_url:
                websiteUrl

        };


        let response;


        try {

            response =
                await fetchWithTimeout(

                    API_ENDPOINT,

                    {

                        method: "POST",

                        headers: {

                            "Authorization":
                                `Bearer ${token}`,

                            "Accept":
                                "application/json",

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                payload
                            )

                    },

                    REQUEST_TIMEOUT

                );

        }

        catch (error) {

            if (
                error.name ===
                "AbortError"
            ) {

                throw new Error(
                    "The audit is taking too long to respond. Please try again."
                );

            }


            throw new Error(
                "Unable to connect to the audit service. Please check your connection and try again."
            );

        }


        if (
            response.status === 401
        ) {

            throw new Error(
                "Your session has expired. Please log in again."
            );

        }


        if (!response.ok) {

            const message =
                await getApiErrorMessage(
                    response
                );


            throw new Error(
                message
            );

        }


        let data;


        try {

            data =
                await response.json();

        }

        catch (error) {

            throw new Error(
                "The audit service returned an invalid response."
            );

        }


        return data;

    }


    // ======================================================
    // EXTRACT AUDIT ID
    // ======================================================

    function getAuditId(
        data
    ) {

        /*
         * Current backend returns AuditRead
         * directly.
         */

        if (
            data &&
            data.id !== undefined &&
            data.id !== null
        ) {

            return data.id;

        }


        /*
         * Defensive support for a future
         * { data: {...} } response wrapper.
         */

        if (
            data?.data &&
            data.data.id !== undefined &&
            data.data.id !== null
        ) {

            return data.data.id;

        }


        return null;

    }


    // ======================================================
    // REDIRECT TO REPORT
    // ======================================================

    function redirectToAudit(
        auditId
    ) {

        const numericId =
            Number(auditId);


        if (
            !Number.isInteger(numericId) ||
            numericId <= 0
        ) {

            throw new Error(
                "The audit was completed, but the server did not return a valid audit ID."
            );

        }


        const reportUrl =
            `/audits/${encodeURIComponent(numericId)}`;


        console.info(
            "[AI Audit] Audit completed:",
            {
                auditId: numericId,
                reportUrl: reportUrl
            }
        );


        window.location.assign(
            reportUrl
        );

    }

    // ======================================================
    // FORM SUBMISSION
    // ======================================================

    async function handleSubmit(
        event
    ) {

        event.preventDefault();


        /*
         * Do not allow a second submission
         * while the first audit is running.
         */

        const button =
            getElement(
                "startAuditButton"
            );


        if (
            button?.disabled
        ) {

            return;

        }


        clearFieldError();

        clearGlobalMessage();


        const input =
            getElement(
                "websiteUrl"
            );


        if (!input) {

            return;

        }


        const validation =
            validateWebsiteUrl(
                input.value
            );


        if (!validation.valid) {

            showFieldError(
                validation.message
            );


            input.focus();

            return;

        }


        /*
         * Put normalized URL back into the field.
         *
         * Example:
         *
         * example.com
         *
         * becomes:
         *
         * https://example.com/
         */

        input.value =
            validation.url;


        updateClearButton();


        setLoadingState(
            true
        );


        try {

            const audit =
                await submitAudit(
                    validation.url
                );


            const auditId =
                getAuditId(
                    audit
                );


            /*
             * The backend has completed the
             * audit and returned the saved AuditRead.
             */

            showGlobalMessage(
                "Audit completed successfully. Opening your audit report...",
                "success"
            );


            await new Promise(
                resolve => setTimeout(
                    resolve,
                    350
                )
            );

            sessionStorage.setItem(
                "audit_completed",
                "true"
            );

            redirectToAudit(
                auditId
            );
        }

        catch (error) {

            console.error(
                "[AI Audit] New audit failed:",
                error
            );


            const message =
                error?.message ||
                "Unable to complete the website audit.";


            /*
             * Authentication failure.
             */

            if (
                message.toLowerCase()
                    .includes(
                        "session has expired"
                    )
            ) {

                showGlobalMessage(
                    message,
                    "error"
                );


                window.setTimeout(
                    () => {

                        window.location.replace(
                            LOGIN_URL
                        );

                    },
                    900
                );


                return;

            }


            showGlobalMessage(
                message,
                "error"
            );

        }

        finally {

            /*
             * If redirect succeeds, the page
             * will leave immediately.
             *
             * If an error occurs, restore the form.
             */

            if (
                document.visibilityState !==
                "hidden"
            ) {

                setLoadingState(
                    false
                );

            }

        }

    }


    // ======================================================
    // LIVE URL INPUT
    // ======================================================

    function handleUrlInput() {

        clearFieldError();

        clearGlobalMessage();

        updateClearButton();

    }


    // ======================================================
    // URL BLUR
    // ======================================================

    function handleUrlBlur() {

        const input =
            getElement(
                "websiteUrl"
            );


        if (!input) {
            return;
        }


        const value =
            input.value.trim();


        if (!value) {

            return;

        }


        const validation =
            validateWebsiteUrl(
                value
            );


        if (!validation.valid) {

            showFieldError(
                validation.message
            );

            return;

        }


        /*
         * Normalize only after the value
         * has passed validation.
         */

        input.value =
            validation.url;


        updateClearButton();

    }


    // ======================================================
    // ENTER KEY
    // ======================================================

    function handleUrlKeydown(
        event
    ) {

        if (
            event.key !== "Enter"
        ) {

            return;

        }


        event.preventDefault();


        const form =
            getElement(
                "newAuditForm"
            );


        if (form) {

            form.requestSubmit();

        }

    }


    // ======================================================
    // INITIALIZATION
    // ======================================================

    function initializeNewAudit() {

        const form =
            getElement(
                "newAuditForm"
            );


        const input =
            getElement(
                "websiteUrl"
            );


        const clearButton =
            getElement(
                "clearWebsiteUrl"
            );


        if (
            !form ||
            !input
        ) {

            return;

        }


        /*
         * Form submit.
         */

        form.addEventListener(
            "submit",
            handleSubmit
        );


        /*
         * Live input.
         */

        input.addEventListener(
            "input",
            handleUrlInput
        );


        /*
         * Validate when leaving field.
         */

        input.addEventListener(
            "blur",
            handleUrlBlur
        );


        /*
         * Enter submits the audit.
         */

        input.addEventListener(
            "keydown",
            handleUrlKeydown
        );


        /*
         * Clear URL.
         */

        clearButton?.addEventListener(
            "click",
            clearWebsiteUrl
        );


        /*
         * Initial state.
         */

        updateClearButton();

        clearFieldError();

        clearGlobalMessage();


        console.info(
            "[AI Audit] New Audit initialized."
        );

    }


    // ======================================================
    // DOM READY
    // ======================================================

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeNewAudit,
            {
                once: true
            }
        );

    }

    else {

        initializeNewAudit();

    }

})();