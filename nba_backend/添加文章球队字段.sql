-- 给文章表添加球队字段
ALTER TABLE article ADD COLUMN team VARCHAR(50) DEFAULT '' COMMENT '所属球队';

-- 更新现有数据（可选，给现有文章设置默认球队）
-- UPDATE article SET team = '湖人' WHERE id > 0;

SELECT '文章球队字段添加成功！' AS message;
