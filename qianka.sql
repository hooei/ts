-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2015-01-15 18:12:34
-- 服务器版本: 5.5.40-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `qianka`
--

-- --------------------------------------------------------

--
-- 表的结构 `accounts`
--

CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `salt` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `pwd` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '1',
  `note` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `salt`, `pwd`, `status`, `note`) VALUES
(1, 'admin', '', '', 0, NULL),
(2, 'test', 'qzZKFWddMYk=', '1e2ab0cdd6e41cc73b812b97acada0b7430a8c141575a23196f6e41643c94290', 1, '密码：123456');

-- --------------------------------------------------------

--
-- 表的结构 `bind_phones`
--

CREATE TABLE IF NOT EXISTS `bind_phones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `callback_orders`
--

CREATE TABLE IF NOT EXISTS `callback_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `oid` int(11) NOT NULL,
  `device` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ad` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `adid` int(11) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL,
  `points` int(11) NOT NULL,
  `price` float NOT NULL DEFAULT '0',
  `platform` tinyint(4) NOT NULL DEFAULT '1',
  `trade_type` tinyint(4) NOT NULL DEFAULT '1',
  `sig` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order` (`order`),
  KEY `oid` (`oid`),
  KEY `user` (`uid`),
  KEY `time` (`create_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=12 ;

--
-- 转存表中的数据 `callback_orders`
--

INSERT INTO `callback_orders` (`id`, `order`, `oid`, `device`, `ad`, `adid`, `uid`, `points`, `price`, `platform`, `trade_type`, `sig`, `create_time`) VALUES
(1, 'YM150105KqumEcgndc', 8, '3E896F09-1135-43EE-AEF6-49EEE8DCABB2', '掌阅iReader', 9819, 15, 770, 1.54, 2, 1, 'ad5d6794ea0851d61f0dcf27a7529e1c', '2015-01-11 10:29:39'),
(2, 'YM150105ZjaxoV-f3a', 11, '16865808-1F39-4CDE-B609-85254135F4E6', '掌阅iReader', 9819, 15, 770, 1.54, 2, 1, '3463a1347e92ea8db7b968e43ede306e', '2015-01-11 10:31:43'),
(3, 'YM141231O1zeI6IFf0', 13, '863396024169003', '疯狂答题', 9877, 14, 227, 0.35, 1, 1, 'bccafe87', '2015-01-11 10:35:35'),
(4, 'YM141228U9Q9QA7A49', 15, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 14, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 03:47:08'),
(5, 'YM141228U9Q9QA7A40', 16, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 8, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 03:57:49'),
(6, 'YM141228U9Q9QA7A50', 17, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 8, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 03:57:53'),
(7, 'YO141228U9Q9QA7A50', 18, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 8, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 06:14:27'),
(8, 'YO141228U9QqQA7A50', 19, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 8, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 06:15:01'),
(9, 'YO141228U9QqoA7A50', 20, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 8, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 06:15:09'),
(10, 'YO141228U9QqoA7A51', 21, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 10, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 06:29:33'),
(11, 'YO141228U9QqoA7A52', 22, 'A2C7508B-9ADB-45A2-94B8-B6F9AE90227C', '囧西游', 1233, 10, 910, 1.4, 2, 1, 'e0ef04e26c3c1782d14c72aeeb348bda', '2015-01-12 06:29:36');

-- --------------------------------------------------------

--
-- 表的结构 `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `oid` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `uid` int(11) NOT NULL COMMENT '设备当前账号',
  `last` int(11) NOT NULL DEFAULT '0' COMMENT '设备切换账户前uid',
  `cid` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `mac` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `ifa` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `aicid` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `udid` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `attr` int(11) NOT NULL DEFAULT '0' COMMENT '设备属性',
  PRIMARY KEY (`id`),
  UNIQUE KEY `oid` (`oid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=22 ;

--
-- 转存表中的数据 `devices`
--

INSERT INTO `devices` (`id`, `oid`, `uid`, `last`, `cid`, `mac`, `ifa`, `aicid`, `udid`, `attr`) VALUES
(1, '123', 3, 0, '', '', NULL, '', '', 0),
(3, '80aa2e45f1decbdea8a5937a004c6bb8', 5, 0, '', '', NULL, '', '', 0),
(6, '22', 8, 0, '', '', NULL, '', '', 0),
(7, '11', 9, 0, '', '', NULL, '', '', 0),
(8, '1fe08985746c0936330dd4fe05014db2', 10, 0, '', '', NULL, '', '', 0),
(9, '769fe540e965775073c91756e8650239', 11, 0, '', '', NULL, '', '', 0),
(10, '1fe08985746c0936330dd4fe05014db3', 12, 0, '', '', NULL, '', '', 0),
(11, '1fe08985746c0936330dd4fe05014db4', 13, 0, '', '', NULL, '', '', 0),
(12, '1fe08985746c0936330dd4fe05014db5', 14, 0, '', '', NULL, '', '', 0),
(13, '1fe08985746c0936330dd4fe05014db6', 15, 0, '', '', NULL, '', '', 0),
(14, '54f628eb35ef08332711040176eed2d6', 17, 0, '6pTzy4eo-qQDk', '020000000000', '381d96b0c1b2484d97e36864ac7c30f6', '301e7724fe9141939824ef3c59b2c63d', '7794263b051303f2af5ba99ca9fa3288130157e8', 0),
(15, '06e9f604153e9ec7e05bbd5adfffe744', 18, 0, 'SMd_AveE7kbA_', '020000000000', 'bc6ef94cba4b4540b74e3da21529182e', 'ac2105031e644d139e122c3ddcbc424b', '8fd23b2b620d40c3729ee1bc58787cc9fc51baeb', 139),
(16, '06e9f604153e9ec7e05bbd5adfffe746', 19, 0, 'SMd_AveE7kbA_', '020000000000', 'bc6ef94cba4b4540b74e3da21529182e', 'ac2105031e644d139e122c3ddcbc424e', '8fd23b2b620d40c3729ee1bc58787cc9fc51baeb', 139),
(17, '780b285edc3e7683c74dba4ce4bc6466', 20, 0, 'DGsp5pz6SxXyH', '020000000000', '9bd307badb5646c2881ef59eb5905ce7', '5e97df1421474ce0baac4b42f4cb718f', '9f8ebcf879904d8a38e5e66e08f8dc0d81116525', 139),
(18, '0b1b82b76cc6c864153c8b17e72b5acb', 584612, 0, 'K-2D1E6rCXC8n', '020000000000', '5721c592bb1e4760acbe47bcdbad11e3', '45551c209b3d4720aa7102a97295a32b', 'b30fa5611468bd997fbecfd41fc0836de5a2314d', 11),
(19, 'bc719015d6c351db4d3badf5d8acbd13', 584613, 0, 'JUMkCxTNPkRsG', '020000000000', '0148fe7b97434292b00953a168599eea', '3503305b6661435e8d6eef6107ca3788', '11a311d2169d4580a0fd37f5494af29474b0d343', 11),
(20, '63b72f19b7d878a70dc6b7600b5030bb', 584614, 0, '8JUVKjXQ0AU1Q', '020000000000', '726da9a59f11404fac47887f69c1875a', '42eb1f0b991748ebaa82d3a614654ac6', 'ba4bd9816ce3e3f02e035638100fab685720e117', 139),
(21, 'f5151b68762334dc9f364b3c27965584', 584615, 0, 'Z9zmp5LHf-WGa', '020000000000', '8261539f91794eb2a72c2efa42129f3e', '8453241ca34b476cb2bb728af9acc989', 'efb4cad6fbbe3264a22d6dec1b0da577413c41b9', 139);

-- --------------------------------------------------------

--
-- 表的结构 `exchange_orders`
--

CREATE TABLE IF NOT EXISTS `exchange_orders` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(8) unsigned NOT NULL,
  `oid` int(11) unsigned NOT NULL COMMENT '全局订单ID',
  `order_num` varchar(50) DEFAULT NULL,
  `points` int(8) unsigned NOT NULL,
  `face_price` float NOT NULL DEFAULT '0',
  `actual_price` float NOT NULL DEFAULT '0',
  `description` varchar(64) DEFAULT NULL,
  `address` varchar(128) NOT NULL,
  `extype` varchar(15) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `status` tinyint(2) DEFAULT '0' COMMENT '10：等待审核；11：审核通过；12：审核拒绝；13：兑换成功；14：兑换失败',
  `notes` text COMMENT '订单备注',
  `wait_audit` tinyint(1) NOT NULL DEFAULT '1',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '兑换时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `oid_2` (`oid`),
  UNIQUE KEY `order_num` (`order_num`),
  KEY `oid` (`oid`),
  KEY `uid` (`uid`),
  KEY `create_time` (`create_time`),
  KEY `orderNum` (`order_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='积分兑换' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `feedbacks`
--

CREATE TABLE IF NOT EXISTS `feedbacks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `type` tinyint(4) NOT NULL DEFAULT '0',
  `task` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `desc` text COLLATE utf8_unicode_ci,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;

--
-- 转存表中的数据 `feedbacks`
--

INSERT INTO `feedbacks` (`id`, `uid`, `type`, `task`, `desc`, `create_time`) VALUES
(1, 15, 1, '大师傅', '阿斯顿发撒旦法撒旦法', '2015-01-12 12:20:59'),
(2, 15, 1, '搜索', '阿斯顿发撒旦法', '2015-01-12 12:22:00'),
(3, 15, 1, '安德森', '打发', '2015-01-12 12:24:21'),
(4, 15, 1, '撒旦法', '阿斯顿发撒旦法', '2015-01-12 12:24:50'),
(5, 584612, 1, '你妹', '你妹', '2015-01-13 12:02:06'),
(6, 584612, 1, '你妹', '你妹', '2015-01-13 12:02:24');

-- --------------------------------------------------------

--
-- 表的结构 `global_orders`
--

CREATE TABLE IF NOT EXISTS `global_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `last` int(11) NOT NULL COMMENT '上一次积分',
  `points` int(11) NOT NULL COMMENT '本次流水积分',
  `otype` tinyint(4) NOT NULL DEFAULT '1' COMMENT '流水类型，1：任务；2：邀请；3：兑换',
  `note` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '流水说明',
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  KEY `record_time` (`record_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=23 ;

--
-- 转存表中的数据 `global_orders`
--

INSERT INTO `global_orders` (`id`, `uid`, `last`, `points`, `otype`, `note`, `record_time`) VALUES
(1, 14, 0, 77, 2, '徒弟 15 任务分成 10%，获得 77 积分', '2015-01-11 10:28:05'),
(2, 8, 0, 38, 2, '徒孙 15 任务分成 5%，获得 38 积分', '2015-01-11 10:28:05'),
(3, 14, 77, 77, 2, '徒弟 15 任务分成 10%，获得 77 积分', '2015-01-11 10:29:28'),
(4, 8, 38, 38, 2, '徒孙 15 任务分成 5%，获得 38 积分', '2015-01-11 10:29:28'),
(5, 15, 123456101, 770, 1, '下载安装 掌阅iReader，获得 770 积分', '2015-01-11 10:29:28'),
(6, 14, 154, 77, 2, '徒弟 15 任务分成 10%，获得 77 积分', '2015-01-11 10:29:39'),
(7, 8, 76, 38, 2, '徒孙 15 任务分成 5%，获得 38 积分', '2015-01-11 10:29:39'),
(8, 15, 123456101, 770, 1, '下载安装 掌阅iReader', '2015-01-11 10:29:39'),
(9, 14, 231, 77, 2, '徒弟 15 完成任务，分成 10%，获得 77 积分', '2015-01-11 10:31:43'),
(10, 8, 114, 38, 2, '徒孙 15 完成任务，分成 5%，获得 38 积分', '2015-01-11 10:31:43'),
(11, 15, 123456101, 770, 1, '下载安装 掌阅iReader，获得 770 积分', '2015-01-11 10:31:43'),
(12, 8, 152, 22, 2, '徒弟 14 完成任务，分成 10%，获得 22 积分', '2015-01-11 10:35:35'),
(13, 14, 308, 227, 1, '下载安装 疯狂答题，获得 227 积分', '2015-01-11 10:35:35'),
(14, 8, 174, 91, 2, '徒弟 14 完成任务，分成 10%，获得 91 积分', '2015-01-12 03:47:08'),
(15, 14, 308, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 03:47:08'),
(16, 8, 265, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 03:57:49'),
(17, 8, 265, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 03:57:53'),
(18, 8, 265, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 06:14:27'),
(19, 8, 265, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 06:15:01'),
(20, 8, 265, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 06:15:09'),
(21, 10, 0, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 06:29:32'),
(22, 10, 0, 910, 1, '下载安装 囧西游，获得 910 积分', '2015-01-12 06:29:36');

-- --------------------------------------------------------

--
-- 表的结构 `invite_counts`
--

CREATE TABLE IF NOT EXISTS `invite_counts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `sons` int(4) NOT NULL DEFAULT '0',
  `grandsons` int(11) NOT NULL DEFAULT '0',
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- 转存表中的数据 `invite_counts`
--

INSERT INTO `invite_counts` (`id`, `uid`, `sons`, `grandsons`, `date`) VALUES
(1, 8, 1, 1, '2015-01-11'),
(2, 14, 1, 0, '2015-01-11'),
(3, 584612, 1, 1, '2015-01-13'),
(4, 584613, 1, 0, '2015-01-13');

-- --------------------------------------------------------

--
-- 表的结构 `options`
--

CREATE TABLE IF NOT EXISTS `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `values` int(11) NOT NULL,
  `description` varchar(200) COLLATE utf8_unicode_ci NOT NULL COMMENT '字段描述',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- 转存表中的数据 `options`
--

INSERT INTO `options` (`id`, `key`, `values`, `description`) VALUES
(1, 'iv_parent', 10, '一级邀请分成，百分比'),
(2, 'iv_grandfather', 5, '二级邀请分成，百分比'),
(3, 'rate', 1000, '积分：现金');

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '用户昵称',
  `phone` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '手机号码',
  `qq` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'QQ',
  `alipay` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '支付宝账号',
  `alipayname` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '支付宝姓名',
  `sex` tinyint(4) NOT NULL DEFAULT '0' COMMENT '性别：0：保密；1：男；2：女',
  `place` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '地区',
  `salt` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pwd` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `headimg` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '用户头像',
  `token` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `points` int(11) NOT NULL DEFAULT '0' COMMENT '当前积分',
  `iv_points` int(11) NOT NULL DEFAULT '0' COMMENT '邀请积分',
  `ex_points` int(11) NOT NULL DEFAULT '0' COMMENT '已兑换积分',
  `tt_points` int(11) NOT NULL DEFAULT '0' COMMENT '总积分',
  `sons` int(11) NOT NULL DEFAULT '0' COMMENT '邀请徒弟人数',
  `grandsons` int(11) NOT NULL DEFAULT '0' COMMENT '邀请徒孙人数',
  `parent` int(11) NOT NULL DEFAULT '0' COMMENT '一级邀请',
  `grandfather` int(11) NOT NULL DEFAULT '0' COMMENT '二级邀请',
  `grade` int(11) NOT NULL DEFAULT '1' COMMENT '用户等级',
  `sign_days` int(11) NOT NULL DEFAULT '0' COMMENT '签到天数',
  `new_bonus` int(11) NOT NULL DEFAULT '1' COMMENT '新用户奖励，0：已领取，1：未领取',
  `first_task` tinyint(4) NOT NULL DEFAULT '1' COMMENT '首次任务，1：是；0：否',
  `first_ex` tinyint(4) NOT NULL DEFAULT '1' COMMENT '首次兑换，1：是；0：否',
  `platform` tinyint(4) NOT NULL DEFAULT '0' COMMENT '系统:0:未知;1:Android,2:iOS',
  `ip` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip_address` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0：正常；-1：禁止兑换；-2：封杀',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `phone` (`phone`),
  KEY `create_time` (`create_time`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=584616 ;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`uid`, `username`, `phone`, `qq`, `alipay`, `alipayname`, `sex`, `place`, `salt`, `pwd`, `headimg`, `token`, `points`, `iv_points`, `ex_points`, `tt_points`, `sons`, `grandsons`, `parent`, `grandfather`, `grade`, `sign_days`, `new_bonus`, `first_task`, `first_ex`, `platform`, `ip`, `ip_address`, `status`, `create_time`) VALUES
(3, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:17:58'),
(4, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:29:32'),
(5, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:33:03'),
(6, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:35:25'),
(7, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:36:08'),
(8, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 265, 265, 0, 265, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-10 12:37:54'),
(9, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.252', '局域网	局域网', 0, '2015-01-11 07:29:37'),
(10, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.252', '局域网	局域网', 0, '2015-01-11 07:54:24'),
(11, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.81', '局域网	局域网', 0, '2015-01-11 08:00:38'),
(12, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-11 08:23:54'),
(13, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 8, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-11 08:25:32'),
(14, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 308, 308, 0, 308, 1, 0, 8, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-11 08:26:42'),
(15, '旦法', NULL, NULL, NULL, NULL, 1, 'guangzh滴ou', NULL, NULL, '/static/headimg/9b/f3/1e5534120fcef87726a0165bcb30e64d.png', NULL, 123456101, 0, 0, 0, 0, 0, 14, 8, 1, 0, 1, 1, 1, 2, '172.16.2.68', '局域网	局域网', 0, '2015-01-11 08:27:21'),
(16, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, '172.16.2.68', '局域网	局域网', 0, '2015-01-12 08:27:19'),
(17, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.68', '局域网	局域网', 0, '2015-01-12 08:29:22'),
(18, 's s s', NULL, NULL, NULL, NULL, 1, '广州', NULL, NULL, '/static/headimg/6f/49/eace1b317ecfe9a712e7e4e0ba2406b6.png', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.81', '局域网	局域网', 0, '2015-01-13 06:33:36'),
(19, '陈杰华', '13570362385', NULL, NULL, NULL, 1, '广州', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.68', '局域网	局域网', 0, '2015-01-13 07:24:24'),
(20, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.251', '局域网	局域网', 0, '2015-01-13 09:41:03'),
(584612, '你妹', NULL, NULL, NULL, NULL, 2, '广州', NULL, NULL, '/static/headimg/65/03/22d18f73b9a6be37b647b857d1046320.png', NULL, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.250', '局域网	局域网', 0, '2015-01-13 11:43:27'),
(584613, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 1, 0, 584612, 0, 1, 0, 1, 1, 1, 2, '172.16.2.251', '局域网	局域网', 0, '2015-01-13 11:50:05'),
(584614, '会回复', NULL, NULL, NULL, NULL, 1, '红红火火', NULL, NULL, '/static/headimg/13/a6/ac22c10c8dad17c26c911062cb54ebd7.png', NULL, 0, 0, 0, 0, 0, 0, 584613, 584612, 1, 0, 1, 1, 1, 2, '172.16.2.252', '局域网	局域网', 0, '2015-01-13 11:53:14'),
(584615, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, '172.16.2.81', '局域网	局域网', 0, '2015-01-14 06:13:38');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
