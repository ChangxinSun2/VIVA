
document.addEventListener("DOMContentLoaded", function () {
      const userId = localStorage.getItem("userId");
      const role = localStorage.getItem("userRole");
      const listContainer = document.getElementById("favorites-list");

      if (!userId || (role !== "user" && role !== "admin")) {
        listContainer.innerHTML = "<p style='color:white;'>Please log in to view your favorites.</p>";
        return;
      }

      fetch(`https://viva-dgzv.onrender.com/api/get_user_favorites/?user_id=${userId}`)
        .then(res => res.json())
        .then(data => {
          if (data.results.length === 0) {
            listContainer.innerHTML = "<p style='color:white;'>There are currently no favorite performances.</p>";
            return;
          }

          let html = "";
          data.results.forEach(show => {
            html += `
              <div class="favorite-item">
                <a href="show_detail.html?id=${show.id}" style="text-decoration:none; color: white;">
                  <img src="${show.picture}" alt="${show.s_name}">
                  <h4>${show.s_name}</h4>
                  <p><strong>Artist:</strong> ${show.actor}</p>
                  <p><strong>Date:</strong> ${show.date}</p>
                  <p><strong>Location:</strong> ${show.address}</p>
                </a>
              </div>
            `;
          });

          listContainer.innerHTML = html;
        })
        .catch(err => {
          console.error("Error loading favorites:", err);
          listContainer.innerHTML = "<p style='color:white;'>Loading failed, please try again later.</p>";
        });
    });