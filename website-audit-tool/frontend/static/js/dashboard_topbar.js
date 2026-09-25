/* ==========================================================
   AI AUDIT TOOL — DASHBOARD TOPBAR
   ----------------------------------------------------------
   Handles:
   - Real logged-in user
   - User dropdown
   - Notifications
   - Real unread notification count
   - Mark notification as read
   - Mark all as read
   - Delete notification
   - Notification refresh
   - Dashboard search
   - Logout
========================================================== */

(function () {

    "use strict";


    /* ======================================================
       CONFIG
    ====================================================== */

    const NOTIFICATION_REFRESH_INTERVAL = 60000;

    let notificationRefreshTimer = null;


    /* ======================================================
       DOM HELPER
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
            "Accept": "application/json"
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
       API REQUEST
    ====================================================== */

    async function apiRequest(
        url,
        options = {}
    ) {

        const response =
            await fetch(
                url,
                {
                    ...options,

                    headers: {
                        ...getAuthHeaders(),
                        ...(options.headers || {})
                    }
                }
            );


        /* ----------------------------------------------
           AUTH EXPIRED
        ---------------------------------------------- */

        if (
            response.status === 401 ||
            response.status === 403
        ) {

            clearAuth();

            window.location.replace("/login");

            throw new Error(
                "Authentication expired."
            );

        }


        /* ----------------------------------------------
           OTHER API ERROR
        ---------------------------------------------- */

        if (!response.ok) {

            let message =
                `Request failed: ${response.status}`;


            try {

                const error =
                    await response.json();


                if (error.detail) {

                    message =
                        error.detail;

                }

            } catch (_) {
                // Keep default message.
            }


            throw new Error(message);

        }


        if (response.status === 204) {

            return null;

        }


        return response.json();

    }


    /* ======================================================
       CLEAR AUTH
    ====================================================== */

    function clearAuth() {

        const keys = [
            "access_token",
            "token",
            "auth_token"
        ];


        keys.forEach((key) => {

            localStorage.removeItem(key);
            sessionStorage.removeItem(key);

        });

    }


    /* ======================================================
       USER INITIALS
    ====================================================== */

    function getUserInitials(name) {

        if (!name) {

            return "--";

        }


        const parts =
            String(name)
                .trim()
                .split(/\s+/)
                .filter(Boolean);


        if (parts.length === 1) {

            return parts[0]
                .substring(0, 2)
                .toUpperCase();

        }


        return (
            parts[0][0] +
            parts[parts.length - 1][0]
        ).toUpperCase();

    }


    /* ======================================================
       LOAD REAL USER
       API:
       GET /api/auth/me
    ====================================================== */

    async function loadTopbarUser() {

        const token =
            getAuthToken();


        if (!token) {

            renderTopbarUser(null);

            return null;

        }


        try {

            const user =
                await apiRequest(
                    "/api/auth/me"
                );


            renderTopbarUser(user);

            return user;

        }
        catch (error) {

            console.error(
                "[Topbar] User loading failed:",
                error
            );


            renderTopbarUser(null);

            return null;

        }

    }


    /* ======================================================
       RENDER USER
    ====================================================== */

    function renderTopbarUser(user) {

        const nameElement =
            $("topbarUserName");

        const roleElement =
            $("topbarUserRole");

        const initialsElement =
            $("topbarUserInitials");

        const dropdownName =
            $("topbarDropdownName");

        const dropdownEmail =
            $("topbarDropdownEmail");

        const dropdownInitials =
            $("topbarDropdownInitials");


        /* ----------------------------------------------
           NOT AUTHENTICATED
        ---------------------------------------------- */

        if (!user) {

            if (nameElement) {

                nameElement.textContent =
                    "Guest User";

            }


            if (roleElement) {

                roleElement.textContent =
                    "Not authenticated";

            }


            if (initialsElement) {

                initialsElement.textContent =
                    "--";

            }


            if (dropdownName) {

                dropdownName.textContent =
                    "Guest User";

            }


            if (dropdownEmail) {

                dropdownEmail.textContent =
                    "Not authenticated";

            }


            if (dropdownInitials) {

                dropdownInitials.textContent =
                    "--";

            }


            return;

        }


        /* ----------------------------------------------
           REAL USER
        ---------------------------------------------- */

        const name =
            user.name ||
            "User";


        const email =
            user.email ||
            "";


        const initials =
            getUserInitials(name);


        if (nameElement) {

            nameElement.textContent =
                name;

        }


        if (roleElement) {

            roleElement.textContent =
                "Website Owner";

        }


        if (initialsElement) {

            initialsElement.textContent =
                initials;

        }


        if (dropdownName) {

            dropdownName.textContent =
                name;

        }


        if (dropdownEmail) {

            dropdownEmail.textContent =
                email;

        }


        if (dropdownInitials) {

            dropdownInitials.textContent =
                initials;

        }

    }


    /* ======================================================
       USER DROPDOWN
    ====================================================== */

    function openUserDropdown() {

        const button =
            $("userProfileButton");

        const dropdown =
            $("userDropdown");


        if (!button || !dropdown) {

            return;

        }


        closeNotificationDropdown();


        dropdown.classList.add("show");


        button.setAttribute(
            "aria-expanded",
            "true"
        );


        dropdown.setAttribute(
            "aria-hidden",
            "false"
        );

    }


    function closeUserDropdown() {

        const button =
            $("userProfileButton");

        const dropdown =
            $("userDropdown");


        if (!button || !dropdown) {

            return;

        }


        dropdown.classList.remove("show");


        button.setAttribute(
            "aria-expanded",
            "false"
        );


        dropdown.setAttribute(
            "aria-hidden",
            "true"
        );

    }


    /* ======================================================
       NOTIFICATION ICON
    ====================================================== */

    function getNotificationIcon(type) {

        switch (type) {

            case "success":
                return "bi-check-circle-fill";

            case "warning":
                return "bi-exclamation-triangle-fill";

            case "error":
                return "bi-x-circle-fill";

            case "info":
                return "bi-info-circle-fill";

            default:
                return "bi-bell-fill";

        }

    }


    /* ======================================================
       NOTIFICATION ICON CLASS
    ====================================================== */

    function getNotificationTypeClass(type) {

        switch (type) {

            case "success":
                return "success";

            case "warning":
                return "warning";

            case "error":
                return "error";

            case "info":
            default:
                return "info";

        }

    }


    /* ======================================================
       ESCAPE HTML
       Prevents notification text from injecting HTML.
    ====================================================== */

    function escapeHTML(value) {

        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }


    /* ======================================================
       NOTIFICATION TIME
    ====================================================== */

    function formatNotificationTime(value) {

        if (!value) {

            return "";

        }


        const date =
            new Date(value);


        if (Number.isNaN(date.getTime())) {

            return "";

        }


        const seconds =
            Math.max(
                0,
                Math.floor(
                    (Date.now() - date.getTime()) /
                    1000
                )
            );


        if (seconds < 60) {

            return "Just now";

        }


        const minutes =
            Math.floor(seconds / 60);


        if (minutes < 60) {

            return `${minutes} min ago`;

        }


        const hours =
            Math.floor(minutes / 60);


        if (hours < 24) {

            return (
                `${hours} hour` +
                (hours === 1 ? "" : "s") +
                " ago"
            );

        }


        const days =
            Math.floor(hours / 24);


        if (days === 1) {

            return "Yesterday";

        }


        if (days < 7) {

            return `${days} days ago`;

        }


        return date.toLocaleDateString(
            undefined,
            {
                day: "numeric",
                month: "short",
                year: "numeric"
            }
        );

    }


    /* ======================================================
       BADGE
    ====================================================== */

    function setNotificationBadge(count) {

        const badge =
            $("notificationCount");


        if (!badge) {

            return;

        }


        const unread =
            Number(count) || 0;


        if (unread <= 0) {

            badge.style.display =
                "none";

            badge.textContent =
                "";

            return;

        }


        badge.style.display =
            "flex";


        badge.textContent =
            unread > 99
                ? "99+"
                : String(unread);

    }


    /* ======================================================
       EMPTY STATE
    ====================================================== */

    function showNotificationEmpty() {

        const list =
            $("notificationList");


        if (!list) {

            return;

        }


        list.innerHTML = `
            <div class="notification-empty">

                <div class="notification-empty-icon">
                    <i class="bi bi-bell-slash"></i>
                </div>

                <h6>No Notifications</h6>

                <p>
                    You're all caught up.
                </p>

            </div>
        `;

    }


    /* ======================================================
       ERROR STATE
    ====================================================== */

    function showNotificationError() {

        const list =
            $("notificationList");


        if (!list) {

            return;

        }


        list.innerHTML = `
            <div class="notification-empty">

                <div class="notification-empty-icon">
                    <i class="bi bi-exclamation-circle"></i>
                </div>

                <h6>
                    Unable to load notifications
                </h6>

                <p>
                    Please refresh and try again.
                </p>

            </div>
        `;

    }


    /* ======================================================
       RENDER NOTIFICATIONS
       
       Backend response:
       
       {
           total: number,
           unread: number,
           notifications: []
       }
    ====================================================== */

    function renderNotifications(payload) {

        const list =
            $("notificationList");


        if (!list) {

            return;

        }


        const notifications =
            Array.isArray(
                payload?.notifications
            )
                ? payload.notifications
                : [];


        const unread =
            Number(payload?.unread) || 0;


        setNotificationBadge(unread);


        if (notifications.length === 0) {

            showNotificationEmpty();

            return;

        }


        list.innerHTML =
            notifications
                .map((notification) => {

                    const id =
                        escapeHTML(
                            notification.id
                        );


                    const type =
                        notification.type ||
                        "info";


                    const unreadClass =
                        notification.is_read
                            ? ""
                            : "unread";


                    const icon =
                        getNotificationIcon(
                            type
                        );


                    const typeClass =
                        getNotificationTypeClass(
                            type
                        );


                    return `
                        <div
                            class="notification-item ${unreadClass}"
                            data-id="${id}"
                            role="button"
                            tabindex="0">

                            <div
                                class="notification-icon ${typeClass}">

                                <i
                                    class="bi ${icon}">
                                </i>

                            </div>

                            <div
                                class="notification-content">

                                <h6>
                                    ${escapeHTML(
                                        notification.title ||
                                        "Notification"
                                    )}
                                </h6>

                                <p>
                                    ${escapeHTML(
                                        notification.message ||
                                        ""
                                    )}
                                </p>

                                <span>
                                    ${escapeHTML(
                                        formatNotificationTime(
                                            notification.created_at
                                        )
                                    )}
                                </span>

                            </div>

                            <button
                                type="button"
                                class="notification-delete"
                                data-id="${id}"
                                title="Delete notification"
                                aria-label="Delete notification">

                                <i class="bi bi-x-lg"></i>

                            </button>

                        </div>
                    `;

                })
                .join("");

    }


    /* ======================================================
       LOAD NOTIFICATIONS
       
       IMPORTANT:
       We use /api/notifications.
       We DO NOT use /api/notifications/unread-count.
    ====================================================== */

    async function loadNotifications() {

        const list =
            $("notificationList");

        const refreshButton =
            $("refreshNotificationsButton");


        if (list) {

            list.innerHTML = `
                <div class="notification-loading">

                    <div
                        class="spinner-border spinner-border-sm text-primary"
                        role="status">
                    </div>

                    <span>
                        Loading notifications...
                    </span>

                </div>
            `;

        }


        if (refreshButton) {

            refreshButton.disabled =
                true;

        }


        try {

            const payload =
                await apiRequest(
                    "/api/notifications"
                );


            renderNotifications(
                payload
            );


            return payload;

        }
        catch (error) {

            console.error(
                "[Topbar] Notifications failed:",
                error
            );


            showNotificationError();


            return null;

        }
        finally {

            if (refreshButton) {

                refreshButton.disabled =
                    false;

            }

        }

    }


    /* ======================================================
       LOAD UNREAD COUNT
       
       Uses the same real notification API.
    ====================================================== */

    async function loadUnreadCount() {

        const token =
            getAuthToken();


        if (!token) {

            setNotificationBadge(0);

            return 0;

        }


        try {

            const payload =
                await apiRequest(
                    "/api/notifications"
                );


            const unread =
                Number(payload?.unread) || 0;


            setNotificationBadge(
                unread
            );


            return unread;

        }
        catch (error) {

            console.error(
                "[Topbar] Unread count failed:",
                error
            );


            return 0;

        }

    }


    /* ======================================================
       OPEN NOTIFICATION DROPDOWN
    ====================================================== */

    function openNotificationDropdown() {

        const button =
            $("notificationButton");

        const dropdown =
            $("notificationDropdown");


        if (!button || !dropdown) {

            return;

        }


        closeUserDropdown();


        dropdown.classList.add("show");


        button.setAttribute(
            "aria-expanded",
            "true"
        );


        dropdown.setAttribute(
            "aria-hidden",
            "false"
        );


        loadNotifications();

    }


    /* ======================================================
       CLOSE NOTIFICATION DROPDOWN
    ====================================================== */

    function closeNotificationDropdown() {

        const button =
            $("notificationButton");

        const dropdown =
            $("notificationDropdown");


        if (!button || !dropdown) {

            return;

        }


        dropdown.classList.remove("show");


        button.setAttribute(
            "aria-expanded",
            "false"
        );


        dropdown.setAttribute(
            "aria-hidden",
            "true"
        );

    }


    /* ======================================================
       MARK SINGLE NOTIFICATION READ
       
       PUT:
       /api/notifications/{id}/read
    ====================================================== */

    async function markNotificationRead(
        id,
        element
    ) {

        if (!id || !element) {

            return;

        }


        if (
            !element.classList.contains(
                "unread"
            )
        ) {

            return;

        }


        try {

            await apiRequest(
                `/api/notifications/${encodeURIComponent(id)}/read`,
                {
                    method: "PUT"
                }
            );


            element.classList.remove(
                "unread"
            );


            await loadUnreadCount();

        }
        catch (error) {

            console.error(
                "[Topbar] Mark read failed:",
                error
            );

        }

    }


    /* ======================================================
       MARK ALL READ
       
       PUT:
       /api/notifications/read-all
    ====================================================== */

    async function markAllNotificationsRead() {

        const button =
            $("markAllNotifications");


        if (button) {

            button.disabled =
                true;

        }


        try {

            await apiRequest(
                "/api/notifications/read-all",
                {
                    method: "PUT"
                }
            );


            document
                .querySelectorAll(
                    "#notificationList .notification-item.unread"
                )
                .forEach((item) => {

                    item.classList.remove(
                        "unread"
                    );

                });


            setNotificationBadge(0);

        }
        catch (error) {

            console.error(
                "[Topbar] Mark all failed:",
                error
            );

        }
        finally {

            if (button) {

                button.disabled =
                    false;

            }

        }

    }


    /* ======================================================
       DELETE NOTIFICATION
       
       DELETE:
       /api/notifications/{id}
    ====================================================== */

    async function deleteNotification(
        id,
        element
    ) {

        if (!id || !element) {

            return;

        }


        try {

            await apiRequest(
                `/api/notifications/${encodeURIComponent(id)}`,
                {
                    method: "DELETE"
                }
            );


            element.remove();


            const remaining =
                document.querySelectorAll(
                    "#notificationList .notification-item"
                ).length;


            if (remaining === 0) {

                showNotificationEmpty();

            }


            await loadUnreadCount();

        }
        catch (error) {

            console.error(
                "[Topbar] Delete failed:",
                error
            );

        }

    }


    /* ======================================================
       SEARCH
    ====================================================== */

    function submitSearch() {

        const input =
            $("dashboardSearch");


        if (!input) {

            return;

        }


        const query =
            input.value.trim();


        if (!query) {

            return;

        }


        window.location.href =
            `/history?search=${encodeURIComponent(query)}`;

    }


    /* ======================================================
       LOGOUT
    ====================================================== */

    function performLogout() {

        clearAuth();

        window.location.replace(
            "/login"
        );

    }


    /* ======================================================
       CLICK HANDLER
       Event delegation = reliable with Jinja includes.
    ====================================================== */

    function handleClick(event) {

        const target =
            event.target;


        /* ----------------------------------------------
           USER BUTTON
        ---------------------------------------------- */

        const userButton =
            target.closest(
                "#userProfileButton"
            );


        if (userButton) {

            event.preventDefault();
            event.stopPropagation();


            const dropdown =
                $("userDropdown");


            if (
                dropdown &&
                dropdown.classList.contains(
                    "show"
                )
            ) {

                closeUserDropdown();

            }
            else {

                openUserDropdown();

            }


            return;

        }


        /* ----------------------------------------------
           NOTIFICATION BUTTON
        ---------------------------------------------- */

        const notificationButton =
            target.closest(
                "#notificationButton"
            );


        if (notificationButton) {

            event.preventDefault();
            event.stopPropagation();


            const dropdown =
                $("notificationDropdown");


            if (
                dropdown &&
                dropdown.classList.contains(
                    "show"
                )
            ) {

                closeNotificationDropdown();

            }
            else {

                openNotificationDropdown();

            }


            return;

        }


        /* ----------------------------------------------
           REFRESH
        ---------------------------------------------- */

        const refreshButton =
            target.closest(
                "#refreshNotificationsButton"
            );


        if (refreshButton) {

            event.preventDefault();
            event.stopPropagation();


            loadNotifications();


            return;

        }


        /* ----------------------------------------------
           MARK ALL
        ---------------------------------------------- */

        const markAllButton =
            target.closest(
                "#markAllNotifications"
            );


        if (markAllButton) {

            event.preventDefault();
            event.stopPropagation();


            markAllNotificationsRead();


            return;

        }


        /* ----------------------------------------------
           LOGOUT
        ---------------------------------------------- */

        const logoutButton =
            target.closest(
                "#logoutButton"
            );


        if (logoutButton) {

            event.preventDefault();
            event.stopPropagation();


            performLogout();


            return;

        }


        /* ----------------------------------------------
           DELETE
        ---------------------------------------------- */

        const deleteButton =
            target.closest(
                ".notification-delete"
            );


        if (deleteButton) {

            event.preventDefault();
            event.stopPropagation();


            const item =
                deleteButton.closest(
                    ".notification-item"
                );


            const id =
                deleteButton.dataset.id;


            deleteNotification(
                id,
                item
            );


            return;

        }


        /* ----------------------------------------------
           NOTIFICATION ITEM
        ---------------------------------------------- */

        const notificationItem =
            target.closest(
                ".notification-item"
            );


        if (notificationItem) {

            const id =
                notificationItem.dataset.id;


            markNotificationRead(
                id,
                notificationItem
            );


            return;

        }


        /* ----------------------------------------------
           CLICK OUTSIDE
        ---------------------------------------------- */

        const userDropdown =
            $("userDropdown");

        const notificationDropdown =
            $("notificationDropdown");


        if (
            userDropdown &&
            !userDropdown.contains(target)
        ) {

            closeUserDropdown();

        }


        if (
            notificationDropdown &&
            !notificationDropdown.contains(target)
        ) {

            closeNotificationDropdown();

        }

    }


    /* ======================================================
       KEYBOARD
    ====================================================== */

    function handleKeydown(event) {

        /* Search ENTER */

        if (
            event.key === "Enter" &&
            event.target.closest(
                "#dashboardSearch"
            )
        ) {

            event.preventDefault();

            submitSearch();

            return;

        }


        /* Escape */

        if (event.key === "Escape") {

            closeUserDropdown();

            closeNotificationDropdown();

        }

    }


    /* ======================================================
       AUTO REFRESH
    ====================================================== */

    function startNotificationRefresh() {

        if (notificationRefreshTimer) {

            clearInterval(
                notificationRefreshTimer
            );

        }


        notificationRefreshTimer =
            setInterval(
                async () => {

                    await loadUnreadCount();


                    const dropdown =
                        $("notificationDropdown");


                    if (
                        dropdown &&
                        dropdown.classList.contains(
                            "show"
                        )
                    ) {

                        await loadNotifications();

                    }

                },
                NOTIFICATION_REFRESH_INTERVAL
            );

    }


    /* ======================================================
       INITIALIZATION
    ====================================================== */

    async function initializeTopbar() {

        console.log(
            "[AI Audit] Dashboard topbar initialized."
        );


        document.addEventListener(
            "click",
            handleClick
        );


        document.addEventListener(
            "keydown",
            handleKeydown
        );


        const userDropdown =
            $("userDropdown");

        const notificationDropdown =
            $("notificationDropdown");


        if (userDropdown) {

            userDropdown.classList.remove(
                "show"
            );

            userDropdown.setAttribute(
                "aria-hidden",
                "true"
            );

        }


        if (notificationDropdown) {

            notificationDropdown.classList.remove(
                "show"
            );

            notificationDropdown.setAttribute(
                "aria-hidden",
                "true"
            );

        }


        /*
         * Load real data immediately.
         */

        await Promise.all([
            loadTopbarUser(),
            loadUnreadCount()
        ]);


        startNotificationRefresh();

    }


    /* ======================================================
       CLEANUP
    ====================================================== */

    window.addEventListener(
        "beforeunload",
        () => {

            if (notificationRefreshTimer) {

                clearInterval(
                    notificationRefreshTimer
                );

            }

        }
    );


    /* ======================================================
       START
    ====================================================== */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initializeTopbar,
            {
                once: true
            }
        );

    }
    else {

        initializeTopbar();

    }


})();