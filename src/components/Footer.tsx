import { memo } from 'react';
import styled from 'styled-components';
import { theme } from '../styles/theme';
import { media, containerStyles } from '../utils/mediaQueries';
import { FOOTER_LINKS, SOCIAL_LINKS, APP_CONFIG } from '../constants';
import { Icon } from './common/Icon';

const FooterContainer = styled.footer`
  background: ${theme.colors.primary.brandDark};
  color: white;
  margin-top: auto;
`;

const FooterContent = styled.div`
  ${containerStyles}
  padding-top: ${theme.spacing['2xl']};
  padding-bottom: ${theme.spacing['2xl']};
`;

const FooterGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: ${theme.spacing['2xl']};
  margin-bottom: ${theme.spacing.xl};

  ${media.lg} {
    grid-template-columns: 1fr 1fr;
    gap: ${theme.spacing.xl};
  }

  ${media.sm} {
    grid-template-columns: 1fr;
  }
`;

const FooterSection = styled.div``;

const FooterLogo = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  margin-bottom: ${theme.spacing.md};
`;

const FooterLogoImg = styled.img`
  height: 60px;
  width: auto;
  filter: brightness(0) invert(1);
`;

const FooterBrand = styled.div`
  h3 {
    font-size: ${theme.typography.fontSize['2xl']};
    font-weight: ${theme.typography.fontWeight.bold};
    margin: 0 0 ${theme.spacing.xs} 0;
  }

  p {
    font-size: ${theme.typography.fontSize.sm};
    margin: 0;
    opacity: 0.8;
  }
`;

const FooterDescription = styled.p`
  font-size: ${theme.typography.fontSize.sm};
  line-height: ${theme.typography.lineHeight.relaxed};
  opacity: 0.9;
  margin-top: ${theme.spacing.md};
`;

const FooterTitle = styled.h4`
  font-size: ${theme.typography.fontSize.lg};
  font-weight: ${theme.typography.fontWeight.semibold};
  margin-bottom: ${theme.spacing.md};
`;

const FooterLinks = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const FooterLink = styled.li`
  margin-bottom: ${theme.spacing.sm};

  a {
    color: white;
    text-decoration: none;
    font-size: ${theme.typography.fontSize.sm};
    opacity: 0.8;
    transition: ${theme.transitions.base};
    display: inline-block;

    &:hover {
      opacity: 1;
      transform: translateX(4px);
    }

    &:focus-visible {
      outline: 2px solid white;
      outline-offset: 2px;
    }
  }
`;

const FooterBottom = styled.div`
  padding-top: ${theme.spacing.xl};
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: ${theme.spacing.md};

  ${media.sm} {
    flex-direction: column;
    text-align: center;
  }
`;

const Copyright = styled.p`
  font-size: ${theme.typography.fontSize.sm};
  margin: 0;
  opacity: 0.8;
`;

const SocialLinks = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
`;

const SocialLink = styled.a`
  width: 36px;
  height: 36px;
  border-radius: ${theme.borderRadius.full};
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-decoration: none;
  transition: ${theme.transitions.base};

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  &:focus-visible {
    outline: 2px solid white;
    outline-offset: 2px;
  }
`;

// Memoized sub-component
const FooterLinkSection = memo<{ title: string; links: readonly { label: string; href: string }[] }>(
  ({ title, links }) => (
    <FooterSection>
      <FooterTitle>{title}</FooterTitle>
      <FooterLinks>
        {links.map((link) => (
          <FooterLink key={link.href}>
            <a href={link.href}>{link.label}</a>
          </FooterLink>
        ))}
      </FooterLinks>
    </FooterSection>
  )
);
FooterLinkSection.displayName = 'FooterLinkSection';

export const Footer = memo(() => {
  const currentYear = new Date().getFullYear();

  return (
    <FooterContainer role="contentinfo">
      <FooterContent>
        <FooterGrid>
          <FooterSection>
            <FooterLogo>
              <FooterLogoImg src="/logo.svg" alt={`${APP_CONFIG.name} Logo`} />
              <FooterBrand>
                <h3>BFA</h3>
                <p>AiP Auditor</p>
              </FooterBrand>
            </FooterLogo>
            <FooterDescription>
              Nowoczesne narzędzie do zarządzania audytami i analizy ryzyka. 
              Połączenie technologii i ludzkiej ekspertyzy dla lepszego biznesu.
            </FooterDescription>
          </FooterSection>

          <FooterLinkSection title="Produkt" links={FOOTER_LINKS.product} />
          <FooterLinkSection title="Firma" links={FOOTER_LINKS.company} />
          <FooterLinkSection title="Pomoc" links={FOOTER_LINKS.help} />
        </FooterGrid>

        <FooterBottom>
          <Copyright>
            © {currentYear} {APP_CONFIG.name}. Wszelkie prawa zastrzeżone.
          </Copyright>

          <SocialLinks role="navigation" aria-label="Social media links">
            {SOCIAL_LINKS.map((social) => (
              <SocialLink
                key={social.name}
                href={social.href}
                aria-label={social.name}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Icon name={social.icon as any} size={18} />
              </SocialLink>
            ))}
          </SocialLinks>
        </FooterBottom>
      </FooterContent>
    </FooterContainer>
  );
});

Footer.displayName = 'Footer';
