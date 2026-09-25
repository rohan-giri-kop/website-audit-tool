/* ==========================================================
   AI Website Audit Tool
   Premium Login Page
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================
       ELEMENTS
    ========================================== */

    const form = document.getElementById("loginForm");

    if (!form) return;

    const email = document.getElementById("loginEmail");
    const password = document.getElementById("loginPassword");

    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");

    const rememberMe = document.getElementById("rememberMe");

    const submitBtn = document.getElementById("loginBtn");

    /* ==========================================
       PASSWORD TOGGLE
    ========================================== */

    const passwordInput = document.getElementById("loginPassword");
    const togglePassword = document.querySelector(".toggle-password");

    if (passwordInput && togglePassword) {

        togglePassword.addEventListener("click", function () {

            const icon = this.querySelector("i");

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                icon.classList.remove("bi-eye-fill");
                icon.classList.add("bi-eye-slash-fill");

            } else {

                passwordInput.type = "password";

                icon.classList.remove("bi-eye-slash-fill");
                icon.classList.add("bi-eye-fill");

            }

        });

    }


    /* ==========================================
       HELPERS
    ========================================== */

    function clearErrors() {

        document.querySelectorAll(".error-text")
            .forEach(el => {

                el.textContent = "";
                el.classList.remove("show");

            });

        document.querySelectorAll(".input-box")
            .forEach(box => {

                box.classList.remove("input-error");
                box.classList.remove("input-success");

            });

    }

    function showError(input, errorElement, message) {

        input.parentElement.classList.add("input-error");

        errorElement.textContent = message;

        errorElement.classList.add("show");

    }

    function showSuccess(input) {

        input.parentElement.classList.remove("input-error");

        input.parentElement.classList.add("input-success");

    }

    function validateEmail(value) {

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

    }

    /* ==========================================
       SUBMIT
    ========================================== */

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        clearErrors();

        let valid = true;

        /* Email */

        if (!email.value.trim()) {

            showError(
                email,
                emailError,
                "Email is required."
            );

            valid = false;

        } else if (!validateEmail(email.value.trim())) {

            showError(
                email,
                emailError,
                "Enter a valid email address."
            );

            valid = false;

        } else {

            showSuccess(email);

        }

        /* Password */

        if (!password.value.trim()) {

            showError(
                password,
                passwordError,
                "Password is required."
            );

            valid = false;

        } else {

            showSuccess(password);

        }

        if (!valid) return;

        /* Loading */

        submitBtn.disabled = true;

        submitBtn.innerHTML = `

            <span class="spinner-border spinner-border-sm"></span>

            Signing In...

        `;

        try {

            const response = await fetch("/api/auth/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    email: email.value.trim().toLowerCase(),

                    password: password.value

                })

            });

            const data = await response.json();

            // Login failed
            if (!response.ok) {

                passwordError.textContent =
                    data.detail || "Incorrect email or password.";

                passwordError.classList.add("show");

                password.parentElement.classList.add("input-error");

                submitBtn.disabled = false;

                submitBtn.innerHTML = `
                    <i class="bi bi-box-arrow-in-right"></i>
                    <span>Sign In</span>
                `;

                return;

            }

            /* ==========================================================
            SAVE JWT AUTHENTICATION TOKEN
            ========================================================== */

            if (!data.access_token) {

                throw new Error(
                    "Login successful but access token was not returned."
                );

            }


            /* ==========================================================
            REMOVE OLD TOKENS
            ========================================================== */

            localStorage.removeItem("access_token");
            localStorage.removeItem("token");
            localStorage.removeItem("auth_token");

            sessionStorage.removeItem("access_token");
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("auth_token");


            /* ==========================================================
            SAVE NEW TOKEN
            ========================================================== */

            if (rememberMe.checked) {

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

            } else {

                sessionStorage.setItem(
                    "access_token",
                    data.access_token
                );

            }
            
            // Success UI
            submitBtn.innerHTML = `
                <i class="bi bi-check-circle-fill"></i>
                <span>Login Successful</span>
            `;

            submitBtn.style.background = "#16A34A";

            setTimeout(() => {

                window.location.href = "/dashboard";

            }, 1000);

        }
        catch (error) {

            console.error(error);

            passwordError.textContent = "Unable to connect to server.";

            passwordError.classList.add("show");

            submitBtn.disabled = false;

            submitBtn.innerHTML = `
                <i class="bi bi-box-arrow-in-right"></i>
                <span>Sign In</span>
            `;

        }
    

    }); // End form.addEventListener

});


window.onload = function () {

    const passwordInput = document.getElementById("loginPassword");
    const togglePassword = document.querySelector(".toggle-password");

    if (!passwordInput || !togglePassword) return;

    togglePassword.onclick = function () {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";
            this.querySelector("i").className = "bi bi-eye-slash-fill";

        } else {

            passwordInput.type = "password";
            this.querySelector("i").className = "bi bi-eye-fill";

        }

    };

};