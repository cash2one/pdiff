<?php 

class SofeeXmlParser { 

/** 
* XML parser handle 
* 
* @var resource 
* @see xml_parser_create() 
*/ 
var $parser; 

/** 
* source encoding 
* 
* @var string 
*/ 
var $srcenc; 

/** 
* target encoding 
* 
* @var string 
*/ 
var $dstenc; 

/** 
* the original struct 
* 
* @access private 
* @var array 
*/ 
var $_struct = array(); 

/** 
* Constructor 
* 
* @access public 
* @param mixed [$srcenc] source encoding 
* @param mixed [$dstenc] target encoding 
* @return void 
* @since 
*/ 
function SofeeXmlParser($srcenc = null, $dstenc = null) { 
$this->srcenc = $srcenc; 
$this->dstenc = $dstenc; 

// initialize the variable. 
$this->parser = null; 
$this->_struct = array(); 
} 

/** 
* Free the resources 
* 
* @access public 
* @return void 
**/ 
function free() { 
if (isset($this->parser) && is_resource($this->parser)) { 
xml_parser_free($this->parser); 
unset($this->parser); 
} 
} 

/** 
* Parses the XML file 
* 
* @access public 
* @param string [$file] the XML file name 
* @return void 
* @since 
*/ 
function parseFile($file) { 
$data = @file_get_contents($file) or die("Can't open file $file for reading!"); 
$this->parseString($data); 
} 

/** 
* Parses a string. 
* 
* @access public 
* @param string [$data] XML data 
* @return void 
*/ 
function parseString($data) { 
if ($this->srcenc === null) { 
$this->parser = @xml_parser_create() or die('Unable to create XML parser resource.'); 
} else { 
$this->parser = @xml_parser_create($this->srcenc) or die('Unable to create XML parser resource with '. $this->srcenc .' encoding.'); 
} 

if ($this->dstenc !== null) { 
@xml_parser_set_option($this->parser, XML_OPTION_TARGET_ENCODING, $this->dstenc) or die('Invalid target encoding'); 
} 
xml_parser_set_option($this->parser, XML_OPTION_CASE_FOLDING, 0); // lowercase tags 
xml_parser_set_option($this->parser, XML_OPTION_SKIP_WHITE, 1); // skip empty tags 
if (!xml_parse_into_struct($this->parser, $data, &$this->_struct)) { 
printf("XML error: %s at line %d", xml_error_string(xml_get_error_code($this->parser)), xml_get_current_line_number($this->parser)); 
$this->free(); 
exit(); 
} 

$this->_count = count($this->_struct); 
$this->free(); 
} 

/** 
* return the data struction 
* 
* @access public 
* @return array 
*/ 
function getTree() { 
$i = 0; 
$tree = array(); 
$tree = $this->addNode( 
$tree, 
$this->_struct[$i]['tag'], 
(isset($this->_struct[$i]['value'])) ? $this->_struct[$i]['value'] : '', 
(isset($this->_struct[$i]['attributes'])) ? $this->_struct[$i]['attributes'] : '', 
$this->getChild($i) 
); 

unset($this->_struct); 
return ($tree); 
} 

/** 
* recursion the children node data 
* 
* @access public 
* @param integer [$i] the last struct index 
* @return array 
*/ 
function getChild(&$i) { 
// contain node data 
$children = array(); 

// loop 
while (++$i < $this->_count) { 
// node tag name 
$tagname = $this->_struct[$i]['tag']; 
$value = isset($this->_struct[$i]['value']) ? $this->_struct[$i]['value'] : ''; 
$attributes = isset($this->_struct[$i]['attributes']) ? $this->_struct[$i]['attributes'] : ''; 

switch ($this->_struct[$i]['type']) { 
case 'open': 
// node has more children 
$child = $this->getChild($i); 
// append the children data to the current node 
$children = $this->addNode($children, $tagname, $value, $attributes, $child); 
break; 
case 'complete': 
// at end of current branch 
$children = $this->addNode($children, $tagname, $value, $attributes); 
break; 
case 'cdata': 
// node has CDATA after one of it's children 
$children['value'] .= $value; 
break; 
case 'close': 
// end of node, return collected data 
return $children; 
break; 
} 

} 
//return $children; 
} 

function addNode($target, $key, $value = '', $attributes = '', $child = '') { 
if (!isset($target[$key]['value']) && !isset($target[$key][0])) { 
if ($child != '') { 
$target[$key] = $child; 
} 
if ($attributes != '') { 
foreach ($attributes as $k => $v) { 
$target[$key][$k] = $v; 
} 
} 

$target[$key]['value'] = $value; 
} else { 
if (!isset($target[$key][0])) { 
// is string or other 
$oldvalue = $target[$key]; 
$target[$key] = array(); 
$target[$key][0] = $oldvalue; 
$index = 1; 
} else { 
// is array 
$index = count($target[$key]); 
} 

if ($child != '') { 
$target[$key][$index] = $child; 
} 

if ($attributes != '') { 
foreach ($attributes as $k => $v) { 
$target[$key][$index][$k] = $v; 
} 
} 
$target[$key][$index]['value'] = $value; 
} 
return $target; 
} 

} 


