/*=========================================================
    AI WEBSITE AUDIT TOOL
    FORGOT PASSWORD
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    /*=====================================================
        ELEMENTS
    =====================================================*/

    const form = document.getElementById("forgotPasswordForm");

    if (!form) return;

    const email = document.getElementById("email");

    const emailError = document.getElementById("emailError");

    const submitBtn = document.getElementById("submitBtn");

    const loader = document.getElementById("btnLoader");

    const btnText = submitBtn.querySelector(".btn-text");

    const successBox = document.getElementById("successMessage");

    /*=====================================================
        EMAIL VALIDATION
    =====================================================*/

    function validateEmail(value) {

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

    }

    /*=====================================================
        CLEAR ERRORS
    =====================================================*/

    function clearErrors() {

        emailError.textContent = "";

        successBox.classList.add("d-none");

        email.parentElement.style.borderColor = "";

        email.parentElement.style.boxShadow = "";

    }

    /*=====================================================
        SHOW ERROR
    =====================================================*/

    function showError(message) {

        emailError.textContent = message;

        email.parentElement.style.borderColor = "#EF4444";

        email.parentElement.style.boxShadow =
            "0 0 0 4px rgba(239,68,68,.10)";

    }

    /*=====================================================
        SHOW SUCCESS
    =====================================================*/

    function showSuccess(message) {

        successBox.querySelector("span").textContent = message;

        successBox.classList.remove("d-none");

    }

    /*=====================================================
        BUTTON LOADING
    =====================================================*/

    function startLoading() {

        submitBtn.disabled = true;

        submitBtn.classList.add("loading");

        btnText.classList.add("d-none");

        loader.classList.remove("d-none");

    }

    function stopLoading() {

        submitBtn.disabled = false;

        submitBtn.classList.remove("loading");

        btnText.classList.remove("d-none");

        loader.classList.add("d-none");

    }

    /*=====================================================
        LIVE VALIDATION
    =====================================================*/

    email.addEventListener("input", () => {

        emailError.textContent = "";

        email.parentElement.style.borderColor = "";

        email.parentElement.style.boxShadow = "";

    });

    /*=====================================================
        SUBMIT
    =====================================================*/

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        clearErrors();

        const emailValue = email.value.trim().toLowerCase();

        if (emailValue === "") {

            showError("Email address is required.");

            return;

        }

        if (!validateEmail(emailValue)) {

            showError("Please enter a valid email address.");

            return;

        }

        startLoading();

        try {

            const response = await fetch("/api/password/forgot", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    email: emailValue

                })

            });

            const data = await response.json();

            stopLoading();

            if (!response.ok) {

                showError(

                    data.detail ||

                    "Unable to process your request."

                );

                return;

            }

            showSuccess(

                data.message ||

                "Password reset link sent successfully."

            );

            submitBtn.innerHTML = `

                <i class="bi bi-check-circle-fill"></i>

                Email Sent

            `;

            submitBtn.style.background = "#16A34A";

            setTimeout(() => {

                window.location.href = "/login";

            }, 3000);

        }

        catch (error) {

            console.error(error);

            stopLoading();

            showError(

                "Unable to connect to the server."

            );

        }

    });

});