# NutriSnap

NutriSnap is an application developed to utilize image recognition technology for extracting nutritional information from Indian food images. The app provides users with approximate nutritional data, including calorie counts and macronutrient breakdowns, by analyzing pictures of their plate.

## Objective
- Use image recognition to extract nutritional information from food images.
- Provide nutritional data like calorie counts and macronutrient breakdowns.
- Explore image segmentation, object detection, and learn the Roboflow framework.

## Approach
1. **Image Segmentation:** Identify food items and their respective classes on the plate.
2. **Object Detection:** Detect the boundaries of the plate.
3. **Volume Estimation:** Estimate the volume of food on the plate.
4. **Nutrient Information:** Use the volume and food class to estimate nutritional information.

## Tech Stack
- Python
- Roboflow
- HTML, CSS
- Flask

## Models Used
- **Indian Food Dataset:** 507 images, 51 classes. Dataset link: [Indian Food Dataset](https://universe.roboflow.com/search?q=indian%2520food)
- **Plate Detection Dataset:** 279 images. Dataset link: [Plate Detection](https://universe.roboflow.com/nutrisnap-zpqca/plates-and-bowls/model/1)
- **Volume Estimation Model:** GitHub link: [Volume Estimation](https://github.com/WhiteXiezx/Food-Volume-Estimation?tab=readme-ov-file#volume-estimation)

## Limitations
- The entire plate must be within the camera frame for accurate analysis.
- Accuracy improvement is limited due to GPU unavailability and lack of datasets.
- Varying calorie content based on food preparation methods cannot be accounted for.


