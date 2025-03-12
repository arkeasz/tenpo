async function captureFrame(video: HTMLVideoElement) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    if (!ctx) {
        console.error("No se pudo obtener el contexto del canvas.");
        return;
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        if (!blob) {
            console.error("No se pudo convertir el canvas a Blob.");
            return;
        }

        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        try {
            const response = await fetch('http://localhost:5000/detect', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('Respuesta del backend:', result);

            if (result.action === 'clic') {
                console.log('¡Gesto de clic detectado!');
            } else {
                console.log('No se detectó ningún gesto.');
            }
        } catch (error) {
            console.error('Error al enviar la imagen al backend:', error);
        }
    }, 'image/jpeg');
}

export default captureFrame;
