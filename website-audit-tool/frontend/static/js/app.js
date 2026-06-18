const API_BASE = '/api';

function getToken() {
  return localStorage.getItem('audit_token') || '';
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`,
  };
}

function saveAuth(response) {
  if (response?.access_token) {
    localStorage.setItem('audit_token', response.access_token);
  }
}

function formatDate(value) {
  if (!value) return '-';
  return new Date(value).toLocaleDateString();
}

function setChartTheme(chart) {
  chart.options.plugins.legend.labels.color = '#334155';
  chart.options.scales.x.ticks.color = '#475569';
  chart.options.scales.y.ticks.color = '#475569';
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.AOS) AOS.init({ duration: 700, once: true, offset: 80 });

  const settingsName =
    document.getElementById("settingsName");

  if(settingsName){
      loadSettings();
  }

  loadPreferences();

  const savePreferencesBtn =
    document.getElementById(
        "savePreferencesBtn"
    );

if(savePreferencesBtn){

    savePreferencesBtn.addEventListener(
        "click",
        () => {

            localStorage.setItem(
                "theme",
                document.getElementById(
                    "themeSelect"
                ).value
            );

            localStorage.setItem(
                "reportFormat",
                document.getElementById(
                    "reportFormat"
                ).value
            );

            localStorage.setItem(
                "defaultUrl",
                document.getElementById(
                    "defaultUrl"
                ).value
            );

            alert(
                "Preferences saved successfully"
            );
        }
    );
}

  const logoutBtn =
    document.getElementById("logoutBtn");

if(logoutBtn){

    logoutBtn.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "audit_token"
            );

            window.location.href =
                "/login";
        }
    );
}



  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = { email: document.getElementById('loginEmail').value, password: document.getElementById('loginPassword').value };
      const response = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const data = await response.json();
      if (!response.ok) return alert(data.detail || 'Login failed');
      saveAuth(data);
      window.location.href = '/dashboard';
    });
  }

  function loadPreferences(){

    const theme =
        localStorage.getItem("theme") || "light";

    const format =
        localStorage.getItem("reportFormat") || "pdf";

    const url =
        localStorage.getItem("defaultUrl") || "";

    const themeSelect =
        document.getElementById("themeSelect");

    if(themeSelect){

        themeSelect.value = theme;

        document.getElementById(
            "reportFormat"
        ).value = format;

        document.getElementById(
            "defaultUrl"
        ).value = url;
    }
}

  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const password = document.getElementById('registerPassword').value;
      const confirm = document.getElementById('registerConfirmPassword').value;
      if (password !== confirm) return alert('Passwords do not match');
      const payload = {
        name: document.getElementById('registerName').value,
        email: document.getElementById('registerEmail').value,
        password,
      };
      const response = await fetch(`${API_BASE}/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const data = await response.json();
      if (!response.ok) return alert(data.detail || 'Registration failed');
      alert('Account created. Please log in.');
      window.location.href = '/login';
    });
  }

  const auditForm = document.getElementById('auditForm');
  if (auditForm) {
    auditForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const loader = document.getElementById('auditLoader');
      loader?.classList.remove('d-none');
      const response = await fetch(`${API_BASE}/audits`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ website_url: document.getElementById('auditUrl').value }),
      });
      const data = await response.json();
      loader?.classList.add('d-none');
      if (!response.ok) return alert(data.detail || 'Audit failed');
      window.location.href = `/audits/${data.id}`;
    });
  }

  const demoAuditForm = document.getElementById('demoAuditForm');
  if (demoAuditForm) {
    demoAuditForm.addEventListener('submit', (event) => {
      event.preventDefault();
      window.location.href = '/login';
    });
  }

  const dashboard = document.getElementById('dashboardChart');
  if (dashboard) {
    bootstrapDashboard();
  }

  const reportRoot = document.querySelector('[data-audit-id]');
  if (reportRoot) {
    bootstrapReport(reportRoot.dataset.auditId);
  }

  const historyTable = document.getElementById('historyTable');
  if (historyTable) {
    loadHistory(historyTable);
  }

  const profilePage = document.getElementById('profilePage');

  if (profilePage) {
      loadProfile();
  }
});


