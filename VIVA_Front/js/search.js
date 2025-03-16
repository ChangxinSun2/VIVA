document.addEventListener("DOMContentLoaded", function () {
    const searchBtn = document.querySelector(".search-btn");
    const searchBox = document.getElementById("search-box");
    const resultsList = document.getElementById("search-results");

    searchBtn.addEventListener("click", function () {
        const query = searchBox.value.trim();
        if (!query) return;

        fetch(`https://viva-dgzv.onrender.com/api/search_show/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsList.innerHTML = "";

                if (data.results.length === 0) {
                    resultsList.innerHTML = "<li class='search-item'>No results found.</li>";
                    return;
                }

                data.results.forEach(show => {
                    const item = document.createElement("li");
                    item.classList.add("search-item");

                    item.innerHTML = `
                  <a href="show_detail.html?id=${show.id}" style="text-decoration: none; color: white;">
                    <img src="${show.picture}" alt="Show Image" style="max-width: 200px; border-radius: 10px;">
                    <h4 style="margin:10px 0;">${show.s_name}</h4>
                    <p><strong>Artist:</strong> ${show.actor}</p>
                    <p><strong>Date:</strong> ${show.date}</p>
                    <p><strong>Location:</strong> ${show.address}</p>
                  </a>
                `;
                    resultsList.appendChild(item);
                });
            })
            .catch(err => {
                console.error("Search error:", err);
                resultsList.innerHTML = "<li class='search-item'>Search failed. Please try again.</li>";
            });
    });

    // Support search by pressing Enter
    searchBox.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            searchBtn.click();
        }
    });
});