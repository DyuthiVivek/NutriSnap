import cv2

# Load the image with alpha channel
image_with_alpha = cv2.imread("/home/dyuthi/Pictures/Screenshots/food2.png", cv2.IMREAD_UNCHANGED)

# Extract the RGB channels (excluding alpha)
rgb_image = image_with_alpha[:, :, :3]

# Save the RGB image without the alpha channel
cv2.imwrite("/home/dyuthi/Pictures/Screenshots/food2.png", rgb_image)

