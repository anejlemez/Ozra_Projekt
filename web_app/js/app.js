const AppState = {
    lang: "sl",
    tekmovanja: [],
    rezultati: [],
    filteredRezultati: [],
    tekmovalci: [],
    selectedTekmovanje: null,
    selectedTekmovalec: null,
    compareOne: null,
    compareTwo: null
};

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    applyTranslations();
    loadTekmovanja();
});

function bindEvents() {
    document.getElementById("languageSelect").addEventListener("change", (event) => {
        AppState.lang = event.target.value;
        applyTranslations();
        rerenderAll();
    });

    document.querySelectorAll("#mainTabs .nav-link").forEach((button) => {
        button.addEventListener("click", () => {
            switchTab(button.dataset.tab);
        });
    });

    document.getElementById("refreshCompetitionsBtn").addEventListener("click", loadTekmovanja);

    document.getElementById("divisionFilterInput").addEventListener("input", () => {
        filterRezultati();
    });

    document.getElementById("clearResultsFilterBtn").addEventListener("click", () => {
        document.getElementById("divisionFilterInput").value = "";
        filterRezultati();
    });

    document.getElementById("searchCompetitorBtn").addEventListener("click", searchTekmovalci);

    document.getElementById("competitorSearchInput").addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            searchTekmovalci();
        }
    });

    document.getElementById("compareBtn").addEventListener("click", compareSelectedCompetitors);
}

function switchTab(tabId) {
    document.querySelectorAll(".tab-section").forEach((section) => {
        section.classList.add("d-none");
    });

    document.getElementById(tabId).classList.remove("d-none");

    document.querySelectorAll("#mainTabs .nav-link").forEach((button) => {
        button.classList.remove("active");

        if (button.dataset.tab === tabId) {
            button.classList.add("active");
        }
    });
}

function applyTranslations() {
    document.documentElement.lang = AppState.lang;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
        const key = element.dataset.i18n;
        element.textContent = tr(key);
    });

    document.querySelectorAll("[data-placeholder-i18n]").forEach((element) => {
        const key = element.dataset.placeholderI18n;
        element.placeholder = tr(key);
    });
}

function rerenderAll() {
    renderTekmovanja();
    renderRezultati();
    renderTekmovalci();
    renderNastopi([]);
    updateComparisonLabels();

    if (AppState.selectedTekmovalec) {
        document.getElementById("selectedCompetitorValue").textContent =
            AppState.selectedTekmovalec.ime_priimek || "-";
    }
}

function showAlert(message, type = "danger") {
    const alertBox = document.getElementById("alertBox");

    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;

    setTimeout(() => {
        alertBox.classList.add("d-none");
    }, 4500);
}

function clearAlert() {
    const alertBox = document.getElementById("alertBox");
    alertBox.classList.add("d-none");
    alertBox.textContent = "";
}

function safe(value) {
    return value === null || value === undefined || value === "" ? "-" : value;
}

async function loadTekmovanja() {
    clearAlert();

    const tableBody = document.getElementById("competitionsTableBody");
    tableBody.innerHTML = `<tr><td colspan="5">${tr("loading")}</td></tr>`;

    try {
        const data = await Api.getTekmovanja();
        AppState.tekmovanja = Array.isArray(data) ? data : [];
        renderTekmovanja();
    } catch (error) {
        tableBody.innerHTML = "";
        showAlert(tr("serverError"));
    }
}

function renderTekmovanja() {
    const tableBody = document.getElementById("competitionsTableBody");
    tableBody.innerHTML = "";

    if (!AppState.tekmovanja.length) {
        tableBody.innerHTML = `<tr><td colspan="5">${tr("noData")}</td></tr>`;
        return;
    }

    AppState.tekmovanja.forEach((item) => {
        const row = document.createElement("tr");

        if (
            AppState.selectedTekmovanje &&
            AppState.selectedTekmovanje.id_tekmovanja === item.id_tekmovanja
        ) {
            row.classList.add("table-active-row");
        }

        row.innerHTML = `
            <td>${safe(item.id_tekmovanja)}</td>
            <td>${safe(item.naziv)}</td>
            <td>${safe(item.leto)}</td>
            <td>${safe(item.tip_tekmovanja)}</td>
            <td>${safe(item.lokacija)}</td>
        `;

        row.addEventListener("click", () => {
            AppState.selectedTekmovanje = item;
            renderTekmovanja();
            loadRezultatiTekmovanja(item.id_tekmovanja);
        });

        tableBody.appendChild(row);
    });
}

async function loadRezultatiTekmovanja(tekmovanjeId) {
    clearAlert();

    document.getElementById("selectedCompetitionText").textContent =
        AppState.selectedTekmovanje
            ? `- ${AppState.selectedTekmovanje.naziv} (${AppState.selectedTekmovanje.leto})`
            : "";

    const tableBody = document.getElementById("resultsTableBody");
    tableBody.innerHTML = `<tr><td colspan="11">${tr("loading")}</td></tr>`;

    try {
        const data = await Api.getRezultatiTekmovanja(tekmovanjeId);
        AppState.rezultati = Array.isArray(data) ? data : [];
        filterRezultati();
    } catch (error) {
        tableBody.innerHTML = "";
        showAlert(tr("serverError"));
    }
}

function filterRezultati() {
    const filterValue = document.getElementById("divisionFilterInput").value.trim().toLowerCase();

    if (!filterValue) {
        AppState.filteredRezultati = [...AppState.rezultati];
    } else {
        AppState.filteredRezultati = AppState.rezultati.filter((item) => {
            return String(item.divizija || "").toLowerCase().includes(filterValue);
        });
    }

    renderRezultati();
}

function renderRezultati() {
    const tableBody = document.getElementById("resultsTableBody");
    const info = document.getElementById("resultsInfo");

    tableBody.innerHTML = "";

    if (!AppState.selectedTekmovanje) {
        info.textContent = tr("selectCompetition");
        tableBody.innerHTML = `<tr><td colspan="11">${tr("selectCompetition")}</td></tr>`;
        return;
    }

    if (!AppState.filteredRezultati.length) {
        info.textContent = "";
        tableBody.innerHTML = `<tr><td colspan="11">${tr("noData")}</td></tr>`;
        return;
    }

    const limited = AppState.filteredRezultati.slice(0, CONFIG.MAX_RESULTS_DISPLAY);

    info.textContent =
        `${tr("displayedLimited")} ${limited.length} ${tr("of")} ${AppState.filteredRezultati.length} ${tr("rows")}.`;

    limited.forEach((item) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${safe(item.id_rezultata)}</td>
            <td>${safe(item.ime_priimek)}</td>
            <td>${safe(item.overallRank)}</td>
            <td>${safe(item.genderRank)}</td>
            <td>${safe(item.divRank)}</td>
            <td>${safe(item.bib)}</td>
            <td>${safe(item.divizija)}</td>
            <td>${safe(item.plavanje)}</td>
            <td>${safe(item.kolesarjenje)}</td>
            <td>${safe(item.tek)}</td>
            <td>${safe(item.skupniCas)}</td>
        `;

        tableBody.appendChild(row);
    });
}

async function searchTekmovalci() {
    clearAlert();

    const input = document.getElementById("competitorSearchInput");
    const ime = input.value.trim();

    if (!ime) {
        showAlert(tr("enterNameWarning"), "warning");
        return;
    }

    const tableBody = document.getElementById("competitorsTableBody");
    tableBody.innerHTML = `<tr><td colspan="5">${tr("loading")}</td></tr>`;

    try {
        const data = await Api.searchTekmovalci(ime);
        AppState.tekmovalci = Array.isArray(data) ? data : [];
        renderTekmovalci();
    } catch (error) {
        tableBody.innerHTML = "";
        showAlert(tr("serverError"));
    }
}

function renderTekmovalci() {
    const tableBody = document.getElementById("competitorsTableBody");
    tableBody.innerHTML = "";

    if (!AppState.tekmovalci.length) {
        tableBody.innerHTML = `<tr><td colspan="5">${tr("noData")}</td></tr>`;
        return;
    }

    AppState.tekmovalci.forEach((item) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${safe(item.id_tekmovalec)}</td>
            <td>${safe(item.ime_priimek)}</td>
            <td>${safe(item.starost)}</td>
            <td>${safe(item.drzava)}</td>
            <td class="d-flex flex-wrap gap-1">
                <button class="btn btn-sm btn-outline-primary" data-action="performances">
                    ${tr("showPerformances")}
                </button>
                <button class="btn btn-sm btn-outline-success" data-action="select-one">
                    ${tr("selectFirst")}
                </button>
                <button class="btn btn-sm btn-outline-secondary" data-action="select-two">
                    ${tr("selectSecond")}
                </button>
            </td>
        `;

        row.querySelector('[data-action="performances"]').addEventListener("click", () => {
            selectTekmovalec(item);
            loadNastopiTekmovalca(item);
        });

        row.querySelector('[data-action="select-one"]').addEventListener("click", () => {
            AppState.compareOne = item;
            updateComparisonLabels();
            showAlert(`${tr("competitorOne")}: ${item.ime_priimek}`, "success");
        });

        row.querySelector('[data-action="select-two"]').addEventListener("click", () => {
            AppState.compareTwo = item;
            updateComparisonLabels();
            showAlert(`${tr("competitorTwo")}: ${item.ime_priimek}`, "success");
        });

        tableBody.appendChild(row);
    });
}

