document.addEventListener('DOMContentLoaded', function () {
    // Check if the cookie is present
    var hasSeenNotice = getCookie('developmentNotice');

    // If the cookie is not present, show the notice
    if (!hasSeenNotice) {
        // Create overlay container
        var overlayContainer = document.createElement('div');
        overlayContainer.id = 'overlay-container';
        overlayContainer.className = 'overlay-container overlay-hidden';

        // Create notice text
        var noticeText = document.createElement('div');
    noticeText.innerHTML = `
        <h1>Thank you for visiting <span style="color: #006fff">BlueMoon AI!</span> 👻</h1>
        <p>If you encounter any issues or bugs, please report them <a style="color:rgba(2,103,236,0.99);" href="https://github.com/BlueMoonAI/BlueMoonAI/issues" target="_blank">here</a>.</p>
    `;

        // Create hCaptcha div
        var hcaptchaDiv = document.createElement('div');
        hcaptchaDiv.id = 'h-captcha';
        hcaptchaDiv.className = 'h-captcha';
        hcaptchaDiv.dataset.sitekey = 'b50264bc-96c7-46cd-8860-f0a846bce551';

        // Create verify button
        var verifyButton = document.createElement('button');
        verifyButton.textContent = 'Verify';
        verifyButton.onclick = verifyAndHideNotice;
        verifyButton.className = 'verify-button';

        // Create verification message
        var verificationMessage = document.createElement('p');
        verificationMessage.className = 'verification-message';

        // Create hCaptcha script
        var hcaptchaScript = document.createElement('script');
        hcaptchaScript.src = 'https://js.hcaptcha.com/1/api.js';
        hcaptchaScript.async = true;
        hcaptchaScript.defer = true;

        // Apply inline styles
        overlayContainer.style.position = 'fixed';
        overlayContainer.style.top = '0';
        overlayContainer.style.left = '0';
        overlayContainer.style.width = '100%';
        overlayContainer.style.height = '100%';
        overlayContainer.style.display = 'flex';
        overlayContainer.style.flexDirection = 'column';
        overlayContainer.style.alignItems = 'center';
        overlayContainer.style.justifyContent = 'center';
        overlayContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        overlayContainer.style.zIndex = '999';
        overlayContainer.style.backdropFilter = 'blur(10px)'; // Adjust the blur level as needed

        noticeText.style.textAlign = 'center';
        noticeText.style.color = '#fff';
        noticeText.style.zIndex = '9999';

        hcaptchaDiv.style.marginTop = '20px';

        verificationMessage.style.color = 'red'; // Red color for the verification message
        verificationMessage.style.marginTop = '10px';
        verificationMessage.style.display = 'none'; // Initially hide the message

        verifyButton.style.background = 'linear-gradient(to right, #3498db, #2ecc71)'; // Gradient blue color for the button
        verifyButton.style.color = '#ffffff'; // White text color
        verifyButton.style.border = 'none';
        verifyButton.style.padding = '10px 20px';
        verifyButton.style.borderRadius = '5px';
        verifyButton.style.cursor = 'pointer';
        verifyButton.style.marginTop = '10px';

        // Append elements to overlay container
        overlayContainer.appendChild(noticeText);
        overlayContainer.appendChild(hcaptchaDiv);
        overlayContainer.appendChild(verifyButton);
        overlayContainer.appendChild(verificationMessage);
        overlayContainer.appendChild(hcaptchaScript);

        // Append overlay container to the document body
        document.body.appendChild(overlayContainer);

        // Show the overlay when the page is loaded
        overlayContainer.classList.remove('overlay-hidden');
    }
});

function verifyAndHideNotice() {
    var hcaptchaResponse = document.getElementById('h-captcha').querySelector('textarea').value;
    var verificationMessage = document.querySelector('.verification-message');

    if (hcaptchaResponse) {
        // Perform hCaptcha verification on the server-side if needed

        // Set a cookie to remember that the notice has been seen
        setCookie('developmentNotice', 'true', 365); // Cookie lasts for 365 days

        // Hide the overlay
        var overlayContainer = document.getElementById('overlay-container');
        overlayContainer.classList.add('overlay-hidden');

        // Refresh the page after successful verification
        window.location.reload();
    } else {
        // Show an error message or take appropriate action if hCaptcha is not verified
        verificationMessage.textContent = 'Please complete hCaptcha verification.';
        verificationMessage.style.display = 'block'; // Display the message
    }
}


// Function to set a cookie
function setCookie(name, value, days) {
    var expires = '';
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

// Function to get the value of a cookie
function getCookie(name) {
    var nameEQ = name + '=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
