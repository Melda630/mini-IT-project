<?php
header("Content-Type: application/json");

/*
  Backend for Member 1:
  - Reads food menu from MySQL
  - Provides menu data to the HTML/JavaScript frontend
  - Provides a simple health check
*/

$host = "localhost";
$user = "root";
$password = "";
$database = "campus_food";

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    echo json_encode([
        "success" => false,
        "message" => "Database connection failed."
    ]);
    exit;
}

$action = $_GET["action"] ?? "";

if ($action === "menu") {
    $result = $conn->query(
        "SELECT id, name, category, description, price
         FROM food_menu
         WHERE available = 1
         ORDER BY id"
    );

    $menu = [];

    while ($row = $result->fetch_assoc()) {
        $menu[] = $row;
    }

    echo json_encode($menu);
    exit;
}

if ($action === "test") {
    echo json_encode([
        "success" => true,
        "message" => "Backend and database are connected."
    ]);
    exit;
}

echo json_encode([
    "success" => false,
    "message" => "Invalid action."
]);
?>