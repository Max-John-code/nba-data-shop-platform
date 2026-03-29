-- 修改article表的image字段类型为LONGTEXT
USE nba_platform;

ALTER TABLE `article` MODIFY COLUMN `image` LONGTEXT COMMENT '图片(base64)';

-- 验证修改
DESCRIBE `article`;
