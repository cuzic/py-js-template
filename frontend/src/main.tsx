import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App';

const rootElement = document.querySelector('#root');
if (rootElement === null) throw new Error('Failed to find the root element');

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
