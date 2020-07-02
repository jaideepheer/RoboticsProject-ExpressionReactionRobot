import pyttsx3
tts = pyttsx3.init(debug=True)
voices = tts.getProperty('voices')
tts.setProperty('voice','hindi')
tts.setProperty('rate', 110)
for voice in voices:
    print('ID:',voice.id)
    print('Name:', voice.name)
tts.say("hello this is a robot.")
print('Voice = ',tts.getProperty('voice'))
tts.runAndWait()