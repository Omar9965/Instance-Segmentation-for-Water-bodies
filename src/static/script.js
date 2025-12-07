const $ = id => document.getElementById(id);
const uploadArea = $('uploadArea');
const fileInput = $('fileInput');
const processBtn = $('processBtn');
const resetBtn = $('resetBtn');
const loading = $('loading');
const errorMsg = $('errorMsg');
const successMsg = $('successMsg');
const imagesContainer = $('imagesContainer');
const buttonsContainer = $('buttonsContainer');
const originalImg = $('originalImg');
const segmentedImg = $('segmentedImg');

let selectedFile = null;

const showMessage = (isError, message) => {
    const [show, hide] = isError ? [errorMsg, successMsg] : [successMsg, errorMsg];
    show.textContent = message;
    show.classList.add('active');
    hide.classList.remove('active');
    
    // Auto-hide success messages after 5 seconds
    if (!isError) {
        setTimeout(() => hide.classList.remove('active'), 5000);
    }
};

const hideMessages = () => {
    errorMsg.classList.remove('active');
    successMsg.classList.remove('active');
};

const handleFileSelect = file => {
    if (!file) return;

    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
        return showMessage(true, '❌ Invalid file type. Please upload JPG, PNG, or TIFF images.');
    }

    if (file.size > 500 * 1024 * 1024) {
        return showMessage(true, '❌ File is too large. Maximum size is 500MB.');
    }

    selectedFile = file;
    showMessage(false, `✅ File "${file.name}" selected successfully!`);

    const reader = new FileReader();
    reader.onload = e => {
        originalImg.src = e.target.result;
        imagesContainer.classList.remove('hidden');
        buttonsContainer.classList.remove('hidden');
        segmentedImg.src = '';
        
        // Scroll to results
        setTimeout(() => {
            imagesContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    };
    reader.readAsDataURL(file);
};

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFileSelect(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', e => handleFileSelect(e.target.files[0]));

processBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        return showMessage(true, '❌ Please select a file first.');
    }

    hideMessages();
    loading.classList.add('active');
    processBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/v1/segment-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Segmentation failed');
        }

        const blob = await response.blob();
        segmentedImg.src = URL.createObjectURL(blob);
        showMessage(false, '✅ Water body segmentation completed successfully!');
        
        // Scroll to see results
        setTimeout(() => {
            imagesContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    } catch (error) {
        showMessage(true, `❌ Error: ${error.message}`);
    } finally {
        loading.classList.remove('active');
        processBtn.disabled = false;
    }
});

resetBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    originalImg.src = '';
    segmentedImg.src = '';
    imagesContainer.classList.add('hidden');
    buttonsContainer.classList.add('hidden');
    hideMessages();
    
    // Scroll back to top
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
});
