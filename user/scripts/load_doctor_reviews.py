import csv
<<<<<<< HEAD
from user.models import Doctor_Reviews  # Add Doctor to the import statement
=======
from user.models import Doctor_Reviews, Doctor  # Add Doctor to the import statement
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
>>>>>>> 6912ffa (Autoformat code with Black)

# Assuming your CSV file is named doctor_reviews.csv
csv_file_path = "/Users/shreya/desktop/doctor_reviews.csv"

with open(csv_file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        doctor_name = row["doctor_name"]
        review_from = row["review_from"]
        rating = (
            int(row["rating"]) if row["rating"] else 0
        )  # Convert to int if not empty, else set to 0
        likes = row["likes"]
        description = row["description"]

        review = Doctor_Reviews.objects.create(
            doctor_name=doctor_name,
            review_from=review_from,
            rating=rating,
            likes=likes,
            description=description,
        )
        review.save()
