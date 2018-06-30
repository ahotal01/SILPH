-- phpMyAdmin SQL Dump
-- version 4.4.15.5
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1:8889
-- Generation Time: June 18, 2018 at 10:07 PM
-- Server version: 5.6.34-log
-- PHP Version: 7.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `puzzle-hunter`
--

-- --------------------------------------------------------

--
-- Table structure for table `teams`
--

CREATE TABLE IF NOT EXISTS `teams` (
  `team_id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(20) NOT NULL UNIQUE,
  `password` varchar(25) NOT NULL,
  `members` varchar(600) DEFAULT NULL,
  `puzzles_solved` int(2) DEFAULT 0,
  `hints_available` int(1) DEFAULT 0
);

--
-- Dumping data for table `teams`
--

INSERT INTO `teams` (`team_id`, `name`, `password`, `members`, `puzzles_solved`, `hints_available`) VALUES
(1, 'Eggplant Parms', 'aaaggimmnnr18', 'CheeseMuffin#5866,Level51#0375,lovemathboy#9877,talkingtree#1556,Teikoku#1077', '41', '0');

-- --------------------------------------------------------

--
-- Table structure for table `puzzles`
--

CREATE TABLE IF NOT EXISTS `puzzles` (
  `puzzle_id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(60) DEFAULT NULL,
  `answer` varchar(60) DEFAULT NULL,
  `value` int(11) DEFAULT 0,
  `prerequisite` int(11) DEFAULT 0
);

--
-- Dumping data for table `puzzles`
--

INSERT INTO `puzzles` (`puzzle_id`, `name`, `answer`, `value`, `prerequisite`) VALUES
(1, 'Thirty-Minute Puzzle', 'HAWAIIAN', '10', `0`),
(2, 'Carthorse', 'CENTER STAGE', '10', '0'),
(3, 'Bridging the Gap', 'ELECTRONVOLT', '10', '0'),
(4, 'Expansion', 'ALTERNATE', '10', '0'),
(5, 'Sense of Belonging', 'SPANISH FLU', '10', '0'),
(6, 'Blind Spots', 'SPEED READING', '10', '0'),
(7, 'Soul of Wit', 'SPECTRAL THIEVES', '20', '40');

-- --------------------------------------------------------

--
-- Table structure for table `submissions`
--

CREATE TABLE IF NOT EXISTS `submissions` (
  `submission_id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `team_id` int(11) NOT NULL,
  `puzzle_id` int(11) NOT NULL,
  `answer` varchar(25) DEFAULT NULL,
  `correct` int(1) DEFAULT 0,
  `time_submitted` DATETIME
);

-- --------------------------------------------------------

--
-- Constraints for dumped tables
--

--
-- Constraints for table `submissions`
--
ALTER TABLE `submissions`
  ADD CONSTRAINT `submissions_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`),
  ADD CONSTRAINT `submissions_ibfk_2` FOREIGN KEY (`puzzle_id`) REFERENCES `puzzles` (`puzzle_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
