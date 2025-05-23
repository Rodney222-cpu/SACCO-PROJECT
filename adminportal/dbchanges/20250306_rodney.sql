CREATE TABLE member_completed_transactions (
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `member_id` BIGINT UNSIGNED,
    `transaction_log_id` BIGINT UNSIGNED,
    `narrative` VARCHAR(255) NOT NULL DEFAULT '',
    `amount` DOUBLE DEFAULT 0,
    `balance_before` DOUBLE DEFAULT 0,
    `balance_after` DOUBLE DEFAULT 0,
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    `updated_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    foreign key `FK_member_completed_transactions_tx_log` (`transaction_log_id`) REFERENCES `transaction_log`(`id`)
)Engine = Innodb;