import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

test('shows the first quiz question after the splash and Get Started', async () => {
  const user = userEvent.setup();
  render(<App />);

  // A 1s splash renders before the welcome screen.
  const start = await waitFor(() => screen.getByRole('button', { name: /get started/i }), {
    timeout: 3000,
  });

  await user.click(start);
  expect(screen.getByText(/What is your budget\?/i)).toBeInTheDocument();
});
