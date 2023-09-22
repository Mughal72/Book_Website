
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get('username');
        if (username) {
            const usernameElement = document.getElementById('username');
            usernameElement.textContent = username;
        }

        const usernameElement = document.getElementById('username');
        if (usernameElement) {
            // Hide username after 4 seconds
            setTimeout(() => {
                usernameElement.style.visibility = 'hidden';
            }, 4000);
        }

function toggleDropdown() {
            var dropdown = document.getElementById("myDropdown");
            dropdown.classList.toggle("show");
        }

        window.onclick = function(event) {
            if (!event.target.matches('.dropbtn')) {
                var dropdowns = document.getElementsByClassName("dropdown-content");
                for (var i = 0; i < dropdowns.length; i++) {
                    var openDropdown = dropdowns[i];
                    if (openDropdown.classList.contains('show')) {
                        openDropdown.classList.remove('show');
                    }
                }
            }
        }


// JavaScript for Recommended Books Slider
const recommendedSliderContent = document.querySelector(".recommended-slider .slider-content");
const prevRecommendedBtn = document.getElementById("prev-recommended-btn");
const nextRecommendedBtn = document.getElementById("next-recommended-btn");
const recommendedBooks = document.querySelectorAll(".recommended-book");
const booksPerPageRecommended = 5; // Number of recommended books to display per page
let currentPageRecommended = 1;

// Next Button Click
nextRecommendedBtn.addEventListener("click", () => {
    if (currentPageRecommended < Math.ceil(recommendedBooks.length / booksPerPageRecommended)) {
        currentPageRecommended++;
        updateRecommendedSlider();
    }
});

// Previous Button Click
prevRecommendedBtn.addEventListener("click", () => {
    if (currentPageRecommended > 1) {
        currentPageRecommended--;
        updateRecommendedSlider();
    }
});

// Update Recommended Slider Position
function updateRecommendedSlider() {
    const startIndex = (currentPageRecommended - 1) * booksPerPageRecommended;
    const endIndex = startIndex + booksPerPageRecommended;

    // Hide all recommended books
    recommendedBooks.forEach((book, index) => {
        if (index >= startIndex && index < endIndex) {
            book.style.display = "block"; // Display recommended books in the current page
        } else {
            book.style.display = "none"; // Hide other recommended books
        }
    });
}

// Generate a random price between $10 and $50
function generateRandomPrice() {
    const minPrice = 10;
    const maxPrice = 50;
    return (Math.random() * (maxPrice - minPrice) + minPrice).toFixed(2);
}

// Initial Recommended Slider Update
updateRecommendedSlider();



