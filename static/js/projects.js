"use strict";

(() => {
    const app = document.getElementById("projects-app");
    if (!app) return;

    const searchForm = document.getElementById("project-search-form");
    const searchInput = document.getElementById("project-query");
    const grid = document.getElementById("grid");
    const loading = document.getElementById("loading");
    const errorState = document.getElementById("error");
    const emptyState = document.getElementById("empty");
    const summary = document.getElementById("search-summary");
    const clearButton = document.getElementById("clear-search");
    const projectForm = document.getElementById("project-form");
    const modal = document.getElementById("add-project-modal");
    const isSuperuser = app.dataset.isSuperuser === "true";
    const SEARCH_DEBOUNCE_DELAY = 300;
    let searchDebounceTimer;
    let projectsAbortController;
    let requestVersion = 0;

    // Semua nilai dari JSON di-escape sebelum dimasukkan ke innerHTML.
    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function repositoryUrl(value) {
        if (!value) return "";
        try {
            const url = new URL(value);
            return ["https:", "http:"].includes(url.protocol) ? url.href : "";
        } catch {
            return "";
        }
    }

    function internalUrl(value) {
        if (!value) return "";
        const url = new URL(value, window.location.origin);
        if (url.origin !== window.location.origin) throw new Error("URL internal tidak valid");
        return url.pathname + url.search;
    }

    function getCookie(name) {
        const cookie = document.cookie.split(";").map(value => value.trim())
            .find(value => value.startsWith(`${name}=`));
        return cookie ? decodeURIComponent(cookie.slice(name.length + 1)) : null;
    }

    function csrfToken() {
        return projectForm?.querySelector('[name="csrfmiddlewaretoken"]')?.value
            || app.dataset.csrfToken || getCookie("csrftoken") || "";
    }

    function displayPageSection(section) {
        loading.classList.toggle("hide", section !== "loading");
        errorState.classList.toggle("hide", section !== "error");
        emptyState.classList.toggle("hide", section !== "empty");
        grid.classList.toggle("hide", section !== "grid");
        grid.setAttribute("aria-busy", String(section === "loading"));
    }

    function buildProjectCardElement(item) {
        const project = item.fields;
        const urls = item.urls;
        const article = document.createElement("article");
        article.className = "experience-card";
        const repo = repositoryUrl(project.repository_url);
        const tokenHtml = `<input type="hidden" name="csrfmiddlewaretoken" value="${escapeHtml(csrfToken())}">`;
        const starCount = Math.max(0, Number(project.star_count) || 0);
        const starTitle = starCount
            ? `Dibintangi oleh ${project.starred_by_names}`
            : "Jadilah yang pertama memberi star";
        const deleteHtml = isSuperuser && urls.delete
            ? `<form method="post" action="${escapeHtml(internalUrl(urls.delete))}" class="project-delete-form">
                   ${tokenHtml}
                   <button type="submit" class="button button-danger">Hapus</button>
               </form>` : "";
        article.innerHTML = `
            <span class="experience-category">${escapeHtml(project.technologies)}</span>
            <h2>${escapeHtml(project.title)}</h2>
            <p class="experience-description">${escapeHtml(project.description)}</p>
            <div class="social-links project-card-actions">
                <a class="social-link" href="${escapeHtml(internalUrl(urls.detail))}">Lihat detail</a>
                ${repo ? `<a class="social-link" href="${escapeHtml(repo)}" target="_blank" rel="noopener noreferrer">Lihat repositori</a>` : ""}
                <form method="post" action="${escapeHtml(internalUrl(urls.star))}" class="star-form">
                    ${tokenHtml}
                    <button type="submit" class="button button-star${project.is_starred ? " is-starred" : ""}"
                            aria-pressed="${project.is_starred ? "true" : "false"}" title="${escapeHtml(starTitle)}">
                        <span aria-hidden="true">★</span> ${project.is_starred ? "Unstar" : "Star"}
                        <span class="star-count">${starCount}</span>
                    </button>
                </form>
                ${deleteHtml}
            </div>`;
        return article;
    }

    function updateSearchControls() {
        const hasQuery = searchInput.value.length > 0;
        clearButton.hidden = !hasQuery;
        document.getElementById("search-hint").hidden = hasQuery;
    }

    async function fetchProjects(searchQuery = "") {
        projectsAbortController?.abort();
        const controller = new AbortController();
        projectsAbortController = controller;
        const version = ++requestVersion;
        displayPageSection("loading");
        summary.textContent = "";
        updateSearchControls();
        try {
            const url = new URL(app.dataset.projectsUrl, window.location.origin);
            if (searchQuery) url.searchParams.set("q", searchQuery);
            const response = await fetch(url, {
                headers: {Accept: "application/json"},
                credentials: "same-origin",
                mode: "same-origin",
                cache: "no-store",
                signal: controller.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const projects = await response.json();
            if (controller.signal.aborted || version !== requestVersion) return;
            if (!Array.isArray(projects)) throw new Error("Format JSON tidak valid");
            const fragment = document.createDocumentFragment();
            projects.forEach(item => fragment.appendChild(buildProjectCardElement(item)));
            grid.replaceChildren(fragment);
            summary.textContent = searchQuery
                ? `${projects.length} proyek ditemukan untuk “${searchQuery}”.`
                : `${projects.length} proyek untuk dijelajahi.`;
            displayPageSection(projects.length ? "grid" : "empty");
        } catch (error) {
            if (error.name === "AbortError" || controller.signal.aborted || version !== requestVersion) return;
            console.error("Gagal memuat proyek:", error);
            displayPageSection("error");
        }
    }

    function searchProjects() {
        const query = searchInput.value.trim();
        const url = new URL(window.location.href);
        url.searchParams.delete("title");
        if (query) url.searchParams.set("q", query);
        else url.searchParams.delete("q");
        window.history.replaceState({}, "", url);
        return fetchProjects(query);
    }

    searchInput.addEventListener("input", () => {
        clearTimeout(searchDebounceTimer);
        projectsAbortController?.abort();
        updateSearchControls();
        searchDebounceTimer = setTimeout(searchProjects, SEARCH_DEBOUNCE_DELAY);
    });
    searchForm.addEventListener("submit", event => {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchProjects();
    });
    clearButton.addEventListener("click", () => {
        clearTimeout(searchDebounceTimer);
        searchInput.value = "";
        searchInput.focus();
        searchProjects();
    });
    document.getElementById("retry-projects").addEventListener("click", searchProjects);
    document.getElementById("test-toast").addEventListener("click", () => {
        showToast("Berhasil", "Notifikasi toast sudah berfungsi!", "success", 3000);
    });
    grid.addEventListener("submit", event => {
        if (event.target.matches(".project-delete-form") && !window.confirm("Yakin ingin menghapus proyek ini?")) {
            event.preventDefault();
        }
    });

    function clearFormErrors() {
        projectForm.querySelectorAll(".form-error").forEach(element => {
            element.textContent = "";
            element.hidden = true;
        });
        projectForm.querySelectorAll("[aria-invalid]").forEach(element => {
            element.removeAttribute("aria-invalid");
            element.removeAttribute("aria-describedby");
        });
    }

    function displayFormErrors(result, status) {
        const messages = [];
        for (const [name, errors] of Object.entries(result.errors || {})) {
            const message = errors.map(error => error.message).join(" ");
            messages.push(message);
            const element = document.getElementById(`ajax-error-${name}`);
            const input = projectForm.elements.namedItem(name);
            if (element) {
                element.textContent = message;
                element.hidden = false;
                if (input) {
                    input.setAttribute("aria-invalid", "true");
                    input.setAttribute("aria-describedby", element.id);
                }
            }
        }
        const message = messages.join(" ") || result.message || (
            status === 403 ? "Permintaan ditolak. Muat ulang halaman dan pastikan kamu login sebagai pemilik."
                : `Proyek belum tersimpan (status ${status}). Silakan coba lagi.`
        );
        const error = document.getElementById("project-form-error");
        error.textContent = message;
        error.hidden = false;
        projectForm.querySelector('[aria-invalid="true"]')?.focus();
        showToast("Gagal menambahkan proyek", message, "error", 6000);
    }

    async function addProject(event) {
        event.preventDefault();
        const submitButton = projectForm.querySelector('button[type="submit"]');
        if (submitButton.disabled) return;
        clearFormErrors();
        submitButton.disabled = true;
        submitButton.textContent = "Menyimpan...";
        try {
            const response = await fetch(app.dataset.createUrl, {
                method: "POST",
                mode: "same-origin",
                credentials: "same-origin",
                headers: {"X-CSRFToken": csrfToken(), Accept: "application/json"},
                body: new FormData(projectForm),
            });
            const result = await response.json().catch(() => ({}));
            if (!response.ok) {
                displayFormErrors(result, response.status);
                return;
            }
            projectForm.reset();
            if (modal.matches(":popover-open")) modal.hidePopover();
            showToast("Berhasil", searchInput.value.trim()
                ? "Proyek tersimpan. Daftar tetap mengikuti pencarianmu; hapus pencarian untuk melihat semua proyek."
                : "Proyek baru berhasil ditambahkan!", "success");
            clearTimeout(searchDebounceTimer);
            await fetchProjects(searchInput.value.trim());
        } catch (error) {
            console.error("Gagal mengirim proyek:", error);
            displayFormErrors({message: "Koneksi terputus. Periksa daftar proyek sebelum mencoba lagi agar tidak menambah data ganda."}, 0);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Tambah proyek";
        }
    }

    if (projectForm) {
        projectForm.addEventListener("submit", addProject);
        modal.addEventListener("toggle", event => {
            if (event.newState === "open") projectForm.querySelector('input[name="title"]')?.focus();
        });
    }
    fetchProjects(searchInput.value.trim());
})();
