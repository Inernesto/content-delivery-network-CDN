<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Upload</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>
            <div class="navbar">
                Admin
            </div>
        </nav>
    </header>

    <main>
        <?php if (isset($_GET['message'])): ?>
            <div class="notify-present" style="background-color: <?php echo $_GET['success'] == 'true' ? '#4CAF50' : '#f44336'; ?>">
                <p style="color: <?php echo $_GET['success'] == 'true' ? '#ffffff' : '#000000'; ?>">
                    <?php echo htmlspecialchars($_GET['message']); ?>
                </p>
            </div>
        <?php endif; ?>

        <div class="form-container">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="title">Title:</label>
                    <input type="text" id="title" name="title" required>
                </div>
                <div class="form-group">
                    <label for="description">Description:</label>
                    <textarea id="description" name="description" required></textarea>
                </div>
                <div class="form-group">
                    <label for="thumbnail">Thumbnail:</label>
                    <input type="file" id="thumbnail" name="thumbnail" required>
                </div>
                <div class="form-group">
                    <label for="video">Video:</label>
                    <input type="file" id="video" name="video" required>
                </div>
                <button type="submit">Upload Content</button>
            </form>
        </div>
    </main>
</body>
</html>
