import { memo } from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';
import { AuditStatus } from '../../types';
import { STATUS_LABELS } from '../../constants';

interface StatusBadgeProps {
  status: AuditStatus;
}

const Badge = styled.span<{ $status: AuditStatus }>`
  display: inline-block;
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.full};
  font-size: ${theme.typography.fontSize.xs};
  font-weight: ${theme.typography.fontWeight.semibold};
  text-transform: uppercase;
  background: ${props => {
    switch (props.$status) {
      case 'completed':
        return theme.colors.semantic.success;
      case 'in-progress':
        return theme.colors.semantic.warning;
      case 'pending':
        return theme.colors.neutral.gray400;
    }
  }};
  color: white;
  white-space: nowrap;
`;

export const StatusBadge = memo<StatusBadgeProps>(({ status }) => {
  return (
    <Badge $status={status} role="status" aria-label={`Status: ${STATUS_LABELS[status]}`}>
      {STATUS_LABELS[status]}
    </Badge>
  );
});

StatusBadge.displayName = 'StatusBadge';
