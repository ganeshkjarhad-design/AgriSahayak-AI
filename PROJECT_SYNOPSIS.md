# PROJECT SYNOPSIS
## AgriSahayak AI
### AI-Based Crop Disease Detection, Agricultural Worker Recommendation and Farm Assistance System

### 1. Introduction
Agriculture often requires quick identification of crop health problems and access to suitable farm workers. AgriSahayak AI is a web-based academic prototype that combines computer vision, machine learning, a worker recommendation module and data analytics in one platform.

### 2. Problem Statement
Farmers may have difficulty identifying crop diseases from visible symptoms and may also struggle to find agricultural workers with the required skill and availability. Existing systems often address these needs separately. The proposed system combines both functions and provides a simple digital interface.

### 3. Objectives
1. Detect selected crop diseases/healthy conditions from leaf images using deep learning.
2. Provide structured, label-based agricultural guidance records linked to model classes.
3. Help farmers search and rank agricultural workers using skill, location, experience and rating.
4. Support worker booking and maintain booking history.
5. Generate simple analytics for crop-health and worker-demand information.

### 4. Scope
The prototype focuses on image classification, worker discovery/recommendation, booking, database management and analytics. It can later be extended with multilingual support, GPS, weather data, notifications, expert verification and mobile deployment.

### 5. Proposed Modules
1. User/Farmer Module
2. Worker Registration Module
3. Crop Disease AI Module
4. Treatment/Guidance Knowledge Module
5. Worker Search Module
6. Recommendation Module
7. Booking Module
8. Database Module
9. Analytics Dashboard
10. Admin/Model Management Module

### 6. Methodology
Image -> preprocessing -> transfer-learning classifier -> class prediction -> confidence -> knowledge-base lookup.
Worker request -> filtering -> feature scoring -> ranked worker list -> booking.

### 7. AI Model
MobileNetV2 transfer learning is used as the baseline image classifier. Input images are resized to 224x224. The pretrained convolutional base extracts visual features, followed by global average pooling, dropout and a softmax classification layer. The model is evaluated using accuracy, precision, recall, F1-score and confusion matrix.

### 8. Recommendation Logic
A transparent baseline score can be:
Score = 0.35 Skill Match + 0.25 Location Match + 0.20 Experience Score + 0.10 Rating Score + 0.10 Availability Match.
Weights can be tuned after collecting real booking data. The prototype first uses database filtering and sorting; an ML recommender can be added after enough interaction data is collected.

### 9. Hardware/Software
Hardware: 4-core CPU, 8 GB RAM minimum; GPU optional.
Software: Python, Flask, SQLite/MySQL, TensorFlow/Keras, OpenCV/Pillow, Pandas, NumPy, Scikit-learn, HTML/CSS/JavaScript.

### 10. Dataset
PlantVillage is a public plant-leaf image dataset. TensorFlow's dataset documentation describes 54,303 images in 38 categories. It is suitable for the disease-classification component. For a stronger Indian deployment, additional locally collected and expert-verified images should be added later.

### 11. Expected Results
- Web application with farmer and worker workflows.
- Disease classifier that outputs a class and confidence score.
- Search/ranking of workers.
- Booking record storage.
- Analytics dashboard.
- Evaluation report with model metrics.

### 12. Limitations
- Public datasets may not represent all Indian field conditions.
- Leaf-image classification does not replace expert diagnosis.
- Worker ratings/availability require real user data.
- Recommendation quality improves only after sufficient interaction data.
- Treatment information must be reviewed and kept current.

### 13. Future Scope
Multilingual Marathi/Hindi/English UI, mobile app, GPS distance calculation, weather-aware risk alerts, voice input, expert verification, real-time notifications, explainable AI, edge/mobile inference and integration with verified agricultural advisories.

### 14. Conclusion
AgriSahayak AI demonstrates how Data Science and AI can be combined with a practical agricultural service platform. The project integrates computer vision, database systems, recommendation logic and analytics in a single academic prototype.
