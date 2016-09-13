<?php
define ('REPORT_PATH',dirname(__FILE__).'/../report');
define ('JSON_DIFF_PATH',dirname(__FILE__).'/json_diff.py');
class DiffData{
	public static $dataPath = '';


	public static function getData($dataPath){
		$content = file_get_contents($dataPath);
		return $content;
	
	}


	public static function getPath(){
		$arrParams = array();
		$arrParams['task'] = $_REQUEST['task'];
		$arrParams['case'] = $_REQUEST['case'];
		$arrParams['status'] = $_REQUEST['status'];
		$path = REPORT_PATH.'/'.$arrParams['task'].'/'.$arrParams['case'].'/'.$arrParams['case'].'.'.$arrParams['status'];
		return $path;


	}	
}
header('Content-type: text/json');
$path = DiffData::getPath();
$path = $path.'.'.'json';
$data = DiffData::getData($path);
echo $data;
?>
