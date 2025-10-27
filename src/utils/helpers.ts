// Helper functions

/**
 * Format a date string to locale format
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Get color from theme based on color key
 */
export const getColorFromKey = (colorKey: string, theme: any): string => {
  switch (colorKey) {
    case 'teal':
      return theme.colors.primary.teal;
    case 'success':
      return theme.colors.semantic.success;
    case 'warning':
      return theme.colors.semantic.warning;
    case 'orange':
      return theme.colors.primary.orange;
    case 'error':
      return theme.colors.semantic.error;
    default:
      return theme.colors.primary.teal;
  }
};

/**
 * Debounce function for performance
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: ReturnType<typeof setTimeout> | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * Check if element is in viewport
 */
export const isInViewport = (element: HTMLElement): boolean => {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
};

/**
 * Format number with locale
 */
export const formatNumber = (num: number): string => {
  return num.toLocaleString('pl-PL');
};

/**
 * Calculate percentage change
 */
export const formatPercentageChange = (change: number): string => {
  const prefix = change > 0 ? '↑' : '↓';
  const absChange = Math.abs(change);
  return `${prefix} ${absChange}% vs. ostatni miesiąc`;
};
