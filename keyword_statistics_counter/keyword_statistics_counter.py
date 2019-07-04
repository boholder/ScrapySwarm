#!/usr/bin/python3
'''
@File : keyword_statistics_counter.py

@Time : 2019/7/4

@Author : Boholder

@Function : Assist module which should be run through console
            WHENEVER the ScrapySwarm project is running (the spiders).

            * What it do:

            It runs a infinite loop,
            count items (by keyword) number crawled by spiders,
            by querying from MongoDB using pymongo module,
            and then maintain a statistics collection in MongoDB
            by updating each keyword's crawled number record.

            * What it for:

            It serves the corresponding
            'spiders running status display controler'
            in the web server back-end.

            Yeh this module and one controler in back-end
            share data via statistics collection.
            Importantly, this process is real-time,
            since I found asynchronous python isn't so easy to code.

            * Statistics collection structure:

                |_id    (Mongodb auto-generating)
                |{str}  keyword
                |{datetime obj} last_modified
                |{dict} item_num_dict
                    {"site1 domain":{int}   crawled number,
                     "site2 domain":{int}   crawled number,
                     ...
                     }
'''
