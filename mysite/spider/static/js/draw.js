


// 随便画个图
var base = +new Date(1968, 9, 3);
var oneDay = 24 * 3600 * 1000;
var date = [];

var data = [Math.random() * 300];

for (var i = 1; i < 20000; i++) {
    var now = new Date(base += oneDay);
    date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
    data.push(Math.round((Math.random() - 0.5) * 20 + data[i - 1]));
}

var option = {
    grid:{
        right:0,
    },
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        type: 'line'
    }],
    dataZoom:[
        [{
            type:'slider',
            start:10,
            end:60
        },{
            type:'inside',
            start:10,
            end:60
        },{
            type:"slider",
            yAxisIndex:0,
            start:10,
            end:60
        },{
            type:'inside',
            yAxisIndex:0,
            start:10,
            end:60
        }]
    ]
};
if(document.getElementById('hotchart')){
    var myChart = echarts.init(document.getElementById('hotchart'));
    myChart.setOption(option)
    myChart.on('click',params=>{
        console.log(params)
        $('.dev-widget-content').text(`${params.name} and ${params.data}`)
        $('.dev-widget').css('visibility','visible')
        $('.dev-widget').css('opacity',1)
    })
}


//随便画个图2
if(document.getElementById('calendarchart')){
    var myChart2=echarts.init(document.getElementById('calendarchart'))
    var option2={
        tooltip:{},
        calendar:{
            range:'2017'
        },
        series:[{
            type:'pie',
            radius:30,
            center:myChart2.convertToPixel('calendar',['2017-01-01',1000]),
            data:[
                {name: '工作', value: Math.round(Math.random() * 24)},
                {name: '娱乐', value: Math.round(Math.random() * 24)},
                {name: '睡觉', value: Math.round(Math.random() * 24)}
            ]
        },{
            type:'pie',
            radius:30,
            data:[
                {name: '工作', value: Math.round(Math.random() * 24)},
                {name: '娱乐', value: Math.round(Math.random() * 24)},
                {name: '睡觉', value: Math.round(Math.random() * 24)}
            ]
        }]
    }
    myChart2.setOption(option2)
}
