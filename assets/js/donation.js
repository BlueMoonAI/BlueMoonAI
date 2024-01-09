// Create a floating donation button dynamically
function createFloatingButton() {
    var button = document.createElement('button');
    button.id = 'donateButton';
    button.textContent = 'Donate';
    button.style.backgroundColor = '#3498db';
    button.style.color = '#fff';
    button.style.border = 'none';
    button.style.padding = '10px 20px';
    button.style.borderRadius = '50%';
    button.style.cursor = 'pointer';
    button.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.2)';
    button.style.position = 'fixed';
    button.style.bottom = '20px';
    button.style.right = '20px';
    button.style.zIndex = '999';

    document.body.appendChild(button);

    // Add event listener to redirect to Ko-fi link
    button.addEventListener('click', function() {
        window.location.href = 'https://ko-fi.com/bluemoonai';
    });
}

// Call the function to create the floating donation button
createFloatingButton();
