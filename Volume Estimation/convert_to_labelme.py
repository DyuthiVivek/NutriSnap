
import json
import base64
import numpy as np
import cv2
from inference_sdk import InferenceHTTPClient

# input_image_path = "/home/dyuthi/Pictures/Screenshots/food2.png"
# input_image_path = "input/test.jpg"

def image_to_base64(input_image_path):
    with open(input_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

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

def generate_circle_points(center, radius, num_points=12):
    points = []
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        points.append([x, y])
    return points

def filter_points(points, img_width, img_height):
    # Filter out points that are out of image bounds
    return [[int(x), int(y)] for x, y in points if 0 <= x < img_width and 0 <= y < img_height]

def convert_to_labelme(result_food, result_plate, input_image_path):
    labelme_data = {
        "version": "4.5.6",
        "flags": {},
        "shapes": []
    }

    # Process food labels
    image_info = result_food['image']
    predictions = result_food['predictions']
    
    for prediction in predictions:
        points = [[point['x'], point['y']] for point in prediction['points']]
        points = ensure_polygon(points)
        points = filter_points(points, image_info['width'], image_info['height'])
        if points:  # Ensure there are points left after filtering
            shape = {
                "label": prediction['class'],
                "points": points,
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            labelme_data['shapes'].append(shape)

    # Process plate labels
    predictions = result_plate['predictions']
    
    for prediction in predictions:
        x, y = prediction['x'], prediction['y']
        width, height = prediction['width'], prediction['height']
        radius = max(width, height) / 2
        center = [x, y]
        points = generate_circle_points(center, radius)
        points = filter_points(points, image_info['width'], image_info['height'])
        if points:  # Ensure there are points left after filtering
            shape = {
                "label": "plate",
                "line_color": None,
                "fill_color": None,
                "points": points,
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            labelme_data['shapes'].append(shape)

    labelme_data["imagePath"] = input_image_path
    image_data = image_to_base64(input_image_path)
    labelme_data["imageData"] = image_data
    labelme_data["imageHeight"] = image_info['height']
    labelme_data["imageWidth"] = image_info['width']

    return json.dumps(labelme_data, indent=2)

def convert_image_to_json(input_image_path, output_file_path):
    CLIENT = InferenceHTTPClient(
        api_url="https://outline.roboflow.com",
        api_key="McnrQqcI6NyxbRYaSnjd"
    )

    result_food = CLIENT.infer(input_image_path, model_id="food-usjv9/1")

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="2JNa2qUJjzPnXLYHkz8e"
    )

    result_plate = CLIENT.infer(input_image_path, model_id="plates-and-bowls/1")

    # Assuming `result_food` and `result_plate` are the dictionaries returned by the inference SDK
    labelme_json = convert_to_labelme(result_food, result_plate, input_image_path)

    # Specify the file path where you want to save the JSON data
    # output_file_path = "labelme_data.json"

    # Write the JSON data to the file
    with open(output_file_path, "w") as json_file:
        json_file.write(labelme_json)

    print(f"LabelMe JSON data has been saved to {output_file_path}")
