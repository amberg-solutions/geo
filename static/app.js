document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    document.getElementById("map-search").addEventListener("submit", (event) => {
        event.preventDefault();
    });

    fetchHtmlMap();
});

async function fetchHtmlMap() {
    const mapNode = document.getElementById("map");
    const loadingNode = document.getElementById("map-loading");
    const statusNode = document.getElementById("map-status");

    try {
        const response = await fetch("/get_map");

        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen von /get_map: ${response.status}`);
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