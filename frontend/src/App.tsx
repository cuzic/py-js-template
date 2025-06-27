import React, { useState } from 'react';

interface CalculatorProps {
  initialValue?: number;
}

function Calculator({ initialValue = 0 }: CalculatorProps): React.JSX.Element {
  const [count, setCount] = useState(initialValue);

  const increment = (): void => {
    setCount((prev) => prev + 1);
  };

  const decrement = (): void => {
    setCount((prev) => prev - 1);
  };

  const reset = (): void => {
    setCount(initialValue);
  };

  return (
    <div style={{ textAlign: 'center', padding: '2rem' }}>
      <h1>React + TypeScript Counter</h1>
      <div
        style={{
          fontSize: '2rem',
          margin: '2rem 0',
          fontWeight: 'bold',
        }}
      >
        Count: {count}
      </div>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
        <button onClick={decrement}>-1</button>
        <button onClick={reset}>Reset</button>
        <button onClick={increment}>+1</button>
      </div>
    </div>
  );
}

export default function App(): React.JSX.Element {
  return <Calculator initialValue={0} />;
}
