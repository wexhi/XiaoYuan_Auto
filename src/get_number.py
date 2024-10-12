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

    # Calculate scaling factors
    scale_x = window.width / config.WINDOW_DEFAULT_WIDTH
    scale_y = window.height / config.WINDOW_DEFAULT_HEIGHT

    def find_question(window_screenshot):
        img = cv2.cvtColor(np.array(window_screenshot), cv2.COLOR_RGB2BGR)
        # Scale coordinates dynamically based on the current window size
        left_number_x1 = int(config.LEFT_NUMBER_X1 * scale_x)
        left_number_x2 = int(config.LEFT_NUMBER_X2 * scale_x)
        left_number_y1 = int(config.LEFT_NUMBER_Y1 * scale_y)
        left_number_y2 = int(config.LEFT_NUMBER_Y2 * scale_y)

        right_number_x1 = int(config.RIGHT_NUMBER_X1 * scale_x)
        right_number_x2 = int(config.RIGHT_NUMBER_X2 * scale_x)
        right_number_y1 = int(config.RIGHT_NUMBER_Y1 * scale_y)
        right_number_y2 = int(config.RIGHT_NUMBER_Y2 * scale_y)
        # 在 img 中画出左边数字的候选框
        cv2.rectangle(
            img,
            (left_number_x1, left_number_y1),
            (left_number_x2, left_number_y2),
            (0, 255, 0),
            2,
        )

        # 在 img 中画出右边数字的候选框
        cv2.rectangle(
            img,
            (right_number_x1, right_number_y1),
            (right_number_x2, right_number_y2),
            (0, 255, 0),
            2,
        )

        # 显示带有候选框的原始图像（img）
        cv2.imshow("Bounding Boxes in Original Image", img)

        # 提取左边和右边的数字区域
        left_number = img[left_number_y1:left_number_y2, left_number_x1:left_number_x2]
        right_number = img[
            right_number_y1:right_number_y2, right_number_x1:right_number_x2
        ]
        return left_number, right_number, img

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
