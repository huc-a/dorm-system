DROP TABLE IF EXISTS `bed`;
CREATE TABLE `bed` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bed_no` varchar(20) NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `room_id` bigint DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK115cuh725wpbt8yxq2lvgg1c9` (`room_id`),
  KEY `FKawvg73odc61efa14yxmosiyn4` (`student_id`),
  CONSTRAINT `FK115cuh725wpbt8yxq2lvgg1c9` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `FKawvg73odc61efa14yxmosiyn4` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `building`;
CREATE TABLE `building` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(255) DEFAULT NULL,
  `code` varchar(20) NOT NULL,
  `floors` int DEFAULT NULL,
  `gender_type` varchar(255) DEFAULT NULL,
  `manager_name` varchar(255) DEFAULT NULL,
  `manager_phone` varchar(255) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKm2ikyg87gkvutwrl9shac57ce` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `check_in`;
CREATE TABLE `check_in` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `check_in_date` date DEFAULT NULL,
  `check_out_date` date DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `bed_id` bigint DEFAULT NULL,
  `room_id` bigint DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK3l2h9mlq6yx9dkgiqwsha7vto` (`bed_id`),
  KEY `FKew8gg2tn8cg5oepw81kyag1i4` (`room_id`),
  KEY `FKdx65dx2qhtwbbb8j459wbuffs` (`student_id`),
  CONSTRAINT `FK3l2h9mlq6yx9dkgiqwsha7vto` FOREIGN KEY (`bed_id`) REFERENCES `bed` (`id`),
  CONSTRAINT `FKdx65dx2qhtwbbb8j459wbuffs` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `FKew8gg2tn8cg5oepw81kyag1i4` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `dorm_leave`;
CREATE TABLE `dorm_leave` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approve_remark` varchar(300) DEFAULT NULL,
  `approver` varchar(255) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `reason` varchar(500) DEFAULT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK9k3qpw314x4eg73gslhlgpwlc` (`student_id`),
  CONSTRAINT `FK9k3qpw314x4eg73gslhlgpwlc` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `fee`;
CREATE TABLE `fee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `due_date` date DEFAULT NULL,
  `electricity_fee` double DEFAULT NULL,
  `electricity_usage` double DEFAULT NULL,
  `pay_time` datetime(6) DEFAULT NULL,
  `period` varchar(10) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `water_fee` double DEFAULT NULL,
  `water_usage` double DEFAULT NULL,
  `room_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKjyitbjcb9nhu43mg6v0uysqvw` (`room_id`),
  CONSTRAINT `FKjyitbjcb9nhu43mg6v0uysqvw` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `hygiene`;
CREATE TABLE `hygiene` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bathroom_score` int DEFAULT NULL,
  `bed_score` int DEFAULT NULL,
  `check_date` date DEFAULT NULL,
  `desk_score` int DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  `ground_score` int DEFAULT NULL,
  `inspector` varchar(255) DEFAULT NULL,
  `remark` varchar(500) DEFAULT NULL,
  `score` int DEFAULT NULL,
  `room_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKev5i5oyn8n8r0544oyj39glpk` (`room_id`),
  CONSTRAINT `FKev5i5oyn8n8r0544oyj39glpk` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` varchar(5000) DEFAULT NULL,
  `publish_time` datetime(6) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `top` bit(1) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `repair`;
CREATE TABLE `repair` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `finish_time` datetime(6) DEFAULT NULL,
  `priority` varchar(255) DEFAULT NULL,
  `repairer` varchar(255) DEFAULT NULL,
  `result` varchar(500) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `room_id` bigint DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK1qewet25idbwsejhube8wjqey` (`room_id`),
  KEY `FK82t490hpytnp9cfdwfes9u4ho` (`student_id`),
  CONSTRAINT `FK1qewet25idbwsejhube8wjqey` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`),
  CONSTRAINT `FK82t490hpytnp9cfdwfes9u4ho` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `room`;
CREATE TABLE `room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `capacity` int DEFAULT NULL,
  `facilities` varchar(255) DEFAULT NULL,
  `floor` int DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `room_no` varchar(20) NOT NULL,
  `room_type` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `building_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK4kmfw73x2vpfymk0ml875rh2q` (`building_id`),
  CONSTRAINT `FK4kmfw73x2vpfymk0ml875rh2q` FOREIGN KEY (`building_id`) REFERENCES `building` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `class_name` varchar(255) DEFAULT NULL,
  `college` varchar(255) DEFAULT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `id_card` varchar(255) DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `student_no` varchar(20) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UKah6pnqt97bv1fcv5bv512fc0f` (`student_no`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `real_name` varchar(255) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `status` int DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK51bvuyvihefoh4kp5syh2jpi4` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS `visitor`;
CREATE TABLE `visitor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_card` varchar(255) DEFAULT NULL,
  `leave_time` datetime(6) DEFAULT NULL,
  `reason` varchar(300) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `visit_time` datetime(6) DEFAULT NULL,
  `visitor_name` varchar(50) NOT NULL,
  `visitor_phone` varchar(255) DEFAULT NULL,
  `room_id` bigint DEFAULT NULL,
  `student_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKg64dp8mjkhxijv1vwsaabu0o0` (`room_id`),
  KEY `FK1yjsybg516vyxav6aq7jo3fkr` (`student_id`),
  CONSTRAINT `FK1yjsybg516vyxav6aq7jo3fkr` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `FKg64dp8mjkhxijv1vwsaabu0o0` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
