import snowboydecoder
import speech_recognition as sr
import time
from Crypto.Cipher import AES
import base64


def detected_callback():
    print ("Hotword Detected")
    detector.terminate()
    speech2text()
    detector.start(detected_callback)
    
def send2website(data):
    
    f= open("/var/www/html/index.html","w+")
    
    t = time.localtime()
    t1 = time.strftime('%Y-%m-%d', t)
    t2 =time.strftime('%H:%M:%S', t)
    
    data2 = data.rjust(10240)
    key = 'ASSWJDWHJ9748hJSJWK8983jJKJS990S'
    cipher = AES.new(key,AES.MODE_ECB)
    encode = base64.b64encode(cipher.encrypt(data2))
    
    html = """<!DOCTYPE html>
    <html>
    <center>
    <h1> The last recording with the pi was at """+ t2 +" on "+ t1 + "." """</h1>
    <p>"""+ encode +"""</p>
    </center>
    </html>"""

    f.write(html)
    f.close()
    
    
 
    
def speech2text():
    reco = sr.Recognizer()
    with sr.Microphone() as s:
        file = reco.listen(s)
    data="error"
    try:
        print(reco.recognize_sphinx(file))
        data = reco.recognize_sphinx(file)
        send2website(data)
    except sr.UnknownValueError:
        print("audio not recognized, please retry")
        send2website(data)
    except sr.RequestError:
        print("Impossible to request results")
        send2website(data)
detector = snowboydecoder.HotwordDetector("Hey_babel.pmdl", sensitivity=0.5, audio_gain=1)


detector.start(detected_callback)


