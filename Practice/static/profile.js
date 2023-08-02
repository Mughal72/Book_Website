// Function to handle profile update
function updateProfile() {
    // Get the form element
    var profileForm = document.getElementById('profile-form');

    // Create a FormData object to store the user data
    var formData = new FormData(profileForm);

    // Send the form data to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/profile', true); // Use the correct route for updating the profile

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Redirect to the "welcome" page after successfully updating the profile
                window.location.href = '/welcome';
            } else {
                // Display error message
                alert('Error saving user information. Please try again.');
                console.error(xhr.statusText); // Print the status text for debugging
            }
        }
    };

    xhr.send(formData); // Send the FormData object
}

// Bind the updateProfile function to the save button
document.getElementById('save-btn').addEventListener('click', function () {
    updateProfile();
});