async function loadProfile() {

    console.log("LOAD PROFILE START");

    const userResponse = await fetch(
        `${API_BASE}/auth/me`,
        {
            headers: authHeaders()
        }
    );

    console.log("STATUS", userResponse.status);

    if (!userResponse.ok) {
        console.log("Unable to load user");
        return;
    }

    const user = await userResponse.json();

    console.log("USER", user);

    document.getElementById("profileName").textContent =
        user.name || "-";

    const initials =
    user.name
        .split(" ")
        .map(n => n[0])
        .join("")
        .substring(0,2);

    document.getElementById(
        "profileAvatar"
    ).textContent = initials;    

    document.getElementById("profileEmail").textContent =
        user.email || "-";

    document.getElementById(
        "profileNameSummary"
    ).textContent =
        user.name || "-";

    document.getElementById(
        "profileEmailSummary"
    ).textContent =
        user.email || "-";    

    document.getElementById("profileJoined").textContent =
        user.created_at
            ? new Date(user.created_at).toLocaleDateString()
            : "Not Available";

    const auditResponse = await fetch(
        `${API_BASE}/audits`,
        {
            headers: authHeaders()
        }
    );

    if (!auditResponse.ok) return;

    const audits = await auditResponse.json();

    document.getElementById("profileTotalAudits").textContent =
        audits.length;

    document.getElementById("profileReports").textContent =
        audits.length;

    const avg = audits.length
        ? audits.reduce((sum, a) => sum + a.overall_score, 0) / audits.length
        : 0;

    document.getElementById("profileAverageScore").textContent =
        avg.toFixed(1);
}


async function loadSettings() {

    const response = await fetch(
        `${API_BASE}/auth/me`,
        {
            headers: authHeaders()
        }
    );

    if(!response.ok) return;

    const user = await response.json();

    document.getElementById(
        "settingsName"
    ).value = user.name;

    document.getElementById(
        "settingsEmail"
    ).value = user.email;
}

async function bootstrapDashboard() {
  const summaryResponse = await fetch(`${API_BASE}/audits`, { headers: authHeaders() });
  const audits = summaryResponse.ok ? await summaryResponse.json() : [];
  const totalAudits = document.getElementById('totalAudits');
  const averageScore = document.getElementById('averageScore');
  const seoScore = document.getElementById('seoScore');
  const performanceScore = document.getElementById('performanceScore');
  const scoreList = document.getElementById('scoreList');
  const recentAudits = document.getElementById('recentAudits');

  const stats = audits.reduce((acc, audit) => {
    acc.count += 1;
    acc.avg += audit.overall_score;
    acc.seo += audit.seo_score;
    acc.performance += audit.performance_score;
    acc.accessibility += audit.accessibility_score;
    acc.security += audit.security_score;
    acc.mobile += audit.mobile_score;
    return acc;
  }, { count: 0, avg: 0, seo: 0, performance: 0, accessibility: 0, security: 0, mobile: 0 });

  const divisor = stats.count || 1;
  totalAudits.textContent = stats.count;
  averageScore.textContent = (stats.avg / divisor).toFixed(1);
  seoScore.textContent = (stats.seo / divisor).toFixed(1);
  performanceScore.textContent = (stats.performance / divisor).toFixed(1);

  scoreList.innerHTML = `
    <div class="d-grid gap-3">
      <div class="d-flex justify-content-between"><span>Accessibility</span><strong>${(stats.accessibility / divisor).toFixed(1)}</strong></div>
      <div class="d-flex justify-content-between"><span>Security</span><strong>${(stats.security / divisor).toFixed(1)}</strong></div>
      <div class="d-flex justify-content-between"><span>Mobile</span><strong>${(stats.mobile / divisor).toFixed(1)}</strong></div>
    </div>
  `;

  recentAudits.innerHTML = audits.slice(0, 6).map(audit => `
    <tr>
      <td>${audit.website_url}</td>
      <td>${audit.overall_score.toFixed(1)}</td>
      <td><span class="badge text-bg-primary">${audit.grade}</span></td>
      <td>${formatDate(audit.created_at)}</td>
      <td class="text-end"><a class="btn btn-sm btn-outline-primary" href="/audits/${audit.id}">Open</a></td>
    </tr>
  `).join('') || '<tr><td colspan="5" class="text-center text-muted py-4">No audits yet.</td></tr>';

  const chart = new Chart(document.getElementById('dashboardChart'), {
    type: 'bar',
    data: {
      labels: ['SEO', 'Performance', 'Accessibility', 'Security', 'Mobile'],
      datasets: [{
        label: 'Average Score',
        data: [stats.seo / divisor, stats.performance / divisor, stats.accessibility / divisor, stats.security / divisor, stats.mobile / divisor],
        backgroundColor: ['#2563eb', '#7c3aed', '#10b981', '#ef4444', '#f59e0b'],
        borderRadius: 12,
      }],
    },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } },
  });
  setChartTheme(chart);
  chart.update();
}

