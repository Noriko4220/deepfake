async function runModel() {
  const videoInput = document.getElementById('video').files[0];
  const imageInput = document.getElementById('image').files[0];

  if (!videoInput || !imageInput) {
    alert('Please upload both video and image files!');
    return;
  }

  const videoFile = new File([videoInput], 'video.mp4', { type: videoInput.type });
  const imageFile = new File([imageInput], 'image.jpg', { type: imageInput.type });

  const formData = new FormData();
  formData.append('video', videoFile);
  formData.append('image', imageFile);

  document.getElementById('loading').style.display = 'block';

  try {
    const uploadResponse = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    if (!uploadResponse.ok) {
      throw new Error(`Upload failed: ${uploadResponse.statusText}`);
    }

    const { message, video_id, image_id } = await uploadResponse.json();
    console.log(message);

    let processedFileReady = false;
    while (!processedFileReady) {
      const pollResponse = await fetch(`http://localhost:5000/status?video_id=${video_id}`);
      if (!pollResponse.ok) {
        throw new Error(`Polling failed: ${pollResponse.statusText}`);
      }

      const { ready } = await pollResponse.json();
      if (ready) {
        processedFileReady = true;
      } else {
        await new Promise((resolve) => setTimeout(resolve, 5000));
      }
    }

    const originalVideo = document.getElementById('originalVideo');
    const processedVideo = document.getElementById('processedVideo');
    originalVideo.src = URL.createObjectURL(videoFile);
    processedVideo.src = 'http://localhost:5000/static/processed/swapped.mp4';

    document.getElementById('loading').style.display = 'none';
    document.getElementById('results').style.display = 'block';

  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while processing the files. Please try again.');
    document.getElementById('loading').style.display = 'none';
  }
}

function showOriginal() {
  const videoContainer = document.getElementById('videoContainer');
  const originalVideo = document.getElementById('originalVideo');
  const processedVideo = document.getElementById('processedVideo');

  videoContainer.className = 'single-video';
  originalVideo.style.display = 'block';
  processedVideo.style.display = 'none';
}

function showProcessed() {
  const videoContainer = document.getElementById('videoContainer');
  const originalVideo = document.getElementById('originalVideo');
  const processedVideo = document.getElementById('processedVideo');

  videoContainer.className = 'single-video';
  originalVideo.style.display = 'none';
  processedVideo.style.display = 'block';
}

function showBoth() {
  const videoContainer = document.getElementById('videoContainer');
  const originalVideo = document.getElementById('originalVideo');
  const processedVideo = document.getElementById('processedVideo');

  videoContainer.className = 'video-container';
  originalVideo.style.display = 'block';
  processedVideo.style.display = 'block';
}
