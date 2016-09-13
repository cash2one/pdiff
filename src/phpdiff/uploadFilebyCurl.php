<?php
$filename = $argv[1];
$job_id = $argv[2];
$post_url = $argv[3];
echo $filename.'\n';
echo $job_id.'\n';
echo $post_url.'\n';
$post_data = array(
		"xml" => "@" . $filename,
		"id" => $job_id,
	);

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $post_url);
curl_setopt($curl, CURLOPT_POST, 1 );
curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec($curl);
#$error = curl_error($curl);
echo $result.'\n';
#echo $error.'\n';
return $result;
?>
