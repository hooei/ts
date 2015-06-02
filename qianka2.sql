-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2015-02-03 14:57:20
-- 服务器版本: 5.5.40-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `qianka2`
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
