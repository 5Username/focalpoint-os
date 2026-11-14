export type Lang = 'en' | 'sw' | 'fr' | 'ar'

const translations: Record<Lang, Record<string, string>> = {
  en: {
    appName: 'FocalPoint OS',
    tagline: 'Toolkit for NGO Security Focal Points',
    briefs: 'Weekly Briefs',
    travel: 'Travel Risk Packs',
    incidents: 'Incident Logger',
    generateBrief: 'Generate Brief',
    compilePack: 'Compile Risk Pack',
    logIncident: 'Log Incident',
    organization: 'Organisation',
    region: 'Region / Focus',
    destination: 'Destination',
    online: 'Online',
    offline: 'Offline',
    disclaimer: 'Research & coordination tool only. Not licensed security advice.'
  },
  sw: {
    appName: 'FocalPoint OS',
    tagline: 'Zana kwa Maafisa wa Usalama wa NGO',
    briefs: 'Ripoti za Wiki',
    travel: 'Pakiti za Hatari za Safari',
    incidents: 'Rekodi ya Matukio',
    generateBrief: 'Tengeneza Ripoti',
    compilePack: 'Tengeneza Pakiti ya Hatari',
    logIncident: 'Rekodi Tukio',
    organization: 'Shirika',
    region: 'Eneo / Makini',
    destination: 'Mahali pa Kwenda',
    online: 'Mtandaoni',
    offline: 'Nje ya Mtandao',
    disclaimer: 'Zana ya utafiti na uratibu tu. Si ushauri wa usalama ulioidhinishwa.'
  },
  fr: {
    appName: 'FocalPoint OS',
    tagline: 'Bo\u00eete \u00e0 outils pour les Points Focaux S\u00e9curit\u00e9 des ONG',
    briefs: 'Briefings Hebdomadaires',
    travel: 'Packs de Risque Voyage',
    incidents: 'Journal des Incidents',
    generateBrief: 'G\u00e9n\u00e9rer le Briefing',
    compilePack: 'Compiler le Pack',
    logIncident: 'Enregistrer un Incident',
    organization: 'Organisation',
    region: 'R\u00e9gion / Focus',
    destination: 'Destination',
    online: 'En ligne',
    offline: 'Hors ligne',
    disclaimer: 'Outil de recherche et de coordination uniquement. Pas un conseil de s\u00e9curit\u00e9 agr\u00e9\u00e9.'
  },
  ar: {
    appName: 'FocalPoint OS',
    tagline: '\u0623\u062f\u0627\u0629 \u0644\u0646\u0642\u0627\u0637 \u0627\u0644\u0627\u0631\u062a\u0643\u0627\u0632 \u0627\u0644\u0623\u0645\u0646\u064a\u0629 \u0641\u064a \u0627\u0644\u0645\u0646\u0638\u0645\u0627\u062a',
    briefs: '\u0627\u0644\u062a\u0642\u0627\u0631\u064a\u0631 \u0627\u0644\u0623\u0633\u0628\u0648\u0639\u064a\u0629',
    travel: '\u062d\u0632\u0645 \u0645\u062e\u0627\u0637\u0631 \u0627\u0644\u0633\u0641\u0631',
    incidents: '\u0633\u062c\u0644 \u0627\u0644\u062d\u0648\u0627\u062f\u062b',
    generateBrief: '\u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u062a\u0642\u0631\u064a\u0631',
    compilePack: '\u0625\u0639\u062f\u0627\u062f \u062d\u0632\u0645\u0629 \u0627\u0644\u0645\u062e\u0627\u0637\u0631',
    logIncident: '\u062a\u0633\u062c\u064a\u0644 \u062d\u0627\u062f\u062b',
    organization: '\u0627\u0644\u0645\u0646\u0638\u0645\u0629',
    region: '\u0627\u0644\u0645\u0646\u0637\u0642\u0629',
    destination: '\u0627\u0644\u0648\u062c\u0647\u0629',
    online: '\u0645\u062a\u0635\u0644',
    offline: '\u063a\u064a\u0631 \u0645\u062a\u0635\u0644',
    disclaimer: '\u0623\u062f\u0627\u0629 \u0628\u062d\u062b \u0648\u062a\u0646\u0633\u064a\u0642 \u0641\u0642\u0637. \u0644\u064a\u0633\u062a \u0645\u0634\u0648\u0631\u0629 \u0623\u0645\u0646\u064a\u0629 \u0645\u0631\u062e\u0635\u0629.'
  }
}

export function t(lang: Lang, key: string): string {
  return translations[lang]?.[key] || translations.en[key] || key
}

export const availableLanguages: { code: Lang; label: string }[] = [
  { code: 'en', label: 'English' },
  { code: 'sw', label: 'Kiswahili' },
  { code: 'fr', label: 'Fran\u00e7ais' },
  { code: 'ar', label: '\u0627\u0644\u0639\u0631\u0628\u064a\u0629' }
]
