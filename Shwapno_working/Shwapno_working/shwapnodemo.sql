-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 21, 2019 at 12:47 PM
-- Server version: 10.1.25-MariaDB
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shwapnodemo`
--

-- --------------------------------------------------------

--
-- Table structure for table `appliancecontrol`
--

CREATE TABLE `appliancecontrol` (
  `appliance_control_id` int(11) NOT NULL,
  `appliance_dev_id` varchar(100) NOT NULL,
  `appliance_current_status` varchar(10) NOT NULL,
  `appliance_updated_at` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `pwrcnsmpdata`
--

CREATE TABLE `pwrcnsmpdata` (
  `pwr_id` int(11) NOT NULL,
  `pwr_dev_id` varchar(50) NOT NULL,
  `pwr_cnsm_rate` varchar(50) NOT NULL,
  `pwr_current_status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tempsensordata`
--

CREATE TABLE `tempsensordata` (
  `temp_sensor_serial` int(11) NOT NULL,
  `temp_dev_id` varchar(100) NOT NULL,
  `temp_dev_data` varchar(100) NOT NULL,
  `updated_at` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `userinfo`
--

CREATE TABLE `userinfo` (
  `id_number` int(11) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `pass_word` varchar(50) NOT NULL,
  `e_mail` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appliancecontrol`
--
ALTER TABLE `appliancecontrol`
  ADD PRIMARY KEY (`appliance_control_id`);

--
-- Indexes for table `pwrcnsmpdata`
--
ALTER TABLE `pwrcnsmpdata`
  ADD PRIMARY KEY (`pwr_id`);

--
-- Indexes for table `tempsensordata`
--
ALTER TABLE `tempsensordata`
  ADD PRIMARY KEY (`temp_sensor_serial`);

--
-- Indexes for table `userinfo`
--
ALTER TABLE `userinfo`
  ADD PRIMARY KEY (`id_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appliancecontrol`
--
ALTER TABLE `appliancecontrol`
  MODIFY `appliance_control_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pwrcnsmpdata`
--
ALTER TABLE `pwrcnsmpdata`
  MODIFY `pwr_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tempsensordata`
--
ALTER TABLE `tempsensordata`
  MODIFY `temp_sensor_serial` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `userinfo`
--
ALTER TABLE `userinfo`
  MODIFY `id_number` int(11) NOT NULL AUTO_INCREMENT;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
