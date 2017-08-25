# -*- coding: utf-8 -*-
import config as configuration
from obj.connection import Connection
from obj.account import Account
import datetime

class Controller:
    def __init__(self):
        self.con = Connection()
        self.con.openCursor()
        self.account_list = self.getAccountList()

    def run_process(self):
        accounts_to_publish = self.getAccountsToPublish()
        self.publish_list(accounts_to_publish)
        self.con.closeConnection()
        return True

    def getAccountList(self):
        accounts_list = []
        account_data = self.con.getAllAccountsData()
        for one_ad in account_data:
            accounts_list.append(Account(one_ad))
        return accounts_list

    def getAccountsToPublish(self):
        accounts_to_publish = []
        now = datetime.datetime.now()
        # print now.year, now.month, now.day, now.hour, now.minute, now.second
        for one_account in self.account_list:
            if one_account.publish_min != 0:
                if now.minute % one_account.publish_min == 0:
                    accounts_to_publish.append(one_account)
        return accounts_to_publish

    def publish_list(self,accounts_list):
        for one_account in accounts_list:
            one_account.getNewTweet(self.con)
            one_account.publish()
            self.con.updateTweetStatus(one_account.table, one_account.tweet["id"])

    # DEPLOY CODE
    def deploy(self):
        for one_account in self.account_list:
            table = str(one_account.table)
            if not table == "":
                self.con.createTable(table)
