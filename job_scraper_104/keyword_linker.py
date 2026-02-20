"""
技術名詞雙向連結處理模組
負責識別技術名詞並轉換為 Obsidian 雙向連結格式
支援自動學習新的技術名詞
"""

import yaml
import re
import logging
from typing import List, Set
from . import config

logger = logging.getLogger(__name__)


class KeywordLinker:
    """技術名詞連結器"""
    
    def __init__(self):
        """初始化關鍵字連結器"""
        self.keywords: Set[str] = set()
        self._load_keywords()
    
    def _load_keywords(self):
        """載入預定義與自動學習的關鍵字"""
        # 載入預定義關鍵字
        try:
            with open(config.KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data:
                    for category, keywords in data.items():
                        if isinstance(keywords, list):
                            self.keywords.update(keywords)
            logger.info(f"已載入 {len(self.keywords)} 個預定義關鍵字")
        except FileNotFoundError:
            logger.warning(f"找不到關鍵字檔案：{config.KEYWORDS_FILE}")
        except Exception as e:
            logger.error(f"載入預定義關鍵字失敗：{e}")
        
        # 載入自動學習的關鍵字
        try:
            with open(config.LEARNED_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'auto_learned' in data:
                    learned = data['auto_learned']
                    if isinstance(learned, list):
                        self.keywords.update(learned)
                        logger.info(f"已載入 {len(learned)} 個自動學習的關鍵字")
        except FileNotFoundError:
            logger.info(f"尚無自動學習的關鍵字檔案")
        except Exception as e:
            logger.error(f"載入自動學習關鍵字失敗：{e}")
    
    def learn_from_specialty(self, specialty_list: List[str]):
        """
        從職缺的「擅長工具」欄位學習新的技術名詞
        
        Args:
            specialty_list: 擅長工具清單
        """
        # 過濾詞彙（排除非技術性詞彙）
        excluded_words = {
            '具備', '熟悉', '了解', '使用', '操作', '經驗',
            '能力', '技能', '工具', '軟體', '系統', '平台',
            '相關', '以上', '以下', '或', '及', '與', '和'
        }
        
        new_keywords = []
        for item in specialty_list:
            # 清理特殊字元與空白
            cleaned = item.strip()
            
            # 過濾太短的詞彙（少於 2 個字元）
            if len(cleaned) < 2:
                continue
            
            # 過濾非技術性詞彙
            if cleaned in excluded_words:
                continue
            
            # 過濾包含中文標點的詞彙
            if any(char in cleaned for char in '，。！？、；：「」『』（）【】'):
                continue
            
            # 如果是新的關鍵字，加入學習清單
            if cleaned not in self.keywords:
                new_keywords.append(cleaned)
                self.keywords.add(cleaned)
        
        # 儲存新學習的關鍵字
        if new_keywords:
            self._save_learned_keywords(new_keywords)
            logger.info(f"學習到 {len(new_keywords)} 個新的技術名詞：{new_keywords}")
    
    def _save_learned_keywords(self, new_keywords: List[str]):
        """
        將新學習的關鍵字儲存至檔案
        
        Args:
            new_keywords: 新學習的關鍵字清單
        """
        try:
            # 讀取現有的學習關鍵字
            try:
                with open(config.LEARNED_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
            except FileNotFoundError:
                data = {}
            
            # 更新清單
            if 'auto_learned' not in data:
                data['auto_learned'] = []
            
            data['auto_learned'].extend(new_keywords)
            data['auto_learned'] = sorted(list(set(data['auto_learned'])))  # 去重並排序
            
            # 寫回檔案
            with open(config.LEARNED_KEYWORDS_FILE, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
            
            logger.info(f"已儲存 {len(new_keywords)} 個新關鍵字至 {config.LEARNED_KEYWORDS_FILE}")
            
        except Exception as e:
            logger.error(f"儲存學習關鍵字失敗：{e}")
    
    def add_links(self, text: str) -> str:
        """
        將文字中的技術名詞轉換為 Obsidian 雙向連結格式
        
        Args:
            text: 原始文字
        
        Returns:
            已加上雙向連結的文字
        """
        if not text:
            return text
        
        # 按照關鍵字長度排序（優先匹配長關鍵字，避免誤匹配）
        sorted_keywords = sorted(self.keywords, key=len, reverse=True)
        
        result = text
        for keyword in sorted_keywords:
            # 使用正則表達式進行完整詞彙匹配
            # \b 為詞彙邊界，確保不會匹配到詞彙的一部分
            pattern = r'\b' + re.escape(keyword) + r'\b'
            
            # 替換為 Obsidian 連結格式（避免重複替換已連結的詞彙）
            replacement = f'[[{keyword}]]'
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def process_job_data(self, job_data: dict) -> dict:
        """
        處理職缺資料，加上技術名詞連結並學習新關鍵字
        
        Args:
            job_data: 職缺資料字典
        
        Returns:
            處理後的職缺資料
        """
        # 從擅長工具欄位學習新關鍵字
        if 'specialty' in job_data and job_data['specialty']:
            self.learn_from_specialty(job_data['specialty'])
        
        # 對各個欄位加上連結
        if 'job_description' in job_data:
            job_data['job_description'] = self.add_links(job_data['job_description'])
        
        if 'requirement' in job_data:
            job_data['requirement'] = self.add_links(job_data['requirement'])
        
        if 'other_requirement' in job_data:
            job_data['other_requirement'] = self.add_links(job_data['other_requirement'])
        
        return job_data
