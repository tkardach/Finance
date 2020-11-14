-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: finance_test
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `balance` decimal(15,2) NOT NULL DEFAULT '0.00',
  `name` varchar(45) NOT NULL,
  `profile` int NOT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `unique_id` (`account_id`),
  KEY `FK_Profile_idx` (`profile`),
  CONSTRAINT `FK_Profile` FOREIGN KEY (`profile`) REFERENCES `profile` (`profile_id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile` (
  `profile_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`profile_id`),
  UNIQUE KEY `unique_email` (`email`),
  UNIQUE KEY `unique_id` (`profile_id`)
) ENGINE=InnoDB AUTO_INCREMENT=547 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recurring_transaction`
--

DROP TABLE IF EXISTS `recurring_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recurring_transaction` (
  `recurring_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `start_date` datetime NOT NULL,
  `timespan` varchar(45) NOT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `to_account` int NOT NULL,
  `from_account` int NOT NULL,
  PRIMARY KEY (`recurring_id`),
  UNIQUE KEY `unique_id` (`recurring_id`),
  KEY `FK_Account_idx` (`to_account`),
  KEY `FK_FromAccount_idx` (`from_account`),
  CONSTRAINT `FK_FromAccount` FOREIGN KEY (`from_account`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_ToAccount` FOREIGN KEY (`to_account`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `single_transaction`
--

DROP TABLE IF EXISTS `single_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `single_transaction` (
  `single_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `date` datetime NOT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `to_account` int NOT NULL,
  `from_account` int NOT NULL,
  PRIMARY KEY (`single_id`),
  UNIQUE KEY `unique_id` (`single_id`),
  KEY `FK_ToAccount_idx` (`to_account`),
  KEY `FK_FromAccount_idx` (`from_account`),
  CONSTRAINT `FK_FromAccount_single` FOREIGN KEY (`from_account`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_ToAccount_single` FOREIGN KEY (`to_account`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-13  9:33:41
