PHP='/home/forum/marsers/mahong/odp/php/bin/php'
POST_RES_URL="http://tip.baidu.com/analysis/autocase"
REPORT_PATH='/home/forum/marsers/jenkins/workspace/pdiff_tip/report'
PYTHON='/home/forum/envtools/CommonTools/python/bin/python'
source /home/forum/.bash_profile
curDir=`echo $(cd "$(dirname "$0")"; pwd)`
cd $curDir
svn up
cd $curDir/src/phpdiff
task=$1
host=$2
host=`echo $host | awk -F ':' '{print $1}'`
cookies=$3
jobID=$4
buildURL=$6
environment_name=$7
souce_server=$8
src_server="ONLINE"
case "$souce_server" in
	"offline" )
		src_server="cq01-testing-forum87.cq01.baidu.com";;
	"sandbox" )
		src_server="tc-testing-sandbox-forum10-vm.epc.baidu.com";;
	*)
		src_server="ONLINE";;
esac
echo $src_server
path="$task"_"$jobID"
rm -rf  $curDir/*_result.xml
$PYTHON phpdiff.py $task $host $cookies $jobID $REPORT_PATH $src_server
report_name="$task"_result.xml
cp -f $curDir/report/$path/result.xml $curDir/$report_name
if [ "xtip" == "x$5" ];then
	echo "upload report to TIP..."
	cd $curDir/src/phpdiff
	$PHP uploadFilebyCurl.php $curDir/report/$path/result.xml $jobID $POST_RES_URL
	exit 0
fi
cd $curDir/src/phpdiff
$PHP xmlToHtml.php $curDir/$report_name $curDir/report.html $buildURL $environment_name
