"""Shared export controls and browser-side recording support for interactive canvases."""


MEDIA_EXPORT_SCRIPT = r"""
(() => {
    const formatSelect = document.getElementById('sel_video_format');
    const fpsSelect = document.getElementById('sel_video_fps');
    let gifFrames = [];
    let gifTimer = null;
    let gifWidth = 1200;
    let gifHeight = 680;
    let activeFormat = null;

    function setRecordingControlsDisabled(disabled) {
        formatSelect.disabled = disabled;
        fpsSelect.disabled = disabled;
        document.getElementById('sel_export_scale').disabled = disabled;
    }

    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    function gifPaletteIndex(r, g, b) {
        return (r & 224) | ((g & 224) >> 3) | (b >> 6);
    }

    function encodeGif(frames, width, height, delay) {
        const bytes = [];
        const pushWord = value => {
            bytes.push(value & 255, (value >> 8) & 255);
        };
        const pushString = value => {
            for (let i = 0; i < value.length; i++) bytes.push(value.charCodeAt(i));
        };
        const pushSubBlocks = data => {
            for (let offset = 0; offset < data.length; offset += 255) {
                const block = data.slice(offset, offset + 255);
                bytes.push(block.length, ...block);
            }
            bytes.push(0);
        };

        pushString('GIF89a');
        pushWord(width);
        pushWord(height);
        bytes.push(247, 0, 0);
        for (let index = 0; index < 256; index++) {
            const red = ((index >> 5) & 7) * 255 / 7;
            const green = ((index >> 2) & 7) * 255 / 7;
            const blue = (index & 3) * 255 / 3;
            bytes.push(Math.round(red), Math.round(green), Math.round(blue));
        }
        pushString('!\xff\x0bNETSCAPE2.0');
        bytes.push(3, 1, 0, 0, 0);

        for (const frame of frames) {
            bytes.push(33, 249, 4, 0);
            pushWord(delay);
            bytes.push(0, 0, 44);
            pushWord(0);
            pushWord(0);
            pushWord(width);
            pushWord(height);
            bytes.push(0, 8);

            const compressed = [];
            let bitBuffer = 0;
            let bitCount = 0;
            let codeSize = 9;
            let nextCode = 258;
            let dictionary = new Map();
            const clearCode = 256;
            const endCode = 257;
            const writeCode = code => {
                bitBuffer |= code << bitCount;
                bitCount += codeSize;
                while (bitCount >= 8) {
                    compressed.push(bitBuffer & 255);
                    bitBuffer >>= 8;
                    bitCount -= 8;
                }
            };
            const resetDictionary = () => {
                dictionary = new Map();
                codeSize = 9;
                nextCode = 258;
            };

            writeCode(clearCode);
            let prefix = frame[0];
            for (let i = 1; i < frame.length; i++) {
                const value = frame[i];
                const key = `${prefix},${value}`;
                const found = dictionary.get(key);
                if (found !== undefined) {
                    prefix = found;
                    continue;
                }

                writeCode(prefix);
                if (nextCode < 4096) {
                    dictionary.set(key, nextCode++);
                    if (nextCode > (1 << codeSize) && codeSize < 12) codeSize++;
                } else {
                    writeCode(clearCode);
                    resetDictionary();
                }
                prefix = value;
            }
            writeCode(prefix);
            writeCode(endCode);
            if (bitCount > 0) compressed.push(bitBuffer & 255);
            pushSubBlocks(compressed);
        }

        bytes.push(59);
        return new Blob([new Uint8Array(bytes)], { type: 'image/gif' });
    }
    window.encodeGifForExport = encodeGif;

    function captureGifFrame() {
        if (!isRecording || !recordCtx) return;
        updateRecordFrame();
        const frameCanvas = document.createElement('canvas');
        frameCanvas.width = gifWidth;
        frameCanvas.height = gifHeight;
        const frameCtx = frameCanvas.getContext('2d', { willReadFrequently: true });
        frameCtx.drawImage(recordCanvas, 0, 0, gifWidth, gifHeight);
        const rgba = frameCtx.getImageData(0, 0, gifWidth, gifHeight).data;
        const indexed = new Uint8Array(gifWidth * gifHeight);
        for (let src = 0, dst = 0; dst < indexed.length; src += 4, dst++) {
            indexed[dst] = gifPaletteIndex(rgba[src], rgba[src + 1], rgba[src + 2]);
        }
        gifFrames.push(indexed);
        if (gifFrames.length >= 90) stopRecording();
    }

    window.startRecording = function() {
        activeFormat = formatSelect.value;
        setRecordingControlsDisabled(true);
        if (activeFormat === 'gif') {
            initRecordCanvas();
            const scale = Math.min(1, Number(document.getElementById('sel_export_scale').value) || 1);
            recordCanvas = document.createElement('canvas');
            recordCanvas.width = 1200 * scale;
            recordCanvas.height = 680 * scale;
            recordCtx = recordCanvas.getContext('2d');
            recordCtx.scale(scale, scale);
            gifWidth = 1200;
            gifHeight = 680;
            gifFrames = [];
            isRecording = true;
            updateRecordFrame();
            btnRecordVideo.innerText = '⏹️ 停止並下載 GIF';
            btnRecordVideo.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
            captureGifFrame();
            gifTimer = setInterval(captureGifFrame, 1000 / Math.min(15, Number(fpsSelect.value) || 10));
            if (!state.isPlaying) togglePlay();
            return;
        }

        initRecordCanvas();
        const scale = Number(document.getElementById('sel_export_scale').value) || 1;
        recordCanvas = document.createElement('canvas');
        recordCanvas.width = 1200 * scale;
        recordCanvas.height = 680 * scale;
        recordCtx = recordCanvas.getContext('2d');
        recordCtx.scale(scale, scale);
        updateRecordFrame();

        if (!window.MediaRecorder || !recordCanvas.captureStream) {
            alert('此瀏覽器不支援 WebM 錄影，請改用 GIF 格式。');
            setRecordingControlsDisabled(false);
            activeFormat = null;
            return;
        }
        let stream;
        try {
            stream = recordCanvas.captureStream(Number(fpsSelect.value) || 30);
            const mimeType = ['video/webm;codecs=vp9', 'video/webm;codecs=vp8', 'video/webm']
                .find(type => MediaRecorder.isTypeSupported(type));
            if (!mimeType) throw new Error('No supported WebM codec');
            mediaRecorder = new MediaRecorder(stream, { mimeType });
        } catch (error) {
            stream?.getTracks().forEach(track => track.stop());
            alert(`無法啟動 WebM 錄影：${error.message}`);
            setRecordingControlsDisabled(false);
            activeFormat = null;
            return;
        }

        recordedChunks = [];
        mediaRecorder.ondataavailable = event => {
            if (event.data && event.data.size) recordedChunks.push(event.data);
        };
        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: mediaRecorder.mimeType || 'video/webm' });
            downloadBlob(blob, `simulation_dynamic_${Date.now()}.webm`);
            stream.getTracks().forEach(track => track.stop());
        };
        mediaRecorder.start(100);
        isRecording = true;
        btnRecordVideo.innerText = '⏹️ 停止並下載 WebM';
        btnRecordVideo.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
        if (!state.isPlaying) togglePlay();
    };

    window.stopRecording = function() {
        if (gifTimer) {
            clearInterval(gifTimer);
            gifTimer = null;
        }
        if (activeFormat === 'gif') {
            isRecording = false;
            btnRecordVideo.innerText = '🎥 錄製動態';
            btnRecordVideo.style.background = '';
            if (state.isPlaying) togglePlay();
            if (!gifFrames.length) {
                alert('沒有錄到可匯出的 GIF 影格。');
                return;
            }
            btnRecordVideo.disabled = true;
            btnRecordVideo.innerText = '⏳ 正在編碼 GIF...';
            setTimeout(() => {
                try {
                    const blob = encodeGif(gifFrames, gifWidth, gifHeight, Math.max(2, Math.round(100 / (Number(fpsSelect.value) || 10))));
                    downloadBlob(blob, `simulation_dynamic_${Date.now()}.gif`);
                    gifFrames = [];
                } catch (error) {
                    alert(`GIF 編碼失敗：${error.message}`);
                } finally {
                    btnRecordVideo.disabled = false;
                    btnRecordVideo.innerText = '🎥 錄製動態';
                    setRecordingControlsDisabled(false);
                    activeFormat = null;
                }
            }, 0);
            return;
        }

        if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
        isRecording = false;
        btnRecordVideo.innerText = '🎥 錄製動態';
        btnRecordVideo.style.background = '';
        setRecordingControlsDisabled(false);
        activeFormat = null;
        if (state.isPlaying) togglePlay();
    };
})();
"""


