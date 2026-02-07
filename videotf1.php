<?php
header('Content-Type: application/vnd.apple.mpegurl');

// احصل على قناة من الرابط
$channel = $_GET['channel'] ?? 'beINAR2';

// رابط iframe Lovetier
$iframe_url = "https://lovetier.bz/player/" . $channel;

// اجلب محتوى iframe
$ch = curl_init($iframe_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36');
$response = curl_exec($ch);
curl_close($ch);

// ابحث عن رابط M3U8 بالتوكن داخل iframe
// غالبًا يكون ضمن JSON أو inline JS
preg_match('/https:\/\/[^\s\'"]+\.m3u8\?token=[^\'"]+/', $response, $matches);
$m3u8_url = $matches[0] ?? '';

if ($m3u8_url) {
    // إعادة توجيه المستخدم مباشرة إلى M3U8 بالتوكن الحالي
    readfile($m3u8_url);
} else {
    http_response_code(404);
    echo "#EXTM3U\n# Channel not found or token expired";
}
?>
