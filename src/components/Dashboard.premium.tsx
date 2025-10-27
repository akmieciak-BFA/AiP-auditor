import { memo } from 'react';
import styled from 'styled-components';
import { theme } from '../styles/theme';
import { media, containerStyles } from '../utils/mediaQueries';
import { MOCK_STATS, MOCK_AUDITS, MOCK_ACTIVITIES } from '../constants';
import { StatusBadge } from './common/StatusBadge';
import { getColorFromKey, formatPercentageChange } from '../utils/helpers';
import type { Audit, Activity } from '../types';

const DashboardContainer = styled.div`
  flex: 1;
  ${containerStyles}
  padding-top: ${theme.spacing['2xl']};
  padding-bottom: ${theme.spacing['2xl']};
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(43, 122, 120, 0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  & > * {
    position: relative;
    z-index: 1;
  }
`;

const PageHeader = styled.div`
  margin-bottom: ${theme.spacing['2xl']};
`;

const PageTitle = styled.h2`
  font-size: ${theme.typography.fontSize['4xl']};
  font-weight: ${theme.typography.fontWeight.extrabold};
  background: linear-gradient(135deg, ${theme.colors.primary.brandDark} 0%, ${theme.colors.primary.teal} 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: ${theme.spacing.sm};
  animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;

  @keyframes fadeInScale {
    from {
      opacity: 0;
      transform: translateY(20px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  ${media.sm} {
    font-size: ${theme.typography.fontSize['3xl']};
  }
`;

const PageSubtitle = styled.p`
  font-size: ${theme.typography.fontSize.lg};
  color: ${theme.colors.neutral.gray600};
  margin-bottom: ${theme.spacing.md};
  animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: ${theme.spacing.xl};
  margin-bottom: ${theme.spacing['2xl']};
`;

const StatCard = styled.article<{ $color: string; $delay: number }>`
  background: white;
  border-radius: ${theme.borderRadius['2xl']};
  padding: ${theme.spacing['xl']};
  position: relative;
  overflow: hidden;
  transition: all ${theme.transitions.base};
  animation: slideUpFade 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${props => props.$delay}s backwards;
  will-change: transform;
  transform: translateZ(0);
  
  @keyframes slideUpFade {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: ${props => props.$color};
    transform: scaleY(0);
    transform-origin: top;
    transition: transform ${theme.transitions.base};
  }

  &::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, ${props => props.$color}15 0%, transparent 70%);
    opacity: 0;
    transition: opacity ${theme.transitions.base};
  }

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);

    &::before {
      transform: scaleY(1);
    }

    &::after {
      opacity: 1;
    }
  }
`;

const StatIcon = styled.div<{ $color: string }>`
  width: 48px;
  height: 48px;
  border-radius: ${theme.borderRadius.xl};
  background: ${props => props.$color}15;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: ${theme.spacing.md};
  font-size: 24px;
  transition: all ${theme.transitions.base};
  
  ${StatCard}:hover & {
    transform: scale(1.1) rotate(5deg);
  }
`;

const StatLabel = styled.div`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: ${theme.typography.fontWeight.semibold};
  margin-bottom: ${theme.spacing.sm};
`;

const StatValue = styled.div`
  font-size: ${theme.typography.fontSize['4xl']};
  font-weight: ${theme.typography.fontWeight.extrabold};
  color: ${theme.colors.neutral.gray900};
  margin-bottom: ${theme.spacing.xs};
  line-height: 1;
`;

const StatChange = styled.div<{ $positive: boolean }>`
  font-size: ${theme.typography.fontSize.sm};
  color: ${props => props.$positive ? theme.colors.semantic.success : theme.colors.semantic.error};
  font-weight: ${theme.typography.fontWeight.semibold};
  display: flex;
  align-items: center;
  gap: ${theme.spacing.xs};
  
  &::before {
    content: '';
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: ${props => props.$positive ? `6px solid ${theme.colors.semantic.success}` : 'none'};
    border-top: ${props => props.$positive ? 'none' : `6px solid ${theme.colors.semantic.error}`};
  }
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: ${theme.spacing.xl};
  margin-bottom: ${theme.spacing['2xl']};

  ${media.lg} {
    grid-template-columns: 1fr;
  }
`;

const Card = styled.section`
  background: white;
  border-radius: ${theme.borderRadius['2xl']};
  padding: ${theme.spacing.xl};
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  animation: slideUpFade 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.3s backwards;
  transition: all ${theme.transitions.base};
  
  &:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  }
`;

const CardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${theme.spacing.lg};
  padding-bottom: ${theme.spacing.md};
  border-bottom: 2px solid ${theme.colors.neutral.gray100};
`;

const CardTitle = styled.h3`
  font-size: ${theme.typography.fontSize['2xl']};
  font-weight: ${theme.typography.fontWeight.bold};
  color: ${theme.colors.primary.brandDark};
  display: flex;
  align-items: center;
  gap: ${theme.spacing.sm};

  &::before {
    content: '';
    width: 4px;
    height: 24px;
    background: ${theme.colors.gradients.primary};
    border-radius: ${theme.borderRadius.full};
  }
