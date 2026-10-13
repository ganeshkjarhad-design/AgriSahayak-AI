# FINAL YEAR PPT CONTENT — 14 SLIDES

## Slide 1 — Title
AgriSahayak AI
AI-Based Crop Disease Detection, Agricultural Worker Recommendation and Farm Assistance System
Student Name | PRN | Department | Guide | Academic Year

## Slide 2 — Problem Background
- Farmers need quick crop-health information.
- Disease symptoms can be difficult to identify.
- Finding suitable agricultural workers can take time.
- Digital services often solve these problems separately.

## Slide 3 — Motivation
- Apply AI to a practical agricultural problem.
- Make disease screening easier.
- Improve worker discovery and matching.
- Demonstrate Data Science, AI, database and web skills.

## Slide 4 — Objectives
- Build an AI leaf-image classifier.
- Store structured crop/disease information.
- Recommend suitable agricultural workers.
- Support worker booking.
- Display analytics.

## Slide 5 — Proposed System
Farmer -> Web App -> Disease AI / Worker Search -> Database -> Analytics

## Slide 6 — System Architecture
Frontend: HTML/CSS/JS
Backend: Flask/Python
AI: MobileNetV2 + TensorFlow
Database: SQLite/MySQL
Analytics: Pandas/Chart.js/Power BI

## Slide 7 — AI Disease Detection
Image upload -> resize/normalize -> MobileNetV2 -> softmax -> predicted class + confidence -> knowledge-base lookup.

## Slide 8 — Dataset
PlantVillage
- ~54k leaf images
- 38 categories in TensorFlow documentation
- 14 crop species represented
- Train/validation/test evaluation
- Additional Indian field images recommended for future work

## Slide 9 — Worker Recommendation
Features:
Skill match
Location
Experience
Rating
Availability
Transparent weighted score -> ranked workers

## Slide 10 — Database / ER Diagram
Show the ER diagram from ER_DIAGRAM.md.

## Slide 11 — Website Screens
Show screenshots of:
Home
Disease prediction
Worker search
Worker registration
Dashboard

## Slide 12 — Evaluation
Disease model:
Accuracy
Precision
Recall
F1-score
Confusion matrix
Recommendation:
Booking success / user feedback after real testing

## Slide 13 — Advantages, Limitations, Future Scope
Advantages: integrated platform, AI-assisted screening, worker matching, analytics.
Limitations: dataset bias, field-image variation, no expert replacement.
Future: multilingual UI, GPS, weather, mobile app, expert verification.

## Slide 14 — Conclusion
AgriSahayak AI combines computer vision, machine learning, recommendation logic, database management and analytics into one agriculture assistance platform.
