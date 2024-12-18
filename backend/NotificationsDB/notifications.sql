CREATE DATABASE IF NOT EXISTS notifications_db;
use notifications_db;

SET GLOBAL event_scheduler = ON;
DROP TABLE IF EXISTS `slack`;

CREATE TABLE IF NOT EXISTS `slack` (
  channel_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  webhook_url VARCHAR(255) NOT NULL,
  app_name VARCHAR(255) NOT NULL,
  workspace_name VARCHAR(255) NOT NULL,
  workspace_url VARCHAR(255) NOT NULL,
  channel_name VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `metrics_logs`;

CREATE TABLE metrics_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric VARCHAR(255),
    instance VARCHAR(255),
    instance_id VARCHAR(255),
    country VARCHAR(255),
    code VARCHAR(50),
    app_id VARCHAR(255),
    app_name VARCHAR(255),
    status VARCHAR(50),
    value VARCHAR(255),
    threshold VARCHAR(255),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE EVENT delete_old_metrics
ON SCHEDULE EVERY 1 DAY
DO
  DELETE FROM metrics_log
  WHERE Logged_at < CURDATE() - INTERVAL 90 DAY;

INSERT INTO slack (webhook_url, app_name, workspace_name, workspace_url, channel_name) VALUES
('https://hooks.slack.com/services/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', 'FYP GlobalGuard', 'FYP Team 5-GlobalGuard', 'fypteam5-globalguard', 'Alerts');