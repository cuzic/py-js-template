import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  it('renders with initial count of 0', () => {
    render(<App />);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('increments count when + button is clicked', () => {
    render(<App />);
    const incrementButton = screen.getByText('+1');
    fireEvent.click(incrementButton);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('decrements count when - button is clicked', () => {
    render(<App />);
    const decrementButton = screen.getByText('-1');
    fireEvent.click(decrementButton);
    expect(screen.getByText('Count: -1')).toBeInTheDocument();
  });

  it('resets count when Reset button is clicked', () => {
    render(<App />);
    const incrementButton = screen.getByText('+1');
    const resetButton = screen.getByText('Reset');
    
    fireEvent.click(incrementButton);
    fireEvent.click(incrementButton);
    expect(screen.getByText('Count: 2')).toBeInTheDocument();
    
    fireEvent.click(resetButton);
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});