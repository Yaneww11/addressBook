document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-bar");
    const categoryFilter = document.getElementById("filter-options");
    const sortOptions = document.getElementById("sort-options");
    const contactsContainer = document.getElementById("contacts-container");
    const paginatorContainer = document.getElementById("paginator-container");

    // Function to send AJAX requests to the backend
    const updateContacts = () => {
        const searchTerm = searchInput.value;
        const selectedCategory = categoryFilter.value;
        const sortOption = sortOptions.value;

        // Create query parameters
        const params = new URLSearchParams({
            search: searchTerm,
            category: selectedCategory,
            sort: sortOption,
        });

        // Send the AJAX request
        fetch(`?${params.toString()}`, {
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

                    // Update pagination links
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
                const url = link.getAttribute("href");
                if (url) {
                    fetchPage(url);
                }
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
                    contactsContainer.innerHTML = data.contacts_html;
                    paginatorContainer.innerHTML = data.paginator_html;

                    // Reattach pagination links
                    setupPaginationLinks();
                }
            })
            .catch(error => console.error("Error fetching page:", error));
    };

    // Initialize pagination links
    setupPaginationLinks();
});
