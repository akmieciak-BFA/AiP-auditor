// Type definitions

export type AuditStatus = 'completed' | 'in-progress' | 'pending';

export interface Audit {
  id: string;
  title: string;
  status: AuditStatus;
  date: string;
}

export interface Activity {
  id: string;
  user: string;
  action: string;
  time: string;
}

export interface Stat {
  id: string;
  label: string;
  value: number;
  change: number;
  positive: boolean;
  color: string;
}

export interface NavigationLink {
  id: string;
  label: string;
  href: string;
}

export interface SocialLink {
  name: string;
  href: string;
  icon: string;
}

export interface FooterLink {
  label: string;
  href: string;
}

export interface FooterLinks {
  product: readonly FooterLink[];
  company: readonly FooterLink[];
  help: readonly FooterLink[];
}
