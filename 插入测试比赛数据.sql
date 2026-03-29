-- 插入多条今日测试比赛数据
USE nba_platform;

-- 获取今天的日期
SET @today = CURDATE();

-- 插入15场测试比赛
INSERT INTO `match` (home_team_name, home_team_logo, home_team_score, away_team_name, away_team_logo, away_team_score, match_date, match_time, status, created_at, updated_at)
VALUES
('湖人', 'LAL', 108, '勇士', 'GSW', 112, @today, '10:00', '已结束', NOW(), NOW()),
('凯尔特人', 'BOS', 115, '热火', 'MIA', 110, @today, '10:30', '已结束', NOW(), NOW()),
('快船', 'LAC', 98, '太阳', 'PHX', 105, @today, '11:00', '已结束', NOW(), NOW()),
('雄鹿', 'MIL', 120, '76人', 'PHI', 118, @today, '11:30', '已结束', NOW(), NOW()),
('掘金', 'DEN', 125, '独行侠', 'DAL', 122, @today, '12:00', '已结束', NOW(), NOW()),
('篮网', 'BKN', 102, '尼克斯', 'NYK', 99, @today, '12:30', '已结束', NOW(), NOW()),
('公牛', 'CHI', 95, '骑士', 'CLE', 101, @today, '13:00', '已结束', NOW(), NOW()),
('老鹰', 'ATL', 110, '黄蜂', 'CHA', 107, @today, '13:30', '已结束', NOW(), NOW()),
('猛龙', 'TOR', 88, '魔术', 'ORL', 92, @today, '14:00', '已结束', NOW(), NOW()),
('步行者', 'IND', 113, '活塞', 'DET', 108, @today, '14:30', '已结束', NOW(), NOW()),
('灰熊', 'MEM', 105, '鹈鹕', 'NOP', 103, @today, '15:00', '已结束', NOW(), NOW()),
('马刺', 'SAS', 97, '火箭', 'HOU', 100, @today, '15:30', '已结束', NOW(), NOW()),
('爵士', 'UTA', 112, '开拓者', 'POR', 109, @today, '16:00', '已结束', NOW(), NOW()),
('国王', 'SAC', 118, '森林狼', 'MIN', 115, @today, '16:30', '已结束', NOW(), NOW()),
('雷霆', 'OKC', 106, '奇才', 'WAS', 104, @today, '17:00', '已结束', NOW(), NOW());

SELECT COUNT(*) as '今日比赛数' FROM `match` WHERE match_date = @today;
