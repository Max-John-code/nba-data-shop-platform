-- 更新精彩回放表结构，将 video_url 和 cover_image 改为文件路径
-- 如果表已存在，先删除旧表
DROP TABLE IF EXISTS `highlight`;

-- 重新创建表
CREATE TABLE `highlight` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `description` text NOT NULL COMMENT '描述',
  `video` varchar(100) NOT NULL COMMENT '视频文件路径',
  `cover_image` varchar(100) DEFAULT NULL COMMENT '封面图片路径',
  `match_date` date NOT NULL COMMENT '比赛日期',
  `teams` varchar(100) NOT NULL COMMENT '对阵球队',
  `views` int NOT NULL DEFAULT '0' COMMENT '观看次数',
  `duration` int NOT NULL DEFAULT '0' COMMENT '时长(秒)',
  `created_at` datetime(6) NOT NULL COMMENT '创建时间',
  `updated_at` datetime(6) NOT NULL COMMENT '更新时间',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用',
  PRIMARY KEY (`id`),
  KEY `idx_match_date` (`match_date`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='精彩回放表';
