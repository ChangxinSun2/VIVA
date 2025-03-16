$(document).ready(function () {
    $('#filter-date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
        clearBtn: true,
        orientation: "bottom left",
        startDate: new Date()
    }).on("changeDate", function () {
        loadShows();  // Automatically triggered after the user selects a date
    });

    // Encapsulate the loading performance function
    function loadShows() {
        const selectedDate = document.getElementById('filter-date').value;
        const selectedLocation = document.getElementById('filter-location').value;

        let url = "https://viva-dgzv.onrender.com/api/get_shows/?";
        if (selectedDate && selectedDate.trim().length === 10) {
            url += `date=${selectedDate}&`;
        }
        if (selectedLocation && selectedLocation !== "null") {
            url += `address=${selectedLocation}`;
        }

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const eventList = document.getElementById("event-list");
                eventList.innerHTML = "";

                if (data.length === 0) {
                    eventList.innerHTML = '<p style="color:white;">No events found.</p>';
                    return;
                }

                data.forEach(show => {
                    const eventCard = `
                                <div class="col-md-4">
                                    <div class="event-card">
                                        <a href="show_detail.html?id=${show.s_id}">
                                            <img src="${show.picture}" alt="${show.s_name}">
                                        </a>
                                        <h3><a href="#">${show.s_name}</a></h3>
                                        <p>Artist: ${show.actor}</p>
                                        <p>Date: ${show.date}</p>
                                        <p>Location: ${show.address}</p>
                                    </div>
                                </div>
                            `;
                    eventList.innerHTML += eventCard;
                });
            })
            .catch(error => {
                console.error("Error fetching shows:", error);
            });
    }

    // Initial load of all shows
    loadShows();
    document.getElementById("filter-location").addEventListener("change", loadShows);
    // document.getElementById("filter-date").addEventListener("change", loadShows);


    $.ajax({
        url: "/api/get_locations/",
        method: "GET",
        success: function (data) {
            let locations = data.locations;
            locations.forEach(loc => {
                $("#filter-location").append(`<option value="${loc}">${loc}</option>`);
            });
        }
    });
});