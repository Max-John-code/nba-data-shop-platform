-- 创建论坛相关表
USE nba_platform;

-- 文章表
CREATE TABLE IF NOT EXISTS `article` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `image` longtext COMMENT '图片(base64)',
  `author_id` bigint NOT NULL COMMENT '作者ID',
  `view_count` int NOT NULL DEFAULT '0' COMMENT '浏览次数',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_author` (`author_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_article_author` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

-- 评论表
CREATE TABLE IF NOT EXISTS `comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `article_id` bigint NOT NULL COMMENT '文章ID',
  `user_id` bigint NOT NULL COMMENT '评论用户ID',
  `content` text NOT NULL COMMENT '评论内容',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_article` (`article_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_comment_article` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- 插入示例文章
INSERT INTO `article` (`title`, `content`, `image`, `author_id`, `view_count`, `created_at`, `updated_at`)
SELECT 
  'NBA总决赛精彩回顾',
  '今年的NBA总决赛可谓是精彩纷呈，双方球队都展现出了顶级的竞技水平。比赛过程跌宕起伏，最终在第七场决出胜负。这场比赛将成为NBA历史上的经典之战。',
  NULL,
  id,
  0,
  NOW(),
  NOW()
FROM `user` WHERE `role` = 'admin' LIMIT 1;

SELECT * FROM `article`;
SELECT * FROM `comment`;
