PHP='/home/forum/marsers/mahong/odp/php/bin/php';
EXPECT_SH='/bin/bash /home/forum/bin/envtools/bin/envupAdvance/tools/lib/expect.sh';
EXPECT='/bin/bash /home/forum/bin/envtools/bin/envupAdvance/tools/lib/expectNeedPwd.sh';
BASEENV='cq01-testing-forum69.vm.baidu.com';
REPORT_ADDRESS='/home/work/orp001/data/app/logtest';
LOG_FOLDER_JEKINS='/home/forum/marsers/mahong/supertest/workspace/log_auto_test';
curDir=`echo $(cd "$(dirname "$0")"; pwd)`
cd $curDir
#svn up
task=$1
host=$2
host1=`echo $host | awk -F ':' '{print $1}'`
host2=$3
host2=`echo $host2 | awk -F ':' '{print $1}'`
testID='testid='$4
buildURL=$5
environment_name=$6
rm -rf  $curDir/report/*

cd $curDir/src/phpdiff
/home/forum/envtools/CommonTools/python/bin/python dataTest.py $task $host1 $host2 $testID
cd $curDir
curl "http://cq01-testing-forum69.vm.baidu.com:8200/service/logtest?method=getAutoRes&"$testID
$EXPECT 2zqwz scp forum@$BASEENV:$REPORT_ADDRESS/report_$4.xml $curDir/report/report.xml;
#$EXPECT forumtest scp forum@$BASEENV:$REPORT_ADDRESS/report_123.xml $curDir/report/report.xml;
$PHP $curDir/xmlToHtml.php $buildURL $environment_name

cp $curDir/report/report.html $LOG_FOLDER_JEKINS
cp $curDir/report/report.xml $LOG_FOLDER_JEKINS
