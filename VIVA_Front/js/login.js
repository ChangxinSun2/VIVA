document.getElementById('login-btn').addEventListener('click', function(event) {
        event.preventDefault();

        let username = document.getElementById('login-username').value;
        let password = document.getElementById('login-password').value;

        if (!username || !password) {
            document.getElementById('login-error-msg').textContent = "Please enter username and password!";
            document.getElementById('login-error-msg').style.display = "block";
            return;
        }

        fetch("https://viva-dgzv.onrender.com/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {

                alert("Login successful!");
                // Storing tokens and roles
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("role", data.role);  // The backend needs to return the role field
                localStorage.setItem("userId", data.user_id);


                // Jump to page based on role
                if (data.role === "admin") {
                    window.location.href = "admin_index.html";
                    localStorage.setItem("userRole", "admin");
                } else if (data.role === "user") {
                    window.location.href = "user_index.html";
                    localStorage.setItem("userRole", "user");
                } else {
                    window.location.href = "index.html";  // fallback
            }

            } else {
                document.getElementById('login-error-msg').textContent = data.error || "Login failed!";
                document.getElementById('login-error-msg').style.display = "block";
            }
        })
        .catch(error => {
            document.getElementById('login-error-msg').textContent = "Error: " + error;
            document.getElementById('login-error-msg').style.display = "block";
        });
    });