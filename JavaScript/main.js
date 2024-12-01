// 页面加载时的动画效果，例如淡入
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.main-content').forEach(function (element) {
        element.style.opacity = 0;
        setTimeout(function () {
            element.style.opacity = 1;
        }, 100);
    });
});

// 表单输入框获取焦点时添加额外的动画效果（这里以放大效果为例，可以根据喜好调整）
const inputElements = document.querySelectorAll('input[type="text"], textarea');
inputElements.forEach(function (input) {
    input.addEventListener('focus', function () {
        this.style.transform = 'scale(1.05)';
        this.style.transition = 'transform 0.3s ease';
    });
    input.addEventListener('blur', function () {
        this.style.transform = 'scale(1)';
        this.style.transition = 'transform 0.3s ease';
    });
});

// 按钮点击时添加动画效果（这里以稍微缩小再恢复的效果为例）
const buttons = document.querySelectorAll('button');
buttons.forEach(function (button) {
    button.addEventListener('mousedown', function () {
        this.style.transform = 'scale(0.95)';
        this.style.transition = 'transform 0.1s ease';
    });
    button.addEventListener('mouseup', function () {
        this.style.transform = 'scale(1)';
        this.style.transition = 'transform 0.1s ease';
    });
});

// 模态框显示和隐藏时的动画效果（淡入淡出）
const modals = document.querySelectorAll('.modal');
modals.forEach(function (modal) {
    modal.addEventListener('show.bs.modal', function () {
        modal.style.opacity = 0;
        setTimeout(function () {
            modal.style.opacity = 1;
        }, 100);
    });
    modal.addEventListener('hide.bs.modal', function () {
        modal.style.opacity = 1;
        setTimeout(function () {
            modal.style.opacity = 0;
        }, 100);
    });
});