import win32gui
import win32ui
import win32con
import cv2
import keyboard
import numpy as np
import win32api
import time

def RightClickWithOutMouse(hwnd, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

# หาจอเกม
def background_screenshot(hwnd, width, height):
    try:
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)

        bmpstr = dataBitMap.GetBitmapBits(True)
        image = np.frombuffer(bmpstr, dtype='uint8')
        image.shape = (height, width, 4)

        return image
    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        return None
    finally:
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

try:
    hWnd = win32gui.FindWindow(None, 'Minecraft Forge* 1.20.1 - Singleplayer')
    if hWnd == 0:
        print("Window not found. Make sure the window title is correct.")
        exit()

    win_size = win32gui.GetWindowRect(hWnd)
    x, y, width, height = win_size[0], win_size[1], 850, 600

    while True:
        game_screenshot = background_screenshot(hWnd, 1280, 960)


        time.sleep(0.033)
        RightClickWithOutMouse(hWnd, 100, 100)

        bgr_screenshot = cv2.cvtColor(game_screenshot, cv2.COLOR_RGB2BGR)
        # cv2.imshow("Grayscale Screenshot", bgr_screenshot)
        cv2.waitKey(1)

        if keyboard.is_pressed("F4"):
            break

    cv2.destroyAllWindows()

except Exception as error:
    if str(error) == "CreateCompatibleDC failed":
        print("Error: CreateCompatibleDC failed")
