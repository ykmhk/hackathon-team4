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

    function setBodyState(open) {
        document.body.classList.toggle('record-form-open', open);
    }

    function openPanel() {
        if (panel) panel.classList.add("open");
        setBodyState(true);
    }
    function closePanel() {
        if (panel) panel.classList.remove("open");
        setBodyState(false);
        if (history.replaceState) {
            history.replaceState(null, "", window.location.pathname + window.location.search);
        }
    }

    function syncAddState() {
        var shouldOpen = window.location.hash === '#add-record' || (window.location.search || '').indexOf('mode=add') !== -1;
        if (shouldOpen) {
            openPanel();
        } else {
            closePanel();
        }
    }

    // The top bar's "+ Add New Record" link points at #add-record.
    document.querySelectorAll('a[href$="#add-record"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            if (panel) {
                event.preventDefault();
                window.location.hash = 'add-record';
                openPanel();
                panel.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    syncAddState();

    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            closePanel();
            if (window.location.hash === '#add-record') {
                history.replaceState(null, "", window.location.pathname + window.location.search);
            }
        });
    }

    window.addEventListener('hashchange', syncAddState);
})();
