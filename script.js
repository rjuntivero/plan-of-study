var completedCourses = [];

//OUTDATED
function addCourse(courseId, courseName) {
    // Check if the course is already in the completedCourses array
    if (!completedCourses.includes(courseName)) {
        // If not, add it to the array and append it to the list
        completedCourses.push(courseName);
        $('#completed-courses-list').append('<p>' + courseName + '</p>');

        // AJAX call to add the course
        $.ajax({
            url: '/add-course',
            method: 'POST',
            data: { course_id: courseId, course_name: courseName }, // Send both course ID and name
            success: function (response) {
                if (response.success) {
                    console.log('Course added successfully:', response.message); // Log the message
                    updateRequiredCoursesList();
                } else {
                    console.error('Failed to add ' + courseName + '.');
                }
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

document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to your button with the class "add-button"
    document.querySelectorAll('.add-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default form submission

            var courseId = this.getAttribute('data-course-id');
            var courseName = this.getAttribute('data-course-name');

            // Send a POST request to add the course
            fetch('/add-course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    course_id: courseId,
                    course_name: courseName
                })
            })
                .then(response => {
                    if (response.ok) {
                        console.log(courseName + ' added successfully.');
                    } else {
                        console.error('Failed to add ' + courseName + '.');
                    }
                })
                .catch(error => {
                    console.error('Error adding course:', error);
                });
        });
    });
});


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


//Generation for Start/End Years in Calendar
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


//Refresh Course 'completed' Attributes
window.onload = function () {
    fetch('/reset-completed-attributes')
        .then(response => {
            if (response.ok) {
                console.log('Completed attributes reset successfully.');
            } else {
                console.error('Failed to reset completed attributes.');
            }
        })
        .catch(error => {
            console.error('An error occurred:', error);
        });

    generateYears();
};


//Generates Required Courses in sidebar
function updateRequiredCoursesList(courses) {
    var requiredCoursesList = $('#required-courses-list');
    requiredCoursesList.empty();

    if (courses && courses.length > 0) {
        courses.forEach(function (course) {
            var courseItem = $('<li>' + course.cname + '</li>');
            // Check if the course is completed, if so, add the class
            if (course.completed) {
                courseItem.addClass('completed-course');
            }
            requiredCoursesList.append(courseItem);
        });
    } else {
        // If no courses are found, display a default message
        requiredCoursesList.append('<li>No required courses found.</li>');
    }
}

