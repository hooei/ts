/** @preserve Copyright 2010-2014 Mideer.com. All Rights Reserved. */
QL = window.QL = window.QL || {};

/**
 任务列表
 --------

 @changelog
 #1     钱鹿活动时间显示
 #2     钱鹿增加渠道号

 */
;(function(win, doc, $, QL) {
    var API         = win.API,
        iswx        = /MicroMessenger/i.test(navigator.userAgent),
        iswb        = /weibo/i.test(navigator.userAgent) || /TencentMicro/i.test(navigator.userAgent) ,
        isqq        = /QQ/i.test(navigator.userAgent),
        isandroid   = /android/i.test(navigator.userAgent),
        isios       = !!navigator.userAgent.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/),
        isios4      = /iPhone OS 4/i.test(navigator.userAgent),
        issafari    = /Safari/i.test(navigator.userAgent),
        issafari6   = /Safari/i.test(navigator.userAgent) && /Version\/6/i.test(navigator.userAgent),
        issafari70  = /Safari/i.test(navigator.userAgent) && /Version\/7\.0/i.test(navigator.userAgent),
        issafari8   = /Safari/i.test(navigator.userAgent) && /Version\/8/i.test(navigator.userAgent),
        isios8      = /Version\/8/i.test(navigator.userAgent),


    /** 私有属性
     -----------------------------------------------------------------*/
    C = {
        an      : 'qd',
        // Todo
        //nm      : API.encode('钱鹿'),
        nm      : '',
        gt      : 1,
        limit   : 0,
        act     : 0,   // 活动开启(0为关闭，１打开),
        surl    : 'http://www.qiandeer.com',    // 媒介链接
        pn      : '',  // 助手传过来的包名
        v       : 0,   // 助手传过来的版本
        l       : 0    // 助手是否在线
    },

    timeLogin = 0,

    Lists = function() {};


    /** 引入百度统计
     ---------------------------------------------------------------- */
    var _hmt = _hmt || [];
    (function() {
        var hm = document.createElement("script");
        hm.src = "//hm.baidu.com/hm.js?9417ceeee141d361619413153e5567ba";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
    })();


    /** 私有方法
     -----------------------------------------------------------------*/
    /**
     *  =init
     *  @about    初始化
     */
    (function init(win) {

        // 对ios8进行宽度设置处理
        if(isios8) {
            var viewport = doc.querySelector("meta[name=viewport]");
            if (win.orientation === -90 || win.orientation === 90) {
                viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0');
            }
            else {
                viewport.setAttribute('content', 'width=320, user-scalable=0');
            }

            document.addEventListener('orientationchange', function () {
                var orient = 1;
                switch (win.orientation) {
                    case 0:
                    case 180:
                        orient = 0;
                        break;
                    case -90:
                    case 90:
                        orient = 1;
                        break;
                }
                ;
                //document.body.setAttribute('class', orient ? 'landscape' : 'portrait');
                var viewport = doc.querySelector("meta[name=viewport]");
                if (orient) {
                    viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0');
                }
                else {
                    viewport.setAttribute('content', 'width=320, user-scalable=0');
                }
            }, false);
        }

        //TO测试
    })(win);

    /**
     *  =init 初始化
     *  @param module
     */
    function init(module) {

        switch (module) {
            case 'update':
                update();
                break;
            case 'login':
                login();
                break;

            case 'home':
                home();
                break;

            case 'detail':
                detail();
                break;

            case 'prentice':
                prentice();
                break;

            case 'feedback':
                feedback();
                break;

            case 'info':
                info();
                break;

            case 'phone':
                phone();
                break;

            case 'switchPhone':
                switchPhone();
                break;

            case 'union':
                union();
                break;

            case 'taskVideo':
                taskVideo();
                break;

            default:
                break;
        }

    }

    // =home 主页
    function home() {

        unit();
        build();

        // 单位换算
        function unit() {
            $('.unit-earn').html(API.numFormat(PD.earn, 2));
            $('.unit-invite').html(API.numFormat(PD.invite, 0));
            $('.unit-total-users').html(API.numFormat(PD.totalUsers, 0));
            $('.unit-total-sons').html(API.numFormat(PD.totalSons, 0));
            $('.unit-total-exchange').html(API.numFormat(PD.totalExchange, 0));
        }

        function build() {
            Lightbox.init();

            // 网页墙地址
            var $earn = $('#earn-url'),
                list = $earn.attr('href');

            if(PD.bound) { // 没领取红包
                Lightbox.show($('#tpl-fill-box').tmpl({money: PD.money}));

                // 输入宴请人ID错误
                if(PD.inputFail) {
                    $('.pack-btn-normal').html('输入的ID无效，重输获得3元');
                }

                // 提交事件
                $('.btn-bound').on('click', function() {
                    var id = $('input[name=uid]').val().trim(),
                        type = parseInt($(this).data('type'));

                    if(type === 1) {
                        if(id.length < 1) {
                            alert('只有输入正确的邀请人ID才能获得3元');
                            return false;
                        }
                    }
                    win.location.href = '/home?pack=1&uid=' + id;
                    return false;
                });
            }
            else { // 已经领取
                // 领取，并提示红包拿到
                if (PD.money && !PD.bound) {
                    // 显示红包
                    Lightbox.show($('#tpl-show-bound').tmpl({money: PD.money}));

                    $('.btn-close-bound').on('tap', function () {
                        Lightbox.hide();

                        // 处理快捷方式
                        try {
                            // 标记第一次
                            API.setLocal('keep-alert', 3);

                            // 将要保存快捷方式的地址改变
                            history.pushState({}, '钱鹿', API.host() + '/home');

                            // 提示添加桌面快捷方式
                            $('body').append($('#tpl-into-destop').tmpl({}));
                            $('.btn-close').on('click', function () {
                                var time = parseInt(API.getLocal('keep-alert'));
                                if (time) {
                                    // 用户点击关闭，就不再弹提示
                                    API.setLocal('keep-alert', --time);
                                }
                                $('.destop-tip').remove();
                            });
                        }
                        catch(e) {
                            $('.destop-tip').remove();
                        }

                        // 有资格参加米禾活动的用户
                        if (PD.showFlow) {
                            showFlow();
                        }
                        else {
                            // 显示活动
                            showActivity();
                        }
                    });
                    $('.money').html(API.numFormat(PD.totalMoney, 2)).removeClass('hidden');
                }
                else { // 已经提示过拿了红包
                    // 提示桌面保存
                    try {
                        var keep = parseInt(API.getLocal('keep-alert'));
                        if (keep && keep > 0) {
                            // 将要保存快捷方式的地址改变
                            history.pushState({}, '钱鹿', API.host() + '/home');
                            $('body').append($('#tpl-into-destop').tmpl({}));
                            $('.btn-close').on('click', function () {
                                var time = parseInt(API.getLocal('keep-alert'));
                                if (time) {
                                    // 用户点击关闭，就不再弹提示
                                    API.setLocal('keep-alert', --time);
                                }
                                $('.destop-tip').remove();
                            });
                        }
                    }
                    catch (e) {
                        $('.destop-tip').remove();
                    }

                    // 金钱增长动画
                    try {
                        $('.money').html('0.00').removeClass('hidden');
                        var money = parseFloat(PD.totalMoney).toFixed(2) * 100;
                        var i = 0;
                        var t = money / 50;
                        var time = setInterval(function () {
                            i = i + t;
                            if (i <= money) {
                                var result = (i / 100).toFixed(2);
                                $('.money').html(API.numFormat(result, 2));
                            }
                            else {
                                var result = (money / 100).toFixed(2);
                                $('.money').html(API.numFormat(result, 2));
                                window.clearInterval(time);
                            }
                        }, 12);
                    }
                    catch (e) {
                        $('.money').html(API.numFormat(PD.totalMoney, 2)).removeClass('hidden');
                    }

                    // 有资格参加米禾活动的用户
                    if (PD.showFlow) {
                        showFlow();
                    }
                    else {
                        // 显示活动
                        showActivity();
                    }
                }
            }
        }

        // 突出等级
        function showPoint() {
            if (PD.showPoint) {
                $('.menu-level').addClass('animated zoomInDown');
            }
        }

        // 显示活动
        function showActivity() {
            // #1 钱鹿活动时间显示
            try {
                if (PD.activeTime) {
                    // 红包活动
                    //var $text = $('.active-time');
                    //setInterval(function () {
                    //    PD.activeTime = PD.activeTime - 1000;
                    //    var t = countTime(PD.activeTime);
                    //    $text.removeClass('hidden').html(API.strFormat('{0}天 {1}：{2}：{3}', t[0], t[1], t[2], t[3]));
                    //}, 1000);
                    //$('.active-text').removeClass('hide');

                    //setTimeout(function() {
                    //    Lightbox.show($('#tpl-active').tmpl({}));
                    //    $('#mbox-contain').on('click', function () {
                    //        Lightbox.hide();
                    //        showPoint();
                    //    });
                    //}, 1);

                    // 显示时间
                    var $text = $('.active-time');
                    setInterval(function () {
                        PD.activeTime = PD.activeTime - 1000;
                        var t = countTime(PD.activeTime);
                        $text.removeClass('hidden').html(API.strFormat('{0}天 {1}：{2}：{3}', t[0], t[1], t[2], t[3]));
                    }, 1000);
                    $('.active-text').removeClass('hide');

                    // 粉丝节活动
                    setTimeout(function() {
                        Lightbox.show($('#tpl-active-2').tmpl({}));
                        $('.btn-fan').on('click', function() {
                            //window.location.href = '/invite';
                            Lightbox.hide();
                        });
                        $('#mbox-contain').on('click', function () {
                            Lightbox.hide();
                        });
                    }, 1)
                }
            }
            catch (e) {
            }
        }

        // 显示米禾活动
        function showFlow() {
            if (PD.showFlow > 1) {
                Lightbox.show($('#tpl-flow-finish').tmpl());
                setTimeout(function() {
                    $('#mbox-contain').one('tap', function() {
                        Lightbox.hide();
                        return false;
                    });
                }, 10);
                return false;
            }
            Lightbox.show($('#tpl-flow').tmpl());

            // 关闭
            $('#flow-close').on('tap', function() {
                Lightbox.hide();
                return false;
            });

            // 获取验证码
            $('#flow-code').on('tap', function() {
                var phone = $('input[name=phone]').val().trim(),
                    $self = $(this);

                // 已经点击，返回
                if ($self.data('work') === 1) {
                    return false;
                }

                // 判断手机号码是否合法
                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1'){
                    alert('请输入正确手机的号码')
                    return false;
                }

                // 设置按钮已点击
                $self.data('work', 1).html('正在获取中');

                // 获取验证码
                API.loadData('/code', {
                    method: 'GET',
                    params: { phone: phone },
                    success: function(result) {
                        if(result && !result.c) {
                            alert('请输入您短信接收到的短信验证码');
                            count($self, 60);
                        }
                        else {
                            var msg = '';
                            try{
                                switch(result.c) {
                                    case -3001:
                                        msg = '手机号码无效，请重试';
                                        break;
                                    case -2001:
                                        msg = '验证码无效，请重试';
                                        break;
                                    case -2002:
                                        msg = '验证码错误，请重试';
                                        break;
                                    case -2003:
                                        msg = '发送过于频繁，请三分钟后重试';
                                        break;
                                    case -2004:
                                        msg = '短信发送失败，请重试';
                                        break;
                                    default :
                                        break;
                                }
                            }
                            catch(e) {
                                msg = '发送失败，请重试';
                            }
                            alert(msg);
                            $self.data('work', 0).html('获取验证码');
                        }
                    },
                    error: function() {
                        alert('网络不通畅，请重试');
                        $self.data('work', 0).html('获取验证码');
                    }
                })

            });

            // 提交手机号码
            $('#flow-submit').on('tap', function() {
                var phone = $('input[name=phone]').val().trim(),
                    code = $('input[name=code]').val().trim(),
                    $self = $(this);

                // 已经点击，返回
                if ($self.data('work') === 1) {
                    return false;
                }

                // 判断手机号码是否合法
                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1'){
                    alert('请输入正确手机的号码')
                    return false;
                }

                // 判断验证码
                if(code.length < 1) {
                    alert('请输入短信验证码');
                    return false;
                }

                // 已点击
                $self.data('work', 1).html('正在提交...');

                // 获取验证码
                API.loadData('/phone', {
                    method: 'POST',
                    params: { phone: phone, code: code, type: 1},
                    success: function(result) {
                        if(result && !result.c) {
                            Lightbox.show($('#tpl-flow-notice').tmpl());
                            $('#flow-success').on('tap', function() {
                                window.location.reload(true);
                                return false;
                            });
                        }
                        else {
                            var msg = '';
                            try{
                                switch(result.c) {
                                    case -1002:
                                        msg = '绑定手机号码出现错误\r\n(本活动仅支持电信号码)';
                                        break;

                                    case -2001:
                                        msg = '验证码无效，请重试';
                                        break;

                                    case -2002:
                                        msg = '验证码错误，请重试';
                                        break;

                                    case -3001:
                                        msg = '手机号码已绑定过，请更换其他手机号码';
                                        break;

                                    default :
                                        break;
                                }
                            }
                            catch(e) {
                                msg = '提交失败，请重试';
                            }
                            alert(msg);
                            $self.data('work', 0).html('提交获得10M流量');
                        }
                    },
                    error: function() {
                        alert('绑定手机出现错误，请重试');
                        $self.data('work', 0).html('提交获得10M流量');
                    }
                })
            });


        }
    }

    // 倒计时60s
    function count($btn, n) {
        if (n === 0) {
            $btn.data('work', 0).html('获取验证码');
            return false;
        }
        else {
            $btn.html(n + '秒后重试');
            n = n - 1;
            setTimeout(function() {
                count($btn, n);
            }, 1000);
        }
    }


    // =login 登录页面
    function login() {
        var appUrl= API.strFormat('itms-services://?action=download-manifest&url={0}', PD.appUrl),
            timer = 0,
            firstOnline = 0,
            params = API.getRequest(); // 第一次在线

        // 排行版
        Lightbox.init();
        rank();

        // android
        if(isandroid) {
            if (params['cne'] && params['cne'] == '32') {
                $('#when-jump').removeClass('hide');
            }
            else {
                $('#when-android').removeClass('hide');
            }
            return false;
        }
        else if(isios) { // ios
            $('#when-ios').removeClass('hide');
            _check(); // 首次检查
            setInterval(_check, 2000);
        }
        else { // pc或者其他
            $('#when-pc').removeClass('hide');
            return false;
        }

        events();

        // 从其他平台过来直接安装
        if(params['fromother'] === '1') {
            $('.btn-install').first().trigger('tap');
            params['fromother'] = 0;
            history.pushState({}, '钱鹿', API.getUrl(API.host() + win.location.pathname, params));
        }

        // 事件处理
        function events() {

            //$('#login-page').on('click', function(e) {
            //    return false;
            //})
            $('#login-page').on('tap', function(e) {
                var e = e || window.event,
                    target = e.target,
                    $this = $(target),
                    ck = parseInt( $this.data('ck') || 0 );

                switch (ck) {
                    // [1] 新版开启
                    case 1:
                        if(iswx) { // 是微信浏览器
                            $('.share-box-wx').removeClass("hide");
                            return false;
                        }
                        else if (iswb || isqq) { // 不是safria浏览器
                            $('.share-box-other').removeClass("hide");
                            return false;
                        };

                        if (C.l && !iswx && !iswb && !isqq) { // 助手在线(并且不是微信,微博,qq浏览器)

                            // 升级(包名不一致)
                            if (C.pn != PD.package) {
                                Lightbox.show($('#tpl-install-update').tmpl({}), 1);
                            }
                            // 升级(版本号升级)
                            else if (PD.version > C.v) {
                                Lightbox.show($('#tpl-install-update').tmpl({}), 1);
                            }
                            else { // 登录

                                // 尝试登录
                                tryLogin();
                                //  显示正在登录
                                Lightbox.show($('#tpl-open-doing').tmpl({}), 1);
                            }
                        }
                        else {
                            Lightbox.show($('#tpl-open-tip').tmpl({}), 1);
                            $('#mbox-contain').one('tap', function() {
                                Lightbox.hide();
                            });
                        }

                        //Lightbox.show($('#tpl-action').tmpl({}), 1);
                        return false;
                        break;

                    // [2] 关闭窗口
                    case 2:
                        Lightbox.hide();
                        return false;

                        break;

                    // [3] 安装应用
                    case 3:
                        // $this.html('准备安装<span class="dotting"></span>');
                        // $this.attr('href', appUrl);

                        if(iswx) { // 是微信浏览器
                            $('.share-box-wx').removeClass("hide");
                            return false;
                        }
                        else if (iswb || isqq) { // 不是safria浏览器
                            $('.share-box-other').removeClass("hide");
                            return false;
                        };

                        // 弹出安装页面
                        Lightbox.show($('#tpl-install-progress').tmpl({}), 1);

                        // 安装应用
                        setTimeout(function() {
                            // 安装应用
                            API.doLocation(appUrl);
                        }, 200);

                        // 轮播教程
                        var slider = new Slider({
                            dom: document.querySelector('.install-tips'),
                            touch: 1,
                            auto: 0,
                            time: 3000,
                            speed: 200,
                            dot: 1
                        });

                        // 稍后再轮播
                        setTimeout(function() {
                            slider.setAuto(1);
                        }, 3000);

                        //　安装进度
                        var p = function(n) {
                            $('.prentice').css({width: n + '%'});
                            setTimeout(function() {
                                // 完成安装助手
                                if (n >=100) {
                                    Lightbox.show($('#tpl-install-done').tmpl({}), 1);
                                    return ;
                                }
                                p(n + 0.75);
                            }, 85);
                            return n + 2;
                        }

                        // 开始安装
                        setTimeout(function() {
                            p(0);
                        }, 2200);

                        return false;
                        break;

                    // [４]　旧版开启米鹿
                    case 4:

                        // #2 增加渠道号 媒介链接
                        var url    = '',
                            params = {ssid: PD.ssid, scode: PD.scode, aurl: API.encode(PD.aurl), surl: API.encode(C.surl), cne: PD.cne,
                                    ex: API.encode(JSON.stringify({a: 'a', b: {c: 'c', d: 2}})), uri: '', pkid: '', jpen: 1, an: C.an, nm: C.nm};

                        C.limit = 0;

                        // 如果是小于ios7.1版本，就传uri
                        //if(issafari6 || issafari70) {
                        //    params['uri'] = API.encode(win.location.href);
                        //}
                        // 都传uri
                        params['uri'] = API.encode(win.location.href.split('###')[0]);

                        $this.html('开启中<span class="dotting"></span>（大约15秒）');
                        params['sign'] = API.getSignature(params, 'c239e87f6691e88fd360eba573a05fb0');
                        url = API.getUrl(API.URL.actionLogin, params);

                        setTimeout(function() {
                            API.doLocation(url);
                        }, 300);

                        // 判断是否开始
                        if(!timeLogin) {
                            timeLogin = setInterval(login, 2000);
                        }

                        // 超过时间，重试
                        setTimeout(function() {
                            $this.html('重试（先安装助手）');
                        }, 20000);

                        break;
                    default :
                        return false;
                }

                e.preventDefault();
                e.stopPropagation();
                return false;
            });
        }

        // 排行版
        function rank() {

            // 保留两位小数位
            PD.totalList.forEach(function(item) {
                item['money'] = item['money'].toFixed(2);
            });
            // 总排行榜
            $('.total-list ').html($('#tpl-total-item').tmpl(PD.totalList));

            // 昨日收入排行榜
            var len = PD.dayList.length;
            PD.dayList.forEach(function(item, index, list) {
                if (index % 4 === 0 && len >= index + 4) {
                    $('.yet-list').append($('<li class="box bac bpc pt6 pb6"></li>').html($('#tpl-yet-item').tmpl(list.slice(index, index + 4))));
                }
            });

            // 提款
            $('.money-list').html($('#tpl-withDraw-item').tmpl(PD.withDrawList));
            new Slider({
                dom: document.querySelector('.slider'),
                touch: 0,
                auto: 1,
                time: 5000, // 时间间隔
                speed: 2000 // 滑动速度
            });
        }

        // 检查在线
        function _check() {
            API._s('wywzping', {}, {
                timeout: 2000,
                success: function(data) {
                    if (!data.c) { // 在线
                        C.pn = data.d;
                        C.v  = data.msg;
                        C.l  = 1;
                        firstOnline++;
                        if (firstOnline === 1) { // 第一次在线
                            // 升级(包名不一致)
                            if (C.pn != PD.package) {
                                Lightbox.show($('#tpl-install-update').tmpl({}), 1);
                            }
                            // 升级(版本号升级)
                            else if (PD.version > C.v) {
                                Lightbox.show($('#tpl-install-update').tmpl({}), 1);
                            }
                            else { // 登录
                                // 尝试登录
                                tryLogin();
                            }
                        }
                        $('.btn-open').removeClass('btn-dark').addClass('btn-secondary').html('开启赚钱之旅');
                        if ($('.panel-open').length > 0 || $('.panel-done').length > 0) {
                            setTimeout(function() {
                                $('#mbox-contain').off('tap');
                                Lightbox.hide();
                            }, 1000);
                        }
                    }
                    else { // 助手出错
                        C.l  = 0;
                        firstOnline = 0;
                        $('.btn-open').removeClass('btn-secondary').addClass('btn-dark').html('开启赚钱之旅<span class="fs-12" data-ck="1">(钱鹿助手未打开)</span>');
                    }
                },
                error: function() {
                    C.l  = 0;
                    firstOnline = 0;
                    $('.btn-open').removeClass('btn-secondary').addClass('btn-dark').html('开启赚钱之旅<span class="fs-12" data-ck="1">(钱鹿助手未打开)</span>');
                }
            });
        }

        // 尝试登录
        function tryLogin() {
            // #2 增加渠道号 媒介链接
            var url    = '',
                params = {ssid: PD.ssid, scode: PD.scode, aurl: PD.aurl, surl: C.surl, cne: PD.cne,
                    ex: JSON.stringify({a: 'a', b: {c: 'c', d: 2}}), uri: '', pkid: '', jpen: 1, an: C.an, nm: C.nm};

            // 如果是微信微博qq　不自动登录
            if (iswx || iswb || isqq) return false;
            // 尝试登录
            API._s('wywzlo', params, {
                timeout: 20000,
                success: function(data) {
                    if (!data.c) {
                        window.location.reload(true);
                    }
                    else {
                        var msg = data.msg;
                        if (msg.indexOf('3211') >= 0) {
                            msg = '越狱设备不能使用钱鹿哦';
                        }
                        else if (msg.indexOf('3214') >=0) {
                            msg = '您的设备有违规操作记录,无法正常使用。';
                        }
                        else if (msg.indexOf('3215') >=0) {
                            msg = '您的设备有违规操作记录,无法正常使用！';
                        }
                        else if (msg.indexOf('3216') >=0) {
                            msg = '您的设备有违规操作记录,无法正常使用～';
                        }

                        Lightbox.show($('#tpl-alert').tmpl({msg: '登录失败' + '，错误信息:<br>'  + msg}), 1);
                        $('#mbox-contain').one('tap', function() {
                            Lightbox.hide();
                        });
                    }
                },
                error: function(status) {
                    if (status == 'timeout') {
                        Lightbox.show($('#tpl-alert').tmpl({msg: '登录失败' + '，错误信息:<br> 网络连接超时，请重新刷新页面；'}), 1);
                        $('#mbox-contain').one('tap', function() {
                            Lightbox.hide();
                        });
                    }
                    else {
                        Lightbox.show($('#tpl-alert').tmpl({msg: '登录失败' + '，错误信息:<br> 通信出错，请重试'}), 1);
                        $('#mbox-contain').one('tap', function() {
                            Lightbox.hide();
                        });
                    }
                }
            });
        }

        // 循环登录
        function login() {
            if(C.limit > 15) {
                return false;
            }
            C.limit++ ;
            API.loadData(API.strFormat('/islogin?t={0}', new Date().getTime()), {
                success: function(data) {
                    if(data && data['c'] === 0) {
                        window.location.reload();
                    }
                },
                error: function() {
                }
            });
        }
    }


    // =update 更新页面
    function update() {
        var appUrl= API.strFormat('itms-services://?action=download-manifest&url={0}', PD.appUrl);

        Lightbox.init();
        events();

        // 事件处理
        function events() {

            //$('#login-page').on('click', function(e) {
            //    return false;
            //});
            $('#login-page').on('tap', function(e) {
                var e = e || window.event,
                    target = e.target,
                    $this = $(target),
                    ck = parseInt( $this.data('ck') || 0 );

                switch (ck) {
                    // [1] 打开提示窗
                    case 1:
                        if(iswx) { // 是微信浏览器
                            $('.share-box-wx').removeClass("hide");
                            return false;
                        }
                        else if (!issafari) { // 不是safria浏览器
                            $('.share-box-other').removeClass("hide");
                            return false;
                        };
                        Lightbox.show($('#tpl-action').tmpl({}), 1);
                        return false;

                        break;

                    // [2] 关闭窗口
                    case 2:
                        Lightbox.hide();
                        return false;

                        break;

                    // [3] 升级
                    case 3:
                        $this.attr('href', appUrl).html('准备升级<span class="dotting"></span>');

                        setTimeout(function() {
                            Lightbox.hide();
                            Lightbox.show($('#tpl-install').tmpl({}), 1);
                            // 7秒后才能点击开启
                            setTimeout(function() {
                                $('.lazy-open-btn').removeClass('btn-disabled');
                            }, 7000);
                        }, 5000);

                        return true;
                        break;

                    case 4:
                        var url    = '',
                            // Todo
                            // 暂时传aurl nm 为空
                            params = {ssid: PD.ssid, scode: PD.scode, aurl: API.encode(PD.aurl),  surl: API.encode(C.surl), cne: PD.cne,
                                ex: API.encode(JSON.stringify({a: 'a', b: {c: 'c', d: 2}})), uri: '', pkid: '', jpen: 1, an: C.an, nm: C.nm};

                        C.limit = 0;

                        // 如果是小于ios7.1版本，就传uri
                        //if(issafari6 || issafari70) {
                        //    params['uri'] = API.encode(win.location.href);
                        //}
                        // 都传uri
                        params['uri'] = API.encode(win.location.href.split('###')[0]);

                        $this.html('开启中<span class="dotting"></span>（大约15秒）');
                        params['sign'] = API.getSignature(params, 'c239e87f6691e88fd360eba573a05fb0'),
                        url = API.getUrl(API.URL.actionLogin, params);

                        setTimeout(function() {
                            API.doLocation(url);
                        }, 300);

                        // 判断是否开始
                        if(!timeLogin) {
                            // 循环登录
                            timeLogin = setInterval(login, 2000);
                        }

                        // 超过时间，重试
                        setTimeout(function() {
                            $this.html('重试（先升级助手）');
                        }, 20000);

                        break;
                    default :
                        return true;
                }

                e.preventDefault();
                e.stopPropagation();
                return false;
            });
        }

        // 循环登录
        function login() {
            if(C.limit > 15) {
                return false;
            }
            C.limit++ ;
            API.loadData(API.strFormat('/islogin?t={0}', new Date().getTime()), {
                success: function(data) {
                    if(data && data['c'] === 0) {
                        window.location.reload();
                    }
                },
                error: function() {
                }
            });
        }

    }


    // =detail 详细页面
    function detail() {

        build();
        events();

        // 构建
        function build() {
            if(!PD.all) {
                $('.page-all').html($('#tpl-all').tmpl({}));
            }
            if(!PD.task) {
                $('.page-task').html($('#tpl-task').tmpl({}));
            }
            if(!PD.prentice) {
                $('.page-prentice').html($('#tpl-prentice').tmpl({}));
            }
            if(!PD.exchange) {
                $('.page-exchange').html($('#tpl-exchange').tmpl({}));
            }
        }

        // 事件
        function events() {

            $('.ui-page .btn-action').on('tap', function() {
                var $this = $(this),
                    type = parseInt($this.data('action'));

                switch(type) {
                    case 2:
                        $this.attr('href', '/task');
                    default:
                        return true;
                }

            });

            $('.menu li').on('tap', function() {
                var $this = $(this),
                    index = parseInt($this.data('index'));

                $('.menu li').removeClass('on');
                $this.addClass('on');

                door(index);
            });
        }

        /**
         *  =door
         *  @about    切换内容屏处理
         *
         *  @param    {number}  t  类型
         *  @param    {string}  m  内容
         */
        function door(t, m) {
            var $target = $(".ui-page");

            switch(t) {
                case 0: // #all
                    $target.pages("all", function($t) {
                        // $t.find(".ui-content").html(m);
                    });
                    break;
                case 1: // #task
                    $target.pages("task", 0, function() {
                    });
                    break;
                case 2: // #prentice
                    $target.pages("prentice", function($t) {
                    }, function() {
                        // win.scrollTo(0, 1);
                    });
                    break;
                case 3:
                    $target.pages("exchange", 0, function() {
                    });
                    break;
                default:
                    break;
            }
        }
    }


    // =prentice 收徒页面
    function prentice() {
        //  点击分享按钮
        //$('.btn-invite').on('click', function(e) {
        //    return false;
        //});
        $('.btn-invite').on('tap', function() {
            var url = API.URL.actionShare,
                title = API.encode('钱鹿带你飞，立拿3元，月入上千'),
                desc = API.encode('有钱鹿当助手，有钱路任你走。红包都快抢完了，你还等什么？点击领取。'),
                icon = API.encode('http://w.qiandeer.com/qd/static/images/icon_default.png'),
                params = {uid: uid, purl: purl ,title: title, desc: desc, icon: icon, uri: '', pkid: '', jpen: 1, shurl: shurl};

            // 如果是小于ios7.1版本，就传uri
            if(issafari && !issafari8) {
                params['uri'] = API.encode(win.location.href.split('###')[0]);
            }

            params['sign'] = API.getSignature(params, 'c239e87f6691e88fd360eba573a05fb0'),
                url = API.getUrl(API.URL.actionShare, params);
            API.doLocation(url);

            //try{
            //
            //    var _checkShare = function() {
            //        var params = {k: 'prentice', v: '', t: '', ac: 1}
            //        API._s('wywzkv', params, {
            //            timeout: 2000,
            //            success: function(data) {
            //                alert(JSON.stringify(data));
            //                try{
            //                    var a = JSON.parse(data.d);
            //                }
            //                catch(e) {alert(e);}
            //                if (!data.c) { // 在线
            //                }
            //                else { // 助手出错
            //                }
            //            },
            //            error: function() {
            //                alert('error');
            //            }
            //        });
            //    }
            //
            //    setInterval(_checkShare, 5000);
            //}
            //catch(e){alert(e);}

            return false;
        });


        //if (C.act) {
        //    $('.active-banner').removeClass('hide');
        //    try {
        //        // #1 钱鹿活动时间显示
        //        var $text = $('.active-time');
        //        setInterval(function() {
        //            activeTime = activeTime - 1000;
        //            var t = countTime(activeTime);
        //            $text.html(API.strFormat('{0}天{1}：{2}：{3}', t[0], t[1], t[2], t[3]));
        //        }, 1000)
        //    }
        //    catch(e) {
        //    }
        //}
    }


    // =feedback 反馈页面
    function feedback() {

        Lightbox.init();
        events();

        // 事件
        function events() {

            API.funTransitionHeight(doc.querySelector('.fb-task'), 300);

            // 监控类型改变
            $('input[name=type]').on('change', function() {
                var $this = $(this),
                    value = parseInt($this.attr('value'));

                if(value === 1) {
                    API.funTransitionHeight(doc.querySelector('.fb-task'), 300);
                    //$('.fb-task').removeClass('hide');
                }
                else {
                    $('.fb-task').css({'height': 0, 'opacity': 0});
                    //$('.fb-task').addClass('hide');
                }
            });

            function isDigit(s)
            {
                var patrn=/^[0-9]{1,20}$/;
                if (!patrn.exec(s)) return false
                return true
            }

            // 提交
            $('.btn-upload').on('click', function() {
                var type = parseInt($('input[name=type]:checked').attr('value')),
                    task = $('input[name=task]').val(),
                    desc = $('textarea[name=desc]').val(),
                    qq = $('input[name=qq]').val();

                if(type === 1 && task.length < 1) {
                    API.alert('请输入您要反馈的应用的名字');
                    return false;
                }
                if(desc.length < 1) {
                    API.alert('请输入您要反馈的描述');
                    return false;
                }
                if (qq.length != 0 && !isDigit(qq)) {
                    API.alert('请输入正确的QQ号码');
                    return false;
                }

                var $btn = $(this).button('loading');

                API.loadData('/feedback', {
                    method: 'POST',
                    params: {type: type, task: task, desc: desc, qq: qq},
                    success: function(result) {
                        if(result && !result.c) {
                            Lightbox.show($('#tpl-success').tmpl({}), 1);
                            $('.btn-reload').on('click', function() {
                                window.location.href='/config';
                            });
                        }
                        else {
                            Lightbox.show($('#tpl-fail').tmpl({msg: '提交服务器出错，请重试'}), 1);
                            $('.btn-close').off().on('click', function() {
                                Lightbox.hide();
                            });
                        }
                        $btn.button('reset');
                    },
                    error: function() {
                        Lightbox.show($('#tpl-fail').tmpl({msg: '网络阻塞，请重试'}), 1);
                        $('.btn-close').off().on('click', function() {
                            Lightbox.hide();
                        });
                        $btn.button('reset');
                    }
                });

                return false;
            });
        }

    }


    // =info 信息页面
    function info() {

        var params = API.getRequest();

        build();
        events();

        // 构建
        function build() {
            var d = new Date();

            if (params['task']) { // 如果是从新手任务过来，就返回新手任务
                $('.toolbar .ctr-left a').attr('href', '/task/teach');
                $('.task-tip').removeClass('hide');
            }

            Lightbox.init();

            try{
                $('input[name=username]').val(PD.username);
                $('input[name=place]').val(PD.place);

                if (PD.birth) {
                    // 生日
                    d.setTime(parseInt(PD.birth));
                    $('input[name=birth]').val(d.Format('yyyy-MM-dd'));
                    $('.birth-text').html($('input[name=birth]').val());
                }

                // 职业
                var options = [];
                PD.works.forEach(function(item) {
                    var $option = {};
                    if (item === PD.work) {
                        $option = '<option selected value="' + item + '">' + item + '</option>';
                        $('.work-text').html(item);
                    }
                    else {
                        $option = '<option value="' + item + '">' + item + '</option>';
                    }
                    options.push($option);
                });
                var $work = $('#work');
                options.forEach(function(item) {
                    $work.append(item);
                });

                if(PD.sex === 1 ) {
                    $('input[name=sex]').first().prop('checked', true);
                }
                else {
                    $('input[name=sex]').last().prop('checked', true);
                }
                $('.avatar').attr('src', PD.icon);
            }
            catch(e) {
            }
        }

        // 事件
        function events() {
            $('#btn-update').on('click',function(e) {
                var username = $('input[name=username]').val().trim(),
                    sex = $('input[name=sex]:checked').attr('value'),
                    birth = $('input[name=birth]').val(),
                    work = $('select[name=work]').val();


                if (username.length < 1) {
                    API.alert('请输入您的名字');
                    return false;
                }

                if (birth.length < 1) {
                    API.alert('请输入您的生日');
                    return false;
                }
                else {
                    birth = new Date(birth).getTime();
                }

                if (work.length < 1) {
                    API.alert('请输入您的职业');
                    return false;
                }

                var $btn = $(this).button('loading');

                try{
                    var task = params['task'] ? 1 : 0;
                    API.loadData('/info', {
                        method: 'POST',
                        params: {username: username, sex: sex, birth: birth, work: work, task: task},
                        success: function(result) {
                            if(result && !result.c) {
                                if (task) {
                                    API.alert('完成新手任务：信息填写<br/> 获得奖励', function () {
                                        window.location.href='/task/teach';
                                    })
                                }
                                else {
                                    API.alert('成功修改信息', function () {
                                        window.location.href = '/config';
                                    });
                                }
                            }
                            else {
                                API.alert('哎呀，服务器出错了，请重试修改信息');
                            }
                            $btn.button('reset');
                        },
                        error: function() {
                            API.alert('哎呀，网络不通畅， 请重试修改信息');
                            $btn.button('reset');
                        }
                    })
                }
                catch(e) {alert(e);}
                return false;
            });

            $('input[name="birth"]').on('change', function() {
                var $this = $(this);
                $('.birth-text').html($this.val());
            });

            $('#work').on('change', function() {
                var $this = $(this);
                $('.work-text').html($this.val());
            });

            $('input[type=file]').on('change', function(e) {
                var file = e.target.files[0],
                    reader = new FileReader(),
                    imagefile = file.type,
                    match = ['image/jpeg', "image/png", "image/jpg"];

                // 判断文件类型
                if( !((imagefile == match[0]) || (imagefile == match[1]) || (imagefile == match[2])) ) {
                    API.alert('哎呀，您上传的图片不符合要求，请重新上传');
                    return false;
                }

                // 限制上传小于1m
                if(file.size && file.size > 1 *1024 *1024) {
                    API.alert('哎呀，您上传的图片超过1M，请重新上传');
                    return false;
                }

                if(typeof reader.readAsDataURL === 'function') {
                    // 读取文件
                    reader.readAsDataURL(file);
                    reader.onload = function(e) {
                        $('.upload-image').attr('src', this.result);
                    };
                }
                else {
                    $('form').get(0).submit();
                    // $('.upload-image').attr('src', this.result);
                }
                Lightbox.show($('#tpl-image').tmpl({}));
                $('.btn-upload').on('click', function() {
                    $('form').get(0).submit();
                    return false;
                });
                $('.btn-close').off().on('click', function() {
                    Lightbox.hide();
                    return false;
                });
            });
        }

    }


    // =phone 绑定手机页面
    function phone() {

        Lightbox.init();
        build();
        events();

        // 构建
        function build() {
            if (PD.phone) {
                $('.ui-page').eq(1).addClass('ui-page-active').html($('#tpl-switch').tmpl({phone: PD.phone ? PD.phone: '未知'}));
            }
            else {
                $('.ui-page').eq(0).addClass('ui-page-active');
            }

        }

        // 事件
        function events() {

            // 获取短信验证码
            $('#get-code').on('click', function () {
                var phone = $('input[name=phone]').val().trim(),
                    $self = $(this);

                // 已经点击，返回
                if ($self.data('work') === 1) {
                    return false;
                }

                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1'){
                    API.alert('请输入正确手机的号码')
                    return false;
                }

                $self.data('work', 1).html('正在获取中');

                API.loadData('/code', {
                    method: 'POST',
                    params: { phone: phone },
                    success: function(result) {
                        if(result && !result.c) {
                            API.alert('请输入您短信接收到的短信验证码');
                            count($self, 60);
                        }
                        else {
                            var msg = '';
                            try{
                                switch(result.c) {
                                    case -3001:
                                        msg = '手机号码无效，请重试';
                                        break;
                                    case -2001:
                                        msg = '验证码无效，请重试';
                                        break;
                                    case -2002:
                                        msg = '验证码错误，请重试';
                                        break;
                                    case -2003:
                                        msg = '发送过于频繁，请三分钟后重试';
                                        break;
                                    case -2004:
                                        msg = '短信发送失败，请重试';
                                        break;
                                    default :
                                        break;
                                }
                            }
                            catch(e) {
                                msg = '发送失败，请重试';
                            }
                            API.alert(msg);
                            $self.data('work', 0).html('获取验证码');
                        }
                    },
                    error: function() {
                        API.alert('网络不通畅，请重试');
                        $self.data('work', 0).html('获取验证码');
                    }
                })
            });


            // 提交
            $('#upload-info').on('click', function(e) {

                var phone = $('input[name=phone]').val().trim(),
                    code = $('input[name=code]').val().trim();

                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1') {
                    API.alert('请输入正确手机的号码')
                    return false;
                }

                if(code.length < 1) {
                    API.alert('请输入短信验证码');
                    return false;
                }

                var $btn = $(this).button('loading');

                API.loadData('/phone', {
                    method: 'POST',
                    params: {phone: phone, code: code},
                    success: function(result) {
                        if(result && !result.c) {
                            API.alert('绑定手机成功', function() {
                                window.location.href = '/config';
                            });
                        }
                        else {
                            var msg = '绑定手机出错，请重试';
                            try{
                                switch(result.c) {
                                    case -2001:
                                        msg = '验证码无效，请重试';
                                        break;
                                    case -2002:
                                        msg = '验证码错误，请重试';
                                        break;
                                    default :
                                        break;
                                }
                            }
                            catch(e) {
                                msg = '提交失败，请重试';
                            }
                            API.alert(msg);
                        }
                        $btn.button('reset');
                    },
                    error: function() {
                        API.alert('绑定手机出现错误，请重试');
                        $btn.button('reset');
                    }
                })

                return false;
            });
        }

    }


    // =switchPhone 更换手机号码
    function switchPhone() {

        var progress = 0; // 进度
        Lightbox.init();
        build();
        events();

        // 构建
        function build() {

            if (PD.phone) {
                // 默认手机号码
                $('input[name=oldphone]').val(PD.phone);
            }
            else {
                // 跳到第二个状态
                $('.menu li').eq(1).addClass('on');
                tab('.ui-panel', 1);
                progress = 1; //标记进入绑定新手的流程
            }
        }

        // 事件
        function events() {

            // 获取短信验证码
            $('.get-code').on('click', function () {
                var phone = progress ? $('input[name=newphone]').val().trim() : $('input[name=oldphone]').val().trim(),
                    $self = $(this);

                // 已经点击，返回
                if ($self.data('work') === 1) {
                    return false;
                }

                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1'){
                    API.alert('请输入正确手机的号码')
                    return false;
                }

                $self.data('work', 1).html('正在获取中');

                // 获取短信验证码
                API.loadData('/code', {
                    method: 'POST',
                    params: { phone: phone },
                    success: function(result) {
                        if(result && !result.c) {
                            API.alert('请输入您短信接收到的短信验证码');
                            count($self, 60);
                        }
                        else {
                            var msg = '';
                            try{
                                switch(result.c) {
                                    case -3001:
                                        msg = '手机号码无效，请重试';
                                        break;
                                    case -2001:
                                        msg = '验证码无效，请重试';
                                        break;
                                    case -2002:
                                        msg = '验证码错误，请重试';
                                        break;
                                    case -2003:
                                        msg = '发送过于频繁，请三分钟后重试';
                                        break;
                                    case -2004:
                                        msg = '短信发送失败，请重试';
                                        break;
                                    default :
                                        break;
                                }
                            }
                            catch(e) {
                                msg = '发送失败，请重试';
                            }
                            API.alert(msg);
                            $self.data('work', 0).html('获取验证码');
                        }
                    },
                    error: function() {
                        API.alert('网络不通畅，请重试');
                        $self.data('work', 0).html('获取验证码');
                    }
                });
            });


            $('.upload-info').on('click', function(e) {

                var phone = progress ? $('input[name=newphone]').val().trim() : $('input[name=oldphone]').val().trim(),
                    code = progress ? $('input[name=newcode]').val().trim() : $('input[name=oldcode]').val().trim();

                if(!/^\d+$/.test(phone) || phone.length != 11 || phone.charAt(0) != '1') {
                    API.alert('请输入正确手机的号码')
                    return false;
                }

                if(code.length < 1) {
                    API.alert('请输入短信验证码');
                    return false;
                }

                var $btn = $(this).button('loading');

                // 处理第一阶段，解绑阶段
                if (!progress) {
                    API.loadData('/phone/unlock', {
                        method: 'POST',
                        params: {phone: phone, code: code},
                        success: function (result) {
                            if (result && !result.c) {
                                $('.menu li').eq(1).addClass('on');
                                tab('.ui-panel', 1);
                                progress = 1; //标记进入绑定新手的流程
                                API.alert('解绑旧手机号码成功,请绑定新手机号码', function () {
                                });
                            }
                            else {
                                var msg = '解绑旧手机出错，请重试';
                                try {
                                    switch (result.c) {
                                        case -2001:
                                            msg = '验证码无效，请重试';
                                            break;
                                        case -2002:
                                            msg = '验证码错误，请重试';
                                            break;
                                        default :
                                            break;
                                    }
                                }
                                catch (e) {
                                    msg = '提交失败，请重试';
                                }
                                API.alert(msg);
                            }
                            $btn.button('reset');
                        },
                        error: function () {
                            API.alert('解绑旧手机出现错误，请重试');
                            $btn.button('reset');
                        }
                    });
                }
                else { //重新绑定
                    API.loadData('/phone', {
                        method: 'POST',
                        params: {phone: phone, code: code},
                        success: function (result) {
                            if (result && !result.c) {
                                $('.menu li').eq(2).addClass('on');
                                API.alert('绑定新手机号码成功', function () {
                                    tab('.ui-panel', 2);
                                    setTimeout(function() {
                                        window.location.href = '/phone';
                                    }, 2000);
                                });
                            }
                            else {
                                var msg = '绑定手机出错，请重试';
                                try {
                                    switch (result.c) {
                                        case -2001:
                                            msg = '验证码无效，请重试';
                                            break;
                                        case -2002:
                                            msg = '验证码错误，请重试';
                                            break;
                                        default :
                                            break;
                                    }
                                }
                                catch (e) {
                                    msg = '提交失败，请重试';
                                }
                                API.alert(msg);
                            }
                            $btn.button('reset');
                        },
                        error: function () {
                            API.alert('绑定手机出现错误，请重试');
                            $btn.button('reset');
                        }
                    })
                }

                return false;
            });
        }

    }


    // 切换tab
    function tab(el, index) {
        $(el).each(function(i) {
            var $this = $(this),
                num = $this.data('index');

            if ($this.hasClass('hide')) {
                if (num === index) {
                    $this.removeClass('hide').addClass('fade in');
                    setTimeout(function() {
                        $this.removeClass('fade in');
                    }, 225);
                }
            }
            else  {
                if (num !== index) {
                    $this.addClass('hide').removeClass('fade out');
                    //$this.addClass('fade out');
                    //setTimeout(function() {
                    //    $this.addClass('hide').removeClass('fade out');
                    //}, 125);
                }
            }
        });
    }


    // =union 联盟任务
    function union() {
        var $duo = $('#task-duo'),
            $wan = $('#task-wan'),
            $zhi = $('#task-zhi'),
            $mi = $('#task-mi'),
            $ju = $('#task-ju');

        $duo.attr('href', API.getUrlSignature(API.URL.actionUnion, {lmid: 'dm', uri: '', pkid: '', jpen: 1}, 'c239e87f6691e88fd360eba573a05fb0'));
        $wan.attr('href', API.getUrlSignature(API.URL.actionUnion, {lmid: 'wp', uri: '', pkid: '', jpen: 1}, 'c239e87f6691e88fd360eba573a05fb0'));
        $zhi.attr('href', API.getUrlSignature(API.URL.actionUnion, {lmid: 'zm', uri: '', pkid: '', jpen: 1}, 'c239e87f6691e88fd360eba573a05fb0'));
        $mi.attr('href', API.getUrlSignature(API.URL.actionUnion, {lmid: 'ym', uri: '', pkid: '', jpen: 1}, 'c239e87f6691e88fd360eba573a05fb0'));
        $ju.attr('href', API.getUrlSignature(API.URL.actionUnion, {lmid: 'zsl', uri: '', pkid: '', jpen: 1}, 'c239e87f6691e88fd360eba573a05fb0'));
    }


    // =taskVideo
    function taskVideo() {

        // 构建
        build();
        events();

        function build() {
            $('.video-space').append($('#tpl-video').tmpl({src: PD.src}));
        }

        function events() {
            var videoPlayer = $('#video-player');

            videoPlayer.on('click', function (e) {
                var $this = $(this),
                    status = parseInt($this.data('status'));

                if(!this.paused) {
                }
                else {
                }
                e.stopPropagation();
            }).on('timeupdate', function(event) {
            }).on('paused', function() {
            }).on('progress', function() {
            }).on('ended', function(event) {
                API.loadData('/task/video', {
                    method: 'POST',
                    params: '',
                    success: function(result) {
                        if(result && !result.c) {
                            try{
                                alert('成功观看视频，请继续分享');
                            }
                            catch (e) {
                                alert(e);
                            }
                        }
                        else {
                            //API.alert('哎呀，服务器出错了，请重试修改信息');
                        }
                    },
                    error: function() {
                        //API.alert('哎呀，网络不通畅， 请重试修改信息');
                    }
                })
            });

            $('.btn-share').on('click', function() {
                var url = API.URL.actionShare,
                    title = API.encode('钱鹿带你飞，立拿3元，月入上千'),
                    desc = API.encode('有钱鹿当助手，有钱路任你走。红包都快抢完了，你还等什么？点击领取。'),
                    icon = API.encode('http://w.qiandeer.com/qd/static/images/icon_default.png'),
                    params = {uid: PD.uid, purl: PD.purl ,title: title, desc: desc, icon: icon, uri: '', pkid: '', jpen: 1, shurl: PD.shurl};

                // 如果是小于ios7.1版本，就传uri
                if(issafari && !issafari8) {
                    params['uri'] = API.encode(win.location.href.split('###')[0]);
                }

                params['sign'] = API.getSignature(params, 'c239e87f6691e88fd360eba573a05fb0'),
                    url = API.getUrl(API.URL.actionShare, params);
                API.doLocation(url);
                return false;
            });
        }
    }


    /**
     *  =countTime
     *
     *  @about      计算剩余时间
     *
     *  @param      {time}      activeTime
     *  @return     {array}     时间
     */
    function countTime(activeTime) {

        if (activeTime < 1) {
            return ['00', '00', '00', '00'];
        }
        else {
            var d = 0, h = 0, m = 0, s = Math.ceil(activeTime / 1000, 0);
            if (s >= 86400) {
                d = Math.floor(s/86400);
                s = s%86400;
            }
            if (s >= 3600) {
                h = Math.floor(s/3600);
                s = s%3600;
            }
            if (s >= 60){
                m = Math.floor(s/60);
                s = s%60;
            }
            return [d < 10 ? '0' + d : d, h < 10 ? '0' + h : h, m < 10 ? '0' + m : m, s < 10 ? '0' + s : s];
        }
    }


    /** 公有属性&方法
     -----------------------------------------------------------------*/
    Lists = {
        /**
         *  =start
         *  @about    启动器
         */
        start: function(module) {
            if(module) {
                // support hover
                document.addEventListener("touchstart", function(){}, true);
                init(module);
            }
        }

    };

    QL.Main = Lists;




})(window, document, Zepto, QL);
