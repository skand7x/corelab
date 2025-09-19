<?php
echo "<h2>All Server Variables</h2>";
echo "<table border='1'>";
echo "<tr><th>Variable Name</th><th>Value</th></tr>";
foreach ($_SERVER as $key => $value) {
    echo "<tr>";
    echo "<td>" . htmlspecialchars($key) . "</td>";
    if (is_array($value)) {
        echo "<td><pre>" . print_r($value, true) . "</pre></td>";
    } else {
        echo "<td>" . htmlspecialchars($value) . "</td>";
    }
    echo "</tr>";
}
echo "</table>";
?>

