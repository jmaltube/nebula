-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 17, 2016 at 11:04 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pampero`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=46 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add abastecimiento', 7, 'add_abastecimiento'),
(20, 'Can change abastecimiento', 7, 'change_abastecimiento'),
(21, 'Can delete abastecimiento', 7, 'delete_abastecimiento'),
(22, 'Can add marca', 8, 'add_marca'),
(23, 'Can change marca', 8, 'change_marca'),
(24, 'Can delete marca', 8, 'delete_marca'),
(25, 'Can add clasificador', 9, 'add_clasificador'),
(26, 'Can change clasificador', 9, 'change_clasificador'),
(27, 'Can delete clasificador', 9, 'delete_clasificador'),
(28, 'Can add bien', 10, 'add_bien'),
(29, 'Can change bien', 10, 'change_bien'),
(30, 'Can delete bien', 10, 'delete_bien'),
(31, 'Can add proveedor', 11, 'add_proveedor'),
(32, 'Can change proveedor', 11, 'change_proveedor'),
(33, 'Can delete proveedor', 11, 'delete_proveedor'),
(34, 'Can add compra', 12, 'add_compra'),
(35, 'Can change compra', 12, 'change_compra'),
(36, 'Can delete compra', 12, 'delete_compra'),
(37, 'Can add lista', 13, 'add_lista'),
(38, 'Can change lista', 13, 'change_lista'),
(39, 'Can delete lista', 13, 'delete_lista'),
(40, 'Can add lista y bien', 14, 'add_listaybien'),
(41, 'Can change lista y bien', 14, 'change_listaybien'),
(42, 'Can delete lista y bien', 14, 'delete_listaybien'),
(43, 'Can add lista y clasificador', 15, 'add_listayclasificador'),
(44, 'Can change lista y clasificador', 15, 'change_listayclasificador'),
(45, 'Can delete lista y clasificador', 15, 'delete_listayclasificador');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$24000$zyTU9xMzrEWk$GXC+64kVLl9RrZ8WkZdeGo5b46cDdyjGFigO3DyXaOM=', '2016-03-18 02:00:15', 1, 'nebula', '', '', '', 1, 1, '2016-03-18 02:00:02');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_abastecimiento`
--

CREATE TABLE IF NOT EXISTS `bienes_app_abastecimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `denominacion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_bien`
--

CREATE TABLE IF NOT EXISTS `bienes_app_bien` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL,
  `denominacion` varchar(100) NOT NULL,
  `unidad` varchar(5) NOT NULL,
  `importado` tinyint(1) NOT NULL,
  `sin_stock` tinyint(1) NOT NULL,
  `bulto` decimal(7,2) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `clasificador_id` int(11) NOT NULL,
  `forma_abastecimiento_id` int(11) NOT NULL,
  `marca_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bienes_app_bien_a2353d82` (`clasificador_id`),
  KEY `bienes_app_bien_3195fe4a` (`forma_abastecimiento_id`),
  KEY `bienes_app_bien_bbec06df` (`marca_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_clasificador`
--

CREATE TABLE IF NOT EXISTS `bienes_app_clasificador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `denominacion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_compra`
--

CREATE TABLE IF NOT EXISTS `bienes_app_compra` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_costeo` tinyint(1) NOT NULL,
  `ultima_fecha` date NOT NULL,
  `costo1` decimal(7,2) NOT NULL,
  `moneda_costo1` varchar(3) NOT NULL,
  `plazo_entrega` smallint(5) unsigned NOT NULL,
  `bien_id` int(11) NOT NULL,
  `proveedor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bienes_app_compra_proveedor_id_014e5d6a_uniq` (`proveedor_id`,`bien_id`),
  KEY `bienes_app_compra_bien_id_a6c6ed52_fk_bienes_app_bien_id` (`bien_id`),
  KEY `bienes_app_compra_7ac33b97` (`proveedor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_lista`
--

CREATE TABLE IF NOT EXISTS `bienes_app_lista` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `tipo` varchar(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_listaybien`
--

