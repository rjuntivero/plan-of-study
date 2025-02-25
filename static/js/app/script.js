import { updateProgressBar, updateStatusText, updateTotalCredits } from './modules/progressUpdate.js';

var completedCourses = [];

// document.addEventListener('DOMContentLoaded', function () {
//   handleSearchFormSubmit();
//   handleMajorSelectChange();
//   handleAddCourseButtonClick();
//   handlePDFFormSubmit();
//   generateYears();
//   openModal('completedCoursesModal');
//   toggleExpand();
// });

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.add-button').forEach((button) => {
    button.addEventListener('click', function (event) {
      event.preventDefault();

      let courseId = this.getAttribute('data-course-id');
      let courseName = this.getAttribute('data-course-name');

      fetch('/add-course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          course_id: courseId,
          course_name: courseName,
        }),
      })
        .then((response) => {
          if (response.ok) {
            console.log(courseName + ' added successfully.');
          } else {
            console.error('Failed to add ' + courseName + '.');
          }
        })
        .catch((error) => {
          console.error('Error adding course:', error);
        });
    });
  });
});

$(document).ready(function () {
  $('#searchForm').submit(function (event) {
    event.preventDefault();

    let filter1Value = $('#filter1').val();
    let filter2Value = $('#filter2').val();
    let filter3Value = $('#filter3').val();

    console.log('Filter 1 Value:', filter1Value);
    console.log('Filter 2 Value:', filter2Value);
    console.log('Filter 3 Value:', filter3Value);

    $('#hidden-filter1').val(filter1Value);
    $('#hidden-filter2').val(filter2Value);
    $('#hidden-filter3').val(filter3Value);

    $.ajax({
      url: '/search',
      method: 'POST',
      data: $('#searchForm').serialize(),
      success: function (response) {
        $('#results').html(response);
      },
      error: function (xhr, status, error) {
        console.error('Error:', error);
      },
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
  let semestersArray = [];

  generatedDivsContainer.innerHTML = '';

  for (let year = startYear; year <= endYear; year++) {
    const semesters = ['Spring', 'Summer', 'Fall'];

    semesters.forEach((semester) => {
      const semesterDiv = document.createElement('div');
      semesterDiv.classList.add('semesterDiv');
      const semesterString = `${semester} ${year}`;
      semesterDiv.textContent = semesterString;

      const removeButton = document.createElement('button');
      removeButton.classList.add('remove-button');
      removeButton.innerHTML = '&#10006;';

      removeButton.onclick = function () {
        semesterDiv.remove();
        semestersArray = semestersArray.filter((item) => item !== semesterString);
        console.log('Semester removed:', semesterString);
        console.log('Semesters array:', semestersArray);
        sendSemestersArray(semestersArray);
      };

      semesterDiv.appendChild(removeButton);
      generatedDivsContainer.appendChild(semesterDiv);

      semestersArray.push(semesterString);
      console.log('Semester added:', semesterString);
      console.log('Semesters array:', semestersArray);
    });
  }
  sendSemestersArray(semestersArray);
}

//Allows for use of semestersArray in Flask
function sendSemestersArray(semestersArray) {
  fetch('/process_semesters', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      semestersArray: semestersArray,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

//Refresh Course 'completed' Attributes
window.onload = function () {
  fetch('/reset-completed-attributes')
    .then((response) => {
      if (response.ok) {
        console.log('Completed attributes reset successfully.');
      } else {
        console.error('Failed to reset completed attributes.');
      }
    })
    .catch((error) => {
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
      if (course.completed) {
        courseItem.addClass('completed-course');
      }
      requiredCoursesList.append(courseItem);
    });
  } else {
    requiredCoursesList.append('<li>No required courses found.</li>');
  }
}

// Function to fetch required courses for the selected major
function fetchRequiredCourses(major) {
  console.log('Selected Major:', major);
  $.ajax({
    url: '/get-required-courses',
    method: 'GET',
    data: { department: major },
    success: function (response) {
      updateRequiredCoursesList(response);
      updateProgressBar(completedCourses, response.length, response);
      updateStatusText(completedCourses.length, response.length);
      updateTotalCredits(response);
    },
    error: function (xhr, status, error) {
      console.error('Error fetching required courses:', error);
    },
  });
}

//Required Courses Dropdown function
$(document).ready(function () {
  $('#major-select').change(function () {
    var selectedMajor = $(this).val();
    if (selectedMajor) {
      fetchRequiredCourses(selectedMajor);
    } else {
      $('#required-courses-list').empty();
    }
  });

  // Add course
  $(document).on('click', '.add-button', function () {
    var selectedMajor = $('#major-select').val();

    if (selectedMajor) {
      var courseId = $(this).closest('form').find('input[name="course_id"]').val();
      var courseName = $(this).closest('form').find('input[name="course_name"]').val();

      if (!completedCourses.some((course) => course.id === courseId && course.name === courseName)) {
        completedCourses.push({ id: courseId, name: courseName });
        $('#completed-courses-list').append('<p>' + courseName + '</p>');

        $.ajax({
          url: '/add-course',
          method: 'POST',
          data: { course_id: courseId, course_name: courseName },
          success: function (response) {
            console.log('Course added successfully:', response.course_name);
            console.log('Completed Courses:', completedCourses);
            fetchRequiredCourses(selectedMajor);
            updateCompletedCoursesModal();
            $('#alert')
              .html('<p class="success">' + courseName + ' has been added to completed courses.</p>')
              .show();
            setTimeout(function () {
              $('#alert').hide();
            }, 5000);
          },
          error: function (xhr, status, error) {
            console.error('Error adding course:', error);
          },
        });
      } else {
        console.log(courseName + ' is already added to the list.');
        $('#alert')
          .html('<p class="error">' + courseName + ' has already been added to completed courses.</p>')
          .show();
        setTimeout(function () {
          $('#alert').hide();
        }, 5000);
      }
    } else {
      $('#alert').html('<p class="error">Please select a major first.</p>').show();
      setTimeout(function () {
        $('#alert').hide();
      }, 5000);
    }
  });

  $(document).on('click', '.remove-course-button', function () {
    var selectedMajor = $('#major-select').val();

    if (selectedMajor) {
      var index = $(this).data('index');

      if (index >= 0 && index < completedCourses.length) {
        var course = completedCourses[index];

        if (course) {
          console.log('Course to remove:', course);

          $.ajax({
            url: '/remove-course',
            method: 'POST',
            data: { course_id: course.id },
            success: function (response) {
              console.log('Course removed successfully:', course);
              completedCourses.splice(index, 1);
              updateRequiredCoursesList();
              fetchRequiredCourses(selectedMajor);
              updateCompletedCoursesModal();

              $('.completed-course').each(function () {
                if ($(this).text() === course.name) {
                  $(this).remove();
                }
              });
            },
            error: function (xhr, status, error) {
              console.error('Error removing course:', error);
            },
          });
        } else {
          console.error('Course is undefined.');
        }
      } else {
        console.error('Invalid index or completedCourses array is empty.');
      }
    } else {
      $('#alert').html('<p class="error">Please select a major first.</p>').show();
      setTimeout(function () {
        $('#alert').hide();
      }, 5000);
    }
  });
});

// Open the modal and populate it with completed courses
function openModal(modalId) {
  var modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'block';

    if (modalId === 'completedCoursesModal') {
      const completedCoursesList = document.getElementById('completedCoursesList');
      completedCoursesList.innerHTML = '';

      if (completedCourses.length > 0) {
        completedCourses.forEach(function (course) {
          const courseItem = document.createElement('div');
          courseItem.textContent = course.id + ' ' + course.name;

          const markIncompleteButton = document.createElement('button');
          markIncompleteButton.textContent = 'Remove';
          markIncompleteButton.classList.add('remove-course-button');
          markIncompleteButton.setAttribute('data-course-id', course.id);
          markIncompleteButton.onclick = function () {};

          courseItem.appendChild(markIncompleteButton);
          completedCoursesList.appendChild(courseItem);
        });
      } else {
        var noCoursesMessage = document.createElement('p');
        noCoursesMessage.textContent = 'No completed courses found.';
        completedCoursesList.appendChild(noCoursesMessage);
      }
    }
    updateCompletedCoursesModal();
  } else {
    console.error('Modal with ID', modalId, 'not found.');
  }
}

// Close the modal
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.style.display = 'none';
}

//Completed Courses Tab
function displayCompletedCourses() {
  const completedCoursesList = document.getElementById('completed-courses-list');
  completedCoursesList.innerHTML = ''; // Clear previous content

  completedCourses.forEach(function (courseId) {
    const courseItem = document.createElement('li');
    courseItem.textContent = courseId;

    completedCoursesList.appendChild(courseItem);
  });
}

//Expand Arrow for Completed Courses Manager
function toggleExpand() {
  var content = document.getElementById('completedCoursesList');
  var arrow = document.querySelector('.expand-arrow');

  if (content.style.display === 'none') {
    content.style.display = 'block';
    arrow.style.display = 'none';
  } else {
    content.style.display = 'none';
    arrow.style.display = 'inline';
  }
}

function updateCompletedCoursesModal() {
  const completedCoursesList = document.getElementById('completedCoursesList');
  completedCoursesList.innerHTML = '';

  if (completedCourses.length > 0) {
    completedCourses.forEach(function (course, index) {
      const courseItem = document.createElement('div');
      courseItem.textContent = course.id + ' ' + course.name;

      const removeButton = document.createElement('button');
      removeButton.textContent = 'Remove';
      removeButton.classList.add('remove-course-button');
      removeButton.setAttribute('data-index', index);
      removeButton.onclick = function () {};

      courseItem.appendChild(removeButton);
      completedCoursesList.appendChild(courseItem);
    });
  } else {
    const noCoursesMessage = document.createElement('p');
    noCoursesMessage.textContent = 'No completed courses found.';
    completedCoursesList.appendChild(noCoursesMessage);
  }
}

// Call the function to display completed courses when needed
document.addEventListener('DOMContentLoaded', function () {
  displayCompletedCourses();
});

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('major-select').addEventListener('change', function () {
    var selectedMajor = this.value;

    document.getElementById('hidden-major-dropdown').value = selectedMajor;

    console.log('Selected Major:', selectedMajor);
  });
});

//Open Stats SidePanel
function openNav() {
  document.getElementById('mySidepanel').style.width = '300px';
}

//Close Stats SidePanel
function closeNav() {
  document.getElementById('mySidepanel').style.width = '0';
}

// function handleGeneratePDFResponse(response) {
//   const pdfData = response.pdf_data;

//   const iframe = document.createElement('iframe');
//   iframe.src = 'data:application/pdf;base64,' + btoa(pdfData);
//   document.body.appendChild(iframe);
// }

//Fetch to_schedule Array From Flask
$(document).ready(function () {
  $('#pdfForm').submit(function (event) {
    event.preventDefault();

    var formData = $(this).serialize();

    $.ajax({
      type: 'POST',
      url: '/generate_pos',
      data: formData,
      success: function (response) {
        console.log(response);
        generateCourses(response);
        $('#alert').html('<p class="success">Plan of Study has been Generated.</p>').show();
        setTimeout(function () {
          $('#alert').hide();
        }, 5000);
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      },
    });
  });
});

//Stats Page Generation
function generateCourses(to_schedule) {
  console.log(to_schedule);

  if (to_schedule && to_schedule.length > 0) {
    let springCourses = [];
    let fallCourses = [];
    let allCourses = [];

    to_schedule.forEach((course) => {
      if (course.spring && !course.fall && !course.summer) {
        springCourses.push(course.cname);
      }
      if (course.fall && !course.spring && !course.summer) {
        fallCourses.push(course.cname);
      }
      if (course.spring && course.fall && course.summer) {
        allCourses.push(course.cname);
      }
    });

    const springHTML = '<h1>Spring Courses:</h1>';
    springCourses.forEach((course) => {
      springHTML += '<p>' + course + '</p>';
    });

    const fallHTML = '<h1>Fall Courses:</h1>';
    fallCourses.forEach((course) => {
      fallHTML += '<p>' + course + '</p>';
    });

    const allHTML = '<h1>Available All Semesters:</h1>';
    allCourses.forEach((course) => {
      allHTML += '<p>' + course + '</p>';
    });

    document.getElementById('springCourses').innerHTML = springHTML;
    document.getElementById('fallCourses').innerHTML = fallHTML;
    document.getElementById('allCourses').innerHTML = allHTML;
  } else {
    console.error('Data is undefined or empty');
  }
}
