import json
import base64
import numpy as np
import cv2

#IMAGE_PATH = "/home/dyuthi/Pictures/Screenshots/food2.png"
IMAGE_PATH = "test.jpg"

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def ensure_polygon(points):
    # Convert points to NumPy array
    points = np.array(points)
    
    # Check if the points form a closed polygon
    if cv2.isContourConvex(points):
        return points.tolist()  # No need to modify, return the points
    
    # If not closed, add the first point at the end to close the shape
    points = np.vstack([points, points[0]])
    return points.tolist()

def ensure_polygon(points):
    # Convert points to NumPy array
    points = np.array(points)
    
    try:
        # Check if the points form a closed polygon
        if cv2.isContourConvex(points):
            return points.tolist()  # No need to modify, return the points
    except cv2.error as e:
        print(f"Error occurred: {e}")
    
    # If not closed, add the first point at the end to close the shape
        points = np.vstack([points, points[0]])
        return points.tolist()

def convert_to_labelme(result):
    image_info = result['image']
    predictions = result['predictions']

    labelme_data = {
        "version": "4.5.6",
        "flags": {},
        "shapes": []
    }

    for prediction in predictions:
        points = [[point['x'], point['y']] for point in prediction['points']]
        points = ensure_polygon(points)  # Ensure the points form a polygon
        shape = {
            "label": prediction['class'],
            "points": points,
            "group_id": None,
            "shape_type": "polygon",
            "flags": {}
        }
        labelme_data['shapes'].append(shape)

    labelme_data["imagePath"] = IMAGE_PATH  # Provide the image path here
    
    # Generate image data and add it to the JSON
    image_data = image_to_base64(IMAGE_PATH)
    labelme_data["imageData"] = image_data
    
    labelme_data["imageHeight"] = image_info['height']
    labelme_data["imageWidth"] = image_info['width']

    return json.dumps(labelme_data, indent=2)

# The rest of your code remains the same...
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="McnrQqcI6NyxbRYaSnjd"
)

result = CLIENT.infer(IMAGE_PATH, model_id="food-usjv9/1")

# Assuming `result` is the dictionary returned by the inference SDK
labelme_json = convert_to_labelme(result)
print(labelme_json)

# Specify the file path where you want to save the JSON data
output_file_path = "labelme_data.json"

# Write the JSON data to the file
with open(output_file_path, "w") as json_file:
    json_file.write(labelme_json)

print(f"LabelMe JSON data has been saved to {output_file_path}")
