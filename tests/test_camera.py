import cv2

print(cv2.__version__)

for backend_name, backend in [
    ("CAP_ANY", cv2.CAP_ANY),
    ("CAP_DSHOW", cv2.CAP_DSHOW),
    ("CAP_MSMF", cv2.CAP_MSMF),
]:
    print(f"\n=== {backend_name} ===")

    for i in range(5):
        print(f"Testing index {i}")

        cap = cv2.VideoCapture(i, backend)

        opened = cap.isOpened()
        print("isOpened:", opened)

        if opened:
            ret, frame = cap.read()
            print("frame:", ret)

            if ret:
                print("Success")
                cv2.imshow("cam", frame)
                cv2.waitKey(3000)
                cv2.destroyAllWindows()
                exit()

        cap.release()