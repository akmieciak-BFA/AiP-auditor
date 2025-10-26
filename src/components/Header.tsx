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
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid ${theme.colors.neutral.gray200};
  box-shadow: ${theme.shadows.sm};
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
  transition: ${theme.transitions.base};

  &:hover {
    transform: scale(1.02);
  }
`;

const LogoImage = styled.img`
  height: 50px;
  width: auto;

  ${media.sm} {
    height: 40px;
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
  font-size: ${theme.typography.fontSize.xl};
  font-weight: ${theme.typography.fontWeight.bold};
  color: ${theme.colors.primary.brandDark};
  line-height: 1;
  margin: 0;
`;

const BrandTagline = styled.p`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
  margin: 0;
  margin-top: 2px;
`;

const Nav = styled.nav<{ $isOpen: boolean }>`
  display: flex;
  align-items: center;
  gap: ${theme.spacing.lg};

  ${media.md} {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: ${theme.spacing.xl};
    box-shadow: ${theme.shadows.lg};
    transform: translateY(${props => props.$isOpen ? '0' : '-100%'});
    opacity: ${props => props.$isOpen ? '1' : '0'};
    visibility: ${props => props.$isOpen ? 'visible' : 'hidden'};
    transition: all ${theme.transitions.base};
    pointer-events: ${props => props.$isOpen ? 'all' : 'none'};
  }
`;

const NavLink = styled.a<{ $active?: boolean }>`
  color: ${props => props.$active ? theme.colors.primary.brandDark : theme.colors.neutral.gray700};
  text-decoration: none;
  font-weight: ${props => props.$active ? theme.typography.fontWeight.semibold : theme.typography.fontWeight.medium};
  font-size: ${theme.typography.fontSize.base};
  position: relative;
  padding: ${theme.spacing.sm} 0;
  cursor: pointer;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: ${props => props.$active ? '100%' : '0'};
    height: 2px;
    background: ${theme.colors.gradients.primary};
    transition: ${theme.transitions.base};
  }

  &:hover {
    color: ${theme.colors.primary.teal};

    &::after {
      width: 100%;
    }
  }
`;

const CTAButton = styled.button`
  background: ${theme.colors.gradients.primary};
  color: white;
  border: none;
  padding: ${theme.spacing.sm} ${theme.spacing.lg};
  border-radius: ${theme.borderRadius.lg};
  font-weight: ${theme.typography.fontWeight.semibold};
  font-size: ${theme.typography.fontSize.base};
  cursor: pointer;
  box-shadow: ${theme.shadows.md};
  transition: ${theme.transitions.base};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${theme.shadows.lg};
  }

  &:active {
    transform: translateY(0);
  }

  &:focus-visible {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: ${theme.spacing.sm};
  color: ${theme.colors.primary.brandDark};
  
  ${media.md} {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &:focus-visible {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

export const Header = memo(() => {
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
          <LogoImage src="/logo.svg" alt={`${APP_CONFIG.name} Logo`} />
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
            Nowy Audyt
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

Header.displayName = 'Header';
