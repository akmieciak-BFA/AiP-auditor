import styled from 'styled-components';
import { theme } from '../styles/theme';

const DashboardContainer = styled.div`
  flex: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: ${theme.spacing['2xl']} ${theme.spacing.xl};
  width: 100%;

  @media (max-width: ${theme.breakpoints.md}) {
    padding: ${theme.spacing.xl} ${theme.spacing.md};
  }
`;

const PageTitle = styled.h2`
  font-size: ${theme.typography.fontSize['4xl']};
  font-weight: ${theme.typography.fontWeight.bold};
  color: ${theme.colors.primary.brandDark};
  margin-bottom: ${theme.spacing.sm};
  animation: fadeIn 0.5s ease-in-out;

  @media (max-width: ${theme.breakpoints.sm}) {
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

const StatCard = styled.div<{ $color?: string }>`
  background: white;
  border-radius: ${theme.borderRadius.xl};
  padding: ${theme.spacing.xl};
  box-shadow: ${theme.shadows.md};
  transition: ${theme.transitions.base};
  animation: fadeIn 0.5s ease-in-out;
  border-left: 4px solid ${props => props.$color || theme.colors.primary.teal};

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

const StatChange = styled.div<{ $positive?: boolean }>`
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

  @media (max-width: ${theme.breakpoints.lg}) {
    grid-template-columns: 1fr;
  }
`;

const Card = styled.div`
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
  
  &:hover {
    color: ${theme.colors.primary.tealDark};
    text-decoration: underline;
  }
`;

const AuditItem = styled.div`
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
`;

const AuditTitle = styled.div`
  font-weight: ${theme.typography.fontWeight.semibold};
  color: ${theme.colors.neutral.gray900};
  margin-bottom: ${theme.spacing.xs};
`;

const AuditMeta = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  font-size: ${theme.typography.fontSize.sm};
  color: ${theme.colors.neutral.gray600};
`;

const StatusBadge = styled.span<{ $status: 'completed' | 'pending' | 'in-progress' }>`
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
      default:
        return theme.colors.neutral.gray400;
    }
  }};
  color: white;
`;

const ActivityItem = styled.div`
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
`;

const ActivityTime = styled.div`
  font-size: ${theme.typography.fontSize.xs};
  color: ${theme.colors.neutral.gray500};
`;

export const Dashboard: React.FC = () => {
  return (
    <DashboardContainer>
      <PageTitle>Dashboard</PageTitle>
      <PageSubtitle>
        Przegląd wszystkich audytów AiP i kluczowych metryk
      </PageSubtitle>

      <StatsGrid>
        <StatCard $color={theme.colors.primary.teal}>
          <StatLabel>Wszystkie Audyty</StatLabel>
          <StatValue>127</StatValue>
          <StatChange $positive={true}>
            ↑ 12% vs. ostatni miesiąc
          </StatChange>
        </StatCard>

        <StatCard $color={theme.colors.semantic.success}>
          <StatLabel>Ukończone</StatLabel>
          <StatValue>98</StatValue>
          <StatChange $positive={true}>
            ↑ 8% vs. ostatni miesiąc
          </StatChange>
        </StatCard>

        <StatCard $color={theme.colors.semantic.warning}>
          <StatLabel>W Trakcie</StatLabel>
          <StatValue>23</StatValue>
          <StatChange $positive={false}>
            ↓ 3% vs. ostatni miesiąc
          </StatChange>
        </StatCard>

        <StatCard $color={theme.colors.primary.orange}>
          <StatLabel>Oczekujące</StatLabel>
          <StatValue>6</StatValue>
          <StatChange $positive={true}>
            ↑ 2% vs. ostatni miesiąc
          </StatChange>
        </StatCard>
      </StatsGrid>

      <ContentGrid>
        <Card>
          <CardHeader>
            <CardTitle>Ostatnie Audyty</CardTitle>
            <CardAction>Zobacz wszystkie →</CardAction>
          </CardHeader>

          <AuditItem>
            <AuditTitle>Audyt bezpieczeństwa systemu bankowego</AuditTitle>
            <AuditMeta>
              <StatusBadge $status="completed">Ukończony</StatusBadge>
              <span>•</span>
              <span>2025-10-24</span>
            </AuditMeta>
          </AuditItem>

          <AuditItem>
            <AuditTitle>Przegląd zgodności RODO</AuditTitle>
            <AuditMeta>
              <StatusBadge $status="in-progress">W trakcie</StatusBadge>
              <span>•</span>
              <span>2025-10-22</span>
            </AuditMeta>
          </AuditItem>

          <AuditItem>
            <AuditTitle>Audyt infrastruktury IT</AuditTitle>
            <AuditMeta>
              <StatusBadge $status="in-progress">W trakcie</StatusBadge>
              <span>•</span>
              <span>2025-10-20</span>
            </AuditMeta>
          </AuditItem>

          <AuditItem>
            <AuditTitle>Analiza ryzyka operacyjnego</AuditTitle>
            <AuditMeta>
              <StatusBadge $status="pending">Oczekujący</StatusBadge>
              <span>•</span>
              <span>2025-10-18</span>
            </AuditMeta>
          </AuditItem>

          <AuditItem>
            <AuditTitle>Kontrola wewnętrzna procesów</AuditTitle>
            <AuditMeta>
              <StatusBadge $status="completed">Ukończony</StatusBadge>
              <span>•</span>
              <span>2025-10-15</span>
            </AuditMeta>
          </AuditItem>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Ostatnia Aktywność</CardTitle>
          </CardHeader>

          <ActivityItem>
            <ActivityText>
              <strong>Jan Kowalski</strong> ukończył audyt bezpieczeństwa
            </ActivityText>
            <ActivityTime>2 godziny temu</ActivityTime>
          </ActivityItem>

          <ActivityItem>
            <ActivityText>
              <strong>Anna Nowak</strong> dodała nowy raport
            </ActivityText>
            <ActivityTime>5 godzin temu</ActivityTime>
          </ActivityItem>

          <ActivityItem>
            <ActivityText>
              <strong>Piotr Wiśniewski</strong> rozpoczął nowy audyt
            </ActivityText>
            <ActivityTime>1 dzień temu</ActivityTime>
          </ActivityItem>

          <ActivityItem>
            <ActivityText>
              <strong>Maria Lewandowska</strong> zaktualizowała ustawienia
            </ActivityText>
            <ActivityTime>2 dni temu</ActivityTime>
          </ActivityItem>

          <ActivityItem>
            <ActivityText>
              <strong>System</strong> wygenerował automatyczny raport miesięczny
            </ActivityText>
            <ActivityTime>3 dni temu</ActivityTime>
          </ActivityItem>
        </Card>
      </ContentGrid>
    </DashboardContainer>
  );
};
