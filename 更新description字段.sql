-- 修改 description 字段为可选
ALTER TABLE `highlight` MODIFY COLUMN `description` text NOT NULL DEFAULT '';
