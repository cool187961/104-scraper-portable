"""
Obsidian 筆記格式化模組
負責將職缺資料轉換為 Obsidian Markdown 格式
"""

import os
import logging
from datetime import datetime
from typing import Dict, List
from . import config

logger = logging.getLogger(__name__)


class ObsidianFormatter:
    """Obsidian 筆記格式化器"""
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        清理文字內容
        
        Args:
            text: 原始文字
        
        Returns:
            清理後的文字
        """
        if not text:
            return ""
        # 移除多餘的空白與換行
        return text.strip()
    
    @staticmethod
    def _format_list(items: List[str], indent: int = 0) -> str:
        """
        格式化清單項目
        
        Args:
            items: 項目清單
            indent: 縮排層級
        
        Returns:
            格式化後的清單文字
        """
        if not items:
            return ""
        
        indent_str = "  " * indent
        return "\n".join([f"{indent_str}- {item}" for item in items if item])
    
    def format_job(self, job_data: Dict) -> str:
        """
        將職缺資料格式化為 Obsidian Markdown
        
        Args:
            job_data: 職缺資料字典，應包含以下欄位：
                - job_id: 職缺 ID
                - title: 職缺標題
                - company: 公司名稱
                - salary: 薪資範圍
                - location: 完整地址
                - job_description: 工作內容
                - education: 學歷要求
                - experience: 工作經驗要求
                - skills: 技能要求清單
                - specialty: 擅長工具清單
                - other_requirement: 其他條件
                - keywords: 關鍵字清單
        
        Returns:
            Obsidian Markdown 格式的筆記內容
        """
        # 提取欄位
        job_id = job_data.get('job_id', '')
        title = self._clean_text(job_data.get('title', '未知職缺'))
        company = self._clean_text(job_data.get('company', '未知公司'))
        salary = self._clean_text(job_data.get('salary', '面議'))
        location = self._clean_text(job_data.get('location', '未提供'))
        job_description = self._clean_text(job_data.get('job_description', ''))
        education = self._clean_text(job_data.get('education', ''))
        experience = self._clean_text(job_data.get('experience', ''))
        skills = job_data.get('skills', [])
        specialty = job_data.get('specialty', [])
        other_requirement = self._clean_text(job_data.get('other_requirement', ''))
        keywords = job_data.get('keywords', [])
        
        # 取得當前時間
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 構建 YAML frontmatter
        frontmatter = f"""---
title: "{title} - {company}"
company: {company}
salary: {salary}
location: {location}
keywords: {keywords}
crawled_at: {now}
job_url: https://www.104.com.tw/job/{job_id}
---
"""
        
        # 構建筆記內容
        content = f"""
# {title} - {company}

## 📍 工作地點
{location}

## 📝 工作內容
{job_description if job_description else '（無詳細說明）'}

## 🎯 條件要求

### 學歷要求
{education if education else '（未指定）'}

### 工作經驗
{experience if experience else '（未指定）'}
"""
        
        # 技能要求
        if skills:
            content += "\n### 技能要求\n"
            content += self._format_list(skills) + "\n"
        
        # 擅長工具
        if specialty:
            content += "\n### 擅長工具\n"
            content += self._format_list(specialty) + "\n"
        
        # 其他條件
        if other_requirement:
            content += f"\n### 其他條件\n{other_requirement}\n"
        
        # 頁尾
        footer = f"""
---
**抓取時間**: {now}  
**職缺連結**: [查看原始職缺](https://www.104.com.tw/job/{job_id})
"""
        
        # 組合完整內容
        full_content = frontmatter + content + footer
        
        return full_content
    
    def save_job_note(self, job_data: Dict, category: str) -> str:
        """
        儲存職缺筆記到檔案
        
        Args:
            job_data: 職缺資料
            category: 類別（資料工程、資料分析、RPA自動化）
        
        Returns:
            儲存的檔案路徑
        """
        # 格式化筆記內容
        content = self.format_job(job_data)
        
        # 產生檔案名稱（使用公司名稱與職缺標題）
        company = job_data.get('company', '未知公司')
        title = job_data.get('title', '未知職缺')
        job_id = job_data.get('job_id', 'unknown')
        
        # 清理檔案名稱中的非法字元
        safe_filename = f"{company}_{title}_{job_id}.md"
        safe_filename = safe_filename.replace('/', '_').replace('\\', '_').replace(':', '_')
        safe_filename = safe_filename.replace('*', '_').replace('?', '_').replace('"', '_')
        safe_filename = safe_filename.replace('<', '_').replace('>', '_').replace('|', '_')
        
        # 構建檔案路徑
        category_dir = os.path.join(config.OUTPUT_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        
        file_path = os.path.join(category_dir, safe_filename)
        
        # 寫入檔案
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"已儲存職缺筆記：{file_path}")
            return file_path
        except Exception as e:
            logger.error(f"儲存職缺筆記失敗：{e}")
            return ""