async function bootstrapReport(auditId) {

  const response = await fetch(
      `${API_BASE}/audits/${auditId}`,
      {
          headers: authHeaders()
      }
  );

  if (!response.ok) {

      document.getElementById("reportSummary").textContent =
          "Sign in to load this report.";

      return;
  }

  const audit = await response.json();

  console.log("AUDIT =", audit);
  console.log("RECOMMENDATIONS =", audit.recommendations);
  
  const screenshot =
  document.getElementById("websiteScreenshot");

  if (
      screenshot &&
      audit.screenshot_path
  ) {
      console.log("SCREENSHOT PATH =", audit.screenshot_path);

    screenshot.src = audit.screenshot_path.replaceAll("\\", "/");

  }
  const perf = audit.performance_metrics || {};
  const security = audit.security_metrics || {};

const a11y = audit.accessibility_metrics || {
    missing_alt_images: 0,
    unlabeled_inputs: 0,
    has_aria_support: false
};


document.getElementById("missingAltImages").textContent =
    a11y.missing_alt_images || 0;

document.getElementById("unlabeledInputs").textContent =
    a11y.unlabeled_inputs || 0;

document.getElementById("ariaSupport").textContent =
    a11y.has_aria_support ? "Yes" : "No";

document.getElementById("securityChecksContent").innerHTML = `
<div class="row g-3">

    ${[
        ["HTTPS Enabled", security.https_enabled],
        ["HSTS Enabled", security.hsts_enabled],
        ["CSP Present", security.csp_present],
        ["X-Frame Options", security.x_frame_options],
        ["X-Content-Type", security.x_content_type],
        ["Referrer Policy", security.referrer_policy],
        ["Server Hidden", security.server_hidden]
    ].map(([label, status]) => `
        <div class="col-lg-3 col-md-4 col-sm-6">
            <div class="card p-3 text-center h-100">

                <span class="badge ${
                    status
                        ? "text-bg-success"
                        : "text-bg-danger"
                }">
                    ${
                        status
                            ? "PASS"
                            : "FAIL"
                    }
                </span>

                <div class="mt-2">
                    ${label}
                </div>

            </div>
        </div>
    `).join("")}

</div>
`;

const perfDiv =
document.getElementById("performanceMetrics");

if (perfDiv) {

    perfDiv.innerHTML = `
        <div class="row g-3">

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>FCP</strong>
                    <div>${perf.first_contentful_paint ?? "-"} s</div>
                </div>
            </div>

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>LCP</strong>
                    <div>${perf.largest_contentful_paint ?? "-"} s</div>
                </div>
            </div>

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>Speed Index</strong>
                    <div>${perf.speed_index ?? "-"} s</div>
                </div>
            </div>

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>TTI</strong>
                    <div>${perf.time_to_interactive ?? "-"} s</div>
                </div>
            </div>

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>TBT</strong>
                    <div>${perf.total_blocking_time ?? "-"} ms</div>
                </div>
            </div>

            <div class="col-md-2">
                <div class="card p-3 text-center">
                    <strong>CLS</strong>
                    <div>${perf.cls || "-"}</div>
                </div>
            </div>

        </div>
    `;
}

document.getElementById("accessibilityValue").textContent =
audit.accessibility_score.toFixed(1);

document.getElementById("accessibilityBar").style.width =
    `${audit.accessibility_score}%`;

  const findings = audit.findings || [];

// AI Recommendations

const recommendations = audit.recommendations || [];
console.log("FOUND AI DIV =", document.getElementById("aiRecommendations"));
console.log("RECOMMENDATIONS DATA =", audit.recommendations);

const aiRecommendations =
    document.getElementById("aiRecommendations");

    if (aiRecommendations) {

        if (recommendations.length > 0) {

            aiRecommendations.innerHTML =
                recommendations.map(rec => {

                    let badgeClass = "bg-secondary";

                    if (rec.priority === "Critical") {
                        badgeClass = "bg-danger";
                    } else if (rec.priority === "High") {
                        badgeClass = "bg-warning text-dark";
                    } else if (rec.priority === "Medium") {
                        badgeClass = "bg-info";
                    } else if (rec.priority === "Low") {
                        badgeClass = "bg-success";
                    }

                    return `
                        <div class="card mb-3 shadow-sm">

                            <div class="card-body">

                                <span class="badge ${badgeClass}">
                                    ${rec.priority}
                                </span>

                                <p class="mt-3 mb-0">
                                    ${rec.recommendation}
                                </p>

                            </div>

                        </div>
                    `;

                }).join("");

        } else {

            aiRecommendations.innerHTML = `
                <div class="alert alert-warning">
                    No AI recommendations available for this audit.
                </div>
            `;

        }
    }

  const uiuxFindings = findings.filter(
    item => item.category === "UI/UX"
);

