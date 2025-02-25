function handleSearchFormSubmit() {
  $('#searchForm').submit(function (event) {
    event.preventDefault();

    const filter1Value = $('#filter1').val();
    const filter2Value = $('#filter2').val();
    const filter3Value = $('#filter3').val();

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
}

function handleMajorSelectChange() {
  $('#major-select').change(function () {
    const selectedMajor = $(this).val();
    if (selectedMajor) {
      fetchRequiredCourses(selectedMajor);
    } else {
      $('#required-courses-list').empty();
    }
  });
}

function handleAddCourseButtonClick() {
  $(document).on('click', '.add-button', function () {
    const selectedMajor = $('#major-select').val();

    if (selectedMajor) {
      const courseId = $(this).closest('form').find('input[name="course_id"]').val();
      const courseName = $(this).closest('form').find('input[name="course_name"]').val();

      if (!completedCourses.some((course) => course.id === courseId && course.name === courseName)) {
        completedCourses.push({ id: courseId, name: courseName });
        $('#completed-courses-list').append('<p>' + courseName + '</p>');
        $.ajax({
          url: '/add-course',
          method: 'POST',
          data: { course_id: courseId, course_name: courseName },
          success: function (response) {
            console.log('Course added successfully:', response.course_name);
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
}
