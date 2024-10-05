-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: constructal_automate_verification_cases
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add plate',7,'add_plate'),(26,'Can change plate',7,'change_plate'),(27,'Can delete plate',7,'delete_plate'),(28,'Can view plate',7,'view_plate'),(29,'Can add stiffened plate',8,'add_stiffenedplate'),(30,'Can change stiffened plate',8,'change_stiffenedplate'),(31,'Can delete stiffened plate',8,'delete_stiffenedplate'),(32,'Can view stiffened plate',8,'view_stiffenedplate'),(33,'Can add biaxial elastic buckling',9,'add_biaxialelasticbuckling'),(34,'Can change biaxial elastic buckling',9,'change_biaxialelasticbuckling'),(35,'Can delete biaxial elastic buckling',9,'delete_biaxialelasticbuckling'),(36,'Can view biaxial elastic buckling',9,'view_biaxialelasticbuckling'),(37,'Can add material',10,'add_material'),(38,'Can change material',10,'change_material'),(39,'Can delete material',10,'delete_material'),(40,'Can view material',10,'view_material'),(41,'Can add stiffened plate analysis',11,'add_stiffenedplateanalysis'),(42,'Can change stiffened plate analysis',11,'change_stiffenedplateanalysis'),(43,'Can delete stiffened plate analysis',11,'delete_stiffenedplateanalysis'),(44,'Can view stiffened plate analysis',11,'view_stiffenedplateanalysis'),(45,'Can add elastic buckling',9,'add_elasticbuckling'),(46,'Can change elastic buckling',9,'change_elasticbuckling'),(47,'Can delete elastic buckling',9,'delete_elasticbuckling'),(48,'Can view elastic buckling',9,'view_elasticbuckling'),(49,'Can add buckling type',12,'add_bucklingtype'),(50,'Can change buckling type',12,'change_bucklingtype'),(51,'Can delete buckling type',12,'delete_bucklingtype'),(52,'Can view buckling type',12,'view_bucklingtype'),(53,'Can add processing status',13,'add_processingstatus'),(54,'Can change processing status',13,'change_processingstatus'),(55,'Can delete processing status',13,'delete_processingstatus'),(56,'Can view processing status',13,'view_processingstatus'),(57,'Can add buckling load type',12,'add_bucklingloadtype'),(58,'Can change buckling load type',12,'change_bucklingloadtype'),(59,'Can delete buckling load type',12,'delete_bucklingloadtype'),(60,'Can view buckling load type',12,'view_bucklingloadtype'),(61,'Can add elasto plastic buckling',14,'add_elastoplasticbuckling'),(62,'Can change elasto plastic buckling',14,'change_elastoplasticbuckling'),(63,'Can delete elasto plastic buckling',14,'delete_elastoplasticbuckling'),(64,'Can view elasto plastic buckling',14,'view_elastoplasticbuckling');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$W7G7YqCLkrdtxJyLS7unKh$JiU9+jj9c249C0G0fhu21EEtL6K1zimsRNLxvGentg4=','2024-06-23 14:34:33.211029',1,'andreiflancanova','','','andreiflancanova@hotmail.com',1,1,'2024-04-25 03:15:38.457814');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_bucklingloadtype`
--

DROP TABLE IF EXISTS `cbeb_bucklingloadtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_bucklingloadtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_bucklingloadtype`
--

LOCK TABLES `cbeb_bucklingloadtype` WRITE;
/*!40000 ALTER TABLE `cbeb_bucklingloadtype` DISABLE KEYS */;
INSERT INTO `cbeb_bucklingloadtype` VALUES (1,'1A'),(2,'2A');
/*!40000 ALTER TABLE `cbeb_bucklingloadtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_elasticbuckling`
--

DROP TABLE IF EXISTS `cbeb_elasticbuckling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_elasticbuckling` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `csi_y` decimal(4,3) NOT NULL,
  `n_cr` decimal(7,2) DEFAULT NULL,
  `sigma_cr` decimal(7,2) DEFAULT NULL,
  `w_center` decimal(8,4) DEFAULT NULL,
  `stiffened_plate_analysis_id` bigint NOT NULL,
  `n_x` decimal(7,3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cbeb_biaxialelasticb_stiffened_plate_anal_5dc6f4e4_fk_cbeb_stif` (`stiffened_plate_analysis_id`),
  CONSTRAINT `cbeb_biaxialelasticb_stiffened_plate_anal_5dc6f4e4_fk_cbeb_stif` FOREIGN KEY (`stiffened_plate_analysis_id`) REFERENCES `cbeb_stiffenedplateanalysis` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_elasticbuckling`
--

LOCK TABLES `cbeb_elasticbuckling` WRITE;
/*!40000 ALTER TABLE `cbeb_elasticbuckling` DISABLE KEYS */;
INSERT INTO `cbeb_elasticbuckling` VALUES (1,1.000,13137.56,729.86,0.0008,1,1.000),(2,1.000,9255.97,514.22,0.0009,2,1.000),(3,1.000,7660.87,425.60,0.0010,3,1.000),(4,1.000,6969.02,387.17,0.0010,4,1.000),(5,1.000,6351.87,352.88,0.0011,5,1.000),(6,1.000,6053.10,336.28,0.0011,6,1.000),(7,1.000,5194.75,288.60,0.0012,7,1.000),(8,1.000,5040.46,280.03,0.0012,8,1.000);
/*!40000 ALTER TABLE `cbeb_elasticbuckling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_elastoplasticbuckling`
--

DROP TABLE IF EXISTS `cbeb_elastoplasticbuckling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_elastoplasticbuckling` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `n_u` decimal(7,2) DEFAULT NULL,
  `sigma_u` decimal(7,2) DEFAULT NULL,
  `w_max` decimal(8,4) DEFAULT NULL,
  `w_dist_img_path` longtext,
  `von_mises_dist_img_path` longtext,
  `stiffened_plate_analysis_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cbeb_elastoplasticbu_stiffened_plate_anal_e6af66d9_fk_cbeb_stif` (`stiffened_plate_analysis_id`),
  CONSTRAINT `cbeb_elastoplasticbu_stiffened_plate_anal_e6af66d9_fk_cbeb_stif` FOREIGN KEY (`stiffened_plate_analysis_id`) REFERENCES `cbeb_stiffenedplateanalysis` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_elastoplasticbuckling`
