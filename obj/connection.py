# -*- coding: utf-8 -*-
import MySQLdb
import config as configuration

class Connection:

    def __init__(self):
        self.db = MySQLdb.connect(host=configuration.dbhost,
                                  user=configuration.dbuser,
                                  passwd=configuration.dbpass,
                                  db=configuration.dbname,
                                  charset='utf8')

    def openCursor(self):
        self.cur = self.db.cursor()

    def closeConnection(self):
        self.db.close()

    def getAllAccountsData(self):
        array_resp = []
        sentense = self.createSelectAllSentense()
        self.cur.execute(sentense)
        for row in self.cur.fetchall():
            if not row[1] == "none":
                array_resp.append({
                    "consumerkey": row[1], "consumersecret": row[2],"accesstoken": row[3], "accesstokensecret": row[4],
                    "account": row[5], "key_word": row[6],"table": row[11], "publish_min": row[12],
                })
        return array_resp


    def getNewTweet(self, table):
        self.cur.execute(self.createSelectGetNewTweetSentense(table))
        for row in self.cur.fetchall():
            if not row[1] == "none":
                return {"id": row[0], "content": row[1]}
        return False

    def updateTweetStatus(self, table, id_tweet):
        self.cur.execute(self.updateTweetPublishSentense(table, id_tweet))
        self.cur.execute(self.updateTweetDatePubSentense(table, id_tweet))
        self.db.commit()
        return True

    def saveTweetsList(self, table, tweets_list):
        for one_tweet in tweets_list:
            self.cur.execute(self.insertTweetSentense(str(table), one_tweet.encode("utf-8")))
            self.db.commit()

    def createTable(self, table_account):
        try:
            self.cur.execute(self.createTableSentense(table_account))
            self.db.commit()
            return True
        except Exception as e:
            print "Error creating tables" + e

    def createTwitterAccountsTable(self):
        try:
            self.cur.execute(self.createTwitterAccountsTableSentense())
            self.db.commit()
            return True
        except Exception as e:
            print "Error creating table " + configuration.account_table
            return False

    def createTwitterAccountsTableSentense(self):
        return (
            "CREATE TABLE IF NOT EXISTS `%s` (" +
            "`id` int(11) NOT NULL AUTO_INCREMENT," +
            "`consumerkey` varchar(255) NOT NULL," +
            "`consumersecret` varchar(255) NOT NULL," +
            "`accesstoken` varchar(255) NOT NULL," +
            "`accesstokensecret` varchar(255) NOT NULL," +
            "`cuenta` varchar(255) NOT NULL," +
            "`palabra_clave` varchar(255) NOT NULL," +
            "`url_fb` varchar(255) NOT NULL," +
            "`fb_app_id` bigint(20) DEFAULT NULL," +
            "`fb_app_secret` varchar(200) DEFAULT NULL," +
            "`fb_token` varchar(200) DEFAULT NULL," +
            "`tabla` varchar(100) NOT NULL," +
            "`publicar_cada` int(11) NOT NULL DEFAULT '7'," +
            "PRIMARY KEY (`id`)" +
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        ) % (configuration.account_table)

    def createTableSentense(self, table_account):
        return ("CREATE TABLE IF NOT EXISTS `%s` (" +
            "`id` int(11) NOT NULL AUTO_INCREMENT," +
            "`content` varchar(150) NOT NULL," +
            "`created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"+
            "`published_date` timestamp NULL DEFAULT NULL,"+
            "`published` int(1) DEFAULT '0'," +
            "PRIMARY KEY (`id`)," +
            "UNIQUE KEY `content` (`content`)" +
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;") % (table_account)

    def createSelectGetNewTweetSentense(self, table):
        if not table == '':
            return 'SELECT * FROM `%s` WHERE `published` = 0 ORDER BY id ASC LIMIT 0,1;' % (table)
        return False

    def createSelectAllSentense(self):
        return 'SELECT * FROM `%s` WHERE 1;' % (configuration.account_table)

    def updateTweetPublishSentense(self,table, id_tweet):
        return 'UPDATE `%s` SET `published` = 1 WHERE `id` = %s' % (str(table), str(id_tweet))

    def updateTweetDatePubSentense(self,table, id_tweet):
        return 'UPDATE `%s` SET `published_date` = NOW() WHERE `id` = %s' % (str(table), str(id_tweet))

    def insertTweetSentense(self, table, one_tweet):
        return 'INSERT INTO `%s`(`content`) VALUES ("%s")' % (table, one_tweet)

