document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-bar");
    const categoryFilter = document.getElementById("filter-options");
    const sortOptions = document.getElementById("sort-options");
    const contactsContainer = document.getElementById("contacts-container");
    const paginatorContainer = document.getElementById("paginator-container");

    let currentParams = new URLSearchParams(window.location.search); // Maintain current filter state

    // Function to send AJAX requests to the backend
    const updateContacts = () => {
        currentParams.set("search", searchInput.value);
        currentParams.set("category", categoryFilter.value);
        currentParams.set("sort", sortOptions.value);

        const filterUrl = `?${currentParams.toString()}`;

        fetch(filterUrl, {
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.contacts_html && data.paginator_html) {
                    // Update the DOM with the new data
                    contactsContainer.innerHTML = data.contacts_html;
                    paginatorContainer.innerHTML = data.paginator_html;

                    // Update the URL to reflect the new filter state
                    window.history.pushState({}, "", filterUrl);

                    // Reinitialize pagination links
                    setupPaginationLinks();
                }
            })
            .catch(error => console.error("Error fetching contacts:", error));
    };

    // Attach event listeners to inputs
    searchInput.addEventListener("input", updateContacts);
    categoryFilter.addEventListener("change", updateContacts);
    sortOptions.addEventListener("change", updateContacts);

    // Function to attach event listeners to paginator links
    const setupPaginationLinks = () => {
        const paginatorLinks = paginatorContainer.querySelectorAll("a");
        paginatorLinks.forEach(link => {
            link.addEventListener("click", event => {
                event.preventDefault();

                const pageUrl = new URL(link.href);
                const pageParams = new URLSearchParams(pageUrl.search);

                // Merge current filters with pagination parameters
                currentParams.forEach((value, key) => {
                    pageParams.set(key, value);
                });

                const fullUrl = `${pageUrl.pathname}?${pageParams.toString()}`;
                fetchPage(fullUrl);
            });
        });
    };

    // Function to handle pagination via AJAX
    const fetchPage = (url) => {
        fetch(url, {
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.contacts_html && data.paginator_html) {
                    // Update the DOM with the new data
                    contactsContainer.innerHTML = data.contacts_html;
                    paginatorContainer.innerHTML = data.paginator_html;

                    // Update the URL to reflect the current page and filters
                    window.history.pushState({}, "", url);

                    // Reinitialize pagination links
                    setupPaginationLinks();
                }
            })
            .catch(error => console.error("Error fetching page:", error));
    };

    // Initialize pagination links
    setupPaginationLinks();
});