def inject_media_export_controls(html_code):
    """Adds format/quality controls and shared recording implementation to a canvas page."""
    controls = """
        <label style="color:#94a3b8;font-size:.75rem;">圖片格式
            <select id="sel_image_format"><option value="png">PNG</option><option value="webp">WebP</option></select>
        </label>
        <label title="GIF 以 1× 解析度輸出；圖片和 WebM 依所選倍率輸出。" style="color:#94a3b8;font-size:.75rem;">圖片／WebM 解析度
            <select id="sel_export_scale"><option value="1">1×</option><option value="2" selected>2×</option><option value="3">3×</option><option value="4">4×</option></select>
        </label>
        <label style="color:#94a3b8;font-size:.75rem;">影片格式
            <select id="sel_video_format"><option value="webm">WebM</option><option value="gif">GIF（1×，最多 90 幀）</option></select>
        </label>
        <label style="color:#94a3b8;font-size:.75rem;">FPS
            <select id="sel_video_fps"><option value="10">10</option><option value="15">15</option><option value="24">24</option><option value="30" selected>30</option></select>
        </label>
    """
    button = '<button class="btn btn-secondary" id="btn_export_png">📸 截圖 PNG</button>'
    html_code = html_code.replace(button, controls + button)
    html_code = html_code.replace('📸 截圖 PNG</button>', '📸 匯出圖片</button>')
    script = f"<script>{MEDIA_EXPORT_SCRIPT}</script>"
    return html_code.replace("</body>", script + "</body>")
