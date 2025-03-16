document.addEventListener("DOMContentLoaded", function () {
        const role = localStorage.getItem("userRole");

        // Automatically jump to the identity homepage
        if (role === "admin" && !window.location.href.includes("admin_index")) {
          window.location.href = "admin_index.html";
        } else if (role === "user" && !window.location.href.includes("user_index")) {
          window.location.href = "user_index.html";
        }
      });

<!-- Dynamically load the first 8 pictures and jump to the details page -->
document.addEventListener("DOMContentLoaded", function () {
    fetch("https://viva-dgzv.onrender.com/api/featured_shows/")
      .then(res => res.json())
      .then(data => {
        let html = "";
        data.forEach(show => {
          html += `
            <div class="col-lg-3 col-md-6 col-sm-6 work">
              <a href="show_detail.html?id=${show.s_id}" class="work-box">
                <div class="gallery-box">
                  <img src="${show.picture}" alt="${show.s_name}" class="gallery-image">
                </div>
                <div class="overlay">
                  <div class="overlay-caption">
                    <p><span class="icon icon-magnifying-glass"></span></p>
                  </div>
                </div>
              </a>
            </div>
          `;
        });
        document.getElementById("dynamic-gallery").innerHTML = html;
      })
      .catch(err => {
        console.error("Failed to load featured shows:", err);
      });
  });

document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("cform");
        const modal = document.getElementById("messageModal");
        const modalMessage = document.getElementById("modalMessage");
        const closeBtn = document.querySelector(".close-btn");

        modal.style.display = "none";

        form.addEventListener("submit", function (event) {
            event.preventDefault();

            let name = document.getElementById("name").value.trim();
            let email = document.getElementById("email").value.trim();
            let message = document.getElementById("comments").value.trim();

            if (name === "") {
                modalMessage.innerHTML = "❌ Please enter your name.";
                modal.style.display = "flex";
                return;
            }

            let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                modalMessage.innerHTML = "❌ Please enter a valid email.";
                modal.style.display = "flex";
                return;
            }

            if (message === "") {
                modalMessage.innerHTML = "❌ Please enter your message.";
                modal.style.display = "flex";
                return;
            }

            modalMessage.innerHTML = "✅ Message sent successfully!";
            modal.style.display = "flex";

            setTimeout(() => {
                modal.style.display = "none";
                form.reset();
            }, 5000);
        });

        closeBtn.addEventListener("click", function () {
            modal.style.display = "none";
            if (modalMessage.innerHTML.includes("✅")) {
                form.reset();
            }
        });

        window.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
                if (modalMessage.innerHTML.includes("✅")) {
                    form.reset();
                }
            }
        });
    });