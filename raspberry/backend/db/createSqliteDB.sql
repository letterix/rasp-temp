DROP TABLE IF EXISTS `sync_queue`;
CREATE TABLE  `sync_queue` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `installation` varchar(100) NOT NULL,
  `table` varchar(100) NOT NULL,
  `method` varchar(100) NOT NULL,
  `data` TEXT NOT NULL,
  `prev` TEXT DEFAULT NULL,
  `last_sync_attempt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`installation`)
)