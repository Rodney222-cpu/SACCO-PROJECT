ALTER TABLE `sacco_member` ADD COLUMN `password` VARCHAR(250) NOT NULL DEFAULT '';
ALTER TABLE `sacco_member` ADD CONSTRAINT `UK_sacco_member_sacco_id_email` UNIQUE KEY `UK_sacco_member_sacco_id_email`(`sacco_id`,`email`);
ALTER TABLE `sacco_member` ADD CONSTRAINT `UK_sacco_member_sacco_id_phone` UNIQUE KEY `UK_sacco_member_sacco_id_phone`(`sacco_id`,`phone`);


