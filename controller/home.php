<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watch Videos</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav class="navbar">Watch Videos</nav>
    </header>

    <main class="video-gallery">
        <?php foreach ($descriptions as $video): ?>
            <div class="video-thumbnail">
            <img src="https://<?= $selectedServer ?>/load-image?id=<?= $video['id'] ?>" alt="Thumbnail" class="video-thumbnail-image">
                <div class="video-info">
                    <p class="video-title"><?= $video['title'] ?></p>
                    <p class="video-content"><?= $video['content'] ?></p>
                </div>
            </div>
        <?php endforeach; ?>
    </main>

    <!-- Modal -->
    <div id="video-modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div class="video-container">
                <video controls id="video-player">
                    <source src="" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    </div>

    <script src="scripts.js"></script>
</body>
</html>
