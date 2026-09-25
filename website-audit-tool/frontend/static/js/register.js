/* ==========================================================
   AI Website Audit Tool
   Premium Register Page JS
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("registerForm");

    if (!form) return;

    const name = document.getElementById("registerName");
    const email = document.getElementById("registerEmail");
    const password = document.getElementById("registerPassword");
    const confirmPassword = document.getElementById("confirmPassword");
    const terms = document.getElementById("terms");

    const strengthBar = document.querySelector(".strength-bar span");
    const strengthText = document.querySelector(".password-strength small");

    const submitBtn = document.querySelector(".register-btn");


    const nameError = document.getElementById("nameError");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const confirmError = document.getElementById("confirmError");
    const termsError = document.getElementById("termsError");


    function updateRule(id, valid){

        const rule = document.getElementById(id);

        const icon = rule.querySelector("i");

        if(valid){

            rule.classList.add("valid");

            icon.className="bi bi-check-circle-fill";

        }else{

            rule.classList.remove("valid");

            icon.className="bi bi-x-circle";

        }

    }

    /* ===========================================
    SHOW / HIDE PASSWORD
    =========================================== */

    function initializePasswordToggle() {

        document.querySelectorAll(".toggle-password").forEach(button => {

            button.onclick = function () {

                const input = button.closest(".input-box").querySelector("input");
                const icon = button.querySelector("i");

                if (!input) return;

                if (input.type === "password") {

                    input.type = "text";

                    icon.className = "bi bi-eye-slash-fill";

                } else {

                    input.type = "password";

                    icon.className = "bi bi-eye-fill";

                }

            };

        });


    }

    initializePasswordToggle();

    /* ==========================================
       Password Strength
    ========================================== */

    password.addEventListener("input", () => {

        const pwd=password.value;

        const length = pwd.length>=8;
        const upper = /[A-Z]/.test(pwd);
        const lower = /[a-z]/.test(pwd);
        const number = /[0-9]/.test(pwd);
        const special = /[^A-Za-z0-9]/.test(pwd);

        updateRule("rule-length",length);
        updateRule("rule-upper",upper);
        updateRule("rule-lower",lower);
        updateRule("rule-number",number);
        updateRule("rule-special",special);

        let score=0;

        [length,upper,lower,number,special].forEach(v=>{
            if(v) score++;
        });

        const fill=document.getElementById("strengthFill");
        const text=document.getElementById("strengthText");

        switch(score){

        case 0:
        case 1:

        fill.style.width="20%";
        fill.style.background="#EF4444";
        text.innerText="Weak Password";
        break;

        case 2:

        fill.style.width="40%";
        fill.style.background="#F97316";
        text.innerText="Fair Password";
        break;

        case 3:

        fill.style.width="60%";
        fill.style.background="#F59E0B";
        text.innerText="Good Password";
        break;

        case 4:

        fill.style.width="80%";
        fill.style.background="#2563EB";
        text.innerText="Strong Password";
        break;

        case 5:

        fill.style.width="100%";
        fill.style.background="#16A34A";
        text.innerText="Very Strong Password";
        break;

        }

    });

    /* ==========================================
       Confirm Password
    ========================================== */

    confirmPassword.addEventListener("input", () => {

        if (confirmPassword.value === "") {

            confirmPassword.style.borderColor = "";

            return;

        }

        if (password.value === confirmPassword.value) {

            confirmPassword.style.borderColor = "#22c55e";

        } else {

            confirmPassword.style.borderColor = "#ef4444";

        }

    });

    /* ==========================================
       Email Validation
    ========================================== */

    function validateEmail(emailValue) {

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue);

    }

    /* ==========================================
       Submit Form
    ========================================== */

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        if (name.value.trim() === "") {

        showError(name, nameError, "Please enter your full name.");

        return;
        }

        if (!validateEmail(email.value)) {

            showError(
                email,
                emailError,
                "Please enter a valid email address."
            );

            return;
        }

        if (password.value.length < 8) {

            showError(
                password,
                passwordError,
                "Password must be at least 8 characters."
            );

            return;
        }

        if (password.value !== confirmPassword.value) {

            showError(
                confirmPassword,
                confirmError,
                "Passwords do not match."
            );

            return;

        }

        if (!terms.checked) {

           termsError.textContent = "Please accept Terms & Privacy Policy.";

            termsError.classList.add("show");

            return;
        }

        /* ===========================
           Loading
        =========================== */

        submitBtn.disabled = true;

        submitBtn.innerHTML = `

            <span class="spinner-border spinner-border-sm"></span>

            Creating Account...

        `;

        try {

            const response = await fetch("/api/auth/register", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({
                    name: name.value.trim(),
                    email: email.value.trim(),
                    password: password.value
                })

            });

            const data = await response.json();

            if (response.ok) {

                submitBtn.innerHTML = `

                    <i class="bi bi-check-circle-fill"></i>

                    Account Created

                `;

                submitBtn.style.background = "#16a34a";

                setTimeout(() => {

                    window.location.href = "/login";

                }, 1500);

            } else {

                alert(data.detail || "Registration failed.");

                submitBtn.disabled = false;

                submitBtn.innerHTML = `

                    <i class="bi bi-person-plus-fill"></i>

                    Create Free Account

                `;

            }

        } catch (err) {

            console.error(err);

            alert("Unable to connect to the server.");

            submitBtn.disabled = false;

            submitBtn.innerHTML = `

                <i class="bi bi-person-plus-fill"></i>

                Create Free Account

            `;

        }

    });

});

function showError(input, errorElement, message){

    input.parentElement.classList.add("input-error");

    input.parentElement.classList.remove("input-success");

    errorElement.textContent = message;

    errorElement.classList.add("show");

}

function showSuccess(input, errorElement){

    input.parentElement.classList.remove("input-error");

    input.parentElement.classList.add("input-success");

    errorElement.textContent="";

    errorElement.classList.remove("show");

}

function clearErrors(){

    document.querySelectorAll(".error-text")
        .forEach(el=>{

            el.textContent="";
            el.classList.remove("show");

        });

    document.querySelectorAll(".input-box")
        .forEach(box=>{

            box.classList.remove("input-error");
            box.classList.remove("input-success");

        });

}