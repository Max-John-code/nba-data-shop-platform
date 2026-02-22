-- 为player表添加player_type字段
-- 在MySQL中执行此脚本

USE nba_platform;

-- 添加player_type字段
ALTER TABLE player 
ADD COLUMN player_type VARCHAR(20) NOT NULL DEFAULT 'ranking' 
COMMENT '类型：ranking-联盟榜单, star-现役球星';

-- 查看表结构确认
DESC player;

-- 查看现有数据（所有现有数据默认为'ranking'类型）
SELECT id, name, team, player_type FROM player;
