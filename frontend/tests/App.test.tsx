import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../src/App';

describe('App', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
  });

  it('renders with initial count of 0', () => {
    render(<App />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments count when + button is clicked', async () => {
    render(<App />);
    const incrementButton = screen.getByText('+1');
    await user.click(incrementButton);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('decrements count when - button is clicked', async () => {
    render(<App />);
    const decrementButton = screen.getByText('-1');
    await user.click(decrementButton);
    expect(screen.getByText('Count: -1')).toBeInTheDocument();
  });

  it('resets count when Reset button is clicked', async () => {
    render(<App />);
    const incrementButton = screen.getByText('+1');
    const resetButton = screen.getByText('Reset');
    
    await user.click(incrementButton);
    await user.click(incrementButton);
    expect(screen.getByText('Count: 2')).toBeInTheDocument();
    
    await user.click(resetButton);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});