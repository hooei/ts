/**
 *  Created by zejie on 15-1-8.
 *  通用方法api
 -----------
 */
var API = (function (win, doc, $) {

    /** 私有属性
     -----------------------------------------------------------------*/

    var URL_ = {
        actionLogin: 'qdeer9dirkt8gk59gk://wywzlo',
        actionShare: 'qdeer9dirkt8gk59gk://wywzshare',
        actionUnion: 'qdeer9dirkt8gk59gk://lmpp'
    },


    /** 公有属性&方法
     -----------------------------------------------------------------*/
    API = {

        URL: {
            actionLogin: URL_.actionLogin,
            actionShare: URL_.actionShare,
            actionUnion: URL_.actionUnion
        },


        /* =host  获取当前host */
        host: function () {
            return win.location.protocol + "//" + win.location.host;
        },


        port       :  46115,       // HTTP 服务器端口
        ports      :  [            // #23  端口组合
            ['46115', '46213', '46249', '46290'],
        ],


        /**
         *  =loadData   获取数据
         *
         *  @param    {string}  url
         *  @param    {object}    opts
         */
        loadData: function (url, opts) {
            var options = {
                timeout: 30000,
                params: '',
                method: 'GET',
                success: function () {
                },
                error: function () {
                }
            };

            $.extend(options, opts);

            $.ajax({
                url: url,
                data: options.params,
                dataType: 'json',
                type: options.method,
                crossDomain: true,
                xhrFields: {
                    withCredentials: true
                },
                timeout: 8000, // 8秒超时
                success: function (data, status, xhr) {
                    // 请求成功处理
                    options.success(data);
                },
                error: function (xhr, status, error) {
                    // 请求接口失败
                    options.error(status);
                }
            });
        },


        // 跨域，由服务器load资源
        proxy: function (selfUrl, opts) {
            var options = {
                timeout: 30000,
                url: opts.url,
                methond: opts.method,
                success: function () {
                },
                error: function () {
                }
            }
            $.extend(options, opts);
            $.ajax({
                url: API.getUrl(selfUrl, {'url': options.url, method: options.method}),
                data: options.params,
                dataType: 'json',
                crossDomain: true,
                // xhrFields: {
                //     withCredentials: true
                // },
                timeout: 8000, // 8秒超时
                success: function (data, status, xhr) {
                    // 请求接口成功
                    var back = data || {c: 1};

                    // 请求成功处理
                    options.success(back);
                },
                error: function (xhr, status, error) {
                    console.log('proxy' + $.stringifyJSON(error));
                    // 请求接口失败
                    options.error(status);
                }
            });
        },


        /**
         *  =sdk
         *  @about    调用本地 HTTP 接口
         *
         *  @param    {string}    at        接口类型
         *  @param    {json}      params    请求二级参数
         *  @param    {function}  suc       请求成功处理（异步）
         *  @param    {function}  err       请求错误处理（异步）
         *  @param    {string}    url
         *  @param    {number}    timeout
         */
        _s: function(at, params, opts) {
            var options = {
                url      :  'http://127.0.0.1:{0}/{1}',
                timeout  :  15000,  // 默认15秒超时
                success  :  function() {},
                error    :  function() {}
            };

            $.extend(options, opts);

            // 处理参数签名
            if (!this.isEmpty(params))
                params['sign'] = this.getEncodeSignature(params, "c239e87f6691e88fd360eba573a05fb0");

            $.ajax({
                //async         :  false,
                url           :  this.strFormat(options.url, this.port, at),
                data          :  params,
                dataType      :  'jsonp',
                jsonp         :  'callback',
                headers       :  {
                    "Origin"  :  API.host()
                },
                timeout       :  options.timeout, // 4?秒超时
                success       :  function(data, status, xhr) {
                    // 请求接口成功
                    var back = data || { c: 1 };

                    // 请求成功处理
                    options.success(back);
                },
                error         :  function(xhr, status, error) {
                    // 请求接口失败
                    options.error(status);
                }
            });
        },


        /**
         *  =_t
         *  @about    统计封装
         *
         *  @param    {string}    category       分类
         *  @param    {string}    action         操作
         *  @param    {string}    label          信息
         *  @param    {string}    value          数值
         */
        _t: function(category, action, label, value) {
            var category = category || '',
                action = action || '',
                label = label || '',
                value = value || '';

            this._baidu(category, action, label, value);
        },


        /**
         *  =_baidu
         *  @about    百度统计
         *
         *  @param    {string}    category       分类
         *  @param    {string}    action         操作
         *  @param    {string}    label          信息
         *  @param    {string}    value          数值
         */
        _baidu: function(c, a, l, v) {
            var _hmt = _hmt || [];

            _hmt.push(['_trackEvent', c, a, l, v]);
        },


        /**
         *  =setData  数据本地存储
         *
         *  @param    {string}   key
         *  @param    {all}      value
         */
        setData: function (key, value) {
            if ($.isArray(value) || $.isPlainObject(value))
                value = $.stringifyJSON(value);

            if ($("#data-" + key).length) {
                $("#data-" + key).html(value);
            }
            else {
                $(API.strFormat('<code id="data-{0}" style="display:none;">{1}</code>',
                    key, value)).appendTo('body');
            }
            return 1;
        },


        /**
         *  =setLocal  数据本地存储, localstorage
         *
         *  @param    {string}   key
         *  @param    {object}      value
         */
        setLocal: function (key, value) {
            if ($.isArray(value) || $.isPlainObject(value))
                value = $.stringifyJSON(value);

            try {
                window.localStorage.setItem(key, value);
                return 1;
            }
            catch (err) {
                return 0;
            }
        },


        /**
         *  =removeLocal  数据本地存储, localstorage
         *
         *  @param    {string}   key
         *  @param    {all}      value
         */
        removeLocal: function (key) {

            try {
                window.localStorage.removeItem(key);
                return 1;
            }
            catch (err) {
                return 0;
            }
        },


        /**
         *  =clearLocal  数据本地存储, localstorage
         *
         *  @param    {string}   key
         *  @param    {all}      value
         */
        clearLocal: function () {

            try {
                window.localStorage.clearItem();
                return 1;
            }
            catch (err) {
                return 0;
            }
        },


        /**
         *  =getLocal  数据本地存储 localstorage
         *
         *  @param    {string}   key
         *  @param    {object}      value 是否转为字符串
         */
        getLocal: function (key, value) {
            var back = window.localStorage.getItem(key);


            if ($.isArray(value) || $.isPlainObject(value))
                value = $.stringifyJSON(value);

            return value ? JSON.parse(back) : back;
        },


        /**
         *  =getData  获取本地存储
         *
         *  @param    {string}   key
         *  @param    {boolean}  hl   是否处理数据
         *  @return    {json/string}  缓存数据
         */
        getData: function (key, hl) {
            hl = hl || 0;

            var value = $("#data-" + key).html();

            if (value) {
                return hl ? $.parseJSON(value) : value;
            }
            return null;
        },


        /**
         *  =get request  获取url参数集合
         *
         *  @param     {string}  param name
         *  @return    {object}  参数集合
         */
        getRequest: function () {
            var url = win.location.search,  // 获取url中"?"后面的字符串
                i = 0,
                args, arg,
                back = new Object();

            if (url == '') return 0;

            if (url.indexOf('?') != -1) {
                args = url.substr(1).split('&');

                for (; i < args.length; i++) {
                    arg = args[i].split('=');
                    back[arg[0]] = arg[1];
                }
                ;
            }

            if (arguments[0]) return back[arguments[0]];
            return back;
        },


        /**
         *  get =signature
         *
         *  @param    {object}    params          API调用的请求参数集合的关联数组，不包含sign参数
         *  @return   {string}                  返回参数签名值
         */
        getSignature: function (params, access_key) {
            var str = '', arr = [];

            // json转为对象数组
            for (var key in params) arr.push(key);

            // 先将参数以其参数名的字典序升序排序
            arr.sort();

            // 遍历排序后的参数数组中的每一个key/value对
            for (var i = 0; i < arr.length; i++) {
                str += API.strFormat("{0}={1}", arr[i], params[arr[i]]);
            }

            str += access_key;
            // 通过md5算法为签名字符串生成一个md5签名，该签名就是我们要追加的sign参数值
            return MD5.hex_md5(str);
        },


        /**
         *  get =signature
         *
         *  @param    {object}    params          API调用的请求参数集合的关联数组，不包含sign参数
         *  @return   {string}                  返回参数签名值
         */
        getEncodeSignature: function (params, access_key) {
            var str = '', arr = [];

            // json转为对象数组
            for (var key in params) arr.push(key);

            // 先将参数以其参数名的字典序升序排序
            arr.sort();

            // 遍历排序后的参数数组中的每一个key/value对
            for (var i = 0; i < arr.length; i++) {
                str += API.strFormat("{0}={1}", arr[i], this.encode(params[arr[i]]));
            }

            str += access_key;
            // 通过md5算法为签名字符串生成一个md5签名，该签名就是我们要追加的sign参数值
            return MD5.hex_md5(str);
        },



        /**
         *  =getUrlSignature
         *  @about    获取带参数签名的完整地址
         *
         *  @param    {string}  url
         *  @param    {json}    params
         *  @param    {string}  access_key
         *  @return   {string}
         */
        getUrlSignature: function(url, params, access_key) {
            var str = '', tmp_arr = [];
            // 生成签名
            params['sign'] = this.getSignature(params, access_key);
            // 拼接参数
            for (var p in params) tmp_arr.push(p +'='+ this.encode(params[p]));
            // 拼接链接
            str += url +'?'+ tmp_arr.join('&');
            return str;
        },


        /**
         *  =get url  获取完整请求地址
         *
         *  @param    {string}    url     请求地址
         *  @param    {object}    params  请求参数
         *  @return   {string}
         */
        getUrl: function (url, params) {
            var query_arr = [];

            for (var key in params) {
                query_arr.push(API.strFormat("{0}={1}", key, params[key]));
            }

            return url + "?" + query_arr.join("&");
        },


        /**
         *  =timeGap 获取间隔间隔
         *  @param    {number}  when
         */
        timeGap: function (w) {
            if (w) {
                return (new Date()).getTime() - API.timestamp;
            }
            else {
                API.timestamp = (new Date()).getTime();
                return API.timestamp;
            }
        },


        /**
         *  =is empty
         *  @about     是否为空
         *
         *  @params    {object}  obj
         */
        isEmpty: function(obj) {
            for (var n in obj) return false;
            return true;
        },


        /**
         *  =random  随机数
         *
         *  @param   {number}  n  0~n间随机数
         */
        random: function (n) {
            return parseInt(Math.random() * n);
        },


        /**
         *  =sortRandom  随机排序
         *
         *  @param    {array}  arr  待排序数组
         */
        sortRandom: function (arr) {
            return arr.sort(function () {
                return Math.random() > 0.5 ? -1 : 1;
            });
        },


        /**
         *  =timeGap 获取间隔间隔
         *  @param    {number}  when
         */
        timeGap: function (w) {
            if (w) {
                return (new Date()).getTime() - API.timestamp;
            }
            else {
                API.timestamp = (new Date()).getTime();
                return API.timestamp;
            }
        },


        /**
         *  =encode & =decode
         *
         *  @param    {string}  s 需要 encode/decode 的字符串
         *  @return   {string}
         */
        encode: function (s) {
            return encodeURIComponent(s);
        },
        decode: function (s) {
            return decodeURIComponent(s);
        },


        /**
         *  =format string 格式化
         *
         *  @param    {string}  str  需要格式化的string
         *  @param    {all}     1~n  {n} 替换内容
         *  @return   {string}       格式化后的string
         */
        strFormat: function (src) {
            if (arguments.length === 0) return null;

            var args = Array.prototype.slice.call(arguments, 1);
            return src.replace(/\{(\d+)\}/g, function (m, i) {
                return args[i];
            });
        },


        /**
         *  =format number 格式化
         *
         *  @param    {number}  num  需要格式化的string
         */
        numFormat: function (num) {
            // 保留 fixed 小数位数
            num = parseFloat(num).toFixed((arguments[1] || 0));

            // 加上逗号
            num += '';
            var x = num.split('.'),
                x1 = x[0],
                x2 = (x.length > 1) ? ('.' + x[1]) : '',
                rgx = /(\d+)(\d{3})/;

            while (rgx.test(x1)) x1 = x1.replace(rgx, '$1' + ',' + '$2');

            return x1 + x2;
        },


        /**
         *  =format name 格式化
         *
         *  @param    {string}  s  名称
         */
        nameFormat: function (s) {
            if (s.length > 4) {
                s = s.substring(0, 4) + '..';
            }
            return s;
        },


        /**
         *  =format desc 格式化
         *
         *  @param    {string}   s  详细介绍
         *  @param    {boolean}  t  是否截取
         */
        descFormat: function (s, t) {
            var r = '', i = 0;

            t = t || 0;
            // 截取介绍
            if (!t && s.length > 280)
                s = s.substring(0, 90) + '...';

            // 介绍格式化
            s = s.replace(/\n/ig, '<br>');
            s = s.split('<br>');

            for (; i < s.length; i++) {
                if (s[i] != '')
                    r += '<p class="indent">' + s[i] + '</p>';
            }

            return r;
        },

        /**
         *  =doLocation
         *  @about  跳转
         *
         *  @param     {string}  url
         */
        doLocation: function(url) {
            var a = doc.createElement("a");
            if (!a.click) {
                win.location = url;
                return;
            }
            a.setAttribute("href", url);
            a.style.display = "none";
            doc.body.appendChild(a);
            a.click();
        },


        /**
         *  =alert
         *  @about   弹出提示
         *
         *  @param     {string}  url
         */
        alert: function(msg, callback) {
            var callback = callback || function() {};
            Lightbox.show($('#tpl-alert').tmpl({msg: msg}), 1);
            $('.btn-close').off().on('click', function() {
                Lightbox.hide();
                callback();
            })
        },

        /**
         *  =funTransitionHeight
         *  @about 有动画地变化高度
         *
         *  @param element
         *  @param time
         */
        funTransitionHeight: function(element, time) { // time, 数值，可缺省
            if (typeof window.getComputedStyle == "undefined") return;

            var height = window.getComputedStyle(element).height;
            element.style.height = "auto";
            var targetHeight = window.getComputedStyle(element).height;
            element.style.height = height;
            setTimeout(function() {
                if (time) element.style.transition = "height "+ time +"ms,opacity " + time + "ms";
                element.style.height = targetHeight;
                element.style.opacity = 1;
            }, 15);
        }


    };

    (function ($) {

        /**
         =template
         @about    简易模板

         @usage

         HTML:
         <script type="text/template" id="tpl-article"><h1>{=title}</h1></script>

         JavaScript:
         $('#tpl-article').tmpl(data).appendTo($item);
         */
        (function($){
            $.fn.tmpl = function(d) {
                var s = $(this[0]).html().trim();
                if ($.isArray(d)) {
                    var li = '',
                        tm = {}, i = 0, len = d.length;
                    for (; i < len; i++) {
                        tm = d[i];
                        li += s.replace(/\{\=(\w+)\}/g, function(all, match) {
                            return tm[match];
                        });
                    }
                    s = li;
                }
                else {
                    s = s.replace(/\{\=(\w+)\}/g, function(all, match) {
                        return d[match];
                    });
                }
                return $(s);
            };
        })($);


        /**
         *  =notice
         *
         *  @param    {number}  t  通知类型
         *  @param    {string}  m  消息
         *  @param    {boolean} w  处理方法  [0]本身变化通知  [1]内含通知
         */
        $.fn.notice = function (t, m, w) {
            w = w || 0;

            var $n = w ? $('<p />').html(m) : $(this).html(m);

            switch (t) {
                default:
                case 0: // [0] 警告
                    $n.attr('class', 'notice');
                    break;

                case 1: // [1] 成功
                    $n.attr('class', 'notice notice-success');
                    break;

                case 2: // [2] 错误
                    $n.attr('class', 'notice notice-error');
                    break;

                case 3: // [3] 信息
                    $n.attr('class', 'notice notice-info');
                    break;

                case 4: // [4] 普通
                    $n.attr('class', 'notice notice-wrap');
                    break;
            }

            if (w) {
                $(this).html($n);
            }
            else {
                if ($n.hasClass('hide')) $n.removeClass('hide');
            }
        };


        /*!
         * jQuery Cookie Plugin v1.4.0
         * https://github.com/carhartl/jquery-cookie
         *
         * Copyright 2013 Klaus Hartl
         * Released under the MIT license
         */
        (function (factory) {
        }(function ($) {

            var pluses = /\+/g;

            function encode(s) {
                return config.raw ? s : encodeURIComponent(s);
            }

            function decode(s) {
                return config.raw ? s : decodeURIComponent(s);
            }

            function stringifyCookieValue(value) {
                return encode(config.json ? JSON.stringify(value) : String(value));
            }

            function parseCookieValue(s) {
                if (s.indexOf('"') === 0) {
                    // This is a quoted cookie as according to RFC2068, unescape...
                    s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
                }

                try {
                    // Replace server-side written pluses with spaces.
                    // If we can't decode the cookie, ignore it, it's unusable.
                    s = decodeURIComponent(s.replace(pluses, ' '));
                } catch (e) {
                    return;
                }

                try {
                    // If we can't parse the cookie, ignore it, it's unusable.
                    return config.json ? JSON.parse(s) : s;
                } catch (e) {
                }
            }

            function read(s, converter) {
                var value = config.raw ? s : parseCookieValue(s);
                return $.isFunction(converter) ? converter(value) : value;
            }

            var config = $.cookie = function (key, value, options) {

                // Write
                if (value !== undefined && !$.isFunction(value)) {
                    options = $.extend({}, config.defaults, options);

                    if (typeof options.expires === 'number') {
                        var days = options.expires, t = options.expires = new Date();
                        t.setDate(t.getDate() + days);
                    }

                    return (document.cookie = [
                        encode(key), '=', stringifyCookieValue(value),
                        options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                        options.path ? '; path=' + options.path : '',
                        options.domain ? '; domain=' + options.domain : '',
                        options.secure ? '; secure' : ''
                    ].join(''));
                }

                // Read

                var result = key ? undefined : {};

                // To prevent the for loop in the first place assign an empty array
                // in case there are no cookies at all. Also prevents odd result when
                // calling $.cookie().
                var cookies = document.cookie ? document.cookie.split('; ') : [];

                for (var i = 0, l = cookies.length; i < l; i++) {
                    var parts = cookies[i].split('=');
                    var name = decode(parts.shift());
                    var cookie = parts.join('=');

                    if (key && key === name) {
                        // If second argument (value) is a function it's a converter...
                        result = read(cookie, value);
                        break;
                    }

                    // Prevent storing a cookie that we couldn't decode.
                    if (!key && (cookie = read(cookie)) !== undefined) {
                        result[name] = cookie;
                    }
                }

                return result;
            };

            config.defaults = {};

            $.removeCookie = function (key, options) {
                if ($.cookie(key) !== undefined) {
                    // Must not alter options, thus extending a fresh object...
                    $.cookie(key, '', $.extend({}, options, {expires: -1}));
                    return true;
                }
                return false;
            };

        }));


        /**
         =pages
         @about    页面切换
         */
        (function($) {
            /**
             *  @param    {string}    p  页面标识
             *  @param    {function}  f  后续执行
             */
            $.fn.pages = function(p, before, after) {
                $(this).each(function(index) {
                    var $this = $(this);
                    if ( $this.data('page') === p ) {
                        setTimeout(function() {
                            (before || function() {})($this);
                            $this.attr('class', 'ui-page ui-page-active fade in');
                            setTimeout(function() {
                                $this.removeClass('fade in');
                            }, 225);
                            (after || function() {})($this);
                        }, 124);
                    }
                    else {
                        if ( $this.hasClass('ui-page-active') ) {
                            $this.attr('class', 'ui-page ui-page-active fade out');
                            setTimeout(function() {
                                $this.removeClass('ui-page-active fade out');
                            }, 125);
                        }
                    }
                });
            };
        })($);


        /** @preserve Copyright 2010-2013 Youmi.net. All Rights Reserved. */
        /**
         lightbox 方法
         -------------

         @usage
         */
        ;(function(win, doc, $) {
            /** 私有属性
             -----------------------------------------------------------------*/
            var Lightbox = {},
                $modal,
                $modalBox,
                $overlay;

            /** 公有方法
             -----------------------------------------------------------------*/
            Lightbox = {

                /**
                 *  =init
                 *  @about    初始化
                 */
                init: function() {
                    if ( !$("#mbox-modal").length )
                        $("body").append('<div id="mbox-overlay" class="overlay hide"></div><div id="mbox-contain" class="modal-box hide"><div id="mbox-modal" class="modal"></div></div>');

                    $modal = $("#mbox-modal");
                    $modalBox = $("#mbox-contain");
                    $overlay = $("#mbox-overlay");

                    $modal.on('touchmove', function() { return false; });
                    //$overlay.on('touchmove', function() { return false; });
                },

                /**
                 *  =show
                 *  @about    显示弹窗
                 *
                 *  @param    {string}  m  内容
                 *  @param    {int}     t  位置
                 */
                show: function(m, t) {
                    if(t) $modal.addClass('bottom');
                    $modalBox.removeClass('hide');
                    $modal.html(m);
                    $overlay.removeClass('hide');
                    return this;
                },


                /**
                 *  =hide
                 *  @about    隐藏弹窗
                 */
                hide: function() {
                    $modalBox.addClass('hide')
                    $modal.html('');
                    $overlay.addClass('hide');
                    return this;
                }
            };

            win.Lightbox = Lightbox;
        })(win, doc, $);



        /* ========================================================================
         * Bootstrap: button.js v3.3.1
         * http://getbootstrap.com/javascript/#buttons
         * ========================================================================
         * Copyright 2011-2015 Twitter, Inc.
         * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
         * ======================================================================== */


        +function ($) {
            'use strict';

            // BUTTON PUBLIC CLASS DEFINITION
            // ==============================

            var Button = function (element, options) {
                this.$element  = $(element)
                this.options   = $.extend({}, Button.DEFAULTS, options)
                this.isLoading = false
            }

            Button.VERSION  = '3.3.1'

            Button.DEFAULTS = {
                //loadingText: 'loading...'
                loadingText: '正在提交...'
            }

            Button.prototype.setState = function (state) {
                var d    = 'disabled'
                var $el  = this.$element
                var val  = $el.is('input') ? 'val' : 'html'
                var data = $el.data()

                state = state + 'Text'

                if (data.resetText == null) $el.data('resetText', $el[val]())

                // push to event loop to allow forms to submit
                setTimeout($.proxy(function () {
                    $el[val](data[state] == null ? this.options[state] : data[state])

                    if (state == 'loadingText') {
                        this.isLoading = true
                        $el.addClass(d).attr(d, d)
                    } else if (this.isLoading) {
                        this.isLoading = false
                        $el.removeClass(d).removeAttr(d)
                    }
                }, this), 0)
            }

            Button.prototype.toggle = function () {
                var changed = true
                var $parent = this.$element.closest('[data-toggle="buttons"]')

                if ($parent.length) {
                    var $input = this.$element.find('input')
                    if ($input.prop('type') == 'radio') {
                        if ($input.prop('checked') && this.$element.hasClass('active')) changed = false
                        else $parent.find('.active').removeClass('active')
                    }
                    if (changed) $input.prop('checked', !this.$element.hasClass('active')).trigger('change')
                } else {
                    this.$element.attr('aria-pressed', !this.$element.hasClass('active'))
                }

                if (changed) this.$element.toggleClass('active')
            }


            // BUTTON PLUGIN DEFINITION
            // ========================

            function Plugin(option) {
                return this.each(function () {
                    var $this   = $(this)
                    var data    = $this.data('bs.button')
                    var options = typeof option == 'object' && option

                    if (!data) $this.data('bs.button', (data = new Button(this, options)))

                    if (option == 'toggle') data.toggle()
                    else if (option) data.setState(option)
                })
            }

            var old = $.fn.button

            $.fn.button             = Plugin
            $.fn.button.Constructor = Button


            // BUTTON NO CONFLICT
            // ==================

            $.fn.button.noConflict = function () {
                $.fn.button = old
                return this
            }


            // BUTTON DATA-API
            // ===============

            $(document)
                .on('click.bs.button.data-api', '[data-toggle^="button"]', function (e) {
                    var $btn = $(e.target)
                    if (!$btn.hasClass('btn')) $btn = $btn.closest('.btn')
                    Plugin.call($btn, 'toggle')
                    e.preventDefault()
                })
                .on('focus.bs.button.data-api blur.bs.button.data-api', '[data-toggle^="button"]', function (e) {
                    $(e.target).closest('.btn').toggleClass('focus', /^focus(in)?$/.test(e.type))
                })

        }($);


    }($, win));

    // 时间格式化
    Date.prototype.Format = function (fmt) { //author: meiz
        var o = {
            "M+": this.getMonth() + 1,                 //月份
            "d+": this.getDate(),                    //日
            "h+": this.getHours(),                   //小时
            "m+": this.getMinutes(),                 //分
            "s+": this.getSeconds(),                 //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds()             //毫秒
        };
        if (/(y+)/.test(fmt))
            fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt))
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }

    return API;

})(window, document, Zepto);
