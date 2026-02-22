-- 创建比赛表
USE nba_platform;

CREATE TABLE IF NOT EXISTS `match` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `home_team_name` varchar(100) NOT NULL COMMENT '主队中文名',
  `home_team_logo` varchar(50) NOT NULL COMMENT '主队英文缩写',
  `home_team_score` int NOT NULL DEFAULT '0' COMMENT '主队得分',
  `away_team_name` varchar(100) NOT NULL COMMENT '客队中文名',
  `away_team_logo` varchar(50) NOT NULL COMMENT '客队英文缩写',
  `away_team_score` int NOT NULL DEFAULT '0' COMMENT '客队得分',
  `match_date` date NOT NULL COMMENT '比赛日期',
  `match_time` time DEFAULT NULL COMMENT '比赛时间',
  `status` varchar(20) NOT NULL DEFAULT 'upcoming' COMMENT '比赛状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_match_date` (`match_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='比赛表';

-- 插入示例数据（今天的比赛）
INSERT INTO `match` (
  `home_team_name`, `home_team_logo`, `home_team_score`,
  `away_team_name`, `away_team_logo`, `away_team_score`,
  `match_date`, `match_time`, `status`, `created_at`, `updated_at`
) VALUES
('洛杉矶湖人', 'LAL', 105, '金州勇士', 'GSW', 102, CURDATE(), '19:30:00', 'finished', NOW(), NOW()),
('芝加哥公牛', 'CHI', 98, '迈阿密热火', 'MIA', 110, CURDATE(), '20:00:00', 'finished', NOW(), NOW()),
('波士顿凯尔特人', 'BOS', 115, '布鲁克林篮网', 'BKN', 108, CURDATE(), '20:30:00', 'finished', NOW(), NOW());

SELECT * FROM `match`;
