<?php
// Extract just the path part of the URI
$requestPath = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$request = $requestPath ?? "/";

switch ($request) {
    case '/' :
        require __DIR__ . '/home.php';
        break;
    case '/upload' :
        // This file returns an array with message and success status
        $result = require __DIR__ . '/upload.php';

        if (!empty($result['message'])) {
            // Redirect with query parameters
            header("Location: /?message=" . urlencode($result['message']) . "&success=" . ($result['success'] ? 'true' : 'false'));

            exit();
        } else {
            // Redirect if no message is set, or handle it differently
            header("Location: /?message=No+action+performed&success=false");

            exit();
        }

        break;
    default:
        http_response_code(404);
        echo '404 Not Found';
        break;
}

?>
