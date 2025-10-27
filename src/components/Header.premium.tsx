import { useState, useCallback, useRef, memo } from 'react';
import styled from 'styled-components';
import { theme } from '../styles/theme';
import { media, containerStyles } from '../utils/mediaQueries';
import { NAVIGATION_LINKS, APP_CONFIG } from '../constants';
import { Icon } from './common/Icon';
import { useClickOutside } from '../hooks/useClickOutside';

const HeaderContainer = styled.header`
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(43, 122, 120, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: all ${theme.transitions.base};
`;

const HeaderContent = styled.div`
  ${containerStyles}
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${theme.spacing.xl};
  padding-top: ${theme.spacing.md};
  padding-bottom: ${theme.spacing.md};
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.md};
  cursor: pointer;
  transition: all ${theme.transitions.base};
  transform: translateZ(0);

  &:hover {
    transform: scale(1.05) translateZ(0);
  }
`;

const LogoImage = styled.picture`
  display: block;
  
  img {
    height: 50px;
    width: auto;
    display: block;
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.1));
    transition: filter ${theme.transitions.base};
    
    ${Logo}:hover & {
      filter: drop-shadow(0 4px 12px rgba(43, 122, 120, 0.3));
    }

    ${media.sm} {
      height: 40px;
    }
  }
`;

const LogoText = styled.div`
  display: flex;
  flex-direction: column;
  
  ${media.sm} {
    display: none;
  }
`;

const BrandName = styled.h1`
  font-size: ${theme.typography.fontSize['2xl']};
  font-weight: ${theme.typography.fontWeight.extrabold};
  background: ${theme.colors.gradients.primary};
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin: 0;
`;

const BrandTagline = styled.p`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
  margin: 0;
  margin-top: 4px;
  font-weight: ${theme.typography.fontWeight.medium};
`;

const Nav = styled.nav<{ $isOpen: boolean }>`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};

  ${media.md} {
    position: fixed;
    top: 78px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: ${theme.spacing.xl};
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    transform: translateY(${props => props.$isOpen ? '0' : '-100%'});
    opacity: ${props => props.$isOpen ? '1' : '0'};
    visibility: ${props => props.$isOpen ? 'visible' : 'hidden'};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    pointer-events: ${props => props.$isOpen ? 'all' : 'none'};
  }
`;

const NavLink = styled.a<{ $active?: boolean }>`
  color: ${props => props.$active ? theme.colors.primary.brandDark : theme.colors.neutral.gray700};
  text-decoration: none;
  font-weight: ${props => props.$active ? theme.typography.fontWeight.bold : theme.typography.fontWeight.medium};
  font-size: ${theme.typography.fontSize.base};
  position: relative;
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  cursor: pointer;
  border-radius: ${theme.borderRadius.md};
  transition: all ${theme.transitions.fast};

  &::after {
    content: '';
    position: absolute;
    bottom: 4px;
    left: 50%;
    transform: translateX(-50%) scaleX(${props => props.$active ? '1' : '0'});
    width: 60%;
    height: 3px;
    background: ${theme.colors.gradients.primary};
    border-radius: ${theme.borderRadius.full};
    transition: transform ${theme.transitions.base};
  }

  &:hover {
    color: ${theme.colors.primary.teal};
    background: ${theme.colors.neutral.gray50};

    &::after {
      transform: translateX(-50%) scaleX(1);
    }
  }
`;

const CTAButton = styled.button`
  background: ${theme.colors.gradients.primary};
  color: white;
  border: none;
  padding: ${theme.spacing.md} ${theme.spacing.xl};
  border-radius: ${theme.borderRadius.xl};
  font-weight: ${theme.typography.fontWeight.bold};
  font-size: ${theme.typography.fontSize.base};
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(43, 122, 120, 0.3);
  transition: all ${theme.transitions.base};
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
  }

  &:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 12px 28px rgba(43, 122, 120, 0.4);

    &::before {
      width: 300px;
      height: 300px;
    }
  }

  &:active {
    transform: translateY(-1px) scale(1.02);
  }

  &:focus-visible {
    outline: 3px solid ${theme.colors.primary.teal};
    outline-offset: 3px;
  }
`;

const MenuButton = styled.button`
  display: none;
  background: ${theme.colors.neutral.gray100};
  border: none;
  cursor: pointer;
  padding: ${theme.spacing.md};
  color: ${theme.colors.primary.brandDark};
  border-radius: ${theme.borderRadius.lg};
  transition: all ${theme.transitions.fast};
  
  ${media.md} {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &:hover {
    background: ${theme.colors.neutral.gray200};
    transform: scale(1.1);
  }

  &:active {
    transform: scale(0.95);
  }

  &:focus-visible {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

export const HeaderPremium = memo(() => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeLink, setActiveLink] = useState('dashboard');
  const navRef = useRef<HTMLElement | null>(null);

  const closeMenu = useCallback(() => {
    setIsMenuOpen(false);
  }, []);

  const toggleMenu = useCallback(() => {
    setIsMenuOpen(prev => !prev);
  }, []);

  const handleLinkClick = useCallback((id: string) => {
    setActiveLink(id);
    closeMenu();
  }, [closeMenu]);

  useClickOutside(navRef, closeMenu);

  return (
    <HeaderContainer role="banner">
      <HeaderContent>
        <Logo onClick={() => handleLinkClick('dashboard')} role="button" tabIndex={0}>
          <LogoImage>
            {/* Try WebP first, fallback to PNG, then SVG */}
            <source srcSet="/logo.webp" type="image/webp" />
            <source srcSet="/logo.png" type="image/png" />
            <img src="/logo.svg" alt={`${APP_CONFIG.name} Logo`} loading="eager" decoding="async" />
          </LogoImage>
          <LogoText>
            <BrandName>BFA</BrandName>
            <BrandTagline>AiP Auditor</BrandTagline>
          </LogoText>
        </Logo>

        <Nav ref={navRef} $isOpen={isMenuOpen} role="navigation" aria-label="Main navigation">
          {NAVIGATION_LINKS.map(link => (
            <NavLink
              key={link.id}
              href={link.href}
              $active={activeLink === link.id}
              onClick={() => handleLinkClick(link.id)}
              aria-current={activeLink === link.id ? 'page' : undefined}
            >
              {link.label}
            </NavLink>
          ))}
          <CTAButton onClick={closeMenu} aria-label="Utwórz nowy audyt">
            <span>✨ Nowy Audyt</span>
          </CTAButton>
        </Nav>

        <MenuButton 
          onClick={toggleMenu}
          aria-label={isMenuOpen ? 'Zamknij menu' : 'Otwórz menu'}
          aria-expanded={isMenuOpen}
          aria-controls="main-navigation"
        >
          <Icon name={isMenuOpen ? 'close' : 'menu'} />
        </MenuButton>
      </HeaderContent>
    </HeaderContainer>
  );
});

HeaderPremium.displayName = 'HeaderPremium';
