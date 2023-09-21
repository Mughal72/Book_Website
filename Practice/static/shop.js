const wrapper = document.querySelector(".sliderWrapper");
const menuItems = document.querySelectorAll(".menuItem");

const products = [
  {
    id: 1,
    title: "Air Force",
    price: 119,
    colors: [
      {
        code: "black",
        img: "./img/air.png",
      },
      {
        code: "darkblue",
        img: "./img/air2.png",
      },
    ],
  },
  {
    id: 2,
    title: "Air Jordan",
    price: 149,
    colors: [
      {
        code: "lightgray",
        img: "./img/jordan.png",
      },
      {
        code: "green",
        img: "./img/jordan2.png",
      },
    ],
  },
  {
    id: 3,
    title: "Blazer",
    price: 109,
    colors: [
      {
        code: "lightgray",
        img: "./img/blazer.png",
      },
      {
        code: "green",
        img: "./img/blazer2.png",
      },
    ],
  },
  {
    id: 4,
    title: "Crater",
    price: 129,
    colors: [
      {
        code: "black",
        img: "./img/crater.png",
      },
      // {
      //   code: "lightgray",
      //   img: "./img/crater2.png",

      // },
    ],
  },
  {
    id: 5,
    title: "Hippie",
    price: 99,
    colors: [
      {
        code: "gray",
        img: "./img/hippie.png",
      },
      {
        code: "black",
        img: "./img/hippie2.png",
      },
    ],
  },
];

let choosenProduct = products[0];

const currentProductImg = document.querySelector(".productImg");
const currentProductTitle = document.querySelector(".productTitle");
const currentProductPrice = document.querySelector(".productPrice");
const currentProductColors = document.querySelectorAll(".color");
const currentProductSizes = document.querySelectorAll(".size");

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    //change the current slide
    wrapper.style.transform = `translateX(${-100 * index}vw)`;

    //change the choosen product
    choosenProduct = products[index];

    //change texts of currentProduct
    currentProductTitle.textContent = choosenProduct.title;
    currentProductPrice.textContent = "$" + choosenProduct.price;
    currentProductImg.src = choosenProduct.colors[0].img;

    //assing new colors
    currentProductColors.forEach((color, index) => {
      color.style.backgroundColor = choosenProduct.colors[index].code;
    });
  });
});

currentProductColors.forEach((color, index) => {
  color.addEventListener("click", () => {
    currentProductImg.src = choosenProduct.colors[index].img;
  });
});

currentProductSizes.forEach((size, index) => {
  size.addEventListener("click", () => {
    currentProductSizes.forEach((size) => {
      size.style.backgroundColor = "white";
      size.style.color = "black";
    });
    size.style.backgroundColor = "black";
    size.style.color = "white";
  });
});


//buy now (payment method) script

const productButton = document.querySelector(".productButton");
const payment = document.querySelector(".payment");
const close = document.querySelector(".close");

productButton.addEventListener("click", () => {
  payment.style.display = "flex";
});

close.addEventListener("click", () => {
  payment.style.display = "none";
});


//for new release (payment method)button
// JavaScript
const productBtn = document.querySelectorAll(".productBtn");
const payForm = document.querySelectorAll(".pay");
const closeBtn = document.querySelectorAll(".Close");

productBtn.forEach((productBtn) => {
  productBtn.addEventListener("click", () => {
    // Get the data-book attribute to identify the corresponding payment form
    const bookId = productBtn.getAttribute("data-book");

    // Hide all payment forms
    payForm.forEach((payForm) => {
      payForm.style.display = "none";
    });

    // Show the payment form corresponding to the clicked book
    const selectedPayForm = document.querySelector(`.pay[data-book="${bookId}"]`);
    selectedPayForm.style.display = "flex";
  });
});

closeBtn.forEach((closeBtn) => {
  closeBtn.addEventListener("click", () => {
    // Hide the parent payment form when the close button is clicked
    const payForm = closeBtn.parentElement;
    payForm.style.display = "none";
  });
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

//Read more button script
document.addEventListener("DOMContentLoaded", function() {
    const descriptions = document.querySelectorAll(".description");
    const readMoreBtns = document.querySelectorAll(".read-more-btn");

    readMoreBtns.forEach(function(btn, index) {
        let expanded = false;

        btn.addEventListener("click", function() {
            if (!expanded) {
                // Expand the description
                descriptions[index].style.maxHeight = "none";
                btn.textContent = "Read Less";
            } else {
                // Collapse the description
                descriptions[index].style.maxHeight = "80px"; // Adjust to the initial max height
                btn.textContent = "Read More";
            }

            expanded = !expanded;
        });
    });
});


//review from script
document.addEventListener("DOMContentLoaded", function() {
    const reviewForm = document.getElementById("add-review-form");
    const reviewList = document.querySelector(".review-list");

    reviewForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const rating = document.getElementById("rating").value;
        const comment = document.getElementById("comment").value;

        // Create a new review element
        const review = document.createElement("div");
        review.classList.add("review");

        // Build the review content
        review.innerHTML = `
            <div class="user-info">
                <img src="https://w7.pngwing.com/pngs/81/570/png-transparent-profile-logo-computer-icons-user-user-blue-heroes-logo-thumbnail.png" alt="${name}" class="fIcon">
                <p>${name}</p>
            </div>
            <div class="rating">
                ${generateRatingStars(rating)}
            </div>
            <p class="review-text">${comment}</p>
        `;

        // Append the review to the review list
        reviewList.appendChild(review);

        // Reset the form
        reviewForm.reset();
    });

    // Function to generate star icons based on the rating
    function generateRatingStars(rating) {
        const filledStars = '<span class="star">&#9733;</span>'.repeat(rating);
        const emptyStars = '<span class="star">&#9734;</span>'.repeat(5 - rating);
        return filledStars + emptyStars;
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("email-error");

    emailInput.addEventListener("input", function() {
        // Regular expression for email validation
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

        if (emailPattern.test(emailInput.value)) {
            // Email is valid
            emailInput.classList.remove("invalid");
            emailInput.classList.add("valid");
            emailError.textContent = ""; // Clear any previous error message
        } else {
            // Email is invalid
            emailInput.classList.remove("valid");
            emailInput.classList.add("invalid");
            emailError.textContent = "Please enter a valid email address.";
        }
    });
});