`;

const CardAction = styled.button`
  background: ${theme.colors.gradients.primary};
  color: white;
  border: none;
  padding: ${theme.spacing.sm} ${theme.spacing.lg};
  border-radius: ${theme.borderRadius.lg};
  font-weight: ${theme.typography.fontWeight.semibold};
  cursor: pointer;
  font-size: ${theme.typography.fontSize.sm};
  transition: all ${theme.transitions.fast};
  box-shadow: 0 4px 12px rgba(43, 122, 120, 0.3);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(43, 122, 120, 0.4);
  }

  &:active {
    transform: translateY(0);
  }

  &:focus-visible {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

const AuditItem = styled.article`
  padding: ${theme.spacing.lg};
  border-radius: ${theme.borderRadius.xl};
  margin-bottom: ${theme.spacing.md};
  background: ${theme.colors.neutral.gray50};
  transition: all ${theme.transitions.base};
  cursor: pointer;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background: ${theme.colors.gradients.primary};
    transform: scaleX(0);
    transition: transform ${theme.transitions.base};
  }

  &:hover {
    background: white;
    transform: translateX(8px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);

    &::before {
      transform: scaleX(1);
    }
  }

  &:last-child {
    margin-bottom: 0;
  }

  &:focus-within {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

const AuditTitle = styled.h4`
  font-weight: ${theme.typography.fontWeight.semibold};
  color: ${theme.colors.neutral.gray900};
  margin-bottom: ${theme.spacing.sm};
  font-size: ${theme.typography.fontSize.base};
`;

const AuditMeta = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
  align-items: center;
`;

const ActivityItem = styled.article`
  padding: ${theme.spacing.md} 0;
  border-bottom: 1px solid ${theme.colors.neutral.gray100};
  transition: all ${theme.transitions.fast};

  &:hover {
    padding-left: ${theme.spacing.sm};
  }

  &:last-child {
    border-bottom: none;
  }
`;

const ActivityText = styled.div`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray700};
  margin-bottom: ${theme.spacing.xs};

  strong {
    font-weight: ${theme.typography.fontWeight.bold};
    color: ${theme.colors.primary.brandDark};
  }
`;

const ActivityTime = styled.time`
  font-size: ${theme.typography.fontSize.xs};
  color: ${theme.colors.neutral.gray500};
`;

// Memoized sub-components
const AuditListItem = memo<{ audit: Audit }>(({ audit }) => (
  <AuditItem tabIndex={0} role="button" aria-label={`Otwórz audyt: ${audit.title}`}>
    <AuditTitle>{audit.title}</AuditTitle>
    <AuditMeta>
      <StatusBadge status={audit.status} />
      <span aria-hidden="true">•</span>
      <time dateTime={audit.date}>{audit.date}</time>
    </AuditMeta>
  </AuditItem>
));
AuditListItem.displayName = 'AuditListItem';

const ActivityListItem = memo<{ activity: Activity }>(({ activity }) => (
  <ActivityItem>
    <ActivityText>
      <strong>{activity.user}</strong> {activity.action}
    </ActivityText>
    <ActivityTime>{activity.time}</ActivityTime>
  </ActivityItem>
));
ActivityListItem.displayName = 'ActivityListItem';

const getStatIcon = (id: string) => {
  switch (id) {
    case 'total': return '📊';
    case 'completed': return '✅';
    case 'in-progress': return '⚡';
    case 'pending': return '⏳';
    default: return '📈';
  }
};

export const DashboardPremium = memo(() => {
  return (
    <DashboardContainer role="main">
      <PageHeader>
        <PageTitle>Dashboard</PageTitle>
        <PageSubtitle>
          Przegląd wszystkich audytów AiP i kluczowych metryk
        </PageSubtitle>
      </PageHeader>

      <StatsGrid role="region" aria-label="Statystyki audytów">
        {MOCK_STATS.map((stat, index) => (
          <StatCard 
            key={stat.id} 
            $color={getColorFromKey(stat.color, theme)}
            $delay={index * 0.1}
            aria-label={`${stat.label}: ${stat.value}`}
          >
            <StatIcon $color={getColorFromKey(stat.color, theme)}>
              {getStatIcon(stat.id)}
            </StatIcon>
            <StatLabel>{stat.label}</StatLabel>
            <StatValue>{stat.value}</StatValue>
            <StatChange $positive={stat.positive} aria-label={formatPercentageChange(stat.change)}>
              {formatPercentageChange(stat.change).substring(2)}
            </StatChange>
          </StatCard>
        ))}
      </StatsGrid>

      <ContentGrid>
        <Card aria-labelledby="recent-audits-title">
          <CardHeader>
            <CardTitle id="recent-audits-title">Ostatnie Audyty</CardTitle>
            <CardAction aria-label="Zobacz wszystkie audyty">
              Zobacz wszystkie →
            </CardAction>
          </CardHeader>

          <div role="list">
            {MOCK_AUDITS.map((audit) => (
              <AuditListItem key={audit.id} audit={audit} />
            ))}
          </div>
        </Card>

        <Card aria-labelledby="recent-activity-title">
          <CardHeader>
            <CardTitle id="recent-activity-title">Ostatnia Aktywność</CardTitle>
          </CardHeader>

          <div role="list">
            {MOCK_ACTIVITIES.map((activity) => (
              <ActivityListItem key={activity.id} activity={activity} />
            ))}
          </div>
        </Card>
      </ContentGrid>
    </DashboardContainer>
  );
});

DashboardPremium.displayName = 'DashboardPremium';
