from ultralytics import YOLO
from json import loads
from utils.const_file import OBJECT_DETECTION_MODEL_PATH, BRAND_DETECTION_MODEL_PATH, RESULTS_DIR
from datetime import datetime 
from utils.file_handler import write_json_to_file


def detect_img_obj(img_path):
    model = YOLO(OBJECT_DETECTION_MODEL_PATH)

    results = model(img_path)

    results_dir = RESULTS_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir.mkdir(exist_ok=True)

    for idx,result in enumerate(results):
        result.save(rf"{results_dir}/img_{idx}.jpg")

    result_json = loads(results[0].to_json())
    print("result json",result_json)
    # print("="*10)
    return_result_json={
        'image_detected': [],
        'confidence_score': []
    }
    for res in result_json:
        return_result_json['image_detected'].append(res["name"])
        return_result_json['confidence_score'].append(res["confidence"])

    write_json_to_file(return_result_json, rf"{results_dir}/result.json")

    return return_result_json

def detect_brand(detect_result, img_path):
    invalid = True
    for val in detect_result['image_detected']:
        if 'bottle' == val:
            invalid = False
    if invalid:
        return {
            "object_detected": detect_result,
            "message": "No bottle detected. Try different images."
        }
    model = YOLO(BRAND_DETECTION_MODEL_PATH)

    results = model(img_path)

    result_json = loads(results[0].to_json())
    print("result json",result_json)

    return_result_json={
        'brand_detected': [],
        'confidence_score': []
    }
    for res in result_json:
        return_result_json['brand_detected'].append(res["name"])
        return_result_json['confidence_score'].append(res["confidence"])
    
    detect_result = {
        'object_detected': detect_result,
        'brand_detected': return_result_json
    }
    return detect_result

if __name__ == "__main__":
    source = rf"images/OIP_1.webp"
    print(detect_img(source))
    print(detect_brand({}, source))
