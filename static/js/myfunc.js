var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: "text/x-c",
    lineNumbers: true,	//显示行号
    theme: "dracula",	//设置主题
    lineWrapping: true,	//代码折叠
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
    matchBrackets: true,	//括号匹配
    autocomplete: true,
    styleActiveLine: true,
//readOnly: true,        //只读
});
editor.setValue("int main(){\n" +
    "  printf(\"hello，world\");\n" +
    "}");
editor.setSize('80%', '90%');

// $("#code").next().css({marginleft: "4%"});

var outer = CodeMirror.fromTextArea(document.getElementById("code-out"), {
    mode: "text/x-c",
    lineNumbers: true,	//显示行号
    theme: "dracula",	//设置主题
    lineWrapping: true,	//代码折叠
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
    matchBrackets: true,	//括号匹配
    autocomplete: true,
    styleActiveLine: true,
    showCursorWhenSelecting: false,
    readOnly: "nocursor",        //只读
});
outer.setValue("请点击编译");
outer.setSize('80%', '90%');

// 本地文件处理
$("#fileImport").click(function () {
    $("#files").click();
});

function fileImport() {
    //获取读取我文件的File对象
    var selectedFile = document.getElementById('files').files[0];
    var name = selectedFile.name;//读取选中文件的文件名
    var size = selectedFile.size;//读取选中文件的大小
    console.log("文件名:" + name + "大小:" + size);

    var reader = new FileReader();//这是核心,读取操作就是由它完成.
    reader.readAsText(selectedFile);//读取文件的内容,也可以读取文件的URL

    reader.onload = function () {
        //当读取完成后回调这个函数,然后此时文件的内容存储到了result中,直接操作即可
        console.log(reader.result);
        editor.setValue(reader.result);
    }
}

// 语法分析
$("#get_table").click(function () {
    myajax.get({
        'url': '/get_table',
        'data': {},
        'success': function (result) {
            if (result) {
                outer.setValue(result)
            } else {
                outer.setValue('网络错误或程序错误')
            }
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});

// 生成四元式
// $("#get_generate").click(function () {
//     console.log('click');
//     myajax.get({
//         'url': '/get_generate',
//         'data': {'message': editor.getValue()},
//         'success': function (result) {
//             if (result) {
//                 outer.setValue(result)
//             } else {
//                 outer.setValue('网络错误或程序错误')
//             }
//         },
//         'fail': function (error) {
//             console.log(error)
//         }
//     })
// });

// 输出字符与变量
$("#get_lexer").click(function () {
    console.log('click');
    myajax.get({
        'url': '/get_lexer',
        'data': {'message': editor.getValue()},
        'success': function (result) {
            if (result) {
                outer.setValue(result)
            } else {
                outer.setValue('网络错误或程序错误')
            }
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});


// 输出语法栈变化
$("#get_lr").click(function () {
    console.log('click');
    myajax.get({
        'url': '/get_lr',
        'data': {'message': editor.getValue()},
        'success': function (result) {
            if (result) {
                outer.setValue(result)
            } else {
                outer.setValue('网络错误或程序错误')
            }
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});


// 输出汇编代码
$("#get_asm").click(function () {
    console.log('click');
    myajax.get({
        'url': '/get_asm',
        'data': {'message': editor.getValue()},
        'success': function (result) {
            if (result) {
                outer.setValue(result)
            } else {
                outer.setValue('网络错误或程序错误')
            }
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});

// 运行结果
$("#run").click(function () {
    myajax.get({
        'url': '/run',
        'data': {'message': editor.getValue()},
        'success': function (result) {
            if (result) {
                outer.setValue(result)
            } else {
                outer.setValue('网络错误或程序错误')
            }
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});

// 运行结果
$("#download").click(function () {
    myajax.get({
        'url': '/download_url',
        'data': {'message': editor.getValue()},
        'success': function (result) {
            window.location.href = result;
        },
        'fail': function (error) {
            console.log(error)
        }
    })
});

$("#start-btn").click(function () {
    $('#welcome').animate({height: "0px", zIndex: "-1", opacity: '0'}, 360);
    // document.getElementById('welcome').style.zIndex = '-1';

});

// ajax功能
var myajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        // this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        $.ajax(args);
    },
};
