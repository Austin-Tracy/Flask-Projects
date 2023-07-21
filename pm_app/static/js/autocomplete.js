const taskTitleInput = document.getElementById('task-title');
const suggestedRemainder = document.getElementById('suggested-remainder');

function fetchTaskSuggestions(query) {
    return fetch(`/autocomplete?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => data.suggestions);
}

function handleKeyDown(event) {
    if (event.keyCode === 9) { // Tab key
        event.preventDefault();
        if (suggestedRemainder.textContent) {
            taskTitleInput.value += suggestedRemainder.textContent;
            suggestedRemainder.textContent = '';
        }
    } else {
        const query = taskTitleInput.value;
        if (query.length >= 2) {
            fetchTaskSuggestions(query).then(suggestions => {
                if (suggestions.length > 0) {
                    const firstSuggestion = suggestions[0];
                    const remainder = firstSuggestion.slice(query.length);
                    suggestedRemainder.textContent = remainder;
                } else {
                    suggestedRemainder.textContent = '';
                }
            });
        } else {
            suggestedRemainder.textContent = '';
        }
    }
}

function updateSuggestedRemainderPosition() {
    const inputText = taskTitleInput.value;
    const textWidth = getTextWidth(inputText, taskTitleInput);
    suggestedRemainder.style.left = `${textWidth}px`;
}

function getTextWidth(text, inputElement) {
    const testElement = document.createElement('span');
    testElement.textContent = text;
    testElement.style.font = window.getComputedStyle(inputElement).font;
    testElement.style.whiteSpace = 'pre';
    document.body.appendChild(testElement);
    const width = testElement.getBoundingClientRect().width;
    document.body.removeChild(testElement);
    return width;
}

taskTitleInput.addEventListener('keydown', handleKeyDown);
taskTitleInput.addEventListener('input', updateSuggestedRemainderPosition);
updateSuggestedRemainderPosition();