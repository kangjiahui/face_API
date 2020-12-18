import asyncio
import websockets
import cv2
from modules.utils.api import *


print(' ========= websocket is going to run =========')


async def time(websocket, path):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, img = video_capture.read()
        if not ret:
            break
        result = search_identity(image=img)
        await websocket.send(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()


start_server = websockets.serve(time, "10.20.50.163", 5678)
print(' ========= websocket running =========')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

