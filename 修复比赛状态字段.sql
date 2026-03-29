-- 修复比赛状态字段，将中文转换为英文
USE nba_platform;

-- 将所有中文状态转换为英文
UPDATE `match` SET status = 'upcoming' WHERE status = '未开始';
UPDATE `match` SET status = 'live' WHERE status = '进行中';
UPDATE `match` SET status = 'finished' WHERE status = '已结束';

-- 验证修改
SELECT id, home_team_name, away_team_name, status FROM `match` LIMIT 10;
