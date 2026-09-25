const API_BASE = "/api";

document.addEventListener("DOMContentLoaded", () => {

    const heroForm = document.getElementById("heroAuditForm");

    if (!heroForm) return;

    heroForm.addEventListener("submit", startAudit);

});

async function startAudit(event){

    event.preventDefault();

    console.log("Audit Started");

}