import cv2


def remove_alpha(image_path):
    # Load the image with alpha channel
    image_with_alpha = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Extract the RGB channels (excluding alpha)
    rgb_image = image_with_alpha[:, :, :3]

    # Save the RGB image without the alpha channel
    cv2.imwrite(image_path, rgb_image)

