import { useState, useEffect, memo } from 'react';
import styled from 'styled-components';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
}

const ImageWrapper = styled.div`
  position: relative;
  display: inline-block;
  
  img {
    display: block;
    width: 100%;
    height: auto;
  }
`;

const Placeholder = styled.div<{ $height?: number }>`
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
  height: ${props => props.$height || 50}px;
  
  @keyframes shimmer {
    0% {
      background-position: 200% 0;
    }
    100% {
      background-position: -200% 0;
    }
  }
`;

/**
 * Optimized image component with:
 * - WebP support with fallback
 * - Lazy loading
 * - Skeleton placeholder
 * - Performance optimizations
 */
export const OptimizedImage = memo<OptimizedImageProps>(({
  src,
  alt,
  width,
  height,
  className,
  priority = false
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    // Try to load WebP version first
    const webpSrc = src.replace(/\.(png|jpg|jpeg)$/i, '.webp');
    const img = new Image();
    
    img.onload = () => {
      setImageSrc(webpSrc);
      setIsLoaded(true);
    };
    
    img.onerror = () => {
      // Fallback to original format
      setImageSrc(src);
      setIsLoaded(true);
    };
    
    img.src = webpSrc;
  }, [src]);

  if (!isLoaded) {
    return <Placeholder $height={height} />;
  }

  return (
    <ImageWrapper className={className}>
      <img
        src={imageSrc}
        alt={alt}
        width={width}
        height={height}
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
      />
    </ImageWrapper>
  );
});

OptimizedImage.displayName = 'OptimizedImage';
