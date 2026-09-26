(function () {
    "use strict";

    // ----- live search filtering (client-side, no reload) -----
    var input = document.getElementById("search-input");
    var list = document.getElementById("record-list");
    var noResults = document.getElementById("no-results");

    function normalise(text) {
        return (text || "").toLowerCase();
    }

    if (input && list) {
        input.addEventListener("input", function () {
            var keyword = normalise(input.value.trim());
            var items = list.querySelectorAll("li[data-date]");
            var visibleCount = 0;

            items.forEach(function (li) {
                var haystack = [
                    li.getAttribute("data-date"),
                    li.getAttribute("data-diagnosis"),
                    li.getAttribute("data-prescription"),
                    li.getAttribute("data-comments")
                ].join(" ").toLowerCase();

                var matches = keyword === "" || haystack.indexOf(keyword) !== -1;
                li.style.display = matches ? "" : "none";
                if (matches) visibleCount += 1;
            });

            if (noResults) {
                noResults.style.display = (visibleCount === 0 && items.length > 0) ? "block" : "none";
            }
        });
    }

    // ----- add-record panel toggle -----
    var panel = document.getElementById("add-record-panel");
    var cancelBtn = document.getElementById("cancel-add");

    function openPanel() {
        if (panel) panel.classList.add("open");
    }
    function closePanel() {
        if (panel) panel.classList.remove("open");
        if (history.replaceState) {
            history.replaceState(null, "", window.location.pathname + window.location.search);
        }
    }

    // The top bar's "+ Add New Record" link points at #add-record.
    document.querySelectorAll('a[href$="#add-record"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            if (panel) {
                event.preventDefault();
                openPanel();
                panel.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    if (window.location.hash === "#add-record") {
        openPanel();
    }

    if (cancelBtn) {
        cancelBtn.addEventListener("click", closePanel);
    }
})();
