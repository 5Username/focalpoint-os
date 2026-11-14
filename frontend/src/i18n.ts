export type Lang = 'en' | 'sw' | 'fr' | 'ar'

const translations: Record<Lang, Record<string, string>> = {
  en: {
    appName: 'FocalPoint OS',
    tagline: 'Toolkit for NGO Security Focal Points',
    briefs: 'Weekly Briefs',
    travel: 'Travel Risk Packs',
    incidents: 'Incident Logger',
    crisis: 'Crisis Overview',
    generateBrief: 'Generate Brief',
    compilePack: 'Compile Risk Pack',
    logIncident: 'Log Incident',
    downloadPdf: 'Download PDF',
    organization: 'Organisation',
    region: 'Region / Focus',
    destination: 'Destination',
    online: 'Online',
    offline: 'Offline',
    language: 'Language',
    disclaimer: 'Research & coordination tool only. Not licensed security advice.'
  },
  sw: {
    appName: 'FocalPoint OS',
    tagline: 'Zana kwa Maafisa wa Usalama wa NGO',
    briefs: 'Ripoti za Wiki',
    travel: 'Pakiti za Hatari za Safari',
    incidents: 'Rekodi ya Matukio',
    crisis: 'Muhtasari wa Mgogoro',
    generateBrief: 'Tengeneza Ripoti',
    compilePack: 'Tengeneza Pakiti ya Hatari',
    logIncident: 'Rekodi Tukio',
    downloadPdf: 'Pakua PDF',
    organization: 'Shirika',
    region: 'Eneo / Makini',
    destination: 'Mahali pa Kwenda',
    online: 'Mtandaoni',
    offline: 'Nje ya Mtandao',
    language: 'Lugha',
    disclaimer: 'Zana ya utafiti na uratibu tu. Si ushauri wa usalama ulioidhinishwa.'
  },
  fr: {
    appName: 'FocalPoint OS',
    tagline: 'Boîte à outils pour les Points Focaux Sécurité des ONG',
    briefs: 'Briefings Hebdomadaires',
    travel: 'Packs de Risque Voyage',
    incidents: 'Journal des Incidents',
    crisis: 'Aperçu de Crise',
    generateBrief: 'Générer le Briefing',
    compilePack: 'Compiler le Pack',
    logIncident: 'Enregistrer un Incident',
    downloadPdf: 'Télécharger PDF',
    organization: 'Organisation',
    region: 'Région / Focus',
    destination: 'Destination',
    online: 'En ligne',
    offline: 'Hors ligne',
    language: 'Langue',
    disclaimer: 'Outil de recherche et de coordination uniquement. Pas un conseil de sécurité agréé.'
  },
  ar: {
    appName: 'FocalPoint OS',
    tagline: 'أداة لنقاط الارتكاز الأمنية في المنظمات',
    briefs: 'التقارير الأسبوعية',
    travel: 'حزم مخاطر السفر',
    incidents: 'سجل الحوادث',
    crisis: 'نظرة عامة على الأزمة',
    generateBrief: 'إنشاء التقرير',
    compilePack: 'إعداد حزمة المخاطر',
    logIncident: 'تسجيل حادث',
    downloadPdf: 'تحميل PDF',
    organization: 'المنظمة',
    region: 'المنطقة',
    destination: 'الوجهة',
    online: 'متصل',
    offline: 'غير متصل',
    language: 'اللغة',
    disclaimer: 'أداة بحث وتنسيق فقط. ليست مشورة أمنية مرخصة.'
  }
}

export function t(lang: Lang, key: string): string {
  return translations[lang]?.[key] || translations.en[key] || key
}

export const availableLanguages: { code: Lang; label: string }[] = [
  { code: 'en', label: 'English' },
  { code: 'sw', label: 'Kiswahili' },
  { code: 'fr', label: 'Français' },
  { code: 'ar', label: 'العربية' }
]
