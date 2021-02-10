mkdir Apk
cp main.py Apk/
cp lib_cliente.py Apk/
cd Apk/
buildozer init
buildozer android debug
rm main.py
rm lib_cliente.py
