// @ts-ignore
import * as THREE from 'three';

let renderer: any, scene: any, camera: any, rtScene: any, rtCamera: any, renderTarget: any, cube: any, rtCubes: any = [];

function initRenderer() {
    const canvas = document.querySelector('#c');
    renderer = new THREE.WebGLRenderer({ antialias: true, canvas });
}

function initScenes() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color('black');

    rtScene = new THREE.Scene();
    rtScene.background = new THREE.Color('red');
}

function initCameras(distance: number) {
    const rtWidth = 512;
    const rtHeight = 512;
    renderTarget = new THREE.WebGLRenderTarget(rtWidth, rtHeight);

    rtCamera = new THREE.PerspectiveCamera(distance * 3, rtWidth / rtHeight, 0.1, 5);
    rtCamera.position.z = 2;

    camera = new THREE.PerspectiveCamera(75, 2, 0.1, 5);
    camera.position.z = 2;
}

function initLights() {
    const light = new THREE.DirectionalLight(0xFFFFFF, 3);
    light.position.set(-1, 2, 4);
    rtScene.add(light);

    const light2 = new THREE.DirectionalLight(0xFFFFFF, 1);
    light2.position.set(-1, 2, 4);
    scene.add(light2);
}

function createObjects() {
    const geometry = new THREE.BoxGeometry(1, 1, 1);

    function makeInstance(color: any, x: number) {
        const material = new THREE.MeshPhongMaterial({ color });
        const cube = new THREE.Mesh(geometry, material);
        rtScene.add(cube);
        cube.position.x = x;
        return cube;
    }

    rtCubes = [
        makeInstance(0x44aa88, 0),
        makeInstance(0x8844aa, -2),
        makeInstance(0xaa8844, 2)
    ];

    const material = new THREE.MeshPhongMaterial({ map: renderTarget.texture });
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
}

function resizeRendererToDisplaySize() {
    const canvas = renderer.domElement;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }
}

function render(time: number) {
    time *= 0.001;
    resizeRendererToDisplaySize();

    rtCubes.forEach((cube: any, ndx:  number) => {
        const speed = 1 + ndx * 0.1;
        const rot = time * speed;
        cube.rotation.x = rot;
        cube.rotation.y = rot;
    });

    renderer.setRenderTarget(renderTarget);
    renderer.render(rtScene, rtCamera);
    renderer.setRenderTarget(null);

    cube.rotation.x = time;
    cube.rotation.y = time * 1.1;

    renderer.render(scene, camera);
    requestAnimationFrame(render);
}

export function draw(distance: number) {
    if (!renderer) {
        initRenderer();
        initScenes();
        initCameras(distance);
        initLights();
        createObjects();
        requestAnimationFrame(render);
    } else {
        rtCamera.fov = distance * 3;
        rtCamera.updateProjectionMatrix();
    }
}