//Required Courses Dropdown function
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
                updateProgressBar(completedCourses.length, response.length)//Update Progress Bar
                updateStatusText(completedCourses.length, response.length);
            },
            error: function (xhr, status, error) {
                console.error('Error fetching required courses:', error);
            }
        });
    }

    // Function to update the progress bar
    function updateProgressBar(completedCoursesCount, totalCoursesCount) {
        var completionPercentage = (completedCoursesCount / totalCoursesCount) * 100;
        var circle = document.querySelector('.progress-ring-circle-progress');
        var radius = circle.r.baseVal.value;
        var circumference = radius * 2 * Math.PI;
        var offset = circumference - completionPercentage / 100 * circumference;

        circle.style.strokeDashoffset = offset;

        // Define color thresholds and corresponding colors
        var color1 = '#FF6347'; // Red
        var color2 = '#FFD700'; // Yellow
        var color3 = '#32CD32'; // Green

        // Calculate color based on completion percentage
        var strokeColor;
        if (completionPercentage < 50) {
            // Linear interpolation between color1 and color2
            var interpolationFactor = completionPercentage / 50; // Range from 0 to 1
            strokeColor = interpolateColors(color1, color2, interpolationFactor);
        } else {
            // Linear interpolation between color2 and color3
            var interpolationFactor = (completionPercentage - 50) / 50; // Range from 0 to 1
            strokeColor = interpolateColors(color2, color3, interpolationFactor);
        }

        // Update the stroke color
        circle.style.stroke = strokeColor;
        document.querySelector('.progress-text').textContent = completionPercentage.toFixed(2) + '%'; // Display with two decimal places
    }

    // Function to interpolate between two colors
    function interpolateColors(color1, color2, factor) {
        if (factor === undefined) factor = 0.5;
        var result = color1.slice();
        for (var i = 1; i < 7; i += 2) {
            // Parse the integer values of the two colors
            var v1 = parseInt(color1.substr(i, 2), 16);
            var v2 = parseInt(color2.substr(i, 2), 16);

            // Interpolate the color component
            var v = Math.round(v1 + (v2 - v1) * factor);

            // Convert it back to hexadecimal and update the result
            result = result.substr(0, i) + v.toString(16).padStart(2, '0') + result.substr(i + 2);
        }
        return result;
    }

    function updateStatusText(completedCoursesCount, totalCoursesCount) {
        var completionPercentage = (completedCoursesCount / totalCoursesCount) * 100;
        var statusText = document.getElementById('status-text');

        if (completionPercentage >= 75) {
            statusText.textContent = 'Status: Good Standing';
            statusText.style.color = 'lightgreen';
        } else if (completionPercentage >= 50) {
            statusText.textContent = 'Status: On Track';
            statusText.style.color = 'yellow';
        } else {
            statusText.textContent = 'Status: Insufficient';
            statusText.style.color = 'red';
        }
    }

    //Prevents Page Refresh when Add Button is Clicked
    $(document).on('click', '.add-button', function () {
        var selectedMajor = $('#major-select').val(); // Get the selected major

        // Check if a major is selected
        if (selectedMajor) {
            var courseId = $(this).closest('form').find('input[name="course_id"]').val();
            var courseName = $(this).closest('form').find('input[name="course_name"]').val();

            // Check if the course is already added
            if (!completedCourses.some(course => course.id === courseId && course.name === courseName)) {
                // If not, add it to the array and append it to the list
                completedCourses.push({ id: courseId, name: courseName });
                $('#completed-courses-list').append('<p>' + courseName + '</p>');

                // AJAX call to add the course
                $.ajax({
                    url: '/add-course',
                    method: 'POST',
                    data: { course_id: courseId, course_name: courseName },
                    success: function (response) {
                        console.log('Course added successfully:', response.course_name);
                        console.log('Completed Courses:', completedCourses);
                        fetchRequiredCourses(selectedMajor); // Call fetchRequiredCourses with the selected major
                        $('#alert').html('<p class="success">' + courseName + ' has been added to completed courses.</p>').show();
                        setTimeout(function () {
                            $('#alert').hide();
                        }, 5000); // Hide the alert after 3 seconds
                    },
                    error: function (xhr, status, error) {
                        console.error('Error adding course:', error);
                    }
                });
            } else {
                // If it's already in the array, do nothing or show a message indicating it's already added
                console.log(courseName + ' is already added to the list.');
                $('#alert').html('<p class="error">' + courseName + ' has already been added to completed courses.</p>').show();
                setTimeout(function () {
                    $('#alert').hide();
                }, 5000); // Hide the alert after 3 seconds
            }
        } else {
            // If no major is selected, show an alert to choose a major first
            $('#alert').html('<p class="error">Please select a major first.</p>').show();
            setTimeout(function () {
                $('#alert').hide();
            }, 5000); // Hide the alert after 3 seconds
        }
    });
});


// Function to open Completed Courses tab
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
}

// Function to close the Completed Courses tab
function closeCompletedCourses() {
    document.getElementById("CompletedCourses").style.display = "none";
}

//Completed Courses Tab
function displayCompletedCourses() {
    var completedCoursesList = document.getElementById('completed-courses-list');
    completedCoursesList.innerHTML = ''; // Clear previous content

    // Iterate over the completedCourses array
    completedCourses.forEach(function (courseId) {
        // Create a list item element for each course
        var courseItem = document.createElement('li');
        courseItem.textContent = courseId; // Display course ID

        // Append the course item to the completed courses list
        completedCoursesList.appendChild(courseItem);
    });
}

// Call the function to display completed courses when needed
document.addEventListener('DOMContentLoaded', function () {
    // Call the displayCompletedCourses function
    displayCompletedCourses();
});

//Plan of Study Generation TEST
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

//Plan of Study PDF Generation
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

// Function to toggle between light and dark modes
function toggleMode() {
    const body = document.body;
    const currentMode = body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode';
    body.classList.toggle('dark-mode');
    body.classList.toggle('light-mode');
}

//Change Light Mode/Dark Mode
document.addEventListener('DOMContentLoaded', function () {
    // Get the mode toggle button
    const modeButton = document.querySelector('.banner__options');

    // Check if the button exists before adding the event listener
    if (modeButton) {
        // Add click event listener to the button
        modeButton.addEventListener('click', function () {
            // Toggle between light and dark modes
            toggleMode();
        });
    } else {
        console.error("Button not found!");
    }
});

