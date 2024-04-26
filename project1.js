function validateForm(event) {
    event.preventDefault();
    
    var name = document.getElementById('name').value;
    console.log('Name value:', name);
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    
    // Whitelisting: Only letters and spaces are allowed in the name
    var nameRegex = /^[a-zA-Z\s]*$/;
if (!nameRegex.test(name)) {
        displayAlert('Oops! It looks like there might be some invalid characters in the name. Please only use letters and spaces.');
        return;
    }
    
    // Blacklisting: Check if email contains common invalid characters
    var invalidEmailChars = /[<>]/;
    if (invalidEmailChars.test(email)) {
        displayAlert('Invalid email. Please remove any invalid characters.');
        return;
    }
    
    // Phone number validation: Should be exactly 10 digits and not contain special characters
    var phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(phone)) {
        displayAlert('Invalid phone number. Please enter exactly 10 numeric digits without any special characters.');
        return;
    }
    
    // Server-side validation and session management would typically be handled using backend code
    // Here, we're simulating server-side processing by logging the form data
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Phone:', phone);
    
    // Clear form fields after submission
    document.getElementById('bookingForm').reset();
}


function displayAlert(message) {
    var modal = document.getElementById('modal');
    var alertMessage = document.getElementById('alertMessage');
    alertMessage.textContent = message;
    modal.style.display = 'block';
    
    // When the user clicks on <span> (x), close the modal
    var closeBtn = document.getElementsByClassName('close')[0];
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}
