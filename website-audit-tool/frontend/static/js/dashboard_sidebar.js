/* ==========================================================
   AI AUDIT TOOL
   DASHBOARD SIDEBAR CONTROLLER
   STEP 2 — REAL USER + REAL NOTIFICATIONS
========================================================== */

(function () {

    "use strict";


    /* ======================================================
       CONFIG
    ====================================================== */

    const STORAGE_KEY =
        "ai_audit_sidebar_collapsed";


    /* ======================================================
       DOM
    ====================================================== */

    function $(id) {

        return document.getElementById(id);

    }


    /* ======================================================
       AUTH TOKEN
    ====================================================== */

    function getAuthToken() {

        const keys = [
            "access_token",
            "token",
            "auth_token"
        ];


        for (const key of keys) {

            const localToken =
                localStorage.getItem(key);

            if (localToken) {

                return localToken;

            }


            const sessionToken =
                sessionStorage.getItem(key);

            if (sessionToken) {

                return sessionToken;

            }

        }


        return null;

    }


    /* ======================================================
       AUTH HEADERS
    ====================================================== */

    function getAuthHeaders() {

        const headers = {
            "Accept":
                "application/json"
        };


        const token =
            getAuthToken();


        if (token) {

            headers["Authorization"] =
                `Bearer ${token}`;

        }


        return headers;

    }


    /* ======================================================
       USER INITIALS
    ====================================================== */

    function getInitials(name) {

        if (!name) {

            return "--";

        }


        const parts =
            String(name)
                .trim()
                .split(/\s+/)
                .filter(Boolean);


        if (!parts.length) {

            return "--";

        }


        if (parts.length === 1) {

            return parts[0]
                .substring(0, 2)
                .toUpperCase();

        }


        return (
            parts[0].charAt(0) +
            parts[parts.length - 1].charAt(0)
        ).toUpperCase();

    }


    /* ======================================================
       SIDEBAR ELEMENTS
    ====================================================== */

    function getSidebarElements() {

        return {

            sidebar:
                $("dashboardSidebar"),

            collapseButton:
                $("sidebarCollapseButton"),

            mobileButton:
                $("mobileSidebarToggle"),

            overlay:
                $("sidebarOverlay"),

            userButton:
                $("sidebarUserButton"),

            userDropdown:
                $("sidebarUserDropdown"),

            logoutButton:
                $("sidebarLogoutButton"),

            userAvatar:
                $("sidebarUserAvatar"),

            userName:
                $("sidebarUserName"),

            userRole:
                $("sidebarUserRole"),

            notificationBadge:
                $("sidebarNotificationBadge")

        };

    }


    /* ======================================================
       SIDEBAR COLLAPSE
    ====================================================== */

    function updateCollapseIcon() {

        const {
            sidebar,
            collapseButton
        } =
            getSidebarElements();


        if (
            !sidebar ||
            !collapseButton
        ) {

            return;

        }


        const icon =
            collapseButton.querySelector(
                "i"
            );


        const collapsed =
            sidebar.classList.contains(
                "collapsed"
            );


        if (icon) {

            icon.classList.toggle(
                "bi-chevron-left",
                !collapsed
            );

            icon.classList.toggle(
                "bi-chevron-right",
                collapsed
            );

        }


        collapseButton.setAttribute(
            "aria-label",
            collapsed
                ? "Expand sidebar"
                : "Collapse sidebar"
        );


        collapseButton.setAttribute(
            "title",
            collapsed
                ? "Expand sidebar"
                : "Collapse sidebar"
        );

    }


    function setSidebarCollapsed(
        collapsed,
        save = true
    ) {

        const {
            sidebar
        } =
            getSidebarElements();


        if (!sidebar) {

            return;

        }


        if (
            window.innerWidth <= 991
        ) {

            sidebar.classList.remove(
                "collapsed"
            );

            updateCollapseIcon();

            return;

        }


        sidebar.classList.toggle(
            "collapsed",
            Boolean(collapsed)
        );


        updateCollapseIcon();


        if (save) {

            localStorage.setItem(
                STORAGE_KEY,
                collapsed
                    ? "true"
                    : "false"
            );

        }


        document.dispatchEvent(
            new CustomEvent(
                "sidebarStateChanged",
                {
                    detail: {
                        collapsed:
                            Boolean(
                                collapsed
                            )
                    }
                }
            )
        );

    }


    function loadSavedSidebarState() {

        const {
            sidebar
        } =
            getSidebarElements();


        if (!sidebar) {

            return;

        }


        if (
            window.innerWidth <= 991
        ) {

            sidebar.classList.remove(
                "collapsed"
            );

            sidebar.classList.remove(
                "mobile-open"
            );

            return;

        }


        const saved =
            localStorage.getItem(
                STORAGE_KEY
            );


        setSidebarCollapsed(
            saved === "true",
            false
        );

    }


    function initializeCollapseButton() {

        const {
            sidebar,
            collapseButton
        } =
            getSidebarElements();


        if (
            !sidebar ||
            !collapseButton
        ) {

            console.error(
                "[Sidebar] Collapse elements missing."
            );

            return;

        }


        collapseButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                if (
                    window.innerWidth <= 991
                ) {

                    return;

                }


                const collapsed =
                    sidebar.classList.contains(
                        "collapsed"
                    );


                setSidebarCollapsed(
                    !collapsed
                );

            }
        );

    }


    /* ======================================================
       MOBILE SIDEBAR
    ====================================================== */

    function openMobileSidebar() {

        const {
            sidebar,
            mobileButton,
            overlay
        } =
            getSidebarElements();


        if (!sidebar) {

            return;

        }


        sidebar.classList.add(
            "mobile-open"
        );


        if (overlay) {

            overlay.classList.add(
                "show"
            );

        }


        if (mobileButton) {

            mobileButton.setAttribute(
                "aria-expanded",
                "true"
            );

        }


        document.body.classList.add(
            "sidebar-mobile-open"
        );

    }


    function closeMobileSidebar() {

        const {
            sidebar,
            mobileButton,
            overlay
        } =
            getSidebarElements();


        if (!sidebar) {

            return;

        }


        sidebar.classList.remove(
            "mobile-open"
        );


        if (overlay) {

            overlay.classList.remove(
                "show"
            );

        }


        if (mobileButton) {

            mobileButton.setAttribute(
                "aria-expanded",
                "false"
            );

        }


        document.body.classList.remove(
            "sidebar-mobile-open"
        );

    }


    function initializeMobileSidebar() {

        const {
            mobileButton,
            overlay
        } =
            getSidebarElements();


        if (mobileButton) {

            mobileButton.addEventListener(
                "click",
                function (event) {

                    event.preventDefault();

                    event.stopPropagation();


                    const sidebar =
                        $("dashboardSidebar");


                    if (!sidebar) {

                        return;

                    }


                    if (
                        sidebar.classList.contains(
                            "mobile-open"
                        )
                    ) {

                        closeMobileSidebar();

                    }
                    else {

                        openMobileSidebar();

                    }

                }
            );

        }


        if (overlay) {

            overlay.addEventListener(
                "click",
                closeMobileSidebar
            );

        }

    }


    /* ======================================================
       USER MENU
    ====================================================== */

    function closeUserMenu() {

        const {
            userButton,
            userDropdown
        } =
            getSidebarElements();


        if (
            !userButton ||
            !userDropdown
        ) {

            return;

        }


        userDropdown.classList.remove(
            "show"
        );


        userButton.setAttribute(
            "aria-expanded",
            "false"
        );

    }


    function openUserMenu() {

        const {
            userButton,
            userDropdown
        } =
            getSidebarElements();


        if (
            !userButton ||
            !userDropdown
        ) {

            return;

        }


        userDropdown.classList.add(
            "show"
        );


        userButton.setAttribute(
            "aria-expanded",
            "true"
        );

    }


    function initializeUserMenu() {

        const {
            userButton,
            userDropdown
        } =
            getSidebarElements();


        if (
            !userButton ||
            !userDropdown
        ) {

            console.error(
                "[Sidebar] User menu elements missing."
            );

            return;

        }


        userButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                const isOpen =
                    userDropdown.classList.contains(
                        "show"
                    );


                if (isOpen) {

                    closeUserMenu();

                }
                else {

                    openUserMenu();

                }

            }
        );


        document.addEventListener(
            "click",
            function (event) {

                if (
                    !userDropdown.contains(
                        event.target
                    ) &&
                    !userButton.contains(
                        event.target
                    )
                ) {

                    closeUserMenu();

                }

            }
        );

    }


    /* ======================================================
       ACTIVE NAVIGATION
    ====================================================== */

    function normalizePath(path) {

        if (!path) {

            return "/";

        }


        let value =
            path
                .split("?")[0]
                .split("#")[0];


        if (
            value.length > 1 &&
            value.endsWith("/")
        ) {

            value =
                value.slice(
                    0,
                    -1
                );

        }


        return value;

    }


    function updateActiveNavigation() {

        const currentPath =
            normalizePath(
                window.location.pathname
            );


        document
            .querySelectorAll(
                ".sidebar-nav-item"
            )
            .forEach(
                function (link) {

                    const href =
                        link.getAttribute(
                            "href"
                        );


                    if (!href) {

                        return;

                    }


                    const linkPath =
                        normalizePath(
                            href
                        );


                    const active =
                        currentPath ===
                            linkPath ||
                        (
                            linkPath !==
                                "/dashboard" &&
                            currentPath.startsWith(
                                linkPath + "/"
                            )
                        );


                    link.classList.toggle(
                        "active",
                        active
                    );

                }
            );

    }


    /* ======================================================
       REAL USER
       
       GET /api/auth/me
    ====================================================== */

    async function loadRealUser() {

        const {
            userAvatar,
            userName,
            userRole
        } =
            getSidebarElements();


        /*
         * Temporary loading state.
         */

        if (userAvatar) {

            userAvatar.textContent =
                "--";

        }


        if (userName) {

            userName.textContent =
                "Loading...";

        }


        if (userRole) {

            userRole.textContent =
                "Account";

        }


        const token =
            getAuthToken();


        if (!token) {

            console.warn(
                "[Sidebar] Authentication token not found."
            );

            return;

        }


        try {

            const response =
                await fetch(
                    "/api/auth/me",
                    {
                        method: "GET",

                        credentials:
                            "include",

                        headers:
                            getAuthHeaders()
                    }
                );


            if (
                response.status === 401 ||
                response.status === 403
            ) {

                console.warn(
                    "[Sidebar] Authentication expired."
                );

                return;

            }


            if (!response.ok) {

                throw new Error(
                    `User API returned ${response.status}`
                );

            }


            const payload =
                await response.json();


            /*
             * Support both:
             *
             * direct user object
             *
             * and
             *
             * { data: user }
             */

            const user =
                payload?.data &&
                typeof payload.data === "object"
                    ? payload.data
                    : payload;


            renderRealUser(
                user
            );

        }
        catch (error) {

            console.error(
                "[Sidebar] Real user request failed:",
                error
            );

        }

    }


    /* ======================================================
       RENDER REAL USER
    ====================================================== */

    function renderRealUser(
        user
    ) {

        const {
            userAvatar,
            userName,
            userRole
        } =
            getSidebarElements();


        if (!user) {

            return;

        }


        const name =
            user.name ||
            user.full_name ||
            user.username ||
            "User";


        const role =
            user.role ||
            user.user_role ||
            "Account";


        const initials =
            getInitials(
                name
            );


        if (userAvatar) {

            userAvatar.textContent =
                initials;

        }


        if (userName) {

            userName.textContent =
                name;

        }


        if (userRole) {

            userRole.textContent =
                formatRole(
                    role
                );

        }


        console.log(
            "[Sidebar] Real user loaded:",
            name
        );

    }


    /* ======================================================
       FORMAT ROLE
    ====================================================== */

    function formatRole(
        role
    ) {

        if (!role) {

            return "Account";

        }


        const value =
            String(role)
                .trim()
                .toLowerCase();


        const map = {

            owner:
                "Website Owner",

            website_owner:
                "Website Owner",

            admin:
                "Administrator",

            administrator:
                "Administrator",

            user:
                "Account",

            member:
                "Member"

        };


        if (
            map[value]
        ) {

            return map[value];

        }


        return String(role)
            .replace(
                /[_-]+/g,
                " "
            )
            .replace(
                /\b\w/g,
                function (letter) {

                    return letter.toUpperCase();

                }
            );

    }


    /* ======================================================
       REAL NOTIFICATIONS
       
       GET /api/notifications
       
       The existing topbar uses this same endpoint and
       reads payload.unread.
    ====================================================== */

    async function loadRealNotificationCount() {

        const badge =
            $("sidebarNotificationBadge");


        if (!badge) {

            return;

        }


        /*
         * Never show fake data.
         */

        badge.textContent =
            "";

        badge.style.display =
            "none";


        const token =
            getAuthToken();


        if (!token) {

            return;

        }


        try {

            const response =
                await fetch(
                    "/api/notifications",
                    {
                        method: "GET",

                        credentials:
                            "include",

                        headers:
                            getAuthHeaders()
                    }
                );


            if (
                response.status === 401 ||
                response.status === 403
            ) {

                return;

            }


            if (!response.ok) {

                throw new Error(
                    `Notification API returned ${response.status}`
                );

            }


            const payload =
                await response.json();


            /*
             * Current API format:
             *
             * {
             *     notifications: [],
             *     unread: 3
             * }
             */

            const unread =
                Number(
                    payload?.unread
                ) || 0;


            if (
                unread <= 0
            ) {

                return;

            }


            badge.textContent =
                unread > 99
                    ? "99+"
                    : String(unread);


            badge.style.display =
                "inline-flex";


            console.log(
                "[Sidebar] Real unread notifications:",
                unread
            );

        }
        catch (error) {

            /*
             * Do not display fake numbers if API fails.
             */

            badge.textContent =
                "";

            badge.style.display =
                "none";


            console.error(
                "[Sidebar] Notification count failed:",
                error
            );

        }

    }


    /* ======================================================
       LOGOUT
    ====================================================== */

    function clearAuthStorage() {

        [
            "access_token",
            "token",
            "auth_token"
        ]
        .forEach(
            function (key) {

                localStorage.removeItem(
                    key
                );

                sessionStorage.removeItem(
                    key
                );

            }
        );

    }


    async function logout() {

        const token =
            getAuthToken();


        try {

            if (token) {

                await fetch(
                    "/api/auth/logout",
                    {
                        method: "POST",

                        credentials:
                            "include",

                        headers:
                            getAuthHeaders()
                    }
                );

            }

        }
        catch (error) {

            console.warn(
                "[Sidebar] Logout API error:",
                error
            );

        }
        finally {

            clearAuthStorage();

            window.location.replace(
                "/login"
            );

        }

    }


    function initializeLogout() {

        const button =
            $("sidebarLogoutButton");


        if (!button) {

            return;

        }


        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();


                logout();

            }
        );

    }


    /* ======================================================
       KEYBOARD
    ====================================================== */

    function initializeKeyboard() {

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key !== "Escape"
                ) {

                    return;

                }


                closeUserMenu();

                closeMobileSidebar();

            }
        );

    }


    /* ======================================================
       NAVIGATION
    ====================================================== */

    function initializeNavigation() {

        document.addEventListener(
            "click",
            function (event) {

                const link =
                    event.target.closest(
                        ".sidebar-nav-item"
                    );


                if (!link) {

                    return;

                }


                if (
                    window.innerWidth <= 991
                ) {

                    closeMobileSidebar();

                }

            }
        );

    }


    /* ======================================================
       RESIZE
    ====================================================== */

    function initializeResize() {

        let timer = null;


        window.addEventListener(
            "resize",
            function () {

                clearTimeout(
                    timer
                );


                timer =
                    setTimeout(
                        function () {

                            if (
                                window.innerWidth > 991
                            ) {

                                closeMobileSidebar();

                                loadSavedSidebarState();

                            }
                            else {

                                const {
                                    sidebar
                                } =
                                    getSidebarElements();


                                if (sidebar) {

                                    sidebar.classList.remove(
                                        "collapsed"
                                    );

                                }


                                updateCollapseIcon();

                            }

                        },
                        120
                    );

            }
        );

    }


    /* ======================================================
       INITIALIZE
    ====================================================== */

    async function initializeSidebar() {

        console.log(
            "[AI Audit] Dashboard sidebar initialized."
        );


        /*
         * UI
         */

        loadSavedSidebarState();

        initializeCollapseButton();

        initializeMobileSidebar();

        initializeUserMenu();

        initializeLogout();

        initializeKeyboard();

        initializeNavigation();

        initializeResize();

        updateActiveNavigation();


        /*
         * REAL DATA
         */

        await Promise.allSettled([

            loadRealUser(),

            loadRealNotificationCount()

        ]);

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
            initializeSidebar,
            {
                once: true
            }
        );

    }
    else {

        initializeSidebar();

    }


    /* ======================================================
       PUBLIC REFRESH
    ====================================================== */

    window.refreshDashboardSidebar =
        function () {

            loadRealUser();

            loadRealNotificationCount();

        };


})();