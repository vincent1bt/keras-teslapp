document.addEventListener("DOMContentLoaded", ready);

function get_prediction(image) {
    const formData = new FormData()
    formData.append('image', image);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        response.json().then(data => {
            const imageClassContainer = document.querySelector("#imageClass");
            const imageClass = data["image_class"];
            imageClassContainer.innerHTML = `Tesla: ${imageClass}`;
        });
    })
    .catch(error => {
        console.log("Hubo un error :c");
    });
}

function imageUploaded(event) {
    const target = event.target;
    const image = target.files[0];

    if (!image) return;
    
    const imageContainer = document.querySelector("#imageContainer");
    imageContainer.src = window.URL.createObjectURL(image);

    get_prediction(image);
}

function ready() {
    const inputFile = document.querySelector("#image");
    inputFile.addEventListener('change', imageUploaded);
}
