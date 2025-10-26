import { Component, ReactNode } from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: ${theme.spacing['2xl']};
  text-align: center;
`;

const ErrorTitle = styled.h2`
  font-size: ${theme.typography.fontSize['3xl']};
  color: ${theme.colors.semantic.error};
  margin-bottom: ${theme.spacing.md};
`;

const ErrorMessage = styled.p`
  font-size: ${theme.typography.fontSize.lg};
  color: ${theme.colors.neutral.gray700};
  margin-bottom: ${theme.spacing.xl};
  max-width: 600px;
`;

const ErrorButton = styled.button`
  background: ${theme.colors.gradients.primary};
  color: white;
  border: none;
  padding: ${theme.spacing.md} ${theme.spacing.xl};
  border-radius: ${theme.borderRadius.lg};
  font-weight: ${theme.typography.fontWeight.semibold};
  font-size: ${theme.typography.fontSize.base};
  cursor: pointer;
  transition: ${theme.transitions.base};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${theme.shadows.lg};
  }
`;

const ErrorDetails = styled.details`
  margin-top: ${theme.spacing.xl};
  padding: ${theme.spacing.md};
  background: ${theme.colors.neutral.gray50};
  border-radius: ${theme.borderRadius.md};
  max-width: 600px;
  text-align: left;

  summary {
    cursor: pointer;
    font-weight: ${theme.typography.fontWeight.semibold};
    color: ${theme.colors.neutral.gray700};
  }

  pre {
    margin-top: ${theme.spacing.md};
    padding: ${theme.spacing.md};
    background: white;
    border-radius: ${theme.borderRadius.sm};
    overflow-x: auto;
    font-size: ${theme.typography.fontSize.sm};
    color: ${theme.colors.semantic.error};
  }
`;

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = (): void => {
    this.setState({ hasError: false, error: undefined });
    window.location.reload();
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <ErrorContainer role="alert">
          <ErrorTitle>Coś poszło nie tak</ErrorTitle>
          <ErrorMessage>
            Przepraszamy, wystąpił nieoczekiwany błąd. Spróbuj odświeżyć stronę.
          </ErrorMessage>
          <ErrorButton onClick={this.handleReset}>
            Odśwież stronę
          </ErrorButton>
          {import.meta.env.DEV && this.state.error && (
            <ErrorDetails>
              <summary>Szczegóły błędu (tylko development)</summary>
              <pre>{this.state.error.toString()}</pre>
            </ErrorDetails>
          )}
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}
