/**
 *  lottery.js 抽奖
 *
 */
// requestanimationframe 兼容性处理
window.requestAnimationFrame = (function() {
    var lastTime = 0;
    return  window.requestAnimationFrame       ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback, element){
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
                timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
})();



window.onload = function () {

    QL.lottery= (function (ym) {
        var getPixelRatio = function(context) {
            var backingStore = context.backingStorePixelRatio ||
                context.webkitBackingStorePixelRatio ||
                context.mozBackingStorePixelRatio ||
                context.msBackingStorePixelRatio ||
                context.oBackingStorePixelRatio ||
                context.backingStorePixelRatio || 1;
            return (window.devicePixelRatio || 1) / backingStore;
        };

        var lottery = (function(window, document) {

            "use strict";

            var canvas = document.getElementById('pointer'),
                ctx = document.getElementById('pointer').getContext("2d"),
                width = ctx.canvas.width,
                height = ctx.canvas.height,
                resource1,
                resource2,
                max_v = Math.PI * 3, // 最高速度540°/s
                v = 0,  // 当前角速度
                acceleration = 3 * Math.PI / 4, // 加速率
                radius = 0,  // 偏转角,
                status = 1,  // 加速或减速,
                range,
                target,
                callback,
                startTime = 0;

            //调用
            var ratio = getPixelRatio(ctx);
            function init() {
                ctx.translate(width/2, height/2);
                resource1 = new Image();
                resource1.onload = function() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(resource1, -204, -204,  408, 408);

                    resource2 = new Image();
                    resource2.onload = function() {
                        ctx.drawImage(resource2, -73, -86, 147 , 172 ) ;
                    };
                    resource2.src = '/static/images/fun/lottery/button.png';
                };
                resource1.src = '/static/images/fun/lottery/prize.png';
                //resource1.src = 'https://git.umlife.net/adsys/qiandeer-issue/uploads/ffd929c0af973356c5650babd9b79ebd/image.png';


                // ctx.translate(pointer.width/2, pointer.height/2);
                // ctx.save();
            }

            function animLoop(t) {
                var time = (startTime == 0)?0:(t -startTime) / 1000;
                ctx.clearRect(-width/2, -height/2, width/2, height/2);
                ctx.save();

                if(status) {
                    v = (max_v > v + acceleration * time)?(v + acceleration * time):max_v;
                } else {
                    if(radius > range[0] && radius < range[1]) {
                        v = 0;
                    } else {
                        acceleration = Math.abs(v / 2 / (target / 4 * Math.PI - radius));
                        v = v - acceleration * time;
                    }
                }

                radius = radius + v * time;
                ctx.rotate(radius);

                radius = radius % (2 * Math.PI);

                ctx.drawImage(resource1, -204, -204, width, height);
                ctx.restore();

                ctx.drawImage(resource2, -73, -86, 147, 172) ;

                startTime = t;

                if(status == 1 || (status == 0 && v > 0)) {
                    window.requestAnimationFrame(animLoop);
                } else {
                    //console.log(callback);
                    callback();
                }
            }

            init();

            return {
                start: function() {
                    window.requestAnimationFrame(animLoop);
                },
                stop: function(r, cb) {
                    switch(r) {
                        case 0:
                            range = [[0, 1/12*Math.PI], [31/12*Math.PI, 2*Math.PI]][Math.floor(Math.random()*2)];
                            break;
                        case 1:
                            range = [3/12*Math.PI, 5/12*Math.PI];
                            break;
                        case 2:
                            range = [7/12*Math.PI, 9/12*Math.PI];
                            break;
                        case 3:
                            range = [11/12*Math.PI, 13/12*Math.PI];
                            break;
                        case 4:
                            range = [15/12*Math.PI, 17/12*Math.PI];
                            break;
                        case 5:
                            range = [19/12*Math.PI, 21/12*Math.PI];
                            break;
                        default:
                            range = [3/12*Math.PI, 5/12*Math.PI];
                    }
                    target = r;
                    status = 0;
                    callback = cb || function() {};
                }
            };

        })(window, document);

        ym.init = function() {

            // 抽奖开始
            $('#pointer').one('click', function() {
                lottery.start();
                $('.lottery-hide').css('visibility', 'hidden');
                setTimeout(function() {
                    lottery.stop(5);
                    setTimeout(function() {

                    });
                }, 3000);
                return false;
                $.ajax({
                    url: '/lottery/draw',
                    dataType: 'json',
                    method: 'POST',
                    cache: false,
                    timeout: 8000,
                    success: function(result) {
                        if (result.c === 0) {
                            lottery.stop(result.id);
                        } else {
                            alert(result.message);
                            lottery.stop(result.id);
                        }
                    },
                    error: function(xhr, status, errorThrown) {
                        if (errorThrown == 'Forbidden') {
                            alert('登陆超时，请重新登陆！');
                            window.location = '/login';
                        } else {
                            alert('发生未知错误！');
                            lottery.stop(1);
                        }
                    },
                    complete: function() {
                        $('#pointer').prop('disabled', 'disabled').css('cursor', 'not-allowed');
                    }
                });
            });

            //新的提交
            $( "#lottery-save" ).on( "click", function () {
                var name = $( "#lottery-name" ).val(),
                    phone = $( "#lottery-phone" ).val(),
                    postcode = $( "#lottery-postcode").val(),
                    address = $( "#lottery-address" ).val();
                if ( !address.length ) {
                    alert( "您还没有填写地址！" );
                    return;
                }
                if ( !name.length ) {
                    alert( "您还没有填写姓名！" );
                    return;
                }
                if ( !/^[1-9]\d{5}$/.test( postcode ) ) {
                    alert( "请输入正确邮编！" );
                    return;
                }
                if ( !/^(13[0-9]|14[0-9]|15[0-9]|18[0-9])\d{8}$/.test( phone ) ) {
                    alert( "请输入正确手机号码！" );
                    return;
                }
                $.ajax({
                    type: "post",
                    url: "/lottery/info",
                    dataType: "json",
                    data:  {
                        name: name,
                        phone: phone,
                        address: address,
                        postcode: postcode
                    },
                    success: function ( result ) {
                        if ( result.message ) {
                            alert( result.message );
                        } else {
                            $( ".response" ).addClass( "hide" );
                            $( ".lottery-result" ).removeClass( "hide" );
                            $( ".lottery-real" ).addClass( "hide" );
                            alert( "谢谢你的参与，我们的工作人员会尽快联系您" );
                            $.fancybox.close();
                            var num = parseInt( $( ".message-num" ).text() ) + 1;
                            $( ".message-num" ).addClass( "has-message" ).text( num );
                        }
                    }
                });
            });
        };

        return ym;
    }(QL.lottery || {}));

    QL.lottery.init();
}