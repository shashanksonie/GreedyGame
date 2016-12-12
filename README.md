# GreedyGame
Session Calculation

Please install mysql connector for python and change the MYSQL config as per the system.

Also, please create MYSQL TABLE using the below query -

CREATE TABLE `greedy` (
  `game_id` varchar(20) DEFAULT NULL,
  `ai5` varchar(32) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  `session_time` float DEFAULT NULL,
  `validity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