function selectTekmovalec(tekmovalec) {
    AppState.selectedTekmovalec = tekmovalec;

    document.getElementById("selectedCompetitorText").textContent =
        `- ${tekmovalec.ime_priimek}`;

    document.getElementById("selectedCompetitorValue").textContent =
        tekmovalec.ime_priimek || "-";
}

async function loadNastopiTekmovalca(tekmovalec) {
    clearAlert();

    const tableBody = document.getElementById("performancesTableBody");
    tableBody.innerHTML = `<tr><td colspan="11">${tr("loading")}</td></tr>`;

    try {
        const [nastopi, najboljsi] = await Promise.all([
            Api.getNastopiTekmovalca(tekmovalec.id_tekmovalec),
            Api.getNajboljsiCas(tekmovalec.id_tekmovalec)
        ]);

        renderNastopi(Array.isArray(nastopi) ? nastopi : []);

        document.getElementById("bestTimeValue").textContent =
            safe(najboljsi.najboljsi);

        document.getElementById("performanceCountValue").textContent =
            Array.isArray(nastopi) ? nastopi.length : 0;

    } catch (error) {
        tableBody.innerHTML = "";
        showAlert(tr("serverError"));
    }
}

function renderNastopi(data) {
    const tableBody = document.getElementById("performancesTableBody");
    tableBody.innerHTML = "";

    if (!data.length) {
        tableBody.innerHTML = `<tr><td colspan="11">${tr("noData")}</td></tr>`;

        if (!AppState.selectedTekmovalec) {
            document.getElementById("bestTimeValue").textContent = "-";
            document.getElementById("performanceCountValue").textContent = "-";
            document.getElementById("selectedCompetitorValue").textContent = "-";
        }

        return;
    }

    data.forEach((item) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${safe(item.id_rezultata)}</td>
            <td>${safe(item.overallRank)}</td>
            <td>${safe(item.genderRank)}</td>
            <td>${safe(item.divRank)}</td>
            <td>${safe(item.bib)}</td>
            <td>${safe(item.divizija)}</td>
            <td>${safe(item.plavanje)}</td>
            <td>${safe(item.kolesarjenje)}</td>
            <td>${safe(item.tek)}</td>
            <td>${safe(item.skupniCas)}</td>
            <td>${safe(item.tk_tekmovanje)}</td>
        `;

        tableBody.appendChild(row);
    });
}

function updateComparisonLabels() {
    document.getElementById("comparisonCompetitorOne").textContent =
        AppState.compareOne ? AppState.compareOne.ime_priimek : "-";

    document.getElementById("comparisonCompetitorTwo").textContent =
        AppState.compareTwo ? AppState.compareTwo.ime_priimek : "-";
}

async function compareSelectedCompetitors() {
    clearAlert();

    if (!AppState.compareOne || !AppState.compareTwo) {
        showAlert(tr("comparisonHelp"), "warning");
        return;
    }

    const tableBody = document.getElementById("comparisonTableBody");

    tableBody.innerHTML = `
        <tr>
            <td colspan="3">${tr("loading")}</td>
        </tr>
    `;

    try {
        const data = await Api.primerjajTekmovalca(
            AppState.compareOne.id_tekmovalec,
            AppState.compareTwo.id_tekmovalec
        );

        const t1 = data.tekmovalec1 || {};
        const t2 = data.tekmovalec2 || {};

        tableBody.innerHTML = `
            <tr>
                <td>${tr("numberOfPerformances")}</td>
                <td>${safe(t1.nastopi)}</td>
                <td>${safe(t2.nastopi)}</td>
            </tr>
            <tr>
                <td>${tr("bestTime")}</td>
                <td>${safe(t1.najboljsi)}</td>
                <td>${safe(t2.najboljsi)}</td>
            </tr>
        `;
    } catch (error) {
        tableBody.innerHTML = "";
        showAlert(tr("serverError"));
    }
}