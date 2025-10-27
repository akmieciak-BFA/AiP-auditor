import { theme } from '../styles/theme';

/**
 * Media query helpers for consistent responsive design
 */

export const media = {
  sm: `@media (max-width: ${theme.breakpoints.sm})`,
  md: `@media (max-width: ${theme.breakpoints.md})`,
  lg: `@media (max-width: ${theme.breakpoints.lg})`,
  xl: `@media (max-width: ${theme.breakpoints.xl})`,
  '2xl': `@media (max-width: ${theme.breakpoints['2xl']})`,
} as const;

export const mediaMin = {
  sm: `@media (min-width: ${theme.breakpoints.sm})`,
  md: `@media (min-width: ${theme.breakpoints.md})`,
  lg: `@media (min-width: ${theme.breakpoints.lg})`,
  xl: `@media (min-width: ${theme.breakpoints.xl})`,
  '2xl': `@media (min-width: ${theme.breakpoints['2xl']})`,
} as const;

// Common container styles with max-width
export const containerStyles = `
  max-width: ${theme.breakpoints.xl};
  margin: 0 auto;
  padding: ${theme.spacing.xl};

  ${media.md} {
    padding: ${theme.spacing.md};
  }
`;
