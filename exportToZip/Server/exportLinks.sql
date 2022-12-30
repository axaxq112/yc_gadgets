/*
 Navicat Premium Data Transfer

 Source Server         : mamp-localhost
 Source Server Type    : MySQL
 Source Server Version : 50734 (5.7.34)
 Source Host           : localhost:3306
 Source Schema         : bsh

 Target Server Type    : MySQL
 Target Server Version : 50734 (5.7.34)
 File Encoding         : 65001

 Date: 30/12/2022 23:57:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for exportLinks
-- ----------------------------
DROP TABLE IF EXISTS `exportLinks`;
CREATE TABLE `exportLinks` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` text,
  `ver` text,
  `absPath` text,
  `insertTs` text,
  `expireTs` text,
  `token` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
