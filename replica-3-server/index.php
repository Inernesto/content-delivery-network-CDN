<?php
// Extract just the path part of the URI
$requestPath = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$request = $requestPath ?? "/";

header('Content-Type: application/json');

switch ($request) {
    case '/':
        http_response_code(200);
    case '/load-content':
        $filePath = __DIR__ . "/replica_contents/descriptions/descriptions.txt";
        parseDescriptions($filePath);
        break;
    case '/load-image':
        $id = $_GET['id'] ?? '';
        loadImage($id);
        break;
    case '/stream-video':
        $id = $_GET['id'] ?? '';
        streamVideo($id);
        break;
    default:
        http_response_code(404);
        echo json_encode(['error' => '404 Not Found']);
        break;
}


/***** Helper Functions *****/
function parseDescriptions($filePath) {
    // Check if the file exists
    if (!file_exists($filePath)) {
        // If the file does not exist, set the HTTP response code to 404 (Not Found)
        http_response_code(404);
        // Optionally, return a JSON error message
        // echo json_encode(['error' => 'File not found']);
        return;
    }

    // If the file exists, proceed with parsing
    $content = file_get_contents($filePath);
    preg_match_all('/<===== (.*) =====>\nID: (.*)\nDate: (.*)\nContent: (.*)\n/sU', $content, $matches, PREG_SET_ORDER);
    $descriptions = [];

    foreach ($matches as $match) {
        $descriptions[] = [
            'title' => $match[1],
            'id' => $match[2],
            'date' => $match[3],
            'content' => $match[4],
        ];
    }

    // Return the descriptions as JSON
    echo json_encode($descriptions);
}


function loadImage($id) {
    $sanitizedId = preg_replace('/[^a-zA-Z0-9-_]/', '', $id);

    $baseDir = __DIR__ . "/replica_contents/thumbnails/";
    $files = glob($baseDir . $sanitizedId . '.*'); // Find files matching the sanitized ID with any extension

    if (!empty($files)) {
        $filePath = $files[0]; // Take the first match
        $mimeType = mime_content_type($filePath);
        header('Content-Type: ' . $mimeType);
        readfile($filePath);
    } else {
        http_response_code(404);
        echo json_encode(['error' => 'Image not found']);
    }
}


function streamVideo($id) {
    // Sanitize the ID to ensure it contains only alphanumeric characters, dashes, or underscores
    $sanitizedId = preg_replace('/[^a-zA-Z0-9-_]/', '', $id);

    $baseDir = __DIR__ . "/replica_contents/videos/";
    $files = glob($baseDir . $sanitizedId . '.*'); // Find files matching the sanitized ID with any extension

    if (empty($files)) {
        http_response_code(404);
        echo json_encode(['error' => 'Video not found']);
        return;
    }

    $videoPath = $files[0];
    $mimeType = mime_content_type($videoPath);
    header('Content-Type: ' . $mimeType);

    $fp = fopen($videoPath, 'rb');

    $size = filesize($videoPath); // File size
    $length = $size;               // Content length
    $start = 0;                   // Start byte
    $end = $size - 1;             // End byte

    header("Accept-Ranges: bytes");

    header("Content-Length: " . ($size - $start));

    fseek($fp, $start);
    $bufferSize = 8 * 1024; // 8KB buffer
    while (!feof($fp) && ftell($fp) <= $end) {
        echo fread($fp, $bufferSize);
        flush();
    }

    fclose($fp);
}

?>
