/* ==========================================================
   AI WEBSITE AUDIT TOOL
   LOGIN JAVASCRIPT
   ----------------------------------------------------------
   Responsibilities:
   - Login validation
   - Password visibility toggle
   - POST /api/auth/login
   - Save JWT token consistently
   - Verify JWT using /api/auth/me
   - Redirect to dashboard
   - Clear old/invalid tokens
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    "use strict";


    /* ==========================================================
       ELEMENTS
    ========================================================== */

    const form =
        document.getElementById("loginForm");

    if (!form) {
        return;
    }


    const email =
        document.getElementById("loginEmail");

    const password =
        document.getElementById("loginPassword");

    const emailError =
        document.getElementById("emailError");

    const passwordError =
        document.getElementById("passwordError");

    const rememberMe =
        document.getElementById("rememberMe");

    const submitBtn =
        document.getElementById("loginBtn");


    /* ==========================================================
       PASSWORD TOGGLE
    ========================================================== */

    const togglePassword =
        document.querySelector(".toggle-password");


    if (
        password &&
        togglePassword
    ) {

        togglePassword.addEventListener(
            "click",
            function () {

                const icon =
                    this.querySelector("i");


                if (
                    password.type === "password"
                ) {

                    password.type = "text";


                    if (icon) {

                        icon.classList.remove(
                            "bi-eye-fill"
                        );

                        icon.classList.add(
                            "bi-eye-slash-fill"
                        );

                    }

                }

                else {

                    password.type = "password";


                    if (icon) {

                        icon.classList.remove(
                            "bi-eye-slash-fill"
                        );

                        icon.classList.add(
                            "bi-eye-fill"
                        );

                    }

                }

            }
        );

    }


    /* ==========================================================
       TOKEN STORAGE KEYS
       ----------------------------------------------------------
       We use ONLY access_token as the main JWT key.
    ========================================================== */

    const TOKEN_KEY =
        "access_token";


    const OLD_TOKEN_KEYS = [
        "token",
        "auth_token",
        "audit_token",
        "accessToken"
    ];


    /* ==========================================================
       CLEAR OLD AUTHENTICATION
    ========================================================== */

    function clearOldAuthentication() {

        /* Main token */

        localStorage.removeItem(
            TOKEN_KEY
        );

        sessionStorage.removeItem(
            TOKEN_KEY
        );


        /* Old token names */

        OLD_TOKEN_KEYS.forEach(
            (key) => {

                localStorage.removeItem(
                    key
                );

                sessionStorage.removeItem(
                    key
                );

            }
        );

    }


    /* ==========================================================
       SAVE AUTHENTICATION TOKEN
    ========================================================== */

    function saveAuthenticationToken(
        token
    ) {

        if (!token) {

            throw new Error(
                "Authentication token was not returned by the server."
            );

        }


        /* Remove all previous tokens */

        clearOldAuthentication();


        /* Save new token */

        if (
            rememberMe &&
            rememberMe.checked
        ) {

            localStorage.setItem(
                TOKEN_KEY,
                token
            );

        }

        else {

            sessionStorage.setItem(
                TOKEN_KEY,
                token
            );

        }


        console.log(
            "[Login] JWT token saved."
        );

    }


    /* ==========================================================
       GET CURRENT TOKEN
    ========================================================== */

    function getAuthenticationToken() {

        return (
            localStorage.getItem(
                TOKEN_KEY
            ) ||
            sessionStorage.getItem(
                TOKEN_KEY
            ) ||
            ""
        );

    }


    /* ==========================================================
       AUTH HEADERS
    ========================================================== */

    function getAuthHeaders() {

        const token =
            getAuthenticationToken();


        if (!token) {

            return {
                "Accept":
                    "application/json"
            };

        }


        return {

            "Accept":
                "application/json",

            "Authorization":
                `Bearer ${token}`

        };

    }


    /* ==========================================================
       CLEAR FORM ERRORS
    ========================================================== */

    function clearErrors() {

        document
            .querySelectorAll(
                ".error-text"
            )
            .forEach(
                (element) => {

                    element.textContent =
                        "";

                    element.classList.remove(
                        "show"
                    );

                }
            );


        document
            .querySelectorAll(
                ".input-box"
            )
            .forEach(
                (box) => {

                    box.classList.remove(
                        "input-error"
                    );

                    box.classList.remove(
                        "input-success"
                    );

                }
            );

    }


    /* ==========================================================
       SHOW ERROR
    ========================================================== */

    function showError(
        input,
        errorElement,
        message
    ) {

        if (input) {

            input.parentElement.classList.add(
                "input-error"
            );

        }


        if (errorElement) {

            errorElement.textContent =
                message;

            errorElement.classList.add(
                "show"
            );

        }

    }


    /* ==========================================================
       SHOW SUCCESS
    ========================================================== */

    function showSuccess(
        input
    ) {

        if (!input) {
            return;
        }


        input.parentElement.classList.remove(
            "input-error"
        );

        input.parentElement.classList.add(
            "input-success"
        );

    }


    /* ==========================================================
       EMAIL VALIDATION
    ========================================================== */

    function validateEmail(
        value
    ) {

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            .test(value);

    }


    /* ==========================================================
       RESET LOGIN BUTTON
    ========================================================== */

    function resetLoginButton() {

        if (!submitBtn) {
            return;
        }


        submitBtn.disabled =
            false;


        submitBtn.style.background =
            "";


        submitBtn.innerHTML = `
            <i class="bi bi-box-arrow-in-right"></i>
            <span>Sign In</span>
        `;

    }


    /* ==========================================================
       LOGIN
    ========================================================== */

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            clearErrors();


            let valid = true;


            /* --------------------------------------------------
               EMAIL
            -------------------------------------------------- */

            const emailValue =
                email.value
                    .trim()
                    .toLowerCase();


            if (!emailValue) {

                showError(
                    email,
                    emailError,
                    "Email is required."
                );

                valid = false;

            }

            else if (
                !validateEmail(
                    emailValue
                )
            ) {

                showError(
                    email,
                    emailError,
                    "Enter a valid email address."
                );

                valid = false;

            }

            else {

                showSuccess(
                    email
                );

            }


            /* --------------------------------------------------
               PASSWORD
            -------------------------------------------------- */

            const passwordValue =
                password.value;


            if (!passwordValue) {

                showError(
                    password,
                    passwordError,
                    "Password is required."
                );

                valid = false;

            }

            else {

                showSuccess(
                    password
                );

            }


            if (!valid) {
                return;
            }


            /* --------------------------------------------------
               LOADING STATE
            -------------------------------------------------- */

            submitBtn.disabled =
                true;


            submitBtn.innerHTML = `
                <span
                    class="spinner-border spinner-border-sm"
                    role="status"
                    aria-hidden="true"
                ></span>
                <span>Signing In...</span>
            `;


            try {

                /* ==================================================
                   IMPORTANT
                   --------------------------------------------------
                   Remove old/expired tokens before login.
                ================================================== */

                clearOldAuthentication();


                /* ==================================================
                   LOGIN REQUEST
                ================================================== */

                console.log(
                    "[Login] Sending login request..."
                );


                const response =
                    await fetch(
                        "/api/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json",

                                "Accept":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    {
                                        email:
                                            emailValue,

                                        password:
                                            passwordValue
                                    }
                                )
                        }
                    );


                /* ==================================================
                   READ RESPONSE
                ================================================== */

                let data = null;


                try {

                    data =
                        await response.json();

                }

                catch (jsonError) {

                    console.error(
                        "[Login] Invalid JSON response:",
                        jsonError
                    );

                    throw new Error(
                        "Invalid server response."
                    );

                }


                console.log(
                    "[Login] HTTP status:",
                    response.status
                );


                /* ==================================================
                   LOGIN ERROR
                ================================================== */

                if (!response.ok) {

                    const message =
                        data?.detail ||
                        data?.message ||
                        "Incorrect email or password.";


                    showError(
                        password,
                        passwordError,
                        message
                    );


                    resetLoginButton();


                    return;

                }


                /* ==================================================
                   CHECK ACCESS TOKEN
                ================================================== */

                const accessToken =
                    data?.access_token;


                if (!accessToken) {

                    console.error(
                        "[Login] Server response:",
                        data
                    );


                    throw new Error(
                        "Login successful, but the server did not return an access token."
                    );

                }


                console.log(
                    "[Login] Access token received."
                );


                /* ==================================================
                   SAVE TOKEN
                ================================================== */

                saveAuthenticationToken(
                    accessToken
                );


                /* ==================================================
                   VERIFY TOKEN
                   --------------------------------------------------
                   This is important.

                   The backend must accept the exact JWT that
                   was returned from /api/auth/login.
                ================================================== */

                console.log(
                    "[Login] Verifying authentication..."
                );


                const verifyResponse =
                    await fetch(
                        "/api/auth/me",
                        {
                            method: "GET",

                            headers:
                                getAuthHeaders()
                        }
                    );


                let verifyData =
                    null;


                try {

                    verifyData =
                        await verifyResponse.json();

                }

                catch (verifyJsonError) {

                    console.error(
                        "[Login] Could not read /api/auth/me response:",
                        verifyJsonError
                    );

                }


                console.log(
                    "[Login] /api/auth/me status:",
                    verifyResponse.status
                );


                /* ==================================================
                   TOKEN INVALID
                ================================================== */

                if (
                    !verifyResponse.ok
                ) {

                    console.error(
                        "[Login] Token verification failed:",
                        verifyData
                    );


                    /*
                     * Remove the token because the backend
                     * rejected it.
                     */

                    clearOldAuthentication();


                    throw new Error(
                        verifyData?.detail ||
                        "Authentication token was rejected by the server."
                    );

                }


                /* ==================================================
                   TOKEN VERIFIED
                ================================================== */

                console.log(
                    "[Login] Authentication verified successfully."
                );


                console.log(
                    "[Login] Current user:",
                    verifyData
                );


                /* ==================================================
                   SUCCESS UI
                ================================================== */

                submitBtn.innerHTML = `
                    <i class="bi bi-check-circle-fill"></i>
                    <span>Login Successful</span>
                `;


                submitBtn.style.background =
                    "#16A34A";


                /* ==================================================
                   REDIRECT
                ================================================== */

                setTimeout(
                    () => {

                        window.location.href =
                            "/dashboard";

                    },
                    700
                );

            }

            catch (error) {

                console.error(
                    "[Login] Error:",
                    error
                );


                /*
                 * If authentication failed,
                 * do not leave an invalid token.
                 */

                clearOldAuthentication();


                let message =
                    "Unable to connect to server.";


                if (
                    error &&
                    error.message
                ) {

                    message =
                        error.message;

                }


                showError(
                    password,
                    passwordError,
                    message
                );


                resetLoginButton();

            }

        }
    );

});