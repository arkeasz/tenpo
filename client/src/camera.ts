
async function startCamera(video: HTMLVideoElement) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        video.srcObject = stream;
    } catch (error) {
        console.error(error);
    }
}

export default startCamera;
