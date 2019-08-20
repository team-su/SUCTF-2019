
create database CTF;
use CTF;
-- phpMyAdmin SQL Dump
-- version 4.7.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 02, 2018 at 03:18 PM
-- Server version: 5.6.35
-- PHP Version: 7.0.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `SUCTF`
--

-- --------------------------------------------------------

--
-- Table structure for table `Flag`
--

CREATE TABLE `Flag` (
  `Flag` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Flag`
--

INSERT INTO `Flag` (`Flag`) VALUES
('SUCTF{SUCTF_baby_sql_chall_120993n810h3}');

