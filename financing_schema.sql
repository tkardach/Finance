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
  `name` varchar(45) NOT NULL,
  `profile` int NOT NULL,
  `balance` decimal(15,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`name`,`profile`),
  UNIQUE KEY `unique_id` (`account_id`),
  KEY `FK_Profile_idx` (`profile`),
  CONSTRAINT `FK_Profile` FOREIGN KEY (`profile`) REFERENCES `profile` (`profile_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2573 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=3449 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recurring_transaction`
--

DROP TABLE IF EXISTS `recurring_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recurring_transaction` (
  `recurring_transaction_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `account` int NOT NULL,
  `start_date` datetime NOT NULL,
  `timespan` varchar(45) NOT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `to_account` int DEFAULT NULL,
  PRIMARY KEY (`recurring_transaction_id`),
  UNIQUE KEY `transaction_id_UNIQUE` (`recurring_transaction_id`),
  KEY `FK_FromAccount_idx` (`account`),
  KEY `FK_ToAccount_recurring_idx` (`to_account`),
  CONSTRAINT `FK_Account_recurring` FOREIGN KEY (`account`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_ToAccount_recurring` FOREIGN KEY (`to_account`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `single_transaction`
--

DROP TABLE IF EXISTS `single_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `single_transaction` (
  `single_transaction_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `account` int NOT NULL,
  `date` datetime NOT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `to_account` int DEFAULT NULL,
  PRIMARY KEY (`single_transaction_id`),
  UNIQUE KEY `single_transaction_id_UNIQUE` (`single_transaction_id`),
  KEY `FK_ToAccount_idx` (`account`),
  KEY `FK_ToAccount_single_idx` (`to_account`),
  CONSTRAINT `FK_Account_single` FOREIGN KEY (`account`) REFERENCES `account` (`account_id`),
  CONSTRAINT `FK_ToAccount_single` FOREIGN KEY (`to_account`) REFERENCES `account` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=419 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-13 16:42:39
