// ===============================
// Weather App JavaScript
// ===============================

// Dark Mode Toggle
const themeBtn = document.getElementById("themeBtn");

if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        const icon = themeBtn.querySelector("i");

        if (document.body.classList.contains("dark")) {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        } else {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        }
    });
}

// Display Current Date and Time
const dateElement = document.getElementById("date");

function updateDateTime() {
    const now = new Date();

    const options = {
        weekday: "long",
        hour: "numeric",
        minute: "2-digit"
    };

    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString("en-US", options);
    }
}

updateDateTime();
setInterval(updateDateTime, 60000);

// Search Button
const searchButton = document.querySelector(".search-box button");
const searchInput = document.querySelector(".search-box input");

if (searchButton && searchInput) {
    searchButton.addEventListener("click", () => {
        const city = searchInput.value.trim();

        if (city === "") {
            alert("Please enter a city name.");
            return;
        }

        alert(`Searching weather for ${city}...`);
    });
}