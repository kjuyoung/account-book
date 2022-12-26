CREATE TABLE `accountbook_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `expenditure` varchar(255) NOT NULL,
  `memo` text NOT NULL,
  `create_date` datetime NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `modify_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_accountbook_table_id` (`id`),
  CONSTRAINT `accountbook_table_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;