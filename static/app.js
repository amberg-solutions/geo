document.addEventListener("DOMContentLoaded", () => {
    const regionSelect = document.getElementById("search-region");

    if (window.lucide) {
        window.lucide.createIcons();
    }

    document.getElementById("map-search").addEventListener("submit", (event) => {
        event.preventDefault();
    });

    regionSelect.addEventListener("change", () => {
        fetchHtmlMap(regionSelect.value);
        fetchSurfaceArea(regionSelect.value);
    });

    fetchHtmlMap();
    fetchRegions();
    fetchLastUpdateTs();
    fetchSurfaceArea();
    fetchRegionCount();
});

async function fetchHtmlMap(region = "all") {
    const mapNode = document.getElementById("map");
    const loadingNode = document.getElementById("map-loading");
    const statusNode = document.getElementById("map-status");

    try {
        const params = new URLSearchParams({ region });
        const response = await fetch(`/api/get_map?${params}`);

        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen von /api/get_map: ${response.status}`);
        }

        const data = await response.json();
        mapNode.addEventListener("load", () => {
            loadingNode.hidden = true;
            statusNode.classList.add("is-ready");
            statusNode.lastChild.textContent = "Karte bereit";
        }, { once: true });
        mapNode.srcdoc = data.map;

    } catch (error) {
        loadingNode.classList.add("is-error");
        loadingNode.innerHTML = "<span>Karte konnte nicht geladen werden.</span>";
        statusNode.lastChild.textContent = "Fehler beim Laden";
        console.error(`Fehler beim Abrufen der Karte: ${error}`);
    }
}

async function fetchRegions() {
    const regionSelect = document.getElementById("search-region");

    try {
        const response = await fetch("/api/fetch_regions");

        if (!response.ok) {
            throw new Error(`Fehler beim Abfragen von /api/fetch_regions: ${response.status}`);
        }

        const data = await response.json();
        const regions = data.regions;
        const options = document.createDocumentFragment();

        for (const region of regions) {
            options.append(new Option(region, region));
        }

        regionSelect.append(options);
    } catch (error) {
        regionSelect.disabled = true;
        console.error(`Fehler beim Abrufen der Regionen: ${error}`);
    }
}

async function fetchLastUpdateTs() {
    const lastUpdateNode = document.getElementById("last-update");

    try {
        response = await fetch(`/api/fetch_last_update_ts`);

        if (!response.ok) {
            throw new Error(`Fehler beim Abfragen von /api/fetch_last_update_ts: ${response.status}`);
        }

        data = await response.json();
        lastUpdateNode.innerHTML = data["ts"] ?? `-`
    } catch (error) {
        log.error(`Fehler beim Abfragen des letzten Updates: ${error}`);
        lastUpdateNode = `-`
    }
}

async function fetchRegionCount() {
    const totalRegionsNode = document.getElementById("total-regions");

    try {
        response = await fetch(`/api/fetch_region_count`);

        if (!response.ok) {
            throw new Error(`Fehler beim Abfragen von /api/fetch_region_count: ${response.status}`);
        }

        data = await response.json();
        totalRegionsNode.innerHTML = data["count"] ?? `-`
    } catch (error) {
        log.error(`Fehler beim Abfragen der Anzahl Regionen: ${error}`);
        totalRegionsNode = `-`
    }
}

async function fetchSurfaceArea(region = "all") {
    const surfaceAreaNode = document.getElementById("surface-area");
    const params = new URLSearchParams({ region });

    try {
        const response = await fetch(`/api/fetch_surface_area?${params}`);

        if (!response.ok) {
            throw new Error(`Fehler beim Abfragen von /api/fetch_surface_area: ${response.status}`);
        }

        const data = await response.json();
        surfaceAreaNode.textContent = data.area ?? "-";
    } catch (error) {
        console.error(`Fehler beim Abfragen der Fläche: ${error}`);
        surfaceAreaNode.textContent = "-";
    }
}