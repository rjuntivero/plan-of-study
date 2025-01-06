var completedCourses = [];
var selectedMajor;
var removeButtons = [];

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
                sendSemestersArray(semestersArray);
            };

            semesterDiv.appendChild(removeButton);
            generatedDivsContainer.appendChild(semesterDiv);

            // Add the semester string to the array
            semestersArray.push(semesterString);
            console.log('Semester added:', semesterString);
            console.log('Semesters array:', semestersArray);
        });
    }
    sendSemestersArray(semestersArray);
}

//Allows for use of semestersArray in Flask
function sendSemestersArray(semestersArray) {
    // Send the semestersArray to Flask using AJAX
    // Make sure to stringify your JSON data and set the Content-Type header to 'application/json'
    fetch('/process_semesters', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            semestersArray: semestersArray
        })
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            console.log(data);
        })
        .catch(error => {
            // Handle any errors
            console.error('Error:', error);
        });
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

// Function to fetch required courses for the selected major
function fetchRequiredCourses(major) {
    console.log("Selected Major:", major);
    $.ajax({
        url: '/get-required-courses',
        method: 'GET',
        data: { department: major }, // Ensure 'department' matches the parameter name in the Flask route
        success: function (response) {
            updateRequiredCoursesList(response);
            updateProgressBar(completedCourses, response.length, response)//Update Progress Bar
            updateStatusText(completedCourses.length, response.length);
            updateTotalCredits(response)
        },
        error: function (xhr, status, error) {
            console.error('Error fetching required courses:', error);
        }
    });
}

// Function to update the progress bar
function updateProgressBar(completedCourses, totalCoursesCount, requiredCourses) {
    console.log('Completed Courses:', completedCourses);
    console.log('Required Courses:', requiredCourses);

    var completedRequiredCourses = [];

    completedCourses.filter(completedCourse => {
        console.log('Checking completed course:', completedCourse);
        var foundRequiredCourse = requiredCourses.some(requiredCourse => {
            console.log('Checking required course:', requiredCourse);
            var comparisonResult = requiredCourse.cname === completedCourse.name;
            console.log('Comparing:', requiredCourse.cname, completedCourse.name, 'Result:', comparisonResult);
            if (comparisonResult) {
                completedRequiredCourses.push(completedCourse);
                return true;
            }
        });
        if (completedCourse.completed && foundRequiredCourse) {
            return true;
        }
    });

    console.log("Completed Required:", completedRequiredCourses);
    var completedRequiredCoursesCount = completedRequiredCourses.length;
    var completionPercentage = (completedRequiredCoursesCount / totalCoursesCount) * 100;
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

//Update Message for Progress Circle Status
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
        statusText.textContent = 'Status: Entrant';
        statusText.style.color = 'orange';
    }
}

//Displayed Total Credits for Each Major
function updateTotalCredits(requiredCourses) {
    // Filter out the required courses that haven't been completed
    const incompleteCourses = requiredCourses.filter(course => !course.completed);

    // Calculate total credits for incomplete courses
    const totalCredits = incompleteCourses.reduce((total, course) => total + course.credit_hrs, 0);

    // Update the HTML element with the total credits
    const totalCreditsElement = document.getElementById('total-credits');
    if (totalCreditsElement) {
        totalCreditsElement.textContent = totalCredits;
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
                        updateCompletedCoursesModal();
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
    // Remove Button for Completed Course Modal
    $(document).on('click', '.remove-course-button', function () {
        var selectedMajor = $('#major-select').val(); // Get the selected major

        // Check if a major is selected
        if (selectedMajor) {
            // Extract the index of the remove button
            var index = $(this).data('index');

            // Check if the index is valid and the completedCourses array is not empty
            if (index >= 0 && index < completedCourses.length) {
                // Extract the course information from the completedCourses array based on the index
                var course = completedCourses[index];

                // Check if course is defined
                if (course) {
                    console.log('Course to remove:', course); // Debug code

                    // AJAX call to remove the course
                    $.ajax({
                        url: '/remove-course',
                        method: 'POST',
                        data: { course_id: course.id }, // Assuming course.id represents the course ID
                        success: function (response) {
                            console.log('Course removed successfully:', course); // Debug code
                            completedCourses.splice(index, 1);
                            // Optionally, update the UI to reflect the removal of the course
                            updateRequiredCoursesList(); // Update the required courses list
                            fetchRequiredCourses(selectedMajor); // Call fetchRequiredCourses with the selected major
                            updateCompletedCoursesModal();

                            // Remove the course from the completed courses modal list
                            $('.completed-course').each(function () {
                                if ($(this).text() === course.name) {
                                    $(this).remove();
                                }
                            });
                        },
                        error: function (xhr, status, error) {
                            console.error('Error removing course:', error);
                        }
                    });
                } else {
                    console.error('Course is undefined.');
                }
            } else {
                console.error('Invalid index or completedCourses array is empty.');
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


// Open the modal and populate it with completed courses
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "block";

        // Add logic to populate different modals with information
        if (modalId === "completedCoursesModal") {
            var completedCoursesList = document.getElementById("completedCoursesList");
            completedCoursesList.innerHTML = ""; // Clear previous content

            // Check if completed courses exist
            if (completedCourses.length > 0) {
                completedCourses.forEach(function (course) {
                    var courseItem = document.createElement("div");
                    courseItem.textContent = course.id + " " + course.name;
                    //Button to mark course as incomplete
                    var markIncompleteButton = document.createElement("button");
                    markIncompleteButton.textContent = "Remove";
                    markIncompleteButton.classList.add("remove-course-button");
                    markIncompleteButton.setAttribute('data-course-id', course.id);
                    markIncompleteButton.onclick = function () {

                    };

                    courseItem.appendChild(markIncompleteButton);
                    completedCoursesList.appendChild(courseItem);
                });
            } else {
                // If no completed courses exist, display a message
                var noCoursesMessage = document.createElement("p");
                noCoursesMessage.textContent = "No completed courses found.";
                completedCoursesList.appendChild(noCoursesMessage);
            }
        }
        updateCompletedCoursesModal();
    } else {
        console.error("Modal with ID", modalId, "not found.");
    }
}


// Close the modal
function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
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

//Expand Arrow for Completed Courses Manager
function toggleExpand() {
    var content = document.getElementById('completedCoursesList');
    var arrow = document.querySelector('.expand-arrow');

    if (content.style.display === "none") {
        content.style.display = "block";
        arrow.style.display = "none"; // Hide the arrow when expanded
    } else {
        content.style.display = "none";
        arrow.style.display = "inline"; // Show the arrow when collapsed
    }
}

function updateCompletedCoursesModal() {
    var completedCoursesList = document.getElementById("completedCoursesList");
    completedCoursesList.innerHTML = ""; // Clear previous content

    // Check if completed courses exist
    if (completedCourses.length > 0) {
        completedCourses.forEach(function (course, index) {
            var courseItem = document.createElement("div");
            courseItem.textContent = course.id + " " + course.name;

            // Create the remove button
            var removeButton = document.createElement("button");
            removeButton.textContent = "Remove";
            removeButton.classList.add("remove-course-button");
            removeButton.setAttribute("data-index", index); // Set the data-index attribute
            removeButton.onclick = function () {
            };

            courseItem.appendChild(removeButton);
            completedCoursesList.appendChild(courseItem);
        });
    } else {
        // If no completed courses exist, display a message
        var noCoursesMessage = document.createElement("p");
        noCoursesMessage.textContent = "No completed courses found.";
        completedCoursesList.appendChild(noCoursesMessage);
    }
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

//hold value of major dropdown for pos modal
document.addEventListener('DOMContentLoaded', function () {
    // Add an event listener to the major dropdown
    document.getElementById('major-select').addEventListener('change', function () {
        // Get the selected value of the major dropdown
        var selectedMajor = this.value;

        // Update the value of the hidden major dropdown
        document.getElementById('hidden-major-dropdown').value = selectedMajor;

        // Log a debug message with the selected major value
        console.log('Selected Major:', selectedMajor);
    });
});


//Open Stats SidePanel
function openNav() {
    document.getElementById("mySidepanel").style.width = "300px";
}

//Close Stats SidePanel
function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
}



function handleGeneratePDFResponse(response) {
    // Access the PDF data from the response
    const pdfData = response.pdf_data;

    // Use the PDF data as needed
    const iframe = document.createElement('iframe');
    iframe.src = 'data:application/pdf;base64,' + btoa(pdfData);
    document.body.appendChild(iframe);
}

//Fetch to_schedule Array From Flask
$(document).ready(function () {
    // Event listener for form submission
    $('#pdfForm').submit(function (event) {
        // Prevent default form submission behavior
        event.preventDefault();

        // Serialize form data
        var formData = $(this).serialize();

        // Send AJAX request to the server
        $.ajax({
            type: "POST",
            url: "/generate_pos",
            data: formData,
            success: function (response) {
                // Handle the response data containing the schedule information
                console.log(response); // Check if the response contains the expected data
                generateCourses(response); // Pass the 'to_schedule' data to the generateCourses function
                $('#alert').html('<p class="success">Plan of Study has been Generated.</p>').show();
                setTimeout(function () {
                    $('#alert').hide();
                }, 5000); // Hide the alert after 3 seconds
            },
            error: function (xhr, status, error) {
                // Handle error
                console.error(xhr.responseText);
            }
        });
    });
});


//Stats Page Generation
function generateCourses(to_schedule) {
    // Log the length of the to_schedule array
    console.log(to_schedule);

    // Check if to_schedule is defined and not null
    if (to_schedule && to_schedule.length > 0) {
        // Initialize arrays for each semester
        var springCourses = [];
        var fallCourses = [];
        var allCourses = [];

        // Iterate over the to_schedule array and populate semester arrays
        to_schedule.forEach(course => {
            if (course.spring && !course.fall && !course.summer) {
                springCourses.push(course.cname);
            }
            if (course.fall && !course.spring && !course.summer) {
                fallCourses.push(course.cname);
            }
            // If a course is available in both spring and fall, include it in allCourses
            if (course.spring && course.fall && course.summer) {
                allCourses.push(course.cname);
            }
        });

        // Generate HTML content for each semester
        var springHTML = "<h1>Spring Courses:</h1>";
        springCourses.forEach(course => {
            springHTML += "<p>" + course + "</p>";
        });

        var fallHTML = "<h1>Fall Courses:</h1>";
        fallCourses.forEach(course => {
            fallHTML += "<p>" + course + "</p>";
        });

        var allHTML = "<h1>Available All Semesters:</h1>";
        allCourses.forEach(course => {
            allHTML += "<p>" + course + "</p>";
        });

        // Insert HTML content into respective div elements
        document.getElementById("springCourses").innerHTML = springHTML;
        document.getElementById("fallCourses").innerHTML = fallHTML;
        document.getElementById("allCourses").innerHTML = allHTML;
    } else {
        // Handle case where data is undefined or empty
        console.error('Data is undefined or empty');
    }
}