$xmlFile = $argv[1];
$htmlFile = $argv[2];
$xml = new SofeeXmlParser(); 
$xml->parseFile($xmlFile); 
$tree = $xml->getTree(); 
unset($xml); 
//$URL="AAA";
//$PROJECTNAME="AAAAAAAAAAAAAAAA";
$URL=$argv[3];
$PROJECTNAME=$argv[4];
$perf = isset($argv[5])?$argv[5]:"";
$proReportHead='<!DOCTYPE html>
<html>
  <head>
    <meta name="generator"
    content="HTML Tidy for HTML5 (experimental) for Windows https://github.com/w3c/tidy-html5/tree/c63cc39" />
    <meta charset="utf-8" />
    <title>Pdiff Html Report</title>
    
    <style>
    /* Table容器样式 */
    #container {
        width: 1060px;
        margin: 0 auto;
        padding: 10px;
    }
	/**
 * Table整体样式
 */
.my-table-class {
    border-collapse: collapse;
    width: 100%;
    font-size: 80%;
}

/**
 * 表头样式 TableHeader
 */
.my-table-header-class tr {
    background-color: #4E90B2;
    color: #fff;
}
.my-table-header-class th {
    border: 1px solid #B5B5B5;
    font-size: 15px;
    font-weight: bold;
    text-align: center;
    vertical-align: middle;
    height: 30px;
}
.tablehead th {
    border: 1px solid #B5B5B5;
    font-size: 15px;
    font-weight: bold;
    text-align: center;
    vertical-align: middle;
    height: 30px;
	background: #FFFFFF;
	color: #000000;
}
/**
 * 表身样式 TableBody
 */
