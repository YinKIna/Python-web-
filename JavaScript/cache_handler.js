window.onload = function() {
    // 禁用浏览器缓存，让页面每次加载都获取最新数据
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href + '?' + new Date().getTime());
    }
};