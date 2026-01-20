/**
 * API service for package management
 */

import { PackageInfo, PackageTier } from '@/lib/packages';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8084';

export interface UpgradePackageRequest {
  package_tier: PackageTier;
}

export interface ClaimPackageResponse {
  message: string;
  package_tier: string;
  package_name: string;
  purchased_at: string;
  is_free_trial: boolean;
}

/**
 * Get current user's package information
 */
export async function getPackageInfo(): Promise<PackageInfo> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/api/user/package-info`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to fetch package info' }));
    throw new Error(error.detail || 'Failed to fetch package info');
  }

  return response.json();
}

/**
 * Claim a package for free (testing - DECISION_CLARITY is free)
 */
export async function claimPackage(packageTier: PackageTier): Promise<ClaimPackageResponse> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/api/user/claim-package`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ package_tier: packageTier }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to claim package' }));
    throw new Error(error.detail || 'Failed to claim package');
  }

  return response.json();
}

/**
 * Upgrade user's package tier
 */
export async function upgradePackage(packageTier: PackageTier): Promise<void> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/api/user/upgrade-package`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ package_tier: packageTier }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to upgrade package' }));
    throw new Error(error.detail || 'Failed to upgrade package');
  }
}

/**
 * Download PDF summary of recommendations
 */
export async function downloadRecommendationsPDF(): Promise<Blob> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/api/download/recommendations-pdf`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to download PDF' }));
    throw new Error(error.detail || 'Failed to download PDF');
  }

  return response.blob();
}

/**
 * Trigger PDF download in browser
 */
export async function triggerPDFDownload(): Promise<void> {
  try {
    const blob = await downloadRecommendationsPDF();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `unipath-recommendations-${new Date().toISOString().split('T')[0]}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    throw error;
  }
}
