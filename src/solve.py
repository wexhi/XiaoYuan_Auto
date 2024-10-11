import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
import time


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

        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # left_number_img = cv2.dilate(left_number_img, kernel)
        # right_number_img = cv2.dilate(right_number_img, kernel)

        # left_number_img = cv2.resize(
        #     left_number_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
        # )
        # right_number_img = cv2.resize(
        #     right_number_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
        # )

        # # 膨胀操作
        # kernel = np.ones((3, 3), np.uint8)
        # left_number_img = cv2.dilate(left_binary, kernel)
        # right_number_img = cv2.dilate(right_binary, kernel)

        # cv2.imshow("left_number_img", left_number_img)
        # cv2.imshow("right_number_img", right_number_img)

        # create window
        cv2.namedWindow("left_number_img", cv2.WINDOW_NORMAL)
        cv2.namedWindow("right_number_img", cv2.WINDOW_NORMAL)
        cv2.imshow("left_number_img", left_number_img)
        cv2.imshow("right_number_img", right_number_img)

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

        def draw_great_than(win_x, win_y):
            pyautogui.moveTo(win_x + 200, win_y + 450)
            pyautogui.dragTo(win_x + 500, win_y + 450)
            pyautogui.moveTo(win_x + 500, win_y + 450)
            pyautogui.dragTo(win_x + 200, win_y + 650)

        def draw_less_than(win_x, win_y):
            pyautogui.moveTo(win_x + 500, win_y + 450)
            pyautogui.dragTo(win_x + 200, win_y + 450)
            pyautogui.moveTo(win_x + 200, win_y + 450)
            pyautogui.dragTo(win_x + 500, win_y + 650)

        def draw_equal(win_x, win_y):
            pyautogui.moveTo(win_x + 200, win_y + 650)
            pyautogui.dragTo(win_x + 500, win_y + 650)
            pyautogui.moveTo(win_x + 200, win_y + 700)
            pyautogui.dragTo(win_x + 500, win_y + 700)

        def draw_flag(operation):
            win_box = [window.left, window.top, window.width, window.height]
            win_x, win_y, win_w, win_h = win_box
            if operation == "<":
                draw_less_than(win_x, win_y)
            elif operation == ">":
                draw_great_than(win_x, win_y)
            elif operation == "=":
                draw_equal(win_x, win_y)
            else:
                pass

        def auto_continue():
            win_box = [window.left, window.top, window.width, window.height]
            win_x, win_y, win_w, win_h = win_box
            pyautogui.click(win_x + 350, win_y + 680, duration=0.5)
            pyautogui.click(win_x + 600, win_y + 1300, duration=0.5)
            pyautogui.click(win_x + 400, win_y + 1170, duration=0.5)

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
            self.isContinue = False

        self.left_num_last = left_num
        self.right_num_last = right_num
