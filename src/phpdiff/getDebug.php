<?php
require_once('getData.php');

class getDebug{


	public static function getCmd(){
		$ignoreAllValueMode = '';
		$path = DiffData::getPath();
		$ignoreKeyKeysPath = $path . 'ignore_key_keys';
		$ignoreValueKeysPath = $path . 'ignore_value_keys';
		$onlineJsonPath = $path.'online'.'.json';
		$offlineJsonPath = $path .'offline'.'.json';
		$ignoreValueKeys = DiffData::getData($ignoreValueKeysPath);
		if ('ALL_VALUE' == $ignoreValueKeys){
			$ignoreAllValueMode = '-V';
			$ignoreValueKeys = '';
		}
		$ignoreKeyKeys = DiffData::getData($ignoreKeyKeysPath);
		$cmd =  '/home/forum/envtools/CommonTools/python/bin/python '.JSON_DIFF_PATH.' -O -a '.$ignoreAllValueMode.' '."'$onlineJsonPath'".' '."'$offlineJsonPath'";
		$arrIgoreKeyKeys = explode(',',$ignoreKeyKeys);
		$arrIgoreValueKeys = explode(',',$ignoreValueKeys);
		foreach($arrIgoreValueKeys as $key => $value){
			if(trim($value)!=''){
				$cmd .= ' -I '.$value;
			}
		}
		foreach($arrIgoreKeyKeys as $key => $value){
			if(trim($value)!=''){
				$cmd .= ' -x '.$value;
			}
		}
		return $cmd;

	}

}
header('Content-type: text/json');
$cmd = getDebug::getCmd();
file_put_contents('debug.log',"[".date('Y-m-d H:i:s')."]\t$cmd\n",FILE_APPEND);
$ret = shell_exec($cmd);
echo trim($ret);
?>
