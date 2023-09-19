const formOpenBtn = document.querySelector("#form-open"),
  home = document.querySelector(".home"),
  formContainer = document.querySelector(".form_container"),
  formCloseBtn = document.querySelector(".form_close"),
  signupBtn = document.querySelector("#signup"),
  loginBtn = document.querySelector("#login"),
  pwShowHide = document.querySelectorAll(".pw_hide");

formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));

pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});

signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
});
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
});


// JavaScript for Featured Books Slider
const sliderContent = document.querySelector(".slider-content");
const prevBtn = document.getElementById("prev-btn");
const nextBtn = document.getElementById("next-btn");
const featuredBooks = document.querySelectorAll(".featured-book");
const booksPerPage = 5; // Number of books to display per page
let currentPage = 1;

// Next Button Click
nextBtn.addEventListener("click", () => {
    if (currentPage < Math.ceil(featuredBooks.length / booksPerPage)) {
        currentPage++;
        updateSlider();
    }
});

// Previous Button Click
prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        updateSlider();
    }
});

// Update Slider Position
function updateSlider() {
    const startIndex = (currentPage - 1) * booksPerPage;
    const endIndex = startIndex + booksPerPage;

    // Hide all books
    featuredBooks.forEach((book, index) => {
        if (index >= startIndex && index < endIndex) {
            book.style.display = "block"; // Display books in the current page
        } else {
            book.style.display = "none"; // Hide other books
        }
    });
}

// Initial Slider Update
updateSlider();
