var result;

function getantitoken(param) { //定义导出函数

        Java.perform(function ()
            {
        //获取内存中已有对象 主动调用
        Java.choose("com.aimi.android.common.http.a",
        {
          //匹配到对象执行的回调函数
          onMatch: function (instance)
          {
            result = instance.c(param,false);
            result = HashMap_tosting(result);
          },
          //搜索完成后执行的回调函数
          onComplete: function ()
          {
          }
        });

    console.log("result: " + result);
  });
  return result;
}

function HashMap_tosting(param_hm){
    var HashMap = Java.use('java.util.HashMap');
    var args_map = Java.cast(param_hm, HashMap);
    return args_map.toString();
}
rpc.exports = {
    getantitoken: getantitoken,
};