# user/scripts/load_reviews.py
import csv
from user.models import Hospital_Reviews

# Assuming your CSV file is named hospital_reviews.csv
csv_file_path = "/Users/shreya/desktop/hospital_reviews.csv"

with open(csv_file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        hospital_name = row["hospital_name"]

        # Assuming your CSV columns are: review_from, rating, likes, description
        review_from = row["review_from"]
        rating = int(row["rating"])
        likes = row["likes"]
        description = row["description"]

        review = Hospital_Reviews.objects.create(
            hospital_name=hospital_name,
            review_from=review_from,
            rating=rating,
            likes=likes,
            description=description,
        )
        review.save()
