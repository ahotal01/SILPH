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
  `name` varchar(60) NOT NULL UNIQUE,
  `password` varchar(25) NOT NULL,
  `members` varchar(150) DEFAULT NULL,
  `discords` varchar(200) DEFAULT NULL,
  `puzzles_solved` int(2) DEFAULT 0,
  `hints_available` int(1) DEFAULT 0
);

--
-- Dumping data for table `teams`
--

INSERT INTO `teams` (`team_id`, `name`, `password`, `members`, `puzzles_solved`, `r1_points`, `r2_points`, `hints_available`) VALUES
(1, 'Eggplant Parms', 'aaaggimmnnr18', 'CheeseMuffin,Level51,lovemathboy,talkingtree,Teikoku', 'CheeseMuffin#5866,Level51#0375,lovemathboy#9877,talkingtree#1556,Teikoku#1077', '41', '9480', '9480', '0');

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
(1, `Double or Nothing`, `HAWAIIAN`, `5`, `0`),
(2, `Carthorse`, `CENTER STAGE`, `5`, `0`),
(3, `Bridging the Gap`, `ELECTRONVOLT`, `5`, `0`),
(4, `Ambidextrous`, `ALTERNATE`, `5`, `0`),
(5, `Sense of Belonging`, `SPANISH FLU`, `5`, `0`),
(6, `Blind Spots`, `SPEED READING`, `5`, `0`),
(7, `A Brief Oration`, `SPECTRAL THIEVES`, `1000`, `20`),
(11, `Fan Service`, `BOULTER`, `10`, `0`),
(12, `Gender Studies`, `RAIN DOWN`, `10`, `0`),
(13, `Namesakes`, `NOVEL CANON`, `10`, `0`),
(14, `Expansion`, `RECREATION`, `10`, `0`),
(15, `word f(ind)`, `ONE IS TOO MANY`, `12`, `10`),
(16, `CAP Contributor`, `BODY CAMOUFLAGE`, `14`, `20`),
(17, `Spacetime`, `HOBBLER`, `16`, `30`),
(18, `Building Bridges`, `FRIEND OR FOE`, `18`, `40`),
(19, `Up Against The Wall`, `GLACIS RAMPART`, `20`, `52`),
(20, `Basic Counting`, `FORESEE`, `22`, `66`),
(21, `Suspect Test`, `VILLAIN`, `24`, `82`),
(22, `World's Longest Port`, `SOUR GRAPES`, `26`, `100`),
(23, `Casting Call`, `MAKE LEATHER`, `28`, `120`),
(24, `Extremely Slow Cookie Clicker`, `WEALTHY`, `30`, `142`),
(25, `A Wrinkle in Time`, `ACETONE`, `32`, `166`),
(26, `Crazy Bracket`, `CLASSIC ARCADE GAMES`, `34`, `192`),
(27, `The Final Battle`, `THE ELDER SCROLLER`, `1000`, `220`);

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
