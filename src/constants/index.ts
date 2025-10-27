// Application constants

export const APP_CONFIG = {
  name: 'BFA AiP Auditor',
  version: '1.0.0',
  maxWidth: '1280px',
} as const;

export const NAVIGATION_LINKS = [
  { id: 'dashboard', label: 'Dashboard', href: '#dashboard' },
  { id: 'audits', label: 'Audyty', href: '#audyty' },
  { id: 'reports', label: 'Raporty', href: '#raporty' },
  { id: 'settings', label: 'Ustawienia', href: '#ustawienia' },
] as const;

export const FOOTER_LINKS = {
  product: [
    { label: 'Funkcje', href: '#features' },
    { label: 'Cennik', href: '#pricing' },
    { label: 'Integracje', href: '#integrations' },
    { label: 'Historia zmian', href: '#changelog' },
  ],
  company: [
    { label: 'O nas', href: '#about' },
    { label: 'Zespół', href: '#team' },
    { label: 'Kariera', href: '#careers' },
    { label: 'Kontakt', href: '#contact' },
  ],
  help: [
    { label: 'Dokumentacja', href: '#docs' },
    { label: 'Wsparcie', href: '#support' },
    { label: 'Polityka prywatności', href: '#privacy' },
    { label: 'Regulamin', href: '#terms' },
  ],
} as const;

export const SOCIAL_LINKS = [
  { name: 'LinkedIn', href: '#linkedin', icon: 'linkedin' },
  { name: 'Twitter', href: '#twitter', icon: 'twitter' },
  { name: 'GitHub', href: '#github', icon: 'github' },
] as const;

// Mock data for dashboard
export const MOCK_STATS = [
  {
    id: 'total',
    label: 'Wszystkie Audyty',
    value: 127,
    change: 12,
    positive: true,
    color: 'teal',
  },
  {
    id: 'completed',
    label: 'Ukończone',
    value: 98,
    change: 8,
    positive: true,
    color: 'success',
  },
  {
    id: 'in-progress',
    label: 'W Trakcie',
    value: 23,
    change: -3,
    positive: false,
    color: 'warning',
  },
  {
    id: 'pending',
    label: 'Oczekujące',
    value: 6,
    change: 2,
    positive: true,
    color: 'orange',
  },
] as const;

export const MOCK_AUDITS = [
  {
    id: '1',
    title: 'Audyt bezpieczeństwa systemu bankowego',
    status: 'completed' as const,
    date: '2025-10-24',
  },
  {
    id: '2',
    title: 'Przegląd zgodności RODO',
    status: 'in-progress' as const,
    date: '2025-10-22',
  },
  {
    id: '3',
    title: 'Audyt infrastruktury IT',
    status: 'in-progress' as const,
    date: '2025-10-20',
  },
  {
    id: '4',
    title: 'Analiza ryzyka operacyjnego',
    status: 'pending' as const,
    date: '2025-10-18',
  },
  {
    id: '5',
    title: 'Kontrola wewnętrzna procesów',
    status: 'completed' as const,
    date: '2025-10-15',
  },
] as const;

export const MOCK_ACTIVITIES = [
  {
    id: '1',
    user: 'Jan Kowalski',
    action: 'ukończył audyt bezpieczeństwa',
    time: '2 godziny temu',
  },
  {
    id: '2',
    user: 'Anna Nowak',
    action: 'dodała nowy raport',
    time: '5 godzin temu',
  },
  {
    id: '3',
    user: 'Piotr Wiśniewski',
    action: 'rozpoczął nowy audyt',
    time: '1 dzień temu',
  },
  {
    id: '4',
    user: 'Maria Lewandowska',
    action: 'zaktualizowała ustawienia',
    time: '2 dni temu',
  },
  {
    id: '5',
    user: 'System',
    action: 'wygenerował automatyczny raport miesięczny',
    time: '3 dni temu',
  },
] as const;

export const STATUS_LABELS = {
  completed: 'Ukończony',
  'in-progress': 'W trakcie',
  pending: 'Oczekujący',
} as const;
