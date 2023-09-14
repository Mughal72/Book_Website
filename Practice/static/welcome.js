
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


// Wait for the DOM to be fully loaded before running the JavaScript
document.addEventListener("DOMContentLoaded", function() {
    // Initialize slideIndex
    let slideIndex = 0;

    // Call the showSlides function to start the slideshow
    showSlides();

    function showSlides() {
        // Get all elements with the class "book-slide"
        let slides = document.getElementsByClassName("book-slide");

        // Hide all slides by default
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        // Increment slideIndex
        slideIndex++;

        // Reset slideIndex if it exceeds the number of slides
        if (slideIndex > slides.length) {
            slideIndex = 1;
        }

        // Display the current slide
        slides[slideIndex - 1].style.display = "block";

        // Change slide every 5 seconds
        setTimeout(showSlides, 5000);
    }
});


