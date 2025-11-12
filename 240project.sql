-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cert`
--

DROP TABLE IF EXISTS `cert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cert` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `cert_body` text,
  `cost` decimal(6,2) DEFAULT NULL,
  `requirements` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cert`
--

LOCK TABLES `cert` WRITE;
/*!40000 ALTER TABLE `cert` DISABLE KEYS */;
INSERT INTO `cert` VALUES (1,'Security+','CompTIA',425.00,'Exam'),(2,'Network+','CompTIA',390.00,'Exam'),(3,'A+','CompTIA',265.00,'Exam'),(4,'CAMP','IAITAM',2400.00,'Course and Exam'),(5,'CHAMP','IAITAM',2400.00,'Course and Exam'),(6,'CITAM','IAITAM',4200.00,'Course and Exam');
/*!40000 ALTER TABLE `cert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `industry` varchar(20) DEFAULT NULL,
  `location` text,
  `size` varchar(10) DEFAULT NULL,
  `website` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'Gr8ttek','Service','Cheyenne, WY','11-50','https://rksbh.com/'),(2,'Communication Resources','Service','5340 Moment Rd, Missoula, MT 59808','11-50','https://communicationres.com'),(3,'Univision Computers','Service','2925 Stockyard Rd, Unit A, Missoula, MT','11-50','https://univisioncomputers.com/'),(4,'Glacier Bancorp','Banking','Kalispell, MT','1000-5000','https://www.gbcijobs.com/');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(14) DEFAULT NULL,
  `name` text,
  `position` text,
  `company` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email_2` (`email`),
  KEY `company` (`company`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`company`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,NULL,'833-878-4GR8',NULL,NULL,1),(2,NULL,'406-327-5013',NULL,NULL,2),(3,NULL,'1-800-597-6623',NULL,NULL,3);
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contract`
--

DROP TABLE IF EXISTS `contract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract` (
  `id` int DEFAULT NULL,
  `terms` text,
  `schedule` text,
  `pay` text,
  KEY `id` (`id`),
  CONSTRAINT `contract_ibfk_1` FOREIGN KEY (`id`) REFERENCES `job` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contract`
--

LOCK TABLES `contract` WRITE;
/*!40000 ALTER TABLE `contract` DISABLE KEYS */;
/*!40000 ALTER TABLE `contract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `full_time`
--

DROP TABLE IF EXISTS `full_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `full_time` (
  `id` int DEFAULT NULL,
  `hourly` decimal(4,2) DEFAULT NULL,
  `benefits` text,
  `schedule` text,
  KEY `id` (`id`),
  CONSTRAINT `full_time_ibfk_1` FOREIGN KEY (`id`) REFERENCES `job` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `full_time`
--

LOCK TABLES `full_time` WRITE;
/*!40000 ALTER TABLE `full_time` DISABLE KEYS */;
INSERT INTO `full_time` VALUES (2,25.00,NULL,NULL),(3,20.00,'Health, Vision, Retirement, Dental, Dog-Friendly','Flexibile'),(4,25.00,NULL,NULL);
/*!40000 ALTER TABLE `full_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `post_date` date DEFAULT NULL,
  `close_date` date DEFAULT NULL,
  `hyperlink` text,
  `company` int NOT NULL,
  `role` int DEFAULT NULL,
  `contact` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_job_company` (`company`),
  KEY `fk_job_role` (`role`),
  KEY `fk_job_contact` (`contact`),
  CONSTRAINT `fk_job_company` FOREIGN KEY (`company`) REFERENCES `company` (`id`),
  CONSTRAINT `fk_job_contact` FOREIGN KEY (`contact`) REFERENCES `contact` (`id`),
  CONSTRAINT `fk_job_role` FOREIGN KEY (`role`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
INSERT INTO `job` VALUES (1,'IT Field Support Technician',NULL,NULL,'https://www.indeed.com/viewjob?jk=a8a0cd53e59070b2&tk=1j5uqq318gooq8bg&from=serp&vjs=3',1,1,1),(2,'IT Help Desk – Tier 2',NULL,NULL,'https://communicationresources.bamboohr.com/careers/61',2,1,2),(3,'IT Technician',NULL,NULL,'https://www.indeed.com/viewjob?jk=b287a4df7f7c7e71&tk=1j5uqq318gooq8bg&from=serp&vjs=3',3,1,3),(4,'CRP Hardware Asset Manager',NULL,NULL,'https://www.indeed.com/viewjob?jk=093eb526c87964ed&tk=1j5uqq318gooq8bg&from=serp&vjs=3',4,2,NULL);
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_cert`
--

DROP TABLE IF EXISTS `job_cert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_cert` (
  `job` int DEFAULT NULL,
  `cert` int DEFAULT NULL,
  KEY `job_id` (`job`),
  KEY `cert_id` (`cert`),
  CONSTRAINT `job_cert_ibfk_1` FOREIGN KEY (`job`) REFERENCES `job` (`id`),
  CONSTRAINT `job_cert_ibfk_2` FOREIGN KEY (`cert`) REFERENCES `cert` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_cert`
--

LOCK TABLES `job_cert` WRITE;
/*!40000 ALTER TABLE `job_cert` DISABLE KEYS */;
INSERT INTO `job_cert` VALUES (4,4),(4,5),(4,6);
/*!40000 ALTER TABLE `job_cert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `part_time`
--

DROP TABLE IF EXISTS `part_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `part_time` (
  `id` int DEFAULT NULL,
  `hourly` decimal(4,2) DEFAULT NULL,
  `schedule` text,
  KEY `id` (`id`),
  CONSTRAINT `part_time_ibfk_1` FOREIGN KEY (`id`) REFERENCES `job` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `part_time`
--

LOCK TABLES `part_time` WRITE;
/*!40000 ALTER TABLE `part_time` DISABLE KEYS */;
INSERT INTO `part_time` VALUES (1,40.00,'On call?');
/*!40000 ALTER TABLE `part_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `avg_wage` decimal(5,2) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `title_2` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Computer Support Specialist',29.59,'Computer and information systems managers, often called information technology (IT) managers, plan, coordinate, and direct computer-related activities in an organization. They help determine the IT goals of an organization and are responsible for implementing computer systems to meet those goals.'),(2,'Computer and Information System Managers',82.31,'Computer and information systems managers, often called information technology (IT) managers, plan, coordinate, and direct computer-related activities in an organization. They help determine the IT goals of an organization and are responsible for implementing computer systems to meet those goals.'),(3,'Network and Computer Systems Administrators',46.54,'Network and computer systems administrators install, configure, and maintain organizations’ local area networks (LANs), wide area networks (WANs), data communication networks, operating systems, and servers.');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-12  0:58:20
