// document.addEventListener("DOMContentLoaded", function () {
//   // Consolidate handling for content and images
//   const contents = document.querySelectorAll(".video-content");
//   contents.forEach((content) => {
//     let words = content.textContent.split(/\s+/);
//     if (words.length > 100) {
//       content.textContent = words.slice(0, 100).join(" ") + " ...";
//     }
//   });

//   const images = document.querySelectorAll(".video-thumbnail-image");
//   images.forEach((image) => {
//     image.addEventListener("click", function (e) {
//       const imgUrl = new URL(e.target.src);
//       const videoId = imgUrl.searchParams.get("id");
//       const videoPlayer = document.getElementById("video-player");
//       const modal = document.getElementById("video-modal");
//       if (videoPlayer && modal) {
//         videoPlayer.src = `${imgUrl.origin}/stream-video?id=${videoId}`;
//         modal.style.display = "flex";
//       } else {
//         console.error("Modal or video player element not found");
//       }
//     });
//   });
// });

// // Set up modal close event
// const closeButton = document.querySelector(".close");
// if (closeButton) {
//   closeButton.addEventListener("click", closeModal);
// }

// function closeModal() {
//   const modal = document.getElementById("video-modal");
//   const videoPlayer = document.getElementById("video-player");
//   if (modal && videoPlayer) {
//     videoPlayer.pause();
//     videoPlayer.currentTime = 0;
//     videoPlayer.src = "";
//     modal.style.display = "none";
//   } else {
//     console.error("Modal or video player element not found on close");
//   }
// }

document.addEventListener("DOMContentLoaded", function () {
  // Consolidate handling for content and images
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

      // Assuming the ID is a query parameter in the image src
      videoPlayer.src = `${imgUrl.origin}/stream-video?id=${videoId}`;
      modal.style.display = "flex";

      // Add error handling for video loading
      videoPlayer.onerror = function () {
        // Handle video loading errors, e.g., if the server is down
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
  videoPlayer.currentTime = 0;
  videoPlayer.src = "";
  modal.style.display = "none";
}

// Handle video loading errors
function handleVideoError(videoId) {
  // Make an AJAX request to the controller to get a new server URL
  fetch(`/change-replica`)
    .then((response) => response.json())
    .then((data) => {
      if (data.replicaUrl) {
        const videoPlayer = document.getElementById("video-player");
        videoPlayer.src = `https://${data.replicaUrl}/stream-video?id=${videoId}`;
      } else {
        //alert("No available servers to stream the video.");
        console.log("No available servers to stream the video.");
      }
    })
    .catch((error) => {
      console.error("Error fetching new server URL:", error);
      // alert("Failed to fetch new server information.");
    });
}
