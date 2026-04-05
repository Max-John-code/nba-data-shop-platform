-- 删除可能存在的表（如果需要）
-- DROP TABLE IF EXISTS highlight_like;
-- DROP TABLE IF EXISTS highlight_favorite;
-- DROP TABLE IF EXISTS article_like;
-- DROP TABLE IF EXISTS article_favorite;

-- 为 article 表添加点赞和收藏字段（如果不存在）
ALTER TABLE article 
ADD COLUMN IF NOT EXISTS likes INT DEFAULT 0 COMMENT '点赞数',
ADD COLUMN IF NOT EXISTS favorites INT DEFAULT 0 COMMENT '收藏数';

-- 为 highlight 表添加点赞和收藏字段（如果不存在）
ALTER TABLE highlight 
ADD COLUMN IF NOT EXISTS likes INT DEFAULT 0 COMMENT '点赞数',
ADD COLUMN IF NOT EXISTS favorites INT DEFAULT 0 COMMENT '收藏数';

-- 创建视频点赞表（不使用外键约束）
CREATE TABLE IF NOT EXISTS highlight_like (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    highlight_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_highlight (user_id, highlight_id),
    INDEX idx_highlight_like_highlight (highlight_id),
    INDEX idx_highlight_like_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频点赞表';

-- 创建视频收藏表（不使用外键约束）
CREATE TABLE IF NOT EXISTS highlight_favorite (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    highlight_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_highlight (user_id, highlight_id),
    INDEX idx_highlight_favorite_highlight (highlight_id),
    INDEX idx_highlight_favorite_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='视频收藏表';

-- 创建文章点赞表（不使用外键约束）
CREATE TABLE IF NOT EXISTS article_like (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    article_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_article (user_id, article_id),
    INDEX idx_article_like_article (article_id),
    INDEX idx_article_like_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章点赞表';

-- 创建文章收藏表（不使用外键约束）
CREATE TABLE IF NOT EXISTS article_favorite (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    article_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_article (user_id, article_id),
    INDEX idx_article_favorite_article (article_id),
    INDEX idx_article_favorite_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章收藏表';

-- 验证表是否创建成功
SHOW TABLES LIKE '%like%';
SHOW TABLES LIKE '%favorite%';