--

LOCK TABLES `cbeb_elastoplasticbuckling` WRITE;
/*!40000 ALTER TABLE `cbeb_elastoplasticbuckling` DISABLE KEYS */;
/*!40000 ALTER TABLE `cbeb_elastoplasticbuckling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_material`
--

DROP TABLE IF EXISTS `cbeb_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_material` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` longtext,
  `young_modulus` decimal(8,2) NOT NULL,
  `poisson_ratio` decimal(4,3) NOT NULL,
  `yielding_stress` decimal(6,2) NOT NULL,
  `tang_modulus` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_material`
--

LOCK TABLES `cbeb_material` WRITE;
/*!40000 ALTER TABLE `cbeb_material` DISABLE KEYS */;
INSERT INTO `cbeb_material` VALUES (1,'Aço AH-36',210000.00,0.300,355.00,0.00),(2,'Aço de Alta Resistência (PISCOPO,2010)',206000.00,0.300,355.00,0.00);
/*!40000 ALTER TABLE `cbeb_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_processingstatus`
--

DROP TABLE IF EXISTS `cbeb_processingstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_processingstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_processingstatus`
--

LOCK TABLES `cbeb_processingstatus` WRITE;
/*!40000 ALTER TABLE `cbeb_processingstatus` DISABLE KEYS */;
INSERT INTO `cbeb_processingstatus` VALUES (1,'Pending'),(2,'Queued'),(3,'In Progress'),(4,'Completed'),(5,'Failed'),(6,'Cancelled');
/*!40000 ALTER TABLE `cbeb_processingstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cbeb_stiffenedplateanalysis`
--

DROP TABLE IF EXISTS `cbeb_stiffenedplateanalysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cbeb_stiffenedplateanalysis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mesh_size` decimal(4,1) NOT NULL,
  `analysis_dir_path` longtext,
  `analysis_rst_file_path` longtext,
  `case_study` longtext,
  `analysis_lgw_file_path` longtext,
  `material_id` bigint NOT NULL,
  `stiffened_plate_id` bigint NOT NULL,
  `num_elem` int unsigned DEFAULT NULL,
  `buckling_load_type_id` bigint NOT NULL,
  `elastic_buckling_status_id` bigint DEFAULT NULL,
  `elasto_plastic_buckling_status_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cbeb_stiffenedplatea_material_id_bb63e863_fk_cbeb_mate` (`material_id`),
  KEY `cbeb_stiffenedplatea_stiffened_plate_id_22674422_fk_csg_stiff` (`stiffened_plate_id`),
  KEY `cbeb_stiffenedplatea_buckling_load_type_i_42a7773c_fk_cbeb_buck` (`buckling_load_type_id`),
  KEY `cbeb_stiffenedplatea_elastic_buckling_sta_a4aad484_fk_cbeb_proc` (`elastic_buckling_status_id`),
  KEY `cbeb_stiffenedplatea_elastoplastic_buckli_3f863238_fk_cbeb_proc` (`elasto_plastic_buckling_status_id`),
  CONSTRAINT `cbeb_stiffenedplatea_buckling_load_type_i_42a7773c_fk_cbeb_buck` FOREIGN KEY (`buckling_load_type_id`) REFERENCES `cbeb_bucklingloadtype` (`id`),
  CONSTRAINT `cbeb_stiffenedplatea_elastic_buckling_sta_a4aad484_fk_cbeb_proc` FOREIGN KEY (`elastic_buckling_status_id`) REFERENCES `cbeb_processingstatus` (`id`),
  CONSTRAINT `cbeb_stiffenedplatea_elasto_plastic_buckl_019dc651_fk_cbeb_proc` FOREIGN KEY (`elasto_plastic_buckling_status_id`) REFERENCES `cbeb_processingstatus` (`id`),
  CONSTRAINT `cbeb_stiffenedplatea_material_id_bb63e863_fk_cbeb_mate` FOREIGN KEY (`material_id`) REFERENCES `cbeb_material` (`id`),
  CONSTRAINT `cbeb_stiffenedplatea_stiffened_plate_id_22674422_fk_csg_stiff` FOREIGN KEY (`stiffened_plate_id`) REFERENCES `csg_stiffenedplate` (`id`),
  CONSTRAINT `cbeb_stiffenedplateanalysis_chk_1` CHECK ((`num_elem` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cbeb_stiffenedplateanalysis`
--

LOCK TABLES `cbeb_stiffenedplateanalysis` WRITE;
/*!40000 ALTER TABLE `cbeb_stiffenedplateanalysis` DISABLE KEYS */;
INSERT INTO `cbeb_stiffenedplateanalysis` VALUES (1,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_6.60_SP_1','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_6.60_SP_1/phi_0.10_L_2_T_2_k_6.60_SP_1.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_6.60_SP_1/phi_0.10_L_2_T_2_k_6.60_SP_1.txt',1,1,6426,1,5,3),(2,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_2.93_SP_2','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_2.93_SP_2/phi_0.10_L_2_T_2_k_2.93_SP_2.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_2.93_SP_2/phi_0.10_L_2_T_2_k_2.93_SP_2.txt',1,2,6120,1,5,3),(3,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.65_SP_3','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.65_SP_3/phi_0.10_L_2_T_2_k_1.65_SP_3.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.65_SP_3/phi_0.10_L_2_T_2_k_1.65_SP_3.txt',1,3,5814,1,4,1),(4,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.08_SP_4','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.08_SP_4/phi_0.10_L_2_T_2_k_1.08_SP_4.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_1.08_SP_4/phi_0.10_L_2_T_2_k_1.08_SP_4.txt',1,4,5814,1,4,1),(5,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.73_SP_5','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.73_SP_5/phi_0.10_L_2_T_2_k_0.73_SP_5.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.73_SP_5/phi_0.10_L_2_T_2_k_0.73_SP_5.txt',1,5,5814,1,4,1),(6,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.54_SP_6','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.54_SP_6/phi_0.10_L_2_T_2_k_0.54_SP_6.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.54_SP_6/phi_0.10_L_2_T_2_k_0.54_SP_6.txt',1,6,5508,1,4,1),(7,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.40_SP_7','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.40_SP_7/phi_0.10_L_2_T_2_k_0.40_SP_7.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.40_SP_7/phi_0.10_L_2_T_2_k_0.40_SP_7.txt',1,7,5508,1,4,1),(8,20.0,'D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.31_SP_8','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.31_SP_8/phi_0.10_L_2_T_2_k_0.31_SP_8.rst','LIMA(2016)','D:/01_Mestrando_Andrei_PPGMC_2022/2024.1/constructal_automate_verification_cases/LIMA(2016)/phi_0.10_L_2_T_2_k_0.31_SP_8/phi_0.10_L_2_T_2_k_0.31_SP_8.txt',1,8,5508,1,4,1);
/*!40000 ALTER TABLE `cbeb_stiffenedplateanalysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `csg_plate`
--

DROP TABLE IF EXISTS `csg_plate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `csg_plate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `a` decimal(8,2) NOT NULL,
  `b` decimal(8,2) NOT NULL,
  `t_0` decimal(8,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `csg_plate`
--

LOCK TABLES `csg_plate` WRITE;
/*!40000 ALTER TABLE `csg_plate` DISABLE KEYS */;
INSERT INTO `csg_plate` VALUES (1,2000.00,1000.00,20.00),(6,250.00,1000.00,20.00),(7,1000.00,1000.00,20.00),(8,4000.00,1000.00,20.00);
/*!40000 ALTER TABLE `csg_plate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `csg_stiffenedplate`
--

DROP TABLE IF EXISTS `csg_stiffenedplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `csg_stiffenedplate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phi` decimal(5,4) NOT NULL,
  `N_ls` int NOT NULL,
  `N_ts` int NOT NULL,
  `k` decimal(6,3) NOT NULL,
  `t_1` decimal(6,2) DEFAULT NULL,
  `h_s` decimal(6,2) DEFAULT NULL,
  `t_s` decimal(6,2) DEFAULT NULL,
  `description` longtext,
  `plate_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `csg_stiffenedplate_plate_id_e2191f91_fk_csg_plate_id` (`plate_id`),
  CONSTRAINT `csg_stiffenedplate_plate_id_e2191f91_fk_csg_plate_id` FOREIGN KEY (`plate_id`) REFERENCES `csg_plate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `csg_stiffenedplate`
--

LOCK TABLES `csg_stiffenedplate` WRITE;
/*!40000 ALTER TABLE `csg_stiffenedplate` DISABLE KEYS */;
INSERT INTO `csg_stiffenedplate` VALUES (1,0.1000,2,2,6.600,18.00,66.00,10.00,'LIMA(2016)',1),(2,0.1000,2,2,2.933,18.00,44.00,15.00,'LIMA(2016)',1),(3,0.1000,2,2,1.650,18.00,33.00,20.00,'LIMA(2016)',1),(4,0.1000,2,2,1.080,18.00,27.00,25.00,'LIMA(2016)',1),(5,0.1000,2,2,0.733,18.00,22.00,30.00,'LIMA(2016)',1),(6,0.1000,2,2,0.543,18.00,19.00,35.00,'LIMA(2016)',1),(7,0.1000,2,2,0.400,18.00,16.00,40.00,'LIMA(2016)',1),(8,0.1000,2,2,0.311,18.00,14.00,45.00,'LIMA(2016)',1);
/*!40000 ALTER TABLE `csg_stiffenedplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(12,'cbeb','bucklingloadtype'),(9,'cbeb','elasticbuckling'),(14,'cbeb','elastoplasticbuckling'),(10,'cbeb','material'),(13,'cbeb','processingstatus'),(11,'cbeb','stiffenedplateanalysis'),(5,'contenttypes','contenttype'),(7,'csg','plate'),(8,'csg','stiffenedplate'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'csg','0001_initial','2024-04-25 02:45:33.081951'),(2,'contenttypes','0001_initial','2024-04-25 03:11:52.535347'),(3,'auth','0001_initial','2024-04-25 03:11:53.848477'),(4,'admin','0001_initial','2024-04-25 03:11:54.096862'),(5,'admin','0002_logentry_remove_auto_add','2024-04-25 03:11:54.112279'),(6,'admin','0003_logentry_add_action_flag_choices','2024-04-25 03:11:54.123315'),(7,'contenttypes','0002_remove_content_type_name','2024-04-25 03:11:54.260973'),(8,'auth','0002_alter_permission_name_max_length','2024-04-25 03:11:54.369122'),(9,'auth','0003_alter_user_email_max_length','2024-04-25 03:11:54.397142'),(10,'auth','0004_alter_user_username_opts','2024-04-25 03:11:54.407606'),(11,'auth','0005_alter_user_last_login_null','2024-04-25 03:11:54.503396'),(12,'auth','0006_require_contenttypes_0002','2024-04-25 03:11:54.510394'),(13,'auth','0007_alter_validators_add_error_messages','2024-04-25 03:11:54.521703'),(14,'auth','0008_alter_user_username_max_length','2024-04-25 03:11:54.639524'),(15,'auth','0009_alter_user_last_name_max_length','2024-04-25 03:11:54.744575'),(16,'auth','0010_alter_group_name_max_length','2024-04-25 03:11:54.774337'),(17,'auth','0011_update_proxy_permissions','2024-04-25 03:11:54.784911'),(18,'auth','0012_alter_user_first_name_max_length','2024-04-25 03:11:54.903219'),(19,'sessions','0001_initial','2024-04-25 03:11:54.977698'),(20,'csg','0002_stiffenedplate','2024-06-03 23:10:31.758789'),(21,'csg','0003_rename_plate_id_stiffenedplate_plate','2024-06-03 23:11:45.323351'),(22,'csg','0004_alter_stiffenedplate_h_s_alter_stiffenedplate_t_1_and_more','2024-06-04 00:46:27.872836'),(23,'cbeb','0001_initial','2024-07-06 20:21:44.991167'),(24,'cbeb','0002_rename_stiffened_plate_analysis_id_biaxialelasticbuckling_stiffened_plate_analysis_and_more','2024-07-06 20:24:10.389832'),(25,'cbeb','0003_rename_description_stiffenedplateanalysis_analysis_dir_path_and_more','2024-07-19 20:11:05.804371'),(26,'cbeb','0004_rename_poisson_ration_material_poisson_ratio','2024-07-24 00:04:52.029253'),(27,'cbeb','0005_biaxialelasticbuckling_n_x_and_more','2024-07-25 04:04:20.169132'),(28,'cbeb','0006_alter_biaxialelasticbuckling_n_cr_and_more','2024-07-25 04:21:38.033437'),(29,'cbeb','0007_rename_biaxialelasticbuckling_elasticbuckling','2024-08-05 02:22:54.812372'),(30,'cbeb','0008_rename_w_max_elasticbuckling_w_center','2024-08-05 04:02:52.253001'),(31,'cbeb','0009_material_tang_modulus','2024-08-08 22:05:05.185026'),(32,'cbeb','0010_bucklingtype_processingstatus','2024-08-09 15:01:33.780401'),(33,'cbeb','0011_rename_bucklingtype_bucklingloadtype','2024-08-09 15:36:08.358268'),(34,'cbeb','0012_stiffenedplateanalysis_buckling_load_type','2024-08-09 15:41:47.182736'),(35,'cbeb','0013_stiffenedplateanalysis_elastic_buckling_status_and_more','2024-08-09 15:41:47.528151'),(36,'cbeb','0014_rename_elastoplastic_buckling_status_stiffenedplateanalysis_elasto_plastic_buckling_status_and_more','2024-08-12 01:37:23.143660'),(37,'cbeb','0015_remove_elastoplasticbuckling_n_yield','2024-08-12 01:37:23.179280');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('tyeg5cbwfk3onx31vj210pwscohrpgyz','.eJxVjMEOwiAQRP-FsyElKyAevfsNhGV3pWpoUtpT479bkh50DnOYNzObimldSlwbz3EkdVVGnX4zTPnFtQN6pvqYdJ7qMo-oe0UftOn7RPy-Hd2_g5Ja6euzBwnoQhoIskNrBBKyOJuFBw8mWEsX8A4yBgECxsC77xIbrKjPF_8FORI:1sLOIb:XZjxOvJPmBV4oiTx0CUnQysT6tnJ36snEQ-OmHbN5EQ','2024-07-07 14:34:33.216015');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'constructal_automate_verification_cases'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-22 17:05:22
