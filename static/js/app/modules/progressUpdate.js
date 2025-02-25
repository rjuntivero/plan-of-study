function updateProgressBar(completedCourses, totalCoursesCount, requiredCourses) {
  console.log('Completed Courses:', completedCourses);
  console.log('Required Courses:', requiredCourses);

  const completedRequiredCourses = [];

  completedCourses.filter((completedCourse) => {
    console.log('Checking completed course:', completedCourse);
    const foundRequiredCourse = requiredCourses.some((requiredCourse) => {
      console.log('Checking required course:', requiredCourse);
      const comparisonResult = requiredCourse.cname === completedCourse.name;
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

  console.log('Completed Required:', completedRequiredCourses);
  const completedRequiredCoursesCount = completedRequiredCourses.length;
  const completionPercentage = (completedRequiredCoursesCount / totalCoursesCount) * 100;

  // Update the progress ring
  const circle = document.querySelector('.progress-ring-circle-progress');
  const radius = circle.r.baseVal.value;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (completionPercentage / 100) * circumference;

  // Offset the stroke dash to reflect the completion percentage
  circle.style.strokeDashoffset = offset;

  // Define colors for the progress ring
  const color1 = '#FF6347'; // Red
  const color2 = '#FFD700'; // Yellow
  const color3 = '#32CD32'; // Green

  let strokeColor;
  if (completionPercentage < 50) {
    const interpolationFactor = completionPercentage / 50;
    strokeColor = interpolateColors(color1, color2, interpolationFactor);
  } else {
    const interpolationFactor = (completionPercentage - 50) / 50;
    strokeColor = interpolateColors(color2, color3, interpolationFactor);
  }

  // Set the stroke color of the progress ring
  circle.style.stroke = strokeColor;

  // Update the percentage text inside the circle
  const percentageText = document.querySelector('svg text');
  percentageText.textContent = `${completionPercentage.toFixed(2)}%`;

  updateStatusText(completedRequiredCoursesCount, totalCoursesCount);
}

// Function to interpolate between two colors
function interpolateColors(color1, color2, factor) {
  if (factor === undefined) factor = 0.5;
  let result = color1.slice();
  for (let i = 1; i < 7; i += 2) {
    let v1 = parseInt(color1.substr(i, 2), 16);
    let v2 = parseInt(color2.substr(i, 2), 16);

    let v = Math.round(v1 + (v2 - v1) * factor);

    result = result.substr(0, i) + v.toString(16).padStart(2, '0') + result.substr(i + 2);
  }
  return result;
}

//Update Message for Progress Circle Status
function updateStatusText(completedCoursesCount, totalCoursesCount) {
  const completionPercentage = (completedCoursesCount / totalCoursesCount) * 100;
  const statusText = document.getElementById('status-text');

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
  const incompleteCourses = requiredCourses.filter((course) => !course.completed);
  const totalCredits = incompleteCourses.reduce((total, course) => total + course.credit_hrs, 0);
  const totalCreditsElement = document.getElementById('total-credits');
  if (totalCreditsElement) {
    totalCreditsElement.textContent = totalCredits;
  }
}

export { updateProgressBar, updateStatusText, updateTotalCredits, interpolateColors };
