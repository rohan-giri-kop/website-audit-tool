/*=========================================================
    AI WEBSITE AUDIT TOOL
    RESET PASSWORD
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    /*=====================================================
        ELEMENTS
    =====================================================*/

    const form = document.getElementById("resetPasswordForm");

    if (!form) return;

    const password = document.getElementById("newPassword");

    const confirmPassword = document.getElementById("confirmPassword");

    const togglePassword = document.getElementById("togglePassword");

    const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

    const strengthBar = document.getElementById("strengthBar");

    const strengthText = document.getElementById("strengthText");

    const passwordError = document.getElementById("passwordError");

    const confirmPasswordError = document.getElementById("confirmPasswordError");

    const passwordMatch = document.getElementById("passwordMatch");

    /*=====================================================
        PASSWORD RULES
    =====================================================*/

    const ruleLength = document.getElementById("ruleLength");

    const ruleUpper = document.getElementById("ruleUpper");

    const ruleLower = document.getElementById("ruleLower");

    const ruleNumber = document.getElementById("ruleNumber");

    const ruleSpecial = document.getElementById("ruleSpecial");

    /*=====================================================
        SHOW / HIDE PASSWORD
    =====================================================*/

    function toggleVisibility(input, button) {

        const icon = button.querySelector("i");

        if (input.type === "password") {

            input.type = "text";

            icon.classList.remove("bi-eye");

            icon.classList.add("bi-eye-slash");

        } else {

            input.type = "password";

            icon.classList.remove("bi-eye-slash");

            icon.classList.add("bi-eye");

        }

    }

    togglePassword.addEventListener("click", () => {

        toggleVisibility(password, togglePassword);

    });

    toggleConfirmPassword.addEventListener("click", () => {

        toggleVisibility(confirmPassword, toggleConfirmPassword);

    });

    /*=====================================================
        PASSWORD STRENGTH
    =====================================================*/

    function updateStrengthMeter(score) {

        const colours = [

            "#EF4444",

            "#F97316",

            "#FACC15",

            "#22C55E",

            "#16A34A"

        ];

        const labels = [

            "Very Weak",

            "Weak",

            "Medium",

            "Strong",

            "Very Strong"

        ];

        strengthBar.style.width = `${score * 20}%`;

        strengthBar.style.background = colours[score - 1] || colours[0];

        strengthText.textContent = labels[score - 1] || "Very Weak";

        strengthText.style.color = colours[score - 1] || colours[0];

    }

    /*=====================================================
        PASSWORD RULE CHECK
    =====================================================*/

    function setRule(rule, valid) {

        const icon = rule.querySelector("i");

        if (valid) {

            rule.classList.add("valid");

            icon.classList.remove("bi-x-circle");

            icon.classList.add("bi-check-circle-fill");

        } else {

            rule.classList.remove("valid");

            icon.classList.remove("bi-check-circle-fill");

            icon.classList.add("bi-x-circle");

        }

    }

    function checkPasswordRules(value) {

        const length = value.length >= 8;

        const upper = /[A-Z]/.test(value);

        const lower = /[a-z]/.test(value);

        const number = /\d/.test(value);

        const special = /[!@#$%^&*(),.?":{}|<>]/.test(value);

        setRule(ruleLength, length);

        setRule(ruleUpper, upper);

        setRule(ruleLower, lower);

        setRule(ruleNumber, number);

        setRule(ruleSpecial, special);

        let score = 0;

        if (length) score++;

        if (upper) score++;

        if (lower) score++;

        if (number) score++;

        if (special) score++;

        updateStrengthMeter(score);

    }

    /*=====================================================
        LIVE PASSWORD STRENGTH
    =====================================================*/

    password.addEventListener("input", () => {

        passwordError.textContent = "";

        checkPasswordRules(password.value);

    });

/*=====================================================
    CONFIRM PASSWORD VALIDATION
=====================================================*/

function validateConfirmPassword() {

    confirmPasswordError.textContent = "";

    passwordMatch.classList.add("d-none");

    if (confirmPassword.value.length === 0) {

        return false;

    }

    if (password.value !== confirmPassword.value) {

        confirmPasswordError.textContent =
            "Passwords do not match.";

        return false;

    }

    passwordMatch.classList.remove("d-none");

    return true;

}

/*=====================================================
    LIVE CONFIRM PASSWORD
=====================================================*/

confirmPassword.addEventListener("input", () => {

    validateConfirmPassword();

});

password.addEventListener("input", () => {

    if (confirmPassword.value.length > 0) {

        validateConfirmPassword();

    }

});

/*=====================================================
    VALIDATE PASSWORD
=====================================================*/

function validatePassword() {

    passwordError.textContent = "";

    const value = password.value;

    if (value.length < 8) {

        passwordError.textContent =
            "Password must contain at least 8 characters.";

        return false;

    }

    if (!/[A-Z]/.test(value)) {

        passwordError.textContent =
            "Password must contain an uppercase letter.";

        return false;

    }

    if (!/[a-z]/.test(value)) {

        passwordError.textContent =
            "Password must contain a lowercase letter.";

        return false;

    }

    if (!/\d/.test(value)) {

        passwordError.textContent =
            "Password must contain a number.";

        return false;

    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) {

        passwordError.textContent =
            "Password must contain a special character.";

        return false;

    }

    return true;

}

/*=====================================================
    SUCCESS MESSAGE
=====================================================*/

const successMessage = document.getElementById(
    "successMessage"
);

/*=====================================================
    SUBMIT BUTTON
=====================================================*/

const submitBtn = document.getElementById(
    "submitBtn"
);

const btnLoader = document.getElementById(
    "btnLoader"
);

const btnText = submitBtn.querySelector(
    ".btn-text"
);

/*=====================================================
    BUTTON LOADING
=====================================================*/

function startLoading() {

    submitBtn.disabled = true;

    submitBtn.classList.add("loading");

    btnText.classList.add("d-none");

    btnLoader.classList.remove("d-none");

}

function stopLoading() {

    submitBtn.disabled = false;

    submitBtn.classList.remove("loading");

    btnText.classList.remove("d-none");

    btnLoader.classList.add("d-none");

}

/*=====================================================
    CLEAR ERRORS
=====================================================*/

function clearErrors() {

    passwordError.textContent = "";

    confirmPasswordError.textContent = "";

    successMessage.classList.add("d-none");

}

/*=====================================================
    FORM VALIDATION
=====================================================*/

function validateForm() {

    clearErrors();

    const passwordValid = validatePassword();

    const confirmValid = validateConfirmPassword();

    return passwordValid && confirmValid;

}

/*=====================================================
    FORM SUBMIT
    (Continues in Part 3C)
=====================================================*/

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    if (!validateForm()) {

        return;

    }

    startLoading();

    /*=====================================================
        READ TOKEN FROM URL
    =====================================================*/

    const params = new URLSearchParams(window.location.search);

    const token = params.get("token");

    if (!token) {

        stopLoading();

        submitBtn.disabled = true;

        passwordError.textContent =
            "Invalid or missing password reset link.";

        return;

    }

    /*=====================================================
        CALL RESET PASSWORD API
    =====================================================*/

    try {

        const response = await fetch("/api/password/reset", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                token: token,

                password: password.value.trim(),

                confirm_password: confirmPassword.value.trim()

            })

        });

        const data = await response.json();

        stopLoading();

        /*=============================================
            FAILED
        =============================================*/

        if (!response.ok) {

            if (data.detail) {

                passwordError.textContent = data.detail;

            } else {

                passwordError.textContent =
                    "Unable to reset password.";

            }

            return;

        }

        /*=============================================
            SUCCESS
        =============================================*/

        successMessage.classList.remove("d-none");

        successMessage.querySelector("span").textContent =
            data.message ||
            "Password updated successfully.";

        submitBtn.innerHTML = `

            <i class="bi bi-check-circle-fill"></i>

            Password Updated

        `;

        submitBtn.style.background = "#16A34A";

        submitBtn.disabled = true;

        /*=============================================
            REDIRECT
        =============================================*/

        setTimeout(() => {

            window.location.href = "/login";

        }, 2500);

    }

    /*=====================================================
        NETWORK ERROR
    =====================================================*/

    catch (error) {

        console.error(error);

        stopLoading();

        passwordError.textContent =
            "Unable to connect to the server.";

    }

});

/*=====================================================
    END DOM CONTENT LOADED
=====================================================*/

});