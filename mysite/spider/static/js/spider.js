function validateForm() {
    x = document.forms["myForm"]["fname"].value;
    if (x == "") {
        alert("爬虫关键字不能为空哦");
        event.preventDefault(); //阻止form表单默认提交
        return;
    }
    $.post("/startsipder",
        {
            "keyword": x,
        },
        function (data, status) {
            if (data == 1) {
                alert("爬虫启动成功")
            } else {
                alert("爬虫已经存在哦")
            }
        });
    event.preventDefault(); //阻止form表单默认提交;
    return true;
}

window.setInterval(refreshDate, 3000);

function refreshDate() {
    var xmlhttp;


    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jsontext = xmlhttp.responseText;
            var obj = JSON.parse(jsontext);
            var groups = obj.split("|");
            var intest = ""
            for (q in groups)
                keyword = q.split(";")[0].split("1")

        }
        document.getElementById("data").innerHTML = xmlhttp.responseText;
    }


    xmlhttp.open("GET", "refreshdata", true);

    xmlhttp.send();

}

// $(document).ready(function () {
//     $(".keyword").click(function () {
//
//         $.post("startsipder",
//             {
//                 keyword: "Donald Duck",
//
//             },
//             function (data, status) {
//                 alert("爬虫启动成功");
//             });
//     });
// });

function refreshDate() {
    var xmlhttp;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jsontext = xmlhttp.responseText.split("&");
            document.getElementById("data").innerHTML = jsontext[0];

            if (jsontext[1] == null || jsontext[1] == "")
                document.getElementById("spider_run").innerHTML = "当前没有爬虫正在运行";
            else document.getElementById("spider_run").innerHTML = jsontext[1];

        }

    }


    xmlhttp.open("GET", "refreshdata", true);

    xmlhttp.send();

}