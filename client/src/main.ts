import './style.css'
import startCamera from './camera';
import captureFrame from './frame';

const video = document.getElementById("video") as HTMLVideoElement;

startCamera(video).then(() => {
  setInterval(() => captureFrame(video), 30)
})

/**
  * soon
  * function captureLoop() {
    captureFrame(video);
    requestAnimationFrame(captureLoop);
  }

  * startCamera(video).then(() => {
    requestAnimationFrame(captureLoop);
  });

 */
