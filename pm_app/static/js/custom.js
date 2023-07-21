// app/static/js/custom.js
// This file is loaded in the base.html template
console.log("Custom JS is loaded!"); // Add this line
function showTemporaryMessage(message, timeout = 2000) {
    const messageContainer = document.createElement('div');
    messageContainer.innerHTML = message;
    messageContainer.style.position = 'fixed';
    messageContainer.style.top = '20px';
    messageContainer.style.left = '20px';
    messageContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    messageContainer.style.color = 'white';
    messageContainer.style.padding = '10px';
    messageContainer.style.borderRadius = '5px';
    messageContainer.style.zIndex = '1050';
    document.body.appendChild(messageContainer);

    setTimeout(() => {
        messageContainer.remove();
    }, timeout);
}

const flashMessageContainer = document.getElementById('flash-message-container');
if (flashMessageContainer) {
    const message = flashMessageContainer.innerText;
    flashMessageContainer.remove();
    showTemporaryMessage(message, 2500);
}

$(document).ready(function() {
    $('#navbarNav').on('show.bs.collapse', function() {
        $('body').addClass('navbar-expanded');
    });

    $('#navbarNav').on('hide.bs.collapse', function() {
        $('body').removeClass('navbar-expanded');
    });
});