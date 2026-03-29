-- 创建留言板表
USE nba_platform;

-- 留言表
CREATE TABLE IF NOT EXISTS `message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL COMMENT '留言用户ID',
  `content` text NOT NULL COMMENT '留言内容',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_message_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='留言表';

-- 插入示例留言
INSERT INTO `message` (`user_id`, `content`, `created_at`)
SELECT 
  id,
  '这个平台太棒了！可以看到最新的NBA资讯和球员数据。',
  NOW()
FROM `user` LIMIT 1;

SELECT * FROM `message`;
