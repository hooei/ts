function Slider(opts){
    //构造函数需要的参数
    this.wrap = opts.dom;
    this.ul = opts.dom.querySelector('ul');
    this.list = this.ul.querySelectorAll('li');
    //this.scaleW = this.list[0].offsetWidth || 0;
    this.scaleW = this.ul.offsetWidth;
    this.time = opts.time || 2000;
    this.speed = opts.speed || 200;
    this.touch = opts.touch || 0;
    this.auto = opts.auto || 0;
    this.timer = 0; // 定时器
    this.isdot = opts.dot || 0;
    this.dotlist = {};
    this.dots = {};

    //构造三步奏
    this.init();
    this.renderDOM();
    this.bindDOM();
}

//第一步 -- 初始化
Slider.prototype.init = function() {
    //设定窗口比率
    //this.radio = window.innerHeight/window.innerWidth;

    //设定初始的索引值
    this.idx = 0;
};

//第二步 -- 根据数据渲染DOM
Slider.prototype.renderDOM = function(){
    var wrap = this.wrap;
    var list = this.list;
    var len = list.length;
    var mHeight= 0;
    var dotlist = this.dotlist;
    var isdot = this.isdot;
    var dots = this.dots;

    this.outer = this.ul;

    //根据元素的
    for(var i = 0; i < len; i++){
        var li = list[i];
        //var item = data[i];

        //li.style.width = window.innerWidth +'px';
        li.style.webkitTransform = 'translate3d('+ i*this.scaleW +'px, 0, 0)';
        if (li.offsetHeight > mHeight) mHeight = li.offsetHeight;
    }

    // 处理点数
    if (isdot && len > 0) {
        var dots = document.createElement('div');
        dots.className = 'slider-dots';

        for(var i = 0; i < len; i++) {
            var item = document.createElement('span');

            if (i === 0) item.className = 'slider-dot active';
            else item.className = 'slider-dot';

            dots.appendChild(item);
        }
        this.dots = dots;
        wrap.appendChild(dots);
    }

    //UL的宽度和画布宽度一致
    this.outer.style.cssText = 'width:' + this.scaleW +'px; height: ' + mHeight + 'px';
};

Slider.prototype.goIndex = function(n){
    var idx = this.idx;
    var lis = this.outer.getElementsByTagName('li');
    var len = lis.length;
    var speed = this.speed;
    var isdot = this.isdot;
    var dots = this.dots;
    var cidx;


    //如果传数字 2,3 之类可以使得直接滑动到该索引
    if(typeof n == 'number'){
        cidx = idx;
        //如果是传字符则为索引的变化
    }else if(typeof n == 'string'){
        cidx = idx + n*1;
    }

    //当索引右超出
    if(cidx > len-1){
        cidx = len - 1;
        //当索引左超出
    }else if(cidx < 0){
        cidx = 0;
    }

    //保留当前索引值
    this.idx = cidx;

    //改变过渡的方式，从无动画变为有动画
    lis[cidx].style.webkitTransition = '-webkit-transform '+ speed +'ms linear';
    lis[cidx-1] && (lis[cidx-1].style.webkitTransition = '-webkit-transform '+ speed +'ms linear');
    lis[cidx+1] && (lis[cidx+1].style.webkitTransition = '-webkit-transform '+ speed +'ms lineart');

    //改变动画后所应该的位移值
    lis[cidx].style.webkitTransform = 'translate3d(0, 0, 0)';
    lis[cidx-1] && (lis[cidx-1].style.webkitTransform = 'translate3d(-'+ this.scaleW +'px, 0, 0)');
    lis[cidx+1] && (lis[cidx+1].style.webkitTransform = 'translate3d('+ this.scaleW +'px, 0, 0)');


    if(isdot && len > 0) {
        var dotlist = dots.querySelectorAll('.slider-dot');
        // 处理点数
        for (var i = 0; i < len; i++) {
            if (i === cidx) dotlist[i].classList.add('active');
            else dotlist[i].classList.remove('active');
        }
    }

};

//第三步 -- 绑定 DOM 事件
Slider.prototype.bindDOM = function(){

    var self = this;
    var scaleW = self.scaleW;
    var outer = self.outer;
    var len = self.list.length;
    var auto = self.auto;
    var isdot = self.isdot;

    if (auto) {
        self.play();
    }

    //手指按下的处理事件
    var startHandler = function(evt){

        // 取消循环
        if (auto && self.t) {
            self.stop();
        }

        //记录刚刚开始按下的时间
        self.startTime = new Date() * 1;

        //记录手指按下的坐标
        self.startX = evt.touches[0].pageX;

        //清除偏移量
        self.offsetX = 0;

        //事件对象
        var target = evt.target;
        while(target.nodeName != 'LI' && target.nodeName != 'BODY'){
            target = target.parentNode;
        }
        self.target = target;

    };

    //手指移动的处理事件
    var moveHandler = function(evt){
        //兼容chrome android，阻止浏览器默认行为
        evt.preventDefault();

        //计算手指的偏移量
        self.offsetX = evt.targetTouches[0].pageX - self.startX;

        var lis = outer.getElementsByTagName('li');
        //起始索引
        var i = self.idx - 1;
        //结束索引
        var m = i + 3;

        //最小化改变DOM属性
        for(i; i < m; i++){
            lis[i] && (lis[i].style.webkitTransition = '-webkit-transform 0s ease-out');
            lis[i] && (lis[i].style.webkitTransform = 'translate3d('+ ((i-self.idx)*self.scaleW + self.offsetX) +'px, 0, 0)');
        }
    };

    //手指抬起的处理事件
    var endHandler = function(evt){
        evt.preventDefault();

        if (self.auto && !self.t) {
            self.play();
        }

        //边界就翻页值
        var boundary = scaleW/6;

        //手指抬起的时间值
        var endTime = new Date() * 1;

        //所有列表项
        var lis = outer.getElementsByTagName('li');

        //当手指移动时间超过300ms 的时候，按位移算
        if(endTime - self.startTime > 300){
            if(self.offsetX >= boundary){
                self.goIndex('-1');
            }else if(self.offsetX < 0 && self.offsetX < -boundary){
                self.goIndex('+1');
            }else{
                self.goIndex('0');
            }
        }else{
            //优化
            //快速移动也能使得翻页
            if(self.offsetX > 50){
                self.goIndex('-1');
            }else if(self.offsetX < -50){
                self.goIndex('+1');
            }else{
                self.goIndex('0');
            }
        }
    };

    //绑定事件
    if (this.touch) {
        outer.addEventListener('touchstart', startHandler);
        outer.addEventListener('touchmove', moveHandler);
        outer.addEventListener('touchend', endHandler);
    }
};

// 第四步　-- auto
Slider.prototype.play = function() {
    var self = this;

    self.t = setInterval(function() {
        self.goIndex('+1');
    }, self.time);
};

//  Stop autoplay
Slider.prototype.stop = function() {
    var self = this;

    self.t = clearInterval(self.t);
};

// set attribute
Slider.prototype.setAuto = function(value) {
    if (value) {
        this.auto = 1;
        this.play();
    }
    else {
        this.auto = 0;
        this.stop();
    }
}
