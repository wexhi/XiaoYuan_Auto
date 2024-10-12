import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
import time
import config


class Solve:
    def __init__(self):
        self.left_num_last = 0
        self.right_num_last = 0
        self.error_count = 0
        self.isContinue = False
        self.operation_save = ["<", ">", "="]

    def solve(self, left_number_img, right_number_img, window):
        # 确保输入图像是 uint8 类型
        if left_number_img.dtype != np.uint8:
            left_number_img = (
                255
                * (left_number_img - np.min(left_number_img))
                / np.ptp(left_number_img)
            ).astype(np.uint8)
        if right_number_img.dtype != np.uint8:
            right_number_img = (
                255
                * (right_number_img - np.min(right_number_img))
                / np.ptp(right_number_img)
            ).astype(np.uint8)

        left_gray = cv2.cvtColor(left_number_img, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right_number_img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, left_number_img = cv2.threshold(left_gray, 127, 255, cv2.THRESH_BINARY)
        _, right_number_img = cv2.threshold(right_gray, 127, 255, cv2.THRESH_BINARY)

        # 将图像数据转换为 PIL 格式
        left_number_img_pil = Image.fromarray(left_number_img)
        right_number_img_pil = Image.fromarray(right_number_img)

        # OCR 识别
        left_num = pytesseract.image_to_string(
            left_number_img_pil, config="--oem 3 --psm 6 outputbase digits"
        )
        right_num = pytesseract.image_to_string(
            right_number_img_pil, config="--oem 3 --psm 6 outputbase digits"
        )

        # string to int
        try:
            left_num = int(left_num)
            right_num = int(right_num)
        except ValueError:
            left_num = 0
            right_num = 0

        # print(f"left_num: {left_num},right_num: {right_num}")
        # print(
        #     f"left_num_last: {self.left_num_last}, right_num_last: {self.right_num_last}"
        # )

        def calculate(left_num, right_num):
            operations = ["<", ">", "=", "break"]
            if left_num < right_num:
                return operations[0]
            elif left_num > right_num:
                return operations[1]
            elif left_num == right_num and left_num != 0 and right_num != 0:
                return operations[2]
            else:
                return operations[3]

        operation = calculate(left_num, right_num)
        # print(f"operation: {operation}")

        def draw_great_than(win_x, win_y, scale_x, scale_y):
            pyautogui.moveTo(win_x + int(200 * scale_x), win_y + int(450 * scale_y))
            pyautogui.dragTo(win_x + int(500 * scale_x), win_y + int(450 * scale_y))
            pyautogui.moveTo(win_x + int(500 * scale_x), win_y + int(450 * scale_y))
            pyautogui.dragTo(win_x + int(200 * scale_x), win_y + int(650 * scale_y))

        def draw_less_than(win_x, win_y, scale_x, scale_y):
            pyautogui.moveTo(win_x + int(500 * scale_x), win_y + int(450 * scale_y))
            pyautogui.dragTo(win_x + int(200 * scale_x), win_y + int(450 * scale_y))
            pyautogui.moveTo(win_x + int(200 * scale_x), win_y + int(450 * scale_y))
            pyautogui.dragTo(win_x + int(500 * scale_x), win_y + int(650 * scale_y))

        def draw_equal(win_x, win_y, scale_x, scale_y):
            pyautogui.moveTo(win_x + int(200 * scale_x), win_y + int(650 * scale_y))
            pyautogui.dragTo(win_x + int(500 * scale_x), win_y + int(650 * scale_y))
            pyautogui.moveTo(win_x + int(200 * scale_x), win_y + int(700 * scale_y))
            pyautogui.dragTo(win_x + int(500 * scale_x), win_y + int(700 * scale_y))

        def draw_flag(operation):
            win_box = [window.left, window.top, window.width, window.height]
            win_x, win_y, win_w, win_h = win_box

            # 计算缩放比例
            scale_x = win_w / config.WINDOW_DEFAULT_WIDTH
            scale_y = win_h / config.WINDOW_DEFAULT_HEIGHT

            # 根据缩放比例调整鼠标点击的坐标
            if operation == "<":
                draw_less_than(win_x, win_y, scale_x, scale_y)
            elif operation == ">":
                draw_great_than(win_x, win_y, scale_x, scale_y)
            elif operation == "=":
                draw_equal(win_x, win_y, scale_x, scale_y)

        def auto_continue():
            win_box = [window.left, window.top, window.width, window.height]
            win_x, win_y, win_w, win_h = win_box

            # 计算缩放比例
            scale_x = win_w / config.WINDOW_DEFAULT_WIDTH
            scale_y = win_h / config.WINDOW_DEFAULT_HEIGHT

            # 调整点击位置
            pyautogui.click(
                win_x + int(350 * scale_x), win_y + int(680 * scale_y), duration=0.5
            )
            pyautogui.click(
                win_x + int(600 * scale_x), win_y + int(1300 * scale_y), duration=0.5
            )
            pyautogui.click(
                win_x + int(400 * scale_x), win_y + int(1170 * scale_y), duration=0.5
            )

        if left_num == 0 and right_num == 0:
            print(
                "没有找到数字，如果游戏进行中，请调整窗口位置，确保为竖屏，且窗口越大越好，需要确保数字在绿色框中"
            )

        if left_num != self.left_num_last or right_num != self.right_num_last:
            self.error_count = 0
            draw_flag(operation)
            print(f"operation: {operation}")
            # print("draw_flag")
            if operation == "break":
                self.isContinue = True

        if (
            left_num == self.left_num_last
            and right_num == self.right_num_last
            and (left_num != 0 or right_num != 0)
        ):  # 当连续识别到相同数字时，计数器加一，可能为识别错误的情况
            self.error_count += 1

        if self.error_count > 5:  # 当连续识别错误次数大于5时，自动点击继续
            for oper in self.operation_save:
                draw_flag(oper)
                time.sleep(1)

        if (
            left_num == 0 and right_num == 0 and self.isContinue
        ):  # 当没识别到数字时，自动点击继续
            time.sleep(5)
            auto_continue()
            print("没有找到数字，可能游戏已结束，自动点击继续")
            self.isContinue = False

        self.left_num_last = left_num
        self.right_num_last = right_num
