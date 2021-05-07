def get_center_point(data):
    return data.relative_bounding_box.xmin + data.relative_bounding_box.width / 2, \
           data.relative_bounding_box.ymin + data.relative_bounding_box.height / 2


def get_rect_data(data):
    return data.relative_bounding_box.xmin, data.relative_bounding_box.ymin, \
           data.relative_bounding_box.width, data.relative_bounding_box.height
