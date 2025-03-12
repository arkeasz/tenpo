import { draw } from "./draw";

let app = document.getElementById("app") as HTMLDivElement;
let res = document.createElement("div") as HTMLDivElement;

async function captureFrame(video: HTMLVideoElement) {
    const canvas = document.getElementById("canvas") as HTMLCanvasElement;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        if (!blob) return;

        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        try {
            const response = await fetch('http://localhost:5000/detect', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error(`Error en la solicitud: ${response.statusText}`);

            const result = await response.json();

            app.appendChild(res);
            if (result.action === 'clic') {
                res.innerHTML = 'clic'
            } else {
                res.innerHTML = 'none'
            }
            draw(result.distance)

        } catch (error) {
            console.error(error);
        }
    }, 'image/jpeg');
}

export default captureFrame;
