import './style.css'
import './reset.css'
import startCamera from './camera';
import captureFrame from './frame';

const video = document.getElementById("video") as HTMLVideoElement;

function captureLoop() {
  captureFrame(video);
  setTimeout(captureLoop, 135);
}

startCamera(video).then(() => {
  captureLoop();
});
