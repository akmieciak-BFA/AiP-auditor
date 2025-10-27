import { memo } from 'react';
import styled, { keyframes } from 'styled-components';
import { theme } from '../../styles/theme';

interface SkeletonLoaderProps {
  width?: string;
  height?: string;
  borderRadius?: string;
  count?: number;
  className?: string;
}

const shimmer = keyframes`
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
`;

const SkeletonBox = styled.div<{
  $width?: string;
  $height?: string;
  $borderRadius?: string;
}>`
  width: ${props => props.$width || '100%'};
  height: ${props => props.$height || '20px'};
  border-radius: ${props => props.$borderRadius || theme.borderRadius.md};
  background: linear-gradient(
    90deg,
    ${theme.colors.neutral.gray100} 25%,
    ${theme.colors.neutral.gray200} 50%,
    ${theme.colors.neutral.gray100} 75%
  );
  background-size: 2000px 100%;
  animation: ${shimmer} 1.5s infinite linear;
  margin-bottom: ${theme.spacing.md};

  &:last-child {
    margin-bottom: 0;
  }
`;

const SkeletonContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

/**
 * Skeleton loader for better perceived performance
 */
export const SkeletonLoader = memo<SkeletonLoaderProps>(({
  width,
  height,
  borderRadius,
  count = 1,
  className
}) => {
  return (
    <SkeletonContainer className={className}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonBox
          key={index}
          $width={width}
          $height={height}
          $borderRadius={borderRadius}
        />
      ))}
    </SkeletonContainer>
  );
});

SkeletonLoader.displayName = 'SkeletonLoader';

// Preset skeleton components
export const SkeletonCard = styled(SkeletonBox)`
  height: 200px;
  border-radius: ${theme.borderRadius.xl};
`;

export const SkeletonText = styled(SkeletonBox)`
  height: 16px;
`;

export const SkeletonTitle = styled(SkeletonBox)`
  height: 32px;
  width: 60%;
`;

export const SkeletonAvatar = styled(SkeletonBox)`
  width: 48px;
  height: 48px;
  border-radius: ${theme.borderRadius.full};
`;