const uiuxDiv =
document.getElementById("uiuxContent");

if (uiuxDiv) {

    uiuxDiv.innerHTML =
        uiuxFindings.length > 0
        ? uiuxFindings.map(item => `
            <div class="card mb-2 p-3">
                <strong>${item.issue}</strong>
                <div class="text-muted">
                    ${item.recommendation}
                </div>
            </div>
        `).join("")
        : "<div class='text-success'>No UI/UX issues detected.</div>";
}

  document.getElementById('reportUrl').textContent = audit.website_url;
  document.getElementById('reportSummary').textContent = audit.summary;
  document.getElementById('seoValue').textContent = audit.seo_score.toFixed(1);
  document.getElementById('performanceValue').textContent = audit.performance_score.toFixed(1);
  document.getElementById('securityValue').textContent = audit.security_score.toFixed(1);
  document.getElementById('mobileValue').textContent = audit.mobile_score.toFixed(1);
  document.getElementById('overallValue').textContent = audit.overall_score.toFixed(1);
  document.getElementById('seoBar').style.width = `${audit.seo_score}%`;
  document.getElementById('performanceBar').style.width = `${audit.performance_score}%`;
  document.getElementById('securityBar').style.width = `${audit.security_score}%`;
  document.getElementById('mobileBar').style.width =`${audit.mobile_score}%`;
  document.getElementById('overallBar').style.width = `${audit.overall_score}%`;
  document.getElementById('downloadPdfBtn')
  .addEventListener('click', async (e) => {

      e.preventDefault();

      const response = await fetch(
          `${API_BASE}/reports/${auditId}/pdf`,
          {
              headers: {
                  Authorization:
                      `Bearer ${getToken()}`
              }
          }
      );

      if (!response.ok) {
          alert("PDF generation failed");
          return;
      }

      const blob =
          await response.blob();

      const url =
          window.URL.createObjectURL(blob);

      const a =
          document.createElement("a");

      a.href = url;

      a.download =
          `audit_${auditId}.pdf`;

      document.body.appendChild(a);

      a.click();

      a.remove();

      window.URL.revokeObjectURL(url);
  });


  document.getElementById('findingStream').innerHTML = findings.slice(0, 4).map(item => `
    <div class="border-bottom pb-3 mb-3">
      <div class="d-flex justify-content-between align-items-center mb-2"><strong>${item.category}</strong><span class="badge text-bg-light">${item.priority}</span></div>
      <div class="text-muted small mb-2">${item.issue}</div>
      <div><strong>Recommendation:</strong> ${item.recommendation}</div>
    </div>
  `).join('');

  document.getElementById('findingsTable').innerHTML = findings.map(item => `
    <tr><td>${item.category}</td><td>${item.issue}</td><td>${item.recommendation}</td><td><span class="badge text-bg-primary">${item.priority}</span></td></tr>
  `).join('');

  const ctx = document.getElementById('reportChart');
  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['SEO', 'Performance', 'Accessibility', 'Security', 'Mobile'],
      datasets: [{
        label: 'Score',
        data: [audit.seo_score, audit.performance_score, audit.accessibility_score, audit.security_score, audit.mobile_score],
        backgroundColor: 'rgba(37, 99, 235, 0.15)',
        borderColor: '#2563eb',
        pointBackgroundColor: '#7c3aed',
      }],
    },
    options: { scales: { r: { beginAtZero: true, max: 100, angleLines: { color: '#cbd5e1' }, grid: { color: '#e2e8f0' }, pointLabels: { color: '#334155' }, ticks: { backdropColor: 'transparent' } } } },
  });
}

async function loadHistory(container) {
  const response = await fetch(`${API_BASE}/audits`, { headers: authHeaders() });
  const audits = response.ok ? await response.json() : [];
  container.innerHTML = audits.map(audit => `
    <tr>
      <td>${audit.website_url}</td>
      <td>${audit.seo_score.toFixed(1)}</td>
      <td>${audit.performance_score.toFixed(1)}</td>
      <td>${audit.security_score.toFixed(1)}</td>
      <td>${audit.overall_score.toFixed(1)}</td>
      <td><span class="badge text-bg-primary">${audit.grade}</span></td>
      <td>${formatDate(audit.created_at)}</td>
      <td><a class="btn btn-sm btn-outline-primary" href="/audits/${audit.id}">View</a></td>
    </tr>
  `).join('') || '<tr><td colspan="8" class="text-center text-muted py-4">No audits available.</td></tr>';
}
