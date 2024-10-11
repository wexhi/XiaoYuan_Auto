import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import config


# Get the window object


def get_number():
    window = gw.getWindowsWithTitle("MuMu模拟器12")[0]

    # Get the screenshot of the window
    windows_box = [window.left, window.top, window.width, window.height]
    # print(windows_box)
    window_screenshot = pyautogui.screenshot(
        region=(window.left, window.top, window.width, window.height)
    )

    def find_question(window_screenshot):
        img = cv2.cvtColor(np.array(window_screenshot), cv2.COLOR_RGB2BGR)
        # Coordinates for left and right number regions
        left_number_x1, left_number_x2, left_number_y1, left_number_y2 = (
            config.LEFT_NUMBER_X1,
            config.LEFT_NUMBER_X2,
            config.LEFT_NUMBER_Y1,
            config.LEFT_NUMBER_Y2,
        )
        # print(left_number_x1, left_number_y1)
        right_number_x1, right_number_x2, right_number_y1, right_number_y2 = (
            config.RIGHT_NUMBER_X1,
            config.RIGHT_NUMBER_X2,
            config.RIGHT_NUMBER_Y1,
            config.RIGHT_NUMBER_Y2,
        )
        roi = img[230:430, :]
        # Extract left and right numbers
        left_number = roi[
            :,
            left_number_x1:left_number_x2,
        ]
        right_number = roi[
            :,
            right_number_x1:right_number_x2,
        ]
        cv2.rectangle(
            img,
            (left_number_x1, left_number_y1),
            (left_number_x2, left_number_y2),
            (0, 255, 0),
            2,
        )
        cv2.rectangle(
            img,
            (right_number_x1, right_number_y1),
            (right_number_x2, right_number_y2),
            (0, 255, 0),
            2,
        )
        return left_number, right_number, roi

    left_number, right_number = np.zeros(
        (
            (config.LEFT_NUMBER_Y2 - config.LEFT_NUMBER_Y1),
            (config.LEFT_NUMBER_X2 - config.LEFT_NUMBER_X1),
            3,
        )
    ), np.zeros(
        (
            (config.RIGHT_NUMBER_Y2 - config.RIGHT_NUMBER_Y1),
            (config.RIGHT_NUMBER_X2 - config.RIGHT_NUMBER_X1),
            3,
        )
    )
    if window.isActive:
        left_number, right_number, _ = find_question(window_screenshot)

    # Check image size validity before returning
    if left_number.size > 0 and right_number.size > 0:
        return left_number, right_number, window
    else:
        return (
            np.zeros(
                (
                    (config.LEFT_NUMBER_Y2 - config.LEFT_NUMBER_Y1),
                    (config.LEFT_NUMBER_X2 - config.LEFT_NUMBER_X1),
                    3,
                )
            ),
            np.zeros(
                (
                    (config.RIGHT_NUMBER_Y2 - config.RIGHT_NUMBER_Y1),
                    (config.RIGHT_NUMBER_X2 - config.RIGHT_NUMBER_X1),
                    3,
                )
            ),
            window,
        )
