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
`;

const PageTitle = styled.h2`
  font-size: ${theme.typography.fontSize['4xl']};
  font-weight: ${theme.typography.fontWeight.bold};
  color: ${theme.colors.primary.brandDark};
  margin-bottom: ${theme.spacing.sm};
  animation: fadeIn 0.5s ease-in-out;

  ${media.sm} {
    font-size: ${theme.typography.fontSize['3xl']};
  }
`;

const PageSubtitle = styled.p`
  font-size: ${theme.typography.fontSize.lg};
  color: ${theme.colors.neutral.gray600};
  margin-bottom: ${theme.spacing['2xl']};
  animation: fadeIn 0.5s ease-in-out 0.1s backwards;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${theme.spacing.xl};
  margin-bottom: ${theme.spacing['2xl']};
`;

const StatCard = styled.article<{ $color: string }>`
  background: white;
  border-radius: ${theme.borderRadius.xl};
  padding: ${theme.spacing.xl};
  box-shadow: ${theme.shadows.md};
  transition: ${theme.transitions.base};
  animation: fadeIn 0.5s ease-in-out;
  border-left: 4px solid ${props => props.$color};

  &:hover {
    transform: translateY(-4px);
    box-shadow: ${theme.shadows.xl};
  }
`;

const StatLabel = styled.div`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: ${theme.typography.fontWeight.medium};
  margin-bottom: ${theme.spacing.sm};
`;

const StatValue = styled.div`
  font-size: ${theme.typography.fontSize['3xl']};
  font-weight: ${theme.typography.fontWeight.bold};
  color: ${theme.colors.neutral.gray900};
  margin-bottom: ${theme.spacing.xs};
`;

const StatChange = styled.div<{ $positive: boolean }>`
  font-size: ${theme.typography.fontSize.sm};
  color: ${props => props.$positive ? theme.colors.semantic.success : theme.colors.semantic.error};
  font-weight: ${theme.typography.fontWeight.medium};
  display: flex;
  align-items: center;
  gap: ${theme.spacing.xs};
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
  border-radius: ${theme.borderRadius.xl};
  padding: ${theme.spacing.xl};
  box-shadow: ${theme.shadows.md};
  animation: fadeIn 0.5s ease-in-out;
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
  font-size: ${theme.typography.fontSize.xl};
  font-weight: ${theme.typography.fontWeight.semibold};
  color: ${theme.colors.primary.brandDark};
`;

const CardAction = styled.button`
  background: none;
  border: none;
  color: ${theme.colors.primary.teal};
  font-weight: ${theme.typography.fontWeight.medium};
  cursor: pointer;
  font-size: ${theme.typography.fontSize.sm};
  transition: ${theme.transitions.fast};
  
  &:hover {
    color: ${theme.colors.primary.tealDark};
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid ${theme.colors.primary.teal};
    outline-offset: 2px;
  }
`;

const AuditItem = styled.article`
  padding: ${theme.spacing.md};
  border-radius: ${theme.borderRadius.lg};
  margin-bottom: ${theme.spacing.md};
  background: ${theme.colors.neutral.gray50};
  transition: ${theme.transitions.base};
  cursor: pointer;

  &:hover {
    background: ${theme.colors.neutral.gray100};
    transform: translateX(4px);
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
  margin-bottom: ${theme.spacing.xs};
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

  &:last-child {
    border-bottom: none;
  }
`;

const ActivityText = styled.div`
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray700};
  margin-bottom: ${theme.spacing.xs};

  strong {
    font-weight: ${theme.typography.fontWeight.semibold};
    color: ${theme.colors.neutral.gray900};
  }
`;

const ActivityTime = styled.time`
  font-size: ${theme.typography.fontSize.xs};
  color: ${theme.colors.neutral.gray500};
`;

// Memoized sub-components for better performance
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

export const Dashboard = memo(() => {
  return (
    <DashboardContainer role="main">
      <PageTitle>Dashboard</PageTitle>
      <PageSubtitle>
        Przegląd wszystkich audytów AiP i kluczowych metryk
      </PageSubtitle>

      <StatsGrid role="region" aria-label="Statystyki audytów">
        {MOCK_STATS.map((stat) => (
          <StatCard 
            key={stat.id} 
            $color={getColorFromKey(stat.color, theme)}
            aria-label={`${stat.label}: ${stat.value}`}
          >
            <StatLabel>{stat.label}</StatLabel>
            <StatValue>{stat.value}</StatValue>
            <StatChange $positive={stat.positive} aria-label={formatPercentageChange(stat.change)}>
              {formatPercentageChange(stat.change)}
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

Dashboard.displayName = 'Dashboard';
