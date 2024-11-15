document.addEventListener("DOMContentLoaded", function () {
  const contents = document.querySelectorAll(".video-content");
  contents.forEach((content) => {
    let words = content.textContent.split(/\s+/);
    if (words.length > 100) {
      content.textContent = words.slice(0, 100).join(" ") + " ...";
    }
  });

  const images = document.querySelectorAll(".video-thumbnail-image");
  images.forEach((image) => {
    image.addEventListener("click", function (e) {
      const imgUrl = new URL(e.target.src);
      const videoId = imgUrl.searchParams.get("id");
      const videoPlayer = document.getElementById("video-player");
      const modal = document.getElementById("video-modal");
      modal.style.display = "flex";

      // Preload and buffer the video for smooth playback
      preloadVideo(imgUrl.origin, videoId, videoPlayer);

      // videoPlayer.onerror = null; // Remove any existing error handler
      videoPlayer.onerror = function () {
        console.log(videoPlayer.currentTime);
        handleVideoError(videoId);
      };
    });
  });

  document.querySelector(".close").addEventListener("click", closeModal);
});

function closeModal() {
  const modal = document.getElementById("video-modal");
  const videoPlayer = document.getElementById("video-player");
  videoPlayer.pause();
  videoPlayer.onerror = null; // Remove any existing video error handler
  videoPlayer.onseeked = null; // Remove any existing video seeking handler
  if (videoPlayer.src.startsWith("blob:")) {
    URL.revokeObjectURL(videoPlayer.src); // Revoke the blob URL
  }
  videoPlayer.src = "";
  videoPlayer.load(); // Ensures the video element stops fetching data and removes buffered data
  modal.style.display = "none";
}

function preloadVideo(serverUrl, videoId, videoPlayer) {
  videoPlayer.src = `${serverUrl}/stream-video?id=${videoId}`;
  videoPlayer.load(); // Start loading the video
  videoPlayer.addEventListener(
    "canplaythrough",
    function () {
      videoPlayer.play();
    },
    { once: true }
  );
}

function handleVideoError(videoId) {
  fetch(`/change-replica`)
    .then((response) => response.json())
    .then((data) => {
      if (data.replicaUrl) {
        preloadVideo(
          `https://${data.replicaUrl}`,
          videoId,
          document.getElementById("video-player")
        );
      } else {
        console.error("No available servers to stream the video.");
      }
    })
    .catch((error) => {
      console.error("Error fetching new server URL:", error);
    });
}
