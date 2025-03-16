function escapeHtml(text) {
      if (!text) return "";
      return text
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }

    document.addEventListener("DOMContentLoaded", function () {
      const role = localStorage.getItem("userRole");
      const container = document.getElementById("manage-list");

      if (role !== "admin") {
        container.innerHTML = "<p style='color:white;'>Only administrators can access this page.</p>";
        return;
      }

      // Get all performances
      fetch("https://viva-dgzv.onrender.com/api/get_all_show_details/")
        .then(res => res.json())
        .then(data => {
          let html = "";
          data.forEach(show => {
            html += `
              <form class="show-form" onsubmit="submitForm(event, ${show.s_id})" id="form-${show.s_id}">
                <h4>Show ID: ${show.s_id}</h4>
                <input type="text" name="s_name" placeholder="Show Name" value="${escapeHtml(show.s_name)}" required>
                <input type="text" name="actor" placeholder="Artist" value="${escapeHtml(show.actor)}" required>
                <input type="date" name="date" value="${escapeHtml(show.date)}" required>
                <input type="text" name="address" placeholder="Address" value="${escapeHtml(show.address)}" required>
                <input type="text" name="genre" placeholder="Genre" value="${escapeHtml(show.genre)}">
                <input type="text" name="link" placeholder="Link" value="${escapeHtml(show.link)}">
                <input type="text" name="picture" placeholder="Picture" value="${escapeHtml(show.picture)}">
                <textarea name="description" placeholder="Description">${escapeHtml(show.description || '')}</textarea>
                <button type="submit">Save changes</button>
                <button type="button" onclick="deleteShow(${show.s_id})" style="margin-left:10px;">Delete a show</button>

              </form>
            `;
          });

          let addHtml = `
            <form class="show-form" onsubmit="submitNewShow(event)">
              <h4>Add new performances</h4>
              <input type="text" name="s_name" placeholder="Show Name" required>
              <input type="text" name="actor" placeholder="Artist" required>
              <input type="date" name="date" required>
              <input type="text" name="address" placeholder="Address" required>
              <input type="text" name="genre" placeholder="Genre">
              <input type="text" name="link" placeholder="Link">
              <input type="text" name="picture" placeholder="Picture">
              <textarea name="description" placeholder="Description"></textarea>
              <button type="submit">Add a show</button>
            </form>
          `;
          html = addHtml + html;

          container.innerHTML = html;
        });
    });

    function submitForm(event, showId) {
      event.preventDefault();

      const form = document.getElementById(`form-${showId}`);
      const formData = new FormData(form);
      const data = {
        s_id: showId,
        s_name: formData.get('s_name'),
        actor: formData.get('actor'),
        date: formData.get('date'),
        address: formData.get('address'),
        genre: formData.get('genre'),
        link: formData.get('link'),
        picture: formData.get('picture'),
        description: formData.get('description')
      };

      fetch("https://viva-dgzv.onrender.com/api/update_show/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
      .then(res => res.json())
      .then(response => {
        alert(response.message);
      })
      .catch(err => {
        console.error("Update failed", err);
        alert("Failed to save, please try again");
      });
    }

    function deleteShow(showId) {
      if (!confirm("Are you sure you want to delete this performance information?")) return;

      fetch(`https://viva-dgzv.onrender.com/api/delete_show/?s_id=${showId}`, {
        method: "DELETE"
      })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        location.reload(); // Refresh the page after deleting
      });
    }

    function submitNewShow(event) {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const data = {
        s_name: formData.get('s_name'),
        actor: formData.get('actor'),
        date: formData.get('date'),
        address: formData.get('address'),
        genre: formData.get('genre'),
        link: formData.get('link'),
        picture: formData.get('picture'),
        description: formData.get('description')
      };

      fetch("https://viva-dgzv.onrender.com/api/create_show/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
      .then(res => res.json())
      .then(response => {
        alert(response.message);
        location.reload(); // Refresh the page after adding
      });
    }