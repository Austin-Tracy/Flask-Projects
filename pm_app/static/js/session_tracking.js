let startTime;

document.addEventListener("DOMContentLoaded", function () {
    startTime = new Date().getTime();
    window.addEventListener("beforeunload", trackTimeOnPage);
});

function trackTimeOnPage() {
    const endTime = new Date().getTime();
    const timeSpent = endTime - startTime;
    const currentPage = window.location.pathname;

    // Send the time spent on the page and the page URL to the server
    fetch('/track-time', {
        method: 'POST',
        body: JSON.stringify({ time_spent: timeSpent, page: currentPage }),
        headers: {
            'Content-Type': 'application/json'
        },
    });
}