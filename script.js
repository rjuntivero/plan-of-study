var completedCourses = [];

//OUTDATED
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

// Prevent form submission from resetting filters
$(document).ready(function () {
    $('#searchForm').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        // Retrieve filter values
        var filter1Value = $('#filter1').val();
        var filter2Value = $('#filter2').val();
        var filter3Value = $('#filter3').val();

        console.log("Filter 1 Value:", filter1Value);
        console.log("Filter 2 Value:", filter2Value);
        console.log("Filter 3 Value:", filter3Value);

        // Set the hidden input values
        $('#hidden-filter1').val(filter1Value);
        $('#hidden-filter2').val(filter2Value);
        $('#hidden-filter3').val(filter3Value);

        // Send form data using AJAX to Flask route
        $.ajax({
            url: '/search',
            method: 'POST',
            data: $('#searchForm').serialize(),
            success: function (response) {
                // Update the search results div with the returned HTML content
                $('#results').html(response);
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});


//Generates Required Courses in sidebar
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

//Generation for Start/End Options in Calendar
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

//Generation for Calendar 
function generateSemesters() {
    const startYear = parseInt(document.getElementById('startYear').value);
    const endYear = parseInt(document.getElementById('endYear').value);
    const generatedDivsContainer = document.getElementById('generatedDivs');
    let semestersArray = []; // Array to store semester strings

    // Clear previous content
    generatedDivsContainer.innerHTML = '';

    for (let year = startYear; year <= endYear; year++) {
        const semesters = ['Spring', 'Summer', 'Fall'];

        semesters.forEach(semester => {
            const semesterDiv = document.createElement('div');
            semesterDiv.classList.add('semesterDiv');
            const semesterString = `${semester} ${year}`;
            semesterDiv.textContent = semesterString;

            const removeButton = document.createElement('button');
            removeButton.classList.add('remove-button');
            removeButton.innerHTML = '&#10006;'; // Unicode for '✖'

            removeButton.onclick = function () {
                semesterDiv.remove();
                // Remove the corresponding semester string from the array
                semestersArray = semestersArray.filter(item => item !== semesterString);
                console.log('Semester removed:', semesterString);
                console.log('Semesters array:', semestersArray);
            };

            semesterDiv.appendChild(removeButton);
            generatedDivsContainer.appendChild(semesterDiv);

            // Add the semester string to the array
            semestersArray.push(semesterString);
            console.log('Semester added:', semesterString);
            console.log('Semesters array:', semestersArray);
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

$(document).ready(function () {
    // Dummy array with class information
    var classes = [
        ["Class 1A", "Class 1B", "Class 1C", "Class 1D", "Class 1E"],
        ["Class 2A", "Class 2B", "Class 2C", "Class 2D", "Class 2E"],
        ["Class 3A", "Class 3B", "Class 3C", "Class 3D", "Class 3E"],
        ["Class 4A", "Class 4B", "Class 4C", "Class 4D", "Class 4E"],
        ["Class 5A", "Class 5B", "Class 5C", "Class 5D", "Class 5E"],
        ["Class 6A", "Class 6B", "Class 6C", "Class 6D", "Class 6E"],
        ["Class 7A", "Class 7B", "Class 7C", "Class 7D", "Class 7E"],
        ["Class 8A", "Class 8B", "Class 8C", "Class 8D", "Class 8E"],
        ["Class 9A", "Class 9B", "Class 9C", "Class 9D", "Class 9E"],
    ];

    // Function to set the course_id and course_name fields in the form
    function setFormData(semester, row) {
        var course_id = classes[semester - 1][row - 1];
        $('#course_id').val(course_id);
        $('#course_name').val("Semester " + semester + " Row " + row);
    }

    // Example: Setting data for Semester 3, Row 2
    setFormData(3, 2);

    // Trigger form submission when the "Generate PDF" button is clicked
    $('#pdfForm').submit();
});
function generatePlanOfStudy() {
    // Retrieve the selected year and advisor name from the form
    var year = document.getElementById("year").value;
    var advisor = document.getElementById("advisor").value;

    // Prepare the form data to be submitted
    var formData = new FormData();
    formData.append("year", year);
    formData.append("advisor", advisor);

    // Send an AJAX request to the Flask route to generate the PDF
    fetch('/generate_pdf', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                // Handle successful response
                console.log("PDF generated successfully!");
            } else {
                // Handle error response
                console.error("Failed to generate PDF!");
            }
        })
        .catch(error => {
            console.error("An error occurred:", error);
        });
}
