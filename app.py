from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)


    # Calculate the required average for midterms and finals
    current_total = prelim_grade * prelim_weight
    required_total = passing_grade - current_total
    midterm_final_weight = midterm_weight + final_weight
    min_required_average = required_total / midterm_final_weight


    # Check if the preliminary grade is within the valid range
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        print("Error: Preliminary grade must be between 0 and 100.")
        return "Error: Preliminary grade must be between 0 and 100.", None

    # If the preliminary grade is 75 or more, the user has already passed
    if prelim_grade >= passing_grade:
        return None, f"Congratulations! You have passed. Required Grade for Midterms and Finals: {min_required_average}%"
   

    # If the required average exceeds 100, it's not possible to pass
    if min_required_average > 100:
        print("Error: It is not possible to achieve the passing grade with this preliminary score.")
        return "Error: It is not possible to achieve the passing grade with this preliminary score.", None

    # Ensure the required average is not below 0
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]

    # Print the required grade
    print(f"Required Grade for Midterms and Finals: {min_required_average}%")
    return None, f"Required Grade for Midterms and Finals: {min_required_average}%"

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    result_message = None
    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            error_message, result_message = calculate_required_grades(prelim_grade)
        except ValueError:
            error_message = "Error: Invalid input. Please enter a valid number."
    return render_template('index.html', error_message=error_message, result_message=result_message)

if __name__ == '__main__':
    app.run(debug=True)
