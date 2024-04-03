var completedCourses = [];

function addCourse(courseName) {
    // Check if the course is already in the completedCourses array
    if (!completedCourses.includes(courseName)) {
        // If not, add it to the array and append it to the list
        completedCourses.push(courseName);
        $('#completed-courses-list').append('<p>' + courseName + '</p>');

        // AJAX call to add the course
        $.ajax({
            url: '/add-course',
            method: 'POST',
            data: { course_name: courseName }, // Send the course name
            success: function (response) {
                console.log('Course added successfully:', response.course_name);
                updateCompletedCoursesList();
            },
            error: function (xhr, status, error) {
                console.error('Error adding course:', error);
            }
        });
    } else {
        // If it's already in the array, do nothing or show a message indicating it's already added
        console.log(courseName + ' is already added to the list.');
    }
}

function updateRequiredCoursesList(courses) {
    var requiredCoursesList = $('#required-courses-list');
    requiredCoursesList.empty();

    if (courses.length > 0) {
        courses.forEach(function (course) {
            var courseItem = $('<li>' + course.cname + '</li>');
            if (course.completed) {
                courseItem.addClass('completed-course'); // Add completed class if the course is completed
            }
            requiredCoursesList.append(courseItem);
        });
    } else {
        requiredCoursesList.append('<li>No required courses found.</li>');
    }
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



$(document).ready(function () {
    // Event listener for major selection change
    $('#major-select').change(function () {
        var selectedMajor = $(this).val();
        if (selectedMajor) {
            fetchRequiredCourses(selectedMajor);
        } else {
            $('#required-courses-list').empty();
        }
    });

    // Function to fetch required courses for the selected major
    function fetchRequiredCourses(major) {
        $.ajax({
            url: '/get-required-courses',
            method: 'GET',
            data: { department: major }, // Ensure 'department' matches the parameter name in the Flask route
            success: function (response) {
                updateRequiredCoursesList(response);
            },
            error: function (xhr, status, error) {
                console.error('Error fetching required courses:', error);
            }
        });
    }

    $(document).on('click', '.add-button', function () {
        var courseId = $(this).data('course-id');
        var courseName = $(this).data('course-name');
        addCourse(courseId, courseName);
        // Send a POST request to add the course
        $.ajax({
            url: '/add-course',
            method: 'POST',
            data: { course_id: courseId, course_name: courseName },
            success: function (response) {
                if (response.success) {
                    console.log(courseName + ' added successfully.');
                } else {
                    console.error('Failed to add ' + courseName + '.');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error adding course:', error);
            }
        });
    });
});


