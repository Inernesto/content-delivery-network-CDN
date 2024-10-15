<!-- upload.php -->
<?php

// Define the base directory for content
$base_dir = __DIR__ . "/origin_contents/";

// Define subdirectories
$video_dir = $base_dir . "videos/";
$thumbnail_dir = $base_dir . "thumbnails/";
$description_dir = $base_dir . "descriptions/";

// Create directories if they do not exist
foreach ([$video_dir, $thumbnail_dir, $description_dir] as $dir) {
    if (!file_exists($dir)) {
        mkdir($dir, 0777, true);
    }
}

// Handle the file uploads and description text
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['video'], $_FILES['thumbnail'], $_POST['description'], $_POST['title'])) {
    // Generate a unique ID based on the current timestamp and a random element
    $unique_id = md5(uniqid(rand(), true));
    $video_extension = pathinfo($_FILES['video']['name'], PATHINFO_EXTENSION);
    $thumbnail_extension = pathinfo($_FILES['thumbnail']['name'], PATHINFO_EXTENSION);
    
    // Create filenames using the unique ID and original extensions
    $video_filename = $unique_id . '.' . $video_extension;
    $thumbnail_filename = $unique_id . '.' . $thumbnail_extension;

    // Process Video Upload
    $video_path = $video_dir . $video_filename;
    if (!move_uploaded_file($_FILES['video']['tmp_name'], $video_path)) {
        return "Error uploading video file."; // Stop processing if file upload fails
    }

    // Process Thumbnail Upload
    $thumbnail_path = $thumbnail_dir . $thumbnail_filename;
    if (!move_uploaded_file($_FILES['thumbnail']['tmp_name'], $thumbnail_path)) {
        return "Error uploading thumbnail file."; // Stop processing if file upload fails
    }

    // Process Description Text
    $description_file = $description_dir . "Descriptions.txt";
    $description_content = "<===== " . $_POST['title'] . " =====>\n";
    $description_content .= "ID: " . $unique_id . "\n";
    $description_content .= "Date: " . date('Y-m-d H:i:s') . "\n";
    $description_content .= "Conetent: ". $_POST['description'] . "\n\n";

    file_put_contents($description_file, $description_content, FILE_APPEND | LOCK_EX);

    $result["message"] = "Files uploaded successfully.";

    $result["success"] = true;

    return $result;
} else {

    $result["message"] = "Invalid file upload.";

    $result["success"] = false;

    return $result;
}
?>
