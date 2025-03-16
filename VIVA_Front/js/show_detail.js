function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

document.addEventListener("DOMContentLoaded", function () {
    const showId = getQueryParam('id');
    if (!showId) {
        document.body.innerHTML = "<h2>Missing Show ID</h2>";
        return;
    }

    const userId = localStorage.getItem("userId");
    const role = localStorage.getItem("userRole");
    let isFavorite = false;

    // Loading details
    fetch(`https://viva-dgzv.onrender.com/api/show_detail/?id=${showId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.body.innerHTML = `<h2>${data.error}</h2>`;
                return;
            }

            const html = `
              <img src="${data.picture}" alt="Show Image" class="show-img">
              <div class="show-title">${data.s_name}</div>
              <div class="show-info"><strong>Artist:</strong> ${data.actor}</div>
              <div class="show-info"><strong>Date:</strong> ${data.date}</div>
              <div class="show-info"><strong>Location:</strong> ${data.address}</div>
              <div class="show-info"><strong>Genre:</strong> ${data.genre}</div>
              <div class="show-description"><strong>Description:</strong> ${data.description}</div>
              <a href="${data.link}" class="ticket-link" target="_blank">Go to Event Link</a>
              <a href="#" id="fav-btn" class="favorite-btn"><i class="fa fa-heart"></i> Collect</a>
            `;
            document.getElementById("show-detail").innerHTML = html;

            // After the page is loaded, first determine whether it has been collected
            if (userId && (role === "user" || role === "admin")) {
                fetch(`https://viva-dgzv.onrender.com/api/check_favorite/?user_id=${userId}&show_id=${showId}`)
                    .then(res => res.json())
                    .then(favData => {
                        if (favData.favorited) {
                            isFavorite = true;
                            const favBtn = document.getElementById("fav-btn");
                            favBtn.classList.add("active");
                            favBtn.innerHTML = '<i class="fa fa-heart"></i> Collected';
                        }
                    });
            }

            // Click the button to toggle state
            document.getElementById("fav-btn").addEventListener("click", function (e) {
                e.preventDefault();

                if (!userId || (role !== "user" && role !== "admin")) {
                    alert("Collection failed, please log in first");
                    return;
                }

                if (!isFavorite) {
                    // Add to favorites
                    fetch("https://viva-dgzv.onrender.com/api/add_favorite/", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({user_id: userId, show_id: showId})
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === "added") {
                                isFavorite = true;
                                const favBtn = document.getElementById("fav-btn");
                                favBtn.classList.add("active");
                                favBtn.innerHTML = '<i class="fa fa-heart"></i> Collected';
                                alert("Successfully collected");
                            }
                        });
                } else {
                    // Remove from favorite
                    fetch(`https://viva-dgzv.onrender.com/api/remove_favorite/?user_id=${userId}&show_id=${showId}`, {
                        method: "DELETE"
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === "removed") {
                                isFavorite = false;
                                const favBtn = document.getElementById("fav-btn");
                                favBtn.classList.remove("active");
                                favBtn.innerHTML = '<i class="fa fa-heart"></i> Collect';
                                alert("Successfully canceled the collection");
                            }
                        });
                }
            });
        });
});