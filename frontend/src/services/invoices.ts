const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8084';

export interface Invoice {
  id: string;
  invoice_number: string;
  date: string;
  package: string;
  package_tier: string;
  amount: number;
  currency: string;
  status: string;
}

export interface InvoicesResponse {
  invoices: Invoice[];
}

/**
 * Get all invoices for the current user
 */
export async function getUserInvoices(): Promise<InvoicesResponse> {
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${API_BASE_URL}/api/user/invoices`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch invoices');
  }

  return response.json();
}
