
function searchCourses() {
    // Get the search term from the input field
    var searchTerm = document.getElementById("search-input").value;

    // Send an AJAX request to the Flask server
    fetch('/search?term=' + searchTerm)
        .then(response => response.json())
        .then(data => {
            // Clear previous search results
            var searchResultsDiv = document.getElementById("search-results");
            searchResultsDiv.innerHTML = '';

            // Create HTML elements for each search result
            data.forEach(course => {
                var courseDiv = document.createElement("div");
                courseDiv.textContent = course.class_id + ' - ' + course.cname;
                searchResultsDiv.appendChild(courseDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

function displaySearchResults(courses) {
    const searchResultsDiv = document.getElementById('search_results');
    searchResultsDiv.innerHTML = '';
    courses.forEach(course => {
        const courseItem = document.createElement('div');
        courseItem.textContent = `${course.id}: ${course.name}`;
        searchResultsDiv.appendChild(courseItem);
    });
}

function generateYears() {
    const startYearSelect = document.getElementById('startYear');
    const endYearSelect = document.getElementById('endYear');
    const currentYear = new Date().getFullYear();
    const futureYears = 5;
    const yearsBefore = 4;

    for (let year = currentYear - yearsBefore; year <= currentYear + futureYears; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        startYearSelect.appendChild(option);
    }

    for (let year = currentYear; year <= currentYear + futureYears; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        endYearSelect.appendChild(option);
    }
}
function generateSemesters() {
    const startYear = parseInt(document.getElementById('startYear').value);
    const endYear = parseInt(document.getElementById('endYear').value);
    const generatedDivsContainer = document.getElementById('generatedDivs');

    // Clear previous content
    generatedDivsContainer.innerHTML = '';

    for (let year = startYear; year <= endYear; year++) {
        const semesters = ['Spring', 'Summer', 'Fall'];

        semesters.forEach(semester => {
            const semesterDiv = document.createElement('div');
            semesterDiv.classList.add('semesterDiv');
            semesterDiv.textContent = `${semester} ${year}`;

            const removeButton = document.createElement('button');
            removeButton.classList.add('remove-button');
            removeButton.innerHTML = '&#10006;'; // Unicode for '✖'

            removeButton.onclick = function () {
                semesterDiv.remove();
            };

            semesterDiv.appendChild(removeButton);
            generatedDivsContainer.appendChild(semesterDiv);
        });
    }
}
window.onload = generateYears;
