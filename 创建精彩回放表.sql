-- 创建精彩回放表
CREATE TABLE IF NOT EXISTS `highlight` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `description` text NOT NULL COMMENT '描述',
  `video_url` varchar(500) NOT NULL COMMENT '视频URL',
  `cover_image` varchar(500) DEFAULT '' COMMENT '封面图片',
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
