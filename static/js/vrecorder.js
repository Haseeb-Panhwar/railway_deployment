
  // collect DOMs
const display = document.querySelector('.display')
const controllerWrapper = document.querySelector('.controllers')
const audioFileInput = document.getElementById('id_audio_file');
const audioForm = document.getElementById('audioFile');

const State = ['Initial', 'Record', 'Download']
let stateIndex = 0
let mediaRecorder, chunks = [], audioURL = ''

// mediaRecorder setup for audio
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    console.log('mediaDevices supported..')

    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorder = new MediaRecorder(stream)

        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data)
        }

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, {'type': 'audio/ogg; codecs=opus'})
            chunks = []
            audioURL = window.URL.createObjectURL(blob)
            document.querySelector('audio').src = audioURL
            audioFileInput.setAttribute('value','audio.ogg')

            convertToMP3(blob)

            console.log("Audio Done!")
            window.alert("Audio File inputted!")
        }
    }).catch(error => {
        console.log('Following error has occurred: ', error)
    })
} else {
    stateIndex = ''
    application(stateIndex)
}

const clearDisplay = () => {
    display.textContent = ''
}

const clearControls = () => {
    controllerWrapper.textContent = ''
}

const record = () => {
    stateIndex = 1
    mediaRecorder.start()
    application(stateIndex)
}

const stopRecording = () => {
    stateIndex = 2
    mediaRecorder.stop()
    application(stateIndex)
}

const downloadAudio = () => {
    const downloadLink = document.createElement('a')
    downloadLink.href = audioURL
    downloadLink.setAttribute('download', 'audio.ogg')
    downloadLink.click()
}

const addButton = (id, funString, text) => {
    const btn = document.createElement('button')
    btn.id = id
    btn.setAttribute('onclick', funString)
    btn.textContent = text
    controllerWrapper.append(btn)
}

const addMessage = (text) => {
    const msg = document.createElement('p')
    msg.textContent = text
    display.append(msg)
}

const addAudio = () => {
    const audio = document.createElement('audio')
    audio.controls = true
    audio.src = audioURL
    display.append(audio)
}

const application = (index) => {
    switch (State[index]) {
        case 'Initial':
            clearDisplay()
            clearControls()

            addButton('record', 'record()', 'Start Recording')
            break;

        case 'Record':
            clearDisplay()
            clearControls()

            addMessage('Recording...')
            addButton('stop', 'stopRecording()', 'Stop Recording')
            break

        case 'Download':
            clearControls()
            clearDisplay()

            addAudio()
            addButton('record', 'record()', 'Record Again')
            break

        default:
            clearControls()
            clearDisplay()

            addMessage('Your browser does not support mediaDevices')
            break;
    }
}

const convertToMP3 = (blob) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(blob);
    reader.onloadend = () => {
        const arrayBuffer = reader.result;
        const audioContext = new AudioContext();
        audioContext.decodeAudioData(arrayBuffer, (audioBuffer) => {
            const pcmArray = audioBuffer.getChannelData(0);
            const mp3encoder = new lamejs.Mp3Encoder(1, audioBuffer.sampleRate, 128);
            const mp3Data = [];
            let sampleBlockSize = 1152;
            for (let i = 0; i < pcmArray.length; i += sampleBlockSize) {
                const sampleChunk = pcmArray.subarray(i, i + sampleBlockSize);
                const mp3Buffer = mp3encoder.encodeBuffer(sampleChunk);
                if (mp3Buffer.length > 0) {
                    mp3Data.push(mp3Buffer);
                }
            }
            const endBuffer = mp3encoder.flush();
            if (endBuffer.length > 0) {
                mp3Data.push(endBuffer);
            }
            const mp3Blob = new Blob(mp3Data, { type: 'audio/mp3' });
            const mp3URL = window.URL.createObjectURL(mp3Blob);
            console.log('MP3 URL:', mp3URL);

            // Update the audio element to use the MP3 file
            document.querySelector('audio').src = mp3URL;

            // You can also add functionality to download the MP3 file
            const downloadLink = document.createElement('a');
            downloadLink.href = mp3URL;
            downloadLink.setAttribute('download', 'audio.mp3');
            downloadLink.textContent = 'Download MP3';
            display.append(downloadLink);
            
        });
    };
}

application(stateIndex)
