def calculate_grade(marks):
    if marks >= 90:
        return "A", "Excellent work! Keep shining! 🌟"
    elif marks >= 80:
        return "B", "Very Good! Keep it up! 👍"
    elif marks >= 70:
        return "C", "Good job! You can do even better! 😊"
    elif marks >= 60:
        return "D", "Don't give up. Keep practicing! 💪"
    else:
        return "F", "Failure is not the end. Work hard and try again! 🚀"


# Get student name
name = input("Enter student name: ")

# Input validation using while loop
while True:
    try:
        marks = int(input("Enter marks (0-100): "))

        if 0 <= marks <= 100:
            break
        else:
            print("❌ Marks must be between 0 and 100. Please try again.")

    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")


# Calculate grade and message
grade, message = calculate_grade(marks)

# Display result
print("\n📊 RESULT FOR", name.upper() + ":")
print("Marks:", str(marks) + "/100")
print("Grade:", grade)
print("Message:", message)