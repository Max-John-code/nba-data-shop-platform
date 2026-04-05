-- 为 highlight 表添加字段
ALTER TABLE highlight ADD COLUMN likes INT DEFAULT 0 COMMENT '点赞数';
ALTER TABLE highlight ADD COLUMN favorites INT DEFAULT 0 COMMENT '收藏数';

-- 为 article 表添加字段
ALTER TABLE article ADD COLUMN likes INT DEFAULT 0 COMMENT '点赞数';
ALTER TABLE article ADD COLUMN favorites INT DEFAULT 0 COMMENT '收藏数';
