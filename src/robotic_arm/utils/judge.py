from robotic_arm.config import CAMERA_CENTER_JUDGEMENT_OFFSET, CAMERA_CENTER_AREA_JUDGEMENT_RATIO

__camera_center_judgement_lower_bound = 0.5 - CAMERA_CENTER_JUDGEMENT_OFFSET
__camera_center_judgement_upper_bound = 0.5 + CAMERA_CENTER_JUDGEMENT_OFFSET
__camera_center_judgement_area = 4 * CAMERA_CENTER_JUDGEMENT_OFFSET ** 2


def is_point_at_camera_center(x: float, y: float) -> bool:
    return __camera_center_judgement_lower_bound <= x <= __camera_center_judgement_upper_bound and \
           __camera_center_judgement_lower_bound <= y <= __camera_center_judgement_upper_bound


def is_rect_at_camera_center_for_data(data) -> bool:
    return is_rect_at_camera_center(data.relative_bounding_box.xmin,
                                    data.relative_bounding_box.ymin,
                                    data.relative_bounding_box.width,
                                    data.relative_bounding_box.height)


def is_rect_at_camera_center(x: float, y: float, width: float, height: float) -> bool:
    xm, ym = x + width, y + height
    if (xm <= __camera_center_judgement_lower_bound or __camera_center_judgement_upper_bound <= x) \
            and (ym <= __camera_center_judgement_lower_bound or __camera_center_judgement_upper_bound <= y):
        return False
    intersection_height = min(xm, __camera_center_judgement_upper_bound) - max(x, __camera_center_judgement_lower_bound)
    intersection_width = min(ym, __camera_center_judgement_upper_bound) - max(y, __camera_center_judgement_lower_bound)
    return intersection_width * intersection_height > CAMERA_CENTER_AREA_JUDGEMENT_RATIO * __camera_center_judgement_area
