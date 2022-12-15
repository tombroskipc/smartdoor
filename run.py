from dotenv import load_dotenv
load_dotenv()
import asyncio
from time import sleep

from init import *

from constant import *

def main():
    capture_service = setup_capture_service()
    face_req_service = setup_facereq_service()
    backend_service = setup_backend_service()

    setup_adafruit_service(capture_service, face_req_service, backend_service)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()