from convert_to_labelme import convert_image_to_json
from remove_alpha_channel import remove_alpha
from demo import main

input_image_path = "input/test.jpg"
output_path = "input/test.json"

remove_alpha(input_image_path)
convert_image_to_json(input_image_path, output_path)
volumes = main()
print(volumes[0])