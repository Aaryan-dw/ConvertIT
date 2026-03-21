// Audio Preview
const audioFile = document.getElementById('audioFile');
if (audioFile) {
    audioFile.addEventListener('change', function(e) {
        const file = this.files[0];
        const previewDiv = document.getElementById('audioPreview');
        if (!file) {
            previewDiv.innerHTML = '';
            return;
        }
        
        previewDiv.innerHTML = '';
        
        if (file.type.startsWith('audio/')) {
            const audio = document.createElement('audio');
            audio.controls = true;
            audio.src = URL.createObjectURL(file);
            previewDiv.appendChild(audio);
        }
    });
}

// Image Preview
const imageFile = document.getElementById('imageFile');
if (imageFile) {
    imageFile.addEventListener('change', function(e) {
        const file = this.files[0];
        const previewDiv = document.getElementById('imagePreview');
        if (!file) {
            previewDiv.innerHTML = '';
            return;
        }
        
        previewDiv.innerHTML = '';
        
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            previewDiv.appendChild(img);
        }
    });
}

// Video Preview
const videoFile = document.getElementById('videoFile');
if (videoFile) {
    videoFile.addEventListener('change', function(e) {
        const file = this.files[0];
        const previewDiv = document.getElementById('videoPreview');
        if (!file) {
            previewDiv.innerHTML = '';
            return;
        }
        
        previewDiv.innerHTML = '';
        
        if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.controls = true;
            video.src = URL.createObjectURL(file);
            previewDiv.appendChild(video);
        }
    });
}