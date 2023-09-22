// Get the search input element
const searchInput = document.getElementById('search_query');

// Define an array of suggested keywords
const suggestedKeywords = ['AI', 'ML', 'Data Science', 'Cloud Computing', 'Fiction', 'Cybersecurity'];

// Get the datalist element for suggestions
const datalist = document.getElementById('keywords');

// Function to update the suggestions
function updateSuggestions() {
    // Clear existing suggestions
    datalist.innerHTML = '';

    // Get the user's input
    const userInput = searchInput.value.toLowerCase();

    // Filter and add matching suggestions
    suggestedKeywords.forEach((keyword) => {
        if (keyword.toLowerCase().includes(userInput)) {
            const option = document.createElement('option');
            option.value = keyword;
            datalist.appendChild(option);
        }
    });
}

// Add an event listener to update suggestions when the user types
searchInput.addEventListener('input', updateSuggestions);

// Event listener for when the input gains focus
searchInput.addEventListener('focus', function () {
    updateSuggestions(); // Update suggestions when the input gains focus
});

// Event listener for when the input loses focus
searchInput.addEventListener('blur', function () {
    datalist.innerHTML = ''; // Clear suggestions when the input loses focus
});
