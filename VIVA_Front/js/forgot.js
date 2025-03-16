document.getElementById('forgot-btn').addEventListener('click', function (event) {
        event.preventDefault();

        let username = document.getElementById('username').value;
        let password = document.getElementById('password').value;
        let password2 = document.getElementById('password2').value;

        if (!username || !password || !password2) {
            alert("Please fill in all fields!");
            return;
        }

        if (password !== password2) {
            alert("The two passwords do not match!");
            return;
        }

        fetch("https://viva-dgzv.onrender.com/api/reset_password/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username, password: password, password2: password2 })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert("Password changed successfully!");
                window.location.href = "login.html";
            } else {
                alert("Modification failed:" + (data.error || "Unknown error"));
            }
        })
        .catch(err => {
            console.error("Request failed:", err);
            alert("Request failed");
        });
    });