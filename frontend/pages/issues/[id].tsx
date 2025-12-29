import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import { issuesAPI } from '@/utils/api';
import { isAuthenticated, isAdmin } from '@/utils/auth';
import toast from 'react-hot-toast';
import dynamic from 'next/dynamic';

const MapView = dynamic(() => import('@/components/MapView'), { ssr: false });

interface Issue {
  id: number;
  title: string;
  description: string;
  category: string;
  status: string;
  latitude: number;
  longitude: number;
  image_url?: string;
  created_at: string;
  updated_at?: string;
  reporter_id: number;
}

export default function IssueDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [issue, setIssue] = useState<Issue | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchIssue();
    }
  }, [id]);

  const fetchIssue = async () => {
    try {
      const response = await issuesAPI.getById(Number(id));
      setIssue(response.data);
    } catch (error: any) {
      toast.error('Failed to load issue');
      router.push('/issues');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      case 'closed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">Loading...</div>
        </div>
      </Layout>
    );
  }

  if (!issue) {
    return null;
  }

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <button
          onClick={() => router.back()}
          className="mb-4 text-primary-600 hover:text-primary-700"
        >
          ← Back to Issues
        </button>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          {issue.image_url && (
            <img
              src={issue.image_url}
              alt={issue.title}
              className="w-full h-96 object-cover"
            />
          )}

          <div className="p-8">
            <div className="flex justify-between items-start mb-4">
              <h1 className="text-3xl font-bold">{issue.title}</h1>
              <span className={`px-4 py-2 text-sm font-semibold rounded-full ${getStatusBadgeColor(issue.status)}`}>
                {issue.status.replace('_', ' ')}
              </span>
            </div>

            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div>
                <h2 className="text-xl font-semibold mb-4">Details</h2>
                <div className="space-y-3">
                  <div>
                    <span className="text-gray-600">Category: </span>
                    <span className="font-semibold capitalize">{issue.category}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Created: </span>
                    <span>{new Date(issue.created_at).toLocaleString()}</span>
                  </div>
                  {issue.updated_at && (
                    <div>
                      <span className="text-gray-600">Updated: </span>
                      <span>{new Date(issue.updated_at).toLocaleString()}</span>
                    </div>
                  )}
                </div>
              </div>

              <div>
                <h2 className="text-xl font-semibold mb-4">Location</h2>
                <div className="h-64 rounded-lg overflow-hidden border border-gray-300">
                  <MapView
                    center={[issue.latitude, issue.longitude]}
                    zoom={15}
                    markers={[{ lat: issue.latitude, lng: issue.longitude, title: issue.title }]}
                  />
                </div>
              </div>
            </div>

            <div className="mb-8">
              <h2 className="text-xl font-semibold mb-4">Description</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{issue.description}</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

