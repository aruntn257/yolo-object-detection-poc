


def write_json_to_file(data, file_path):
    import json
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2,  ensure_ascii=False)