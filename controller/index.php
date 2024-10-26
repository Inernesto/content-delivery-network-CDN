<?php

// List of servers
$servers = [
    'replica-1.local',
    'replica-2.local',
    'replica-3.local'
];

// Route handling
$requestPath = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

switch ($requestPath) {

    case '/':
        $selectedServer = selectReplicaServer($servers);
        if ($selectedServer) {
            $json = fetchContent($selectedServer);
            if ($json) { // Check if the fetch was successful
                $descriptions = json_decode($json, true);
                require __DIR__ . '/home.php';
            } else {
                http_response_code(503);
                echo 'Content fetch failed from replica server';
            }
        } else {
            http_response_code(503);
            echo 'No available replica servers';
        }
        break;

    case '/change-replica':
        // Select the replica server
        $replicaUrl = selectReplicaServer($servers);
        if ($replicaUrl) {
            // Send the selected replica URL back to the client
            header("Content-Type: application/json");
            echo json_encode(['replicaUrl' => $replicaUrl]);
        } else {
            // Handle the error case where no replica could be selected
            http_response_code(404);
            echo json_encode(['error' => 'No available replicas']);
        }
        break;
    default:
        http_response_code(404);
        echo '404 Not Found';
    break;
}


// Function to check if a server is reachable
function isServerAvailable($server) {
    $server = "https://" . $server . "/load-content";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $server);
    curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_2_0); // Force HTTP/2
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // This will return the response as a string from curl_exec()
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_NOBODY, true); // Comment this to switch to a GET request
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // For development with self-signed certs

    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if($httpcode >= 200 && $httpcode < 300){ // Check HTTP status code
        return true;
    }

    return false;
}


// Function to fetch the contents from replica servers
function fetchContent($server) {
    $server = "https://" . $server . "/load-content";
    $attempts = 3;  // Maximum number of attempts

    for ($i = 0; $i < $attempts; $i++) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $server);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_2_0);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // For development with self-signed certs

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        // Check if the response is successful and not empty
        if ($httpCode >= 200 && $httpCode < 300 && !empty($response)) {
            return $response;  // Return the successful response
        }

        // Optional: sleep for a second before retrying to avoid hammering the server
        sleep(1);
    }

    return false; // Return false after exhausting all attempts
}


// Function to select replica server
function selectReplicaServer ($servers) {
    // Session to keep track of last chosen server
    session_start();
    if (!isset($_SESSION['last_index'])) {
        $_SESSION['last_index'] = 0;
    }

    $serverCount = count($servers);
    $attempts = $serverCount;
    while ($attempts-- > 0) {
        $_SESSION['last_index'] = ($_SESSION['last_index'] + 1) % $serverCount;
        $server = $servers[$_SESSION['last_index']];
        if (isServerAvailable($server)) {
            return $server;
        }
    }

    return false;
}

?>

