import cv2
import trackpy as tp
import numpy as np
import pandas as pd 

# Video dosyasını açma
input_video_path = '/Users/mevasaglamtas/Downloads/'

output_video_path = '/Users/mevasaglamtas/Downloads/outputvideo/'
output_excel_path ='/Users/mevasaglamtas/Downloads/outputexcel/'
# Bos excel dosyasi
# Console prompt for selection of files

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
diameters = [5, 11, 21]  # Farklı çaplarda parçacıkları tespit etme ==> burası işe yaramıyor olabilir 

# Kareleri işleme
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale'e çevirme
    # Check filters

    # Tespit edilen tüm parçacıkları birleştirmek için boş bir DataFrame oluşturma 
    all_features = pd.DataFrame()

    for diameter in diameters:
        f = tp.locate(gray, diameter, invert=True, minmass=100)  # Parçacık tespiti
        if f is not None and not f.empty:
            all_features = pd.concat([all_features, f]) # data framelerin birleştirilmesi

    if not all_features.empty:
        # Tespit edilen parçacıkları çerçeveye çizme
        for index, row in all_features.iterrows():
            cv2.circle(frame, (int(row['x']), int(row['y'])), int(diameter // 2), (0, 0, 255), 1)
# pandas.read_excel(io, sheet_name=0, *, header=0, names=None, index_col=None, usecols=None, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, parse_dates=False, date_parser=_NoDefault.no_default, date_format=None, thousands=None, decimal='.', comment=None, skipfooter=0, storage_options=None, dtype_backend=_NoDefault.no_default, engine_kwargs=None)

    cv2.imshow('Tracked Video', frame)  # İşlenmiş kareyi gösterme

    # 'q' tuşuna basıldığında videoyu durdur
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()

print("Processing complete. Video displayed.")
