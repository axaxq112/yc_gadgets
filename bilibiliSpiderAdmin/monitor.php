<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>aid增长状况实时监测</title>
    <meta http-equiv="Pragma" content="no-cache"> 
    <script src="./jquery.min.js"></script>
    <script src="./echarts.min.js"></script>
</head>
<body>
    <div id="main" style="margin:0 auto;"></div>
    <span id="retSpan1" class="retSpan1" style="display:block;margin:0 auto;text-align:center;font-size:16px;">最新记录时间（来自数据库）:</span>
    <br>
    <span id="retSpan2" class="retSpan2" style="display:block;margin:0 auto;text-align:center;font-size:16px;">差值:</span>

    <script>
        var main = document.getElementById("main");
        function resizeMain() {
            main.style.width = window.innerWidth+'px';
            //main.style.height = window.innerHeight+'px';
            main.style.height = "500px";
        };
        resizeMain();

        var hrChart = echarts.init(document.getElementById("main"));

        var dataX = []; //x轴对应时间
        var dataY = []; //y轴对应aid

        function sleep(NumMillis) {
            var nowTime = new Date();
            var exitTime = nowTime.getTime() + NumMillis;
            while (true) {
                now = new Date();
                if (now.getTime() > exitTime)
                    return;
            }
        }

        function updateObject(aidStr, timeStr) {
            if (dataX.length < 10 && dataY.length < 10) {
                if (dataX.length != dataY.length) {
                    alert("返回数据有误，两Object不能重合");
                } else {
                    dataX.push([timeStr]);
                    dataY.push([parseInt(aidStr)]);
                    return "inserted";
                }
            } else if (dataX.length == 10 && dataY.length == 10) { //被调用添加的时候，dataObj的长度为10，需要删除第一个内容然后push
                //删除两个Obj中的第一个内容
                dataX.shift();
                dataY.shift();
                //在最后分别都添加一项
                dataX.push([timeStr]);
                dataY.push([parseInt(aidStr)]);
                return "inserted";
            }
        }

        function ajaxRefreshLatestTime(){
            $.ajax({
                type: "GET",
                url: "getData.php",
                data: "type=2",
                dataType: "text",
                success: function (data) {
                    $("#retSpan1").html("最新记录时间（来自数据库）:" + data);
                },
                error: function(error) {
                    ajaxRefreshLatestTime();
                }
            });
        }

        function ajaxAutoRefresh() {
            $.ajax({
                url: "getData.php",
                data: "type=1",
                type: 'GET',
                dataType: 'text',
                success: function(data) {
                    data = data.toString();
                    var strList = data.split("|");
                    ajaxAidStr = strList[0];
                    ajaxTimeStr = strList[1];

                    if(ajaxAidStr == null || ajaxTimeStr == null){
                        window.location.reload();
                    }
                    if(ajaxAidStr == "" || ajaxTimeStr == ""){
                        window.location.reload();
                    }
                    console.info("当前获取到的aid:" + ajaxAidStr);
                    console.info("当前获取到的TimeStr:" + ajaxTimeStr);
                    updateObject(ajaxAidStr, ajaxTimeStr);
                    hrFun(dataX, dataY); //这里的dataX和dataY都是外部的，已经过updateObject修改（包含最近10条数据)
                },
                error: function(error) {
                    console.warn(error);
                    window.location.reload();
                }
            });
        }

        function hrFun(x_data, y_data) {

            if(x_data.length != y_data.length){
                window.location.reload();
            }

            tmpDataY = [2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 11000000];

            for (var k in y_data) {
                int_y_data = parseInt(y_data[k]);

                tmpDataY[k] = int_y_data;
            }

            //console.info("y_data", tmpDataY);

            hrChart.setOption({
                color: ['#3398DB'],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                legend: {
                    data: ['aid值']
                },
                grid: {
                    left: '3%',
                    right: '20%',
                    bottom: '20%',
                    containLabel: true
                },
                xAxis: [{
                    type: 'category',
                    data: x_data,
                    axisLabel: {
                        interval: 0,  //坐标轴刻度标签的显示间隔.设置成 0 强制显示所有标签。设置为 1，隔一个标签显示一个标签。
                        rotate: 45,//倾斜度 -90 至 90 默认为0
                    }
                }],
                yAxis: [{ // 纵轴标尺固定
                    type: 'value',
                    scale: true,
                    name: 'aid',
                    min: tmpDataY[9] - 170, //最小值
                    max: tmpDataY[9], //最大值
                    splitNumber: 10,
                    boundaryGap: [0.4, 0.4]
                }],
                series: [{
                    name: 'aid',
                    type: 'line',
                    data: tmpDataY
                }]
            }, true);
        }

        //先快速请求10次，先呈现出图像（要不然没有y轴）
        var i = 0;
        for (var i = 0; i < 10; i++) {
            ajaxAutoRefresh();
            sleep(500); //间隔500毫秒
        }

        setTimeout(() => {
            if(dataX.length != 10 || dataY.length != 10){
                alert("本页初始化时出现问题,点击确定后自动刷新");
                console.log("error");
                window.location.reload();
         }
         console.info("ok");
        }, 3000);


        function calc_D_value() {
            if(dataX.length == 10 && dataY.length == 10){
                calcTmp1 = dataY[9] - dataY[8];
                calcTmp2 = dataY[8] - dataY[7];
                calcTmp3 = dataY[9] - dataY[0];
                retStr = "20秒内结果如下:";
                retStr += "<br> 第10项与第9项相差:" +calcTmp1.toString() + "条";
                retStr += "<br> 第9项与第8项相差:" +calcTmp2.toString() + "条";
                retStr += "<br> 第10项与第1项相差:" +calcTmp3.toString() + "条";
                predictNum = calcTmp3 * 3;
                retStr += "<br>预计一分钟增长:" +predictNum.toString() + "条";
                $("#retSpan2").html(retStr);
                }
        }

        window.onresize = () =>{
            console.info("resize");
            resizeMain();
            hrChart.resize();
        } 

        var refreshInterval = 2000;
        setInterval(calc_D_value, refreshInterval);
        setInterval(ajaxAutoRefresh, refreshInterval);
        setInterval(ajaxRefreshLatestTime, refreshInterval);
    </script>
</body>
</html>