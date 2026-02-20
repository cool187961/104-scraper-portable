"""
排程管理模組
負責定時執行爬蟲任務
"""

import schedule
import time
import logging
from .scraper import JobScraper
from . import config

logger = logging.getLogger(__name__)


class JobScheduler:
    """爬蟲排程器"""
    
    def __init__(self):
        """初始化排程器"""
        self.scraper = JobScraper()
    
    def run_scraper(self):
        """執行爬蟲任務"""
        logger.info("排程觸發：開始執行爬蟲任務")
        try:
            self.scraper.scrape_all()
            logger.info("排程任務執行完成")
        except Exception as e:
            logger.error(f"排程任務執行失敗：{e}")
    
    def start(self):
        """
        啟動排程器
        每天在指定時間執行爬蟲
        """
        logger.info(f"排程器已啟動，將於每天 {config.SCHEDULE_TIME} 執行爬蟲")
        
        # 設定排程
        schedule.every().day.at(config.SCHEDULE_TIME).do(self.run_scraper)
        
        # 持續運行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分鐘檢查一次