.my-table-body-class tr {
    background-color: #fff;
}
.my-table-body-class td {
    border: 1px solid #B5B5B5;
    text-align: center;
    vertical-align: middle;
    height: 30px;
    font-size: 15px;
	    word-break: break-all;
}
</style>
  </head>
  <body>
  ';
  $proReportContent="";
  $proReportContentHead="";
  $proReportContentBody="";
  $caseTotal=0;
  $casePass=0;
  $caseFail=0;
  $n=0;
  $k=0;
  $m=0;

  if(! $tree['testsuites']['testsuite'][0]) {
  	
  	$temp = $tree['testsuites']['testsuite'];
  	
  	$tree['testsuites']['testsuite'] = array();
  	$tree['testsuites']['testsuite'][0] = $temp;
  }
  
   $i=count($tree['testsuites']['testsuite']);
  
  
   for($j=0;$j<$i;$j++){
	 $name=$tree['testsuites']['testsuite'][$j]['name'];
	 $testcase=$tree['testsuites']['testsuite'][$j]['testcase'];
	$proReportContentHead='<tbody id="my-table-body-id" class="my-table-body-class">
	       <tr>
		  <td style="width:7%;">MODE+版本页面</td>
		  <td style="width:70%;" colspan="7">'.$name.'</td>
		  </tr>	 
        ';
    //echo $tree['testsuites']['testsuite'][$j]['name'];
	$k=count($testcase);
	$m=count($testcase, COUNT_RECURSIVE);
	if($k == $m){
     $n++;
	 if($testcase['passed'] == "1"){
		$passed = "通过";
		$casePass++;
		}else{
			$passed = '<font color="red">失败</font>';
			$caseFail++;
			}
		//add by xiwu, -2.3% or 2.1%
		$regx = "#^-?\d{0,2}\.\d{0,2}%$#";
		if(preg_match($regx,$val['failure']['value']))		
		{
			$link = isset($val['failure']['value'])? $val['failure']['value'] : '0%';
		}else{
			$link = isset($val['failure']['value'])?'<a href='.$val['failure']['value'].'>diff report</a>' : '';
		}
		//add by xiwu
     $proReportContentBody.="<tr>
            <td>".$n."</td>
            <td><a href='".$testcase['url']."' target='_blank'>".$testcase['name']."</a></td>
            <td>".$passed."</td>
            <td>$link</td>
          </tr>";
	}else{
	 foreach($testcase as $key=>$val){
     $n++;
	 //echo $val['keys_res'];
	if($val['passed'] == "1"){
		$passed = "通过";
		$casePass++;
		}else{
			$passed = '<font color="red">失败</font>';
			$caseFail++;
			}
		//add by xiwu, like -2.4% or 1.3%
		$regx = "#^-?\d{0,2}\.\d{0,2}%$#";
		if(preg_match($regx,$val['failure']['value']))		
		{
			$link = isset($val['failure']['value'])? $val['failure']['value'] : '0%';
			$old_c = "old_value:".file_get_contents($val['url'].".perf.old");
			$new_c = "new_value:".file_get_contents($val['url'].".perf.new");
		}else{
			$link = isset($val['failure']['value'])?'<a href='.$val['failure']['value'].'>diff report</a>' : '';
		}
		if($perf === "perf" && $val['passed'] == 1 )
		{
			$old_v = file_get_contents($val['url'].".perf.old");
			$new_v = file_get_contents($val['url'].".perf.new");
                        $old_c = "old_value:$old_v";
                        $new_c = "new_value:$new_v";
                        $link = (round(($new_v/$old_v - 1), 4)) * 100 ."%";
		}
		//add by xiwu
     $proReportContentBody.="<tr>
            <td>".$n."</td>
            <td><a href='".$val['url']."' target='_blank'>".$val['name']."</a></td>
            <td>".$passed."</td>
	    <td>$link</td>";
		//add by xiwu
	if($perf == "perf")
	{
		$proReportContentBody.= "<td>".$old_c."; ".$new_c." </td>";
	}
	//add by xiwu
         $proReportContentBody.= "</tr>";
	 }
	}
	$proReportContent.=$proReportContentHead.$proReportContentBody;
    $proReportContentBody="";
}
$proReport=' <br><br><div id="container">
      <table id="my-table-id" class="my-table-class">
        <thead id="my-table-header-id" class="my-table-header-class tablehead">
          <tr>
		  <th style="width:10%;">URL</th>
            <th style="width: 90%;" ><a href="'.$URL.'">'.$URL.'</a></th>
          </tr>
		  <tr>
           <th style="width: 10%;" >项目名称</th>
           <th style="width: 90%;" >'.$PROJECTNAME.'</th>
		  </tr>
        </thead>
        <tbody id="my-table-body-id" class="my-table-body-class">
          <tr>
            <td style="width: 50%;" colspan="2">case总数:&nbsp;'.$n.'&nbsp;&nbsp;&nbsp;case成功数:&nbsp;'.$casePass.'&nbsp;&nbsp;&nbsp; case失败数:&nbsp;<font color="red">'.$caseFail.'</font></td>
          </tr>
		  </tbody>
		  </table>
           </div><br>';
$proReportTitle='
      <div id="container">
      <table id="my-table-id" class="my-table-class">
        <thead id="my-table-header-id" class="my-table-header-class">
	';
if($perf == "perf")
{
	$proReportTitle .= '<tr>
            <th style="width: 8%;">序号</th>
            <th style="width: 20%;">用例名称</th>
            <th style="width: 15%;">执行结果</th>
            <th style="width: 15%;">性能差异</th>
            <th style="width: 42%;">原始数据</th>
	    </tr>';
}else{
	$proReportTitle .= '<tr>
            <th style="width: 8%;">序号</th>
            <th style="width: 14%;">用例名称</th>
            <th style="width: 6%;">执行结果</th>
            <th style="width: 13%;">Diff报表</th>
</tr>';
}
	    
$proReportTitle .='</thead>';


$proReportTail='</tbody>
      </table>
    </div>
  </body>
</html>';
$contents=$proReportHead."\n".$proReport."\n".$proReportTitle."\n".$proReportContent."\n".$proReportTail;
file_put_contents($htmlFile,"");
file_put_contents($htmlFile,$contents,LOCK_EX);
?>
