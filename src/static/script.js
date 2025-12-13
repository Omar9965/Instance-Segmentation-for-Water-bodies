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
const selectedFilesDiv = $('selectedFiles');
const fileList = $('fileList');
const resultsGrid = $('resultsGrid');

let selectedFiles = [];

const showMessage = (isError, message) => {
    const [show, hide] = isError ? [errorMsg, successMsg] : [successMsg, errorMsg];
    show.textContent = message;
    show.classList.add('active');
    hide.classList.remove('active');
    
    if (!isError) {
        setTimeout(() => show.classList.remove('active'), 5000);
    }
};

const hideMessages = () => {
    errorMsg.classList.remove('active');
    successMsg.classList.remove('active');
};

const handleFileSelect = files => {
    if (!files || files.length === 0) return;

    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff'];
    const validFiles = [];
    
    for (const file of files) {
        if (!validTypes.includes(file.type)) {
            showMessage(true, `❌ "${file.name}" has invalid type. Use JPG, PNG, or TIFF.`);
            continue;
        }
        if (file.size > 500 * 1024 * 1024) {
            showMessage(true, `❌ "${file.name}" is too large. Max 500MB.`);
            continue;
        }
        validFiles.push(file);
    }

    if (validFiles.length === 0) return;

    selectedFiles = validFiles;
    showMessage(false, `✅ ${validFiles.length} file(s) selected successfully!`);

    // Show file list
    fileList.innerHTML = selectedFiles.map(f => `<li>📄 ${f.name}</li>`).join('');
    selectedFilesDiv.classList.remove('hidden');
    buttonsContainer.classList.remove('hidden');
    imagesContainer.classList.add('hidden');
    resultsGrid.innerHTML = '';
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
    handleFileSelect(e.dataTransfer.files);
});

fileInput.addEventListener('change', e => handleFileSelect(e.target.files));

processBtn.addEventListener('click', async () => {
    if (selectedFiles.length === 0) {
        return showMessage(true, '❌ Please select files first.');
    }

    hideMessages();
    loading.classList.add('active');
    processBtn.disabled = true;
    resultsGrid.innerHTML = '';

    try {
        // Process each file individually to get visualized images
        for (const file of selectedFiles) {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/v1/segment-image', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Failed to process ${file.name}`);
            }

            const blob = await response.blob();
            const segmentedUrl = URL.createObjectURL(blob);
            
            // Create original image URL
            const originalUrl = URL.createObjectURL(file);

            // Add result card
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <h3 class="result-filename">📄 ${file.name}</h3>
                <div class="result-images">
                    <div class="result-image-box">
                        <span class="result-label">Original</span>
                        <img src="${originalUrl}" alt="Original" />
                    </div>
                    <div class="result-image-box">
                        <span class="result-label">Segmented</span>
                        <img src="${segmentedUrl}" alt="Segmented" />
                    </div>
                </div>
            `;
            resultsGrid.appendChild(resultCard);
        }

        imagesContainer.classList.remove('hidden');
        showMessage(false, `✅ Successfully processed ${selectedFiles.length} image(s)!`);
        
        setTimeout(() => {
            imagesContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        showMessage(true, `❌ Error: ${error.message}`);
    } finally {
        loading.classList.remove('active');
        processBtn.disabled = false;
    }
});

resetBtn.addEventListener('click', () => {
    selectedFiles = [];
    fileInput.value = '';
    fileList.innerHTML = '';
    resultsGrid.innerHTML = '';
    selectedFilesDiv.classList.add('hidden');
    imagesContainer.classList.add('hidden');
    buttonsContainer.classList.add('hidden');
    hideMessages();
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
});