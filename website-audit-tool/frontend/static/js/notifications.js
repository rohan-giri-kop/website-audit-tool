/* ==========================================================
   AI AUDIT TOOL
   NOTIFICATIONS PAGE
========================================================== */

(function () {

    "use strict";


    /* ======================================================
       STATE
    ====================================================== */

    let allNotifications = [];

    let currentFilter = "all";

    let loading = false;


    /* ======================================================
       HELPERS
    ====================================================== */

    function $(id) {

        return document.getElementById(id);

    }


    function getAuthToken() {

        const keys = [
            "access_token",
            "token",
            "auth_token"
        ];


        for (const key of keys) {

            const local =
                localStorage.getItem(key);

            if (local) {

                return local;

            }


            const session =
                sessionStorage.getItem(key);

            if (session) {

                return session;

            }

        }


        return null;

    }


    function getHeaders() {

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
       ESCAPE HTML
    ====================================================== */

    function escapeHTML(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return "";

        }


        return String(value)
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


    /* ======================================================
       ICON
    ====================================================== */

    function getNotificationIcon(
        type
    ) {

        switch (
            String(type || "")
                .toLowerCase()
        ) {

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
       TYPE CLASS
    ====================================================== */

    function getTypeClass(
        type
    ) {

        const allowed = [
            "success",
            "warning",
            "error",
            "info"
        ];


        const value =
            String(type || "info")
                .toLowerCase();


        return allowed.includes(value)
            ? value
            : "info";

    }


    /* ======================================================
       TIME
    ====================================================== */

    function formatNotificationTime(
        dateTime
    ) {

        if (!dateTime) {

            return "";

        }


        const date =
            new Date(dateTime);


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return "";

        }


        const now =
            new Date();


        const seconds =
            Math.floor(
                (now - date) / 1000
            );


        if (seconds < 60) {

            return "Just now";

        }


        const minutes =
            Math.floor(
                seconds / 60
            );


        if (minutes < 60) {

            return `${minutes} min ago`;

        }


        const hours =
            Math.floor(
                minutes / 60
            );


        if (hours < 24) {

            return `${hours} hour${
                hours === 1
                    ? ""
                    : "s"
            } ago`;

        }


        const days =
            Math.floor(
                hours / 24
            );


        if (days === 1) {

            return "Yesterday";

        }


        if (days < 7) {

            return `${days} days ago`;

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


    /* ======================================================
       API
       
       GET /api/notifications
    ====================================================== */

    async function fetchNotifications() {

        const response =
            await fetch(
                "/api/notifications",
                {
                    method: "GET",

                    credentials:
                        "include",

                    headers:
                        getHeaders()
                }
            );


        if (
            response.status === 401 ||
            response.status === 403
        ) {

            window.location.href =
                "/login";

            return null;

        }


        if (!response.ok) {

            throw new Error(
                `Notification API failed: ${response.status}`
            );

        }


        return await response.json();

    }


    /* ======================================================
       LOAD
    ====================================================== */

    async function loadNotifications() {

        if (loading) {

            return;

        }


        loading = true;


        showLoading();


        try {

            const payload =
                await fetchNotifications();


            if (!payload) {

                return;

            }


            /*
             * Existing backend response:
             *
             * {
             *     total,
             *     unread,
             *     notifications
             * }
             */

            allNotifications =
                Array.isArray(
                    payload.notifications
                )
                    ? payload.notifications
                    : [];


            updateSummary(
                payload
            );


            renderFilteredNotifications();


        }
        catch (error) {

            console.error(
                "[Notifications] Load failed:",
                error
            );


            showError();

        }
        finally {

            loading = false;

        }

    }


    /* ======================================================
       SUMMARY
    ====================================================== */

    function updateSummary(
        payload
    ) {

        const total =
            Number(
                payload?.total
            ) ||
            allNotifications.length;


        const unread =
            Number(
                payload?.unread
            ) ||
            allNotifications.filter(
                notification =>
                    !notification.is_read
            ).length;


        const read =
            Math.max(
                0,
                total - unread
            );


        const totalElement =
            $("notificationTotal");


        const unreadElement =
            $("notificationUnread");


        const readElement =
            $("notificationRead");


        const allCount =
            $("allFilterCount");


        const unreadCount =
            $("unreadFilterCount");


        const readCount =
            $("readFilterCount");


        if (totalElement) {

            totalElement.textContent =
                total;

        }


        if (unreadElement) {

            unreadElement.textContent =
                unread;

        }


        if (readElement) {

            readElement.textContent =
                read;

        }


        if (allCount) {

            allCount.textContent =
                total;

        }


        if (unreadCount) {

            unreadCount.textContent =
                unread;

        }


        if (readCount) {

            readCount.textContent =
                read;

        }


        const status =
            $("notificationPageStatus");


        if (status) {

            status.textContent =
                unread > 0
                    ? `${unread} unread`
                    : "All caught up";

        }

    }


    /* ======================================================
       FILTER
    ====================================================== */

    function getFilteredNotifications() {

        switch (
            currentFilter
        ) {

            case "unread":

                return allNotifications.filter(
                    notification =>
                        !notification.is_read
                );


            case "read":

                return allNotifications.filter(
                    notification =>
                        notification.is_read
                );


            default:

                return allNotifications;

        }

    }


    function initializeFilters() {

        document
            .querySelectorAll(
                ".notification-filter"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            currentFilter =
                                this.dataset.filter ||
                                "all";


                            document
                                .querySelectorAll(
                                    ".notification-filter"
                                )
                                .forEach(
                                    item =>
                                        item.classList.toggle(
                                            "active",
                                            item === this
                                        )
                                );


                            renderFilteredNotifications();

                        }
                    );

                }
            );

    }


    /* ======================================================
       RENDER
    ====================================================== */

    function renderFilteredNotifications() {

        const list =
            $("notificationsPageList");


        if (!list) {

            return;

        }


        const notifications =
            getFilteredNotifications();


        hideStates();


        if (
            notifications.length === 0
        ) {

            showEmpty();

            return;

        }


        list.innerHTML =
            notifications
                .map(
                    notification =>
                        createNotificationHTML(
                            notification
                        )
                )
                .join("");


        bindNotificationActions();

    }


    /* ======================================================
       NOTIFICATION HTML
    ====================================================== */

    function createNotificationHTML(
        notification
    ) {

        const id =
            escapeHTML(
                notification.id
            );


        const type =
            getTypeClass(
                notification.type
            );


        const icon =
            getNotificationIcon(
                notification.type
            );


        const unread =
            !notification.is_read;


        return `

            <article
                class="
                    notification-page-item
                    ${unread ? "unread" : ""}
                "
                data-notification-id="${id}"
            >


                <div
                    class="
                        notification-page-icon
                        ${type}
                    "
                >

                    <i
                        class="bi ${icon}"
                    ></i>

                </div>



                <div
                    class="notification-page-content"
                >


                    <div
                        class="notification-page-top"
                    >

                        <h3
                            class="notification-page-title"
                        >
                            ${escapeHTML(
                                notification.title ||
                                "Notification"
                            )}
                        </h3>


                        <span
                            class="notification-page-time"
                        >
                            ${escapeHTML(
                                formatNotificationTime(
                                    notification.created_at
                                )
                            )}
                        </span>

                    </div>


                    <p
                        class="notification-page-message"
                    >
                        ${escapeHTML(
                            notification.message ||
                            ""
                        )}
                    </p>


                    <div
                        class="notification-page-actions"
                    >


                        ${
                            unread
                                ? `
                                    <button
                                        type="button"
                                        class="
                                            notification-action-button
                                            mark-read
                                        "
                                        data-id="${id}"
                                    >

                                        <i
                                            class="bi bi-check2"
                                        ></i>

                                        Mark as read

                                    </button>
                                  `
                                : `
                                    <span
                                        class="
                                            notification-action-button
                                        "
                                    >

                                        <i
                                            class="bi bi-check2-circle"
                                        ></i>

                                        Read

                                    </span>
                                  `
                        }


                        <button
                            type="button"
                            class="
                                notification-action-button
                                delete
                            "
                            data-id="${id}"
                        >

                            <i
                                class="bi bi-trash3"
                            ></i>

                            Delete

                        </button>


                    </div>


                </div>


            </article>

        `;

    }


    /* ======================================================
       ACTION EVENTS
    ====================================================== */

    function bindNotificationActions() {

        document
            .querySelectorAll(
                ".notification-action-button.mark-read"
            )
            .forEach(
                button => {

                    button.addEventListener(
                        "click",
                        function () {

                            markNotificationRead(
                                this.dataset.id
                            );

                        }
                    );

                }
            );


        document
            .querySelectorAll(
                ".notification-action-button.delete"
            )
            .forEach(
                button => {

                    button.addEventListener(
                        "click",
                        function () {

                            deleteNotification(
                                this.dataset.id
                            );

                        }
                    );

                }
            );

    }


    /* ======================================================
       MARK ONE READ
       
       PUT /api/notifications/{id}/read
    ====================================================== */

    async function markNotificationRead(
        id
    ) {

        if (!id) {

            return;

        }


        try {

            const response =
                await fetch(
                    `/api/notifications/${encodeURIComponent(id)}/read`,
                    {
                        method: "PUT",

                        credentials:
                            "include",

                        headers:
                            getHeaders()
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Mark read failed: ${response.status}`
                );

            }


            const notification =
                allNotifications.find(
                    item =>
                        String(item.id) ===
                        String(id)
                );


            if (notification) {

                notification.is_read =
                    true;

            }


            updateLocalSummary();

            renderFilteredNotifications();


            /*
             * Keep topbar/sidebar badge synchronized.
             */

            refreshDashboardNotifications();

        }
        catch (error) {

            console.error(
                "[Notifications] Mark read failed:",
                error
            );

        }

    }


    /* ======================================================
       MARK ALL READ
       
       PUT /api/notifications/read-all
    ====================================================== */

    async function markAllNotificationsRead() {

        const button =
            $("markAllNotificationsPage");


        if (button) {

            button.disabled =
                true;

        }


        try {

            const response =
                await fetch(
                    "/api/notifications/read-all",
                    {
                        method: "PUT",

                        credentials:
                            "include",

                        headers:
                            getHeaders()
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Mark all failed: ${response.status}`
                );

            }


            allNotifications =
                allNotifications.map(
                    notification => ({
                        ...notification,
                        is_read: true
                    })
                );


            updateLocalSummary();

            renderFilteredNotifications();


            refreshDashboardNotifications();

        }
        catch (error) {

            console.error(
                "[Notifications] Mark all failed:",
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
       DELETE
       
       DELETE /api/notifications/{id}
    ====================================================== */

    async function deleteNotification(
        id
    ) {

        if (!id) {

            return;

        }


        try {

            const response =
                await fetch(
                    `/api/notifications/${encodeURIComponent(id)}`,
                    {
                        method: "DELETE",

                        credentials:
                            "include",

                        headers:
                            getHeaders()
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Delete failed: ${response.status}`
                );

            }


            allNotifications =
                allNotifications.filter(
                    notification =>
                        String(notification.id) !==
                        String(id)
                );


            updateLocalSummary();

            renderFilteredNotifications();


            refreshDashboardNotifications();

        }
        catch (error) {

            console.error(
                "[Notifications] Delete failed:",
                error
            );

        }

    }


    /* ======================================================
       LOCAL SUMMARY
    ====================================================== */

    function updateLocalSummary() {

        updateSummary(
            {
                total:
                    allNotifications.length,

                unread:
                    allNotifications.filter(
                        notification =>
                            !notification.is_read
                    ).length
            }
        );

    }


    /* ======================================================
       REFRESH TOPBAR / SIDEBAR
    ====================================================== */

    function refreshDashboardNotifications() {

        /*
         * dashboard_topbar.js exposes its notification
         * refresh indirectly through the existing page.
         *
         * If available, refresh the sidebar directly.
         */

        if (
            typeof window
                .refreshDashboardSidebar ===
            "function"
        ) {

            window.refreshDashboardSidebar();

        }

    }


    /* ======================================================
       STATES
    ====================================================== */

    function hideStates() {

        $("notificationsLoading")
            ?.classList.add(
                "hidden"
            );


        $("notificationsEmpty")
            ?.classList.add(
                "hidden"
            );


        $("notificationsError")
            ?.classList.add(
                "hidden"
            );


        $("notificationsPageList")
            ?.classList.remove(
                "hidden"
            );

    }


    function showLoading() {

        $("notificationsLoading")
            ?.classList.remove(
                "hidden"
            );


        $("notificationsEmpty")
            ?.classList.add(
                "hidden"
            );


        $("notificationsError")
            ?.classList.add(
                "hidden"
            );


        const list =
            $("notificationsPageList");


        if (list) {

            list.innerHTML =
                "";

        }

    }


    function showEmpty() {

        $("notificationsLoading")
            ?.classList.add(
                "hidden"
            );


        $("notificationsEmpty")
            ?.classList.remove(
                "hidden"
            );


        $("notificationsError")
            ?.classList.add(
                "hidden"
            );

    }


    function showError() {

        $("notificationsLoading")
            ?.classList.add(
                "hidden"
            );


        $("notificationsEmpty")
            ?.classList.add(
                "hidden"
            );


        $("notificationsError")
            ?.classList.remove(
                "hidden"
            );

    }


    /* ======================================================
       BUTTONS
    ====================================================== */

    function initializeButtons() {

        $("refreshNotificationsPage")
            ?.addEventListener(
                "click",
                loadNotifications
            );


        $("markAllNotificationsPage")
            ?.addEventListener(
                "click",
                markAllNotificationsRead
            );


        $("retryNotificationsPage")
            ?.addEventListener(
                "click",
                loadNotifications
            );

    }


    /* ======================================================
       START
    ====================================================== */

    function initialize() {

        console.log(
            "[AI Audit] Notifications page initialized."
        );


        initializeFilters();

        initializeButtons();

        loadNotifications();

    }


    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            {
                once:true
            }
        );

    }
    else {

        initialize();

    }


})();