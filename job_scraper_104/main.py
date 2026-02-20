"""
主程式入口
支援手動與排程兩種執行模式
"""

import sys
import os
import argparse
import logging

# 設定 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加專案路徑到 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from job_scraper_104.scraper import JobScraper
from job_scraper_104.scheduler import JobScheduler
from job_scraper_104 import config

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='104 人力銀行職缺爬蟲系統（混合方案）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  手動模式（立即執行）:
    python main.py --mode manual
    
  排程模式（定時執行）:
    python main.py --mode schedule
    
注意事項:
  1. 請確保 Chrome 已使用 CDP 模式啟動
  2. chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\\Chrome User Data"
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['manual', 'schedule'],
        default='manual',
        help='執行模式：manual（手動立即執行）或 schedule（排程定時執行）'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'manual':
            logger.info("=" * 80)
            logger.info("手動模式：立即執行爬蟲")
            logger.info("=" * 80)
            logger.info(f"關鍵字: {config.KEYWORDS}")
            logger.info(f"每個關鍵字抓取數量: {config.MAX_JOBS_PER_KEYWORD}")
            logger.info(f"排序方式: {config.SORT_BY}")
            logger.info(f"去重: {'啟用' if config.ENABLE_DEDUPLICATION else '停用'}")
            logger.info("=" * 80)
            
            # 初始化爬蟲（使用 CDP）
            scraper = JobScraper(use_cdp=True, cdp_url="http://localhost:9527")
            
            # 執行爬蟲
            scraper.scrape_all()
            
            logger.info("=" * 80)
            logger.info("爬蟲執行完成！")
            logger.info("=" * 80)
            
        elif args.mode == 'schedule':
            logger.info("=" * 80)
            logger.info("排程模式：定時執行爬蟲")
            logger.info("=" * 80)
            logger.info(f"排程時間: 每天 {config.SCHEDULE_TIME}")
            logger.info(f"關鍵字: {config.KEYWORDS}")
            logger.info(f"每個關鍵字抓取數量: {config.MAX_JOBS_PER_KEYWORD}")
            logger.info("=" * 80)
            logger.info("按 Ctrl+C 停止排程")
            logger.info("=" * 80)
            
            # 初始化排程器
            scheduler = JobScheduler()
            
            # 啟動排程
            scheduler.start()
            
    except KeyboardInterrupt:
        logger.info("\n使用者中斷執行")
    except Exception as e:
        logger.error(f"執行時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
