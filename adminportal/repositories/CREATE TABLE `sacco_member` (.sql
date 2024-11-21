CREATE TABLE `sacco_member` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `sacco_id` bigint unsigned DEFAULT NULL,
  `account_number` varchar(255) NOT NULL DEFAULT '',
  `fname` varchar(255) NOT NULL DEFAULT '',
  `lname` varchar(255) NOT NULL DEFAULT '',
  `gender` varchar(10) NOT NULL DEFAULT '',
  `phone` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `role` enum('CHAIRPERSON','TREASURER','SECRETARY','REGULAR MEMBER') NOT NULL DEFAULT 'REGULAR MEMBER',
  `balance` double DEFAULT '0',
  `next_of_kin_name` varchar(255) NOT NULL DEFAULT '',
  `date_of_birth` date DEFAULT NULL,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_sacco_unique_member_id` (`sacco_id`,`account_number`),
  CONSTRAINT `FK_sacco_member_sacco_id` FOREIGN KEY (`sacco_id`) REFERENCES `sacco` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;