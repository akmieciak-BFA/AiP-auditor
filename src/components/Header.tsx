import { useState } from 'react';
import styled from 'styled-components';
import { theme } from '../styles/theme';

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
  max-width: 1280px;
  margin: 0 auto;
  padding: ${theme.spacing.md} ${theme.spacing.xl};
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${theme.spacing.xl};

  @media (max-width: ${theme.breakpoints.md}) {
    padding: ${theme.spacing.md};
  }
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

  @media (max-width: ${theme.breakpoints.sm}) {
    height: 40px;
  }
`;

const LogoText = styled.div`
  display: flex;
  flex-direction: column;
  
  @media (max-width: ${theme.breakpoints.sm}) {
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

  @media (max-width: ${theme.breakpoints.md}) {
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
    transition: all ${theme.transitions.base};
    pointer-events: ${props => props.$isOpen ? 'all' : 'none'};
  }
`;

const NavLink = styled.a`
  color: ${theme.colors.neutral.gray700};
  text-decoration: none;
  font-weight: ${theme.typography.fontWeight.medium};
  font-size: ${theme.typography.fontSize.base};
  position: relative;
  padding: ${theme.spacing.sm} 0;
  cursor: pointer;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
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

  &.active {
    color: ${theme.colors.primary.brandDark};
    font-weight: ${theme.typography.fontWeight.semibold};

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
`;

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: ${theme.spacing.sm};
  color: ${theme.colors.primary.brandDark};

  @media (max-width: ${theme.breakpoints.md}) {
    display: block;
  }

  svg {
    width: 24px;
    height: 24px;
  }
`;

export const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>
          <LogoImage src="/logo.svg" alt="BFA Logo" />
          <LogoText>
            <BrandName>BFA</BrandName>
            <BrandTagline>AiP Auditor</BrandTagline>
          </LogoText>
        </Logo>

        <Nav $isOpen={isMenuOpen}>
          <NavLink className="active" onClick={() => setIsMenuOpen(false)}>
            Dashboard
          </NavLink>
          <NavLink onClick={() => setIsMenuOpen(false)}>
            Audyty
          </NavLink>
          <NavLink onClick={() => setIsMenuOpen(false)}>
            Raporty
          </NavLink>
          <NavLink onClick={() => setIsMenuOpen(false)}>
            Ustawienia
          </NavLink>
          <CTAButton onClick={() => setIsMenuOpen(false)}>
            Nowy Audyt
          </CTAButton>
        </Nav>

        <MenuButton onClick={() => setIsMenuOpen(!isMenuOpen)}>
          {isMenuOpen ? (
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </MenuButton>
      </HeaderContent>
    </HeaderContainer>
  );
};
