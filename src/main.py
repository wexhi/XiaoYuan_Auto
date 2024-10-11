# 小猿口算PK
# 1. 读取屏幕上的题目
# 2. 识别题目
# 3. 计算题目
# 4. 鼠标模拟输出答案

from get_number import get_number
from solve import Solve
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if __name__ == "__main__":
    solve = Solve()
    while True:
        left_number_img, right_number_img, window = get_number()
        if window.isActive:
            solve.solve(left_number_img, right_number_img, window)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
