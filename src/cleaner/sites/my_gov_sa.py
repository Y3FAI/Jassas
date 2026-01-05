"""
Parser for my.gov.sa service pages.
Extracts structured service information, filters out noise.
"""
import re
from bs4 import BeautifulSoup
from .base import SiteParser


class MyGovSaParser(SiteParser):
    """Parser optimized for my.gov.sa service pages."""

    # Noise patterns to remove from text
    NOISE_PATTERNS = [
        r'شاركنا رأيك.*?(?=\n|$)',
        r'هل أعجبك محتوى.*?(?=\n|$)',
        r'التعليقات والاقتراحات.*?إرسال',
        r'ملفات تعريف الارتباط.*?رفض',
        r'تحتاج مساعدة\؟.*?(?=\n|$)',
        r'سياسة الخصوصية.*?(?=\n|$)',
        r'\d+ من الزوّار.*?(?=\n|$)',
        r'تاريخ آخر تحديث.*?(?=\n|$)',
        r'مسجل لدى هيئة.*?(?=\n|$)',
        r'روابط المواقع الإلكترونية.*?للتشفير',
        r'c \d{4} جميع الحقوق.*?(?=\n|$)',
        # Share buttons
        r'مشاركة الصفحة',
        r'مشاركة عبر إكس',
        r'مشاركة عبر لينكدإن',
        r'مشاركة عبر فيسبوك',
        r'مشاركة عبر واتساب',
        r'مشاركة عبر البريد',
        # Breadcrumbs (line starting with الرئيسية)
        r'^الرئيسية\n',
        r'^الخدمات\n',
        # Action buttons
        r'تفضيل الصفحة',
        r'ابدأ الخدمة',
        r'اتفاقية مستوى الخدمة',
        r'تحميل دليل المستخدم',
        r'تطبيقات ذات صلة',
        r'الاطلاع على الأسئلة الشائعة',
        r'الاطلاع على رابط الفروع',
        r'الاطلاع على الموقع',
    ]

    # Section labels we want to extract
    SERVICE_SECTIONS = [
        'خطوات',
        'متطلبات',
        'المستندات المطلوبة',
        'الفئة المستهدفة',
        'الجمهور المستهدف',
        'قنوات تقديم الخدمة',
        'التكلفة',
        'مدة الخدمة',
        'أوقات العمل',
        'الهاتف',
        'البريد الإلكتروني',
    ]

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract service-specific content."""
        # Get title and description for deduplication
        h1 = soup.find('h1')
        h1_text = h1.get_text(strip=True) if h1 else ''

        meta = soup.find('meta', attrs={'name': 'description'})
        desc_text = meta['content'].strip() if meta and meta.get('content') else ''

        # Get main content area
        main = soup.find('main')
        if not main:
            return ''

        content_div = main.find('div')
        if not content_div:
            return ''

        raw_text = content_div.get_text(separator='\n', strip=True)
        clean_text = self._clean_service_text(raw_text)

        # Remove duplicate title/description from content
        if h1_text:
            clean_text = clean_text.replace(h1_text + '\n', '', 1)
        if desc_text:
            clean_text = clean_text.replace(desc_text + '\n', '', 1)

        result = clean_text

        # Final cleanup
        result = re.sub(r'\n{3,}', '\n\n', result)  # Max 2 newlines
        result = re.sub(r' {2,}', ' ', result)  # Max 1 space

        return result.strip()

    def _clean_service_text(self, text: str) -> str:
        """Remove noise from service text."""
        # Remove noise patterns
        for pattern in self.NOISE_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)

        # Remove footer-like content (after certain markers)
        cutoff_markers = [
            'نظرة عامة عن المملكة',
            'روابط مهمة',
            'دعم والمساعدة',
            'تواصل معنا',
            'أدوات الإتاحة',
        ]
        for marker in cutoff_markers:
            idx = text.find(marker)
            if idx > 0:
                text = text[:idx]

        return text.strip()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract clean title (remove site suffix)."""
        title = ""

        # Prefer H1 for service name
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)
        elif soup.title:
            title = soup.title.get_text(strip=True)
            # Remove common suffixes
            title = re.sub(r'\s*[|\-]\s*المنصة الوطنية.*$', '', title)
            title = re.sub(r'\s*[|\-]\s*منصة.*$', '', title)

        return title.strip()