CREATE TABLE IF NOT EXISTS `bienes_app_listaybien` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descuento` decimal(3,2) NOT NULL,
  `visible` tinyint(1) NOT NULL,
  `bien_id` int(11) NOT NULL,
  `lista_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bienes_app_listaybien_bien_id_c7c32269_fk_bienes_app_bien_id` (`bien_id`),
  KEY `bienes_app_listaybien_lista_id_3f078a8e_fk_bienes_app_lista_id` (`lista_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_listayclasificador`
--

CREATE TABLE IF NOT EXISTS `bienes_app_listayclasificador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descuento` decimal(3,2) NOT NULL,
  `visible` tinyint(1) NOT NULL,
  `clasificador_id` int(11) NOT NULL,
  `lista_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bienes_ap_clasificador_id_4bd9a67d_fk_bienes_app_clasificador_id` (`clasificador_id`),
  KEY `bienes_app_listayclasif_lista_id_b0a9b3b2_fk_bienes_app_lista_id` (`lista_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_marca`
--

CREATE TABLE IF NOT EXISTS `bienes_app_marca` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `denominacion` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `bienes_app_proveedor`
--

CREATE TABLE IF NOT EXISTS `bienes_app_proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `contacto` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(7, 'bienes_app', 'abastecimiento'),
(10, 'bienes_app', 'bien'),
(9, 'bienes_app', 'clasificador'),
(12, 'bienes_app', 'compra'),
(13, 'bienes_app', 'lista'),
(14, 'bienes_app', 'listaybien'),
(15, 'bienes_app', 'listayclasificador'),
(8, 'bienes_app', 'marca'),
(11, 'bienes_app', 'proveedor'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2016-03-18 01:59:39'),
(2, 'auth', '0001_initial', '2016-03-18 01:59:41'),
(3, 'admin', '0001_initial', '2016-03-18 01:59:42'),
(4, 'admin', '0002_logentry_remove_auto_add', '2016-03-18 01:59:42'),
(5, 'contenttypes', '0002_remove_content_type_name', '2016-03-18 01:59:42'),
(6, 'auth', '0002_alter_permission_name_max_length', '2016-03-18 01:59:42'),
(7, 'auth', '0003_alter_user_email_max_length', '2016-03-18 01:59:42'),
(8, 'auth', '0004_alter_user_username_opts', '2016-03-18 01:59:43'),
(9, 'auth', '0005_alter_user_last_login_null', '2016-03-18 01:59:43'),
(10, 'auth', '0006_require_contenttypes_0002', '2016-03-18 01:59:43'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2016-03-18 01:59:43'),
(12, 'bienes_app', '0001_initial', '2016-03-18 01:59:47'),
(13, 'sessions', '0001_initial', '2016-03-18 01:59:47'),
(14, 'auth', '0001_squashed_0001_initial', '2016-03-18 01:59:47');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ni3bdwitkfhuc8220d7isb4pq63skary', 'Y2M2N2FlMjYzZWEwYjBkMmVjODVlYjkwYzhmMjM2NmEzNmFjNjExMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImI3N2NkNDA0YTVkOTlhNTlkYWJmYzgxOGFhZWRmNTUxMDFlMWNlYTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-04-01 02:00:15');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `bienes_app_bien`
--
ALTER TABLE `bienes_app_bien`
  ADD CONSTRAINT `bienes_app_bien_marca_id_6408d93f_fk_bienes_app_marca_id` FOREIGN KEY (`marca_id`) REFERENCES `bienes_app_marca` (`id`),
  ADD CONSTRAINT `bienes_ap_clasificador_id_ca358e99_fk_bienes_app_clasificador_id` FOREIGN KEY (`clasificador_id`) REFERENCES `bienes_app_clasificador` (`id`),
  ADD CONSTRAINT `D7a91d34616104c1435df7800901e399` FOREIGN KEY (`forma_abastecimiento_id`) REFERENCES `bienes_app_abastecimiento` (`id`);

--
-- Constraints for table `bienes_app_compra`
--
ALTER TABLE `bienes_app_compra`
  ADD CONSTRAINT `bienes_app_comp_proveedor_id_7225fc9d_fk_bienes_app_proveedor_id` FOREIGN KEY (`proveedor_id`) REFERENCES `bienes_app_proveedor` (`id`),
  ADD CONSTRAINT `bienes_app_compra_bien_id_a6c6ed52_fk_bienes_app_bien_id` FOREIGN KEY (`bien_id`) REFERENCES `bienes_app_bien` (`id`);

--
-- Constraints for table `bienes_app_listaybien`
--
ALTER TABLE `bienes_app_listaybien`
  ADD CONSTRAINT `bienes_app_listaybien_lista_id_3f078a8e_fk_bienes_app_lista_id` FOREIGN KEY (`lista_id`) REFERENCES `bienes_app_lista` (`id`),
  ADD CONSTRAINT `bienes_app_listaybien_bien_id_c7c32269_fk_bienes_app_bien_id` FOREIGN KEY (`bien_id`) REFERENCES `bienes_app_bien` (`id`);

--
-- Constraints for table `bienes_app_listayclasificador`
--
ALTER TABLE `bienes_app_listayclasificador`
  ADD CONSTRAINT `bienes_app_listayclasif_lista_id_b0a9b3b2_fk_bienes_app_lista_id` FOREIGN KEY (`lista_id`) REFERENCES `bienes_app_lista` (`id`),
  ADD CONSTRAINT `bienes_ap_clasificador_id_4bd9a67d_fk_bienes_app_clasificador_id` FOREIGN KEY (`clasificador_id`) REFERENCES `bienes_app_clasificador` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
