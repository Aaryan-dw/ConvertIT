// Audio Form Loading
const audioForm = document.getElementById('audioForm');
if (audioForm) {
    audioForm.addEventListener('submit', function(e) {
        const loadingBar = document.getElementById('loadingBar');
        const loadingText = document.getElementById('loadingText');
        const submitBtn = this.querySelector('button[type="submit"]');
        
        if (loadingBar && loadingText) {
            loadingBar.style.display = 'block';
            loadingText.style.display = 'block';
            if (submitBtn) submitBtn.disabled = true;
        }
    });
}

// Video Form Loading
const videoForm = document.getElementById('videoForm');
if (videoForm) {
    videoForm.addEventListener('submit', function(e) {
        const loadingBar = document.getElementById('loadingBarVideo');
        const loadingText = document.getElementById('loadingTextVideo');
        const submitBtn = this.querySelector('button[type="submit"]');
        
        if (loadingBar && loadingText) {
            loadingBar.style.display = 'block';
            loadingText.style.display = 'block';
            if (submitBtn) submitBtn.disabled = true;
        }
    });
}