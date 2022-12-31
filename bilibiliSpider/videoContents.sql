/*
 Navicat Premium Data Transfer

 Source Server         : mamp-localhost
 Source Server Type    : MySQL
 Source Server Version : 50734 (5.7.34)
 Source Host           : localhost:3306
 Source Schema         : bilibiliSpider

 Target Server Type    : MySQL
 Target Server Version : 50734 (5.7.34)
 File Encoding         : 65001

 Date: 31/12/2022 11:21:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for videoContents
-- ----------------------------
DROP TABLE IF EXISTS `videoContents`;
CREATE TABLE `videoContents` (
  `id` int(30) unsigned NOT NULL AUTO_INCREMENT,
  `aid` int(255) DEFAULT NULL,
  `bvid` text CHARACTER SET utf8,
  `cid` int(255) DEFAULT NULL,
  `video_title` text,
  `video_desc` text,
  `video_tname` text,
  `video_pic` text CHARACTER SET utf8,
  `video_pubYear` int(10) DEFAULT NULL,
  `video_pubMonth` int(10) DEFAULT NULL,
  `video_pubDay` int(10) DEFAULT NULL,
  `video_pubHour` int(10) DEFAULT NULL,
  `video_pubMinute` int(10) DEFAULT NULL,
  `video_pubSecond` int(10) DEFAULT NULL,
  `ownerMid` int(255) DEFAULT NULL,
  `ownerName` text CHARACTER SET utf8,
  `ownerFace` text CHARACTER SET utf8,
  `statView` int(255) DEFAULT NULL,
  `statLike` int(255) DEFAULT NULL,
  `statDanmaku` int(255) DEFAULT NULL,
  `statCoin` int(255) DEFAULT NULL,
  `statShare` int(255) DEFAULT NULL,
  `statFavorite` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5716983 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
