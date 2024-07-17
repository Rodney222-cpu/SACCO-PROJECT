CREATE TABLE `acg_privilege`(
    `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `acg_id` BIGINT UNSIGNED,
    `privilege_name` VARCHAR(255) NOT NULL DEFAULT '',
    `created_on` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `UK_unique_privilege` (`acg_id`,`privilege_name`)
) Engine = Innodb;