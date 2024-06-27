import cv2
import trackpy as tp
import numpy as np
import pandas as pd 

# Video dosyasını açma
input_video_path = '/Users/mevasaglamtas/Downloads/WhatsApp Video 2024-06-23 at 15.07.09.mp4'
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print("Error: Input video not opened.")
    exit()

# Videonun özelliklerini alma
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}, Frame Width: {frame_width}, Frame Height: {frame_height}, Frame Count: {frame_count}")

# Trackpy parametreleri
diameters = [5, 15, 21]  # Farklı çaplarda parçacıkları tespit etme

# Kareleri işleme
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale'e çevirme

    # Tespit edilen tüm parçacıkları birleştirmek için boş bir DataFrame oluştur
    all_features = pd.DataFrame()

    for diameter in diameters:
        f = tp.locate(gray, diameter, invert=True, minmass=100)  # Parçacık tespiti
        if f is not None and not f.empty:
            all_features = pd.concat([all_features, f])

    if not all_features.empty:
        # Tespit edilen parçacıkları çerçeveye çizme
        for index, row in all_features.iterrows():
            cv2.circle(frame, (int(row['x']), int(row['y'])), int(diameter // 2), (0, 0, 255), 1)


    cv2.imshow('Tracked Video', frame)  # İşlenmiş kareyi gösterme

    # 'q' tuşuna basıldığında videoyu durdur
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()

print("Processing complete. Video displayed.")
