import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import { isAuthenticated, getUser } from '@/utils/auth';
import { issuesAPI, notificationsAPI } from '@/utils/api';
import Link from 'next/link';
import toast from 'react-hot-toast';

interface Issue {
  id: number;
  title: string;
  description: string;
  category: string;
  status: string;
  created_at: string;
}

interface Notification {
  id: number;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    resolved: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/auth/login');
      return;
    }

    setUser(getUser());
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [issuesRes, notificationsRes] = await Promise.all([
        issuesAPI.getAll({ limit: 5 }),
        notificationsAPI.getAll({ limit: 5, unread_only: true }),
      ]);

      setIssues(issuesRes.data);
      setNotifications(notificationsRes.data);

      // Calculate stats
      const allIssues = await issuesAPI.getAll({ limit: 100 });
      const total = allIssues.data.length;
      const pending = allIssues.data.filter((i: Issue) => i.status === 'pending').length;
      const resolved = allIssues.data.filter((i: Issue) => i.status === 'resolved' || i.status === 'closed').length;

      setStats({ total, pending, resolved });
    } catch (error: any) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
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

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-gray-600 mb-2">Total Issues</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-gray-600 mb-2">Pending</h3>
            <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-gray-600 mb-2">Resolved</h3>
            <p className="text-3xl font-bold text-green-600">{stats.resolved}</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Recent Issues */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Recent Issues</h2>
              <Link href="/issues" className="text-primary-600 hover:text-primary-700">
                View All
              </Link>
            </div>
            <div className="space-y-4">
              {issues.length === 0 ? (
                <p className="text-gray-500">No issues yet</p>
              ) : (
                issues.map((issue) => (
                  <Link
                    key={issue.id}
                    href={`/issues/${issue.id}`}
                    className="block p-4 border rounded-lg hover:bg-gray-50"
                  >
                    <h3 className="font-semibold">{issue.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{issue.description.substring(0, 100)}...</p>
                    <div className="flex justify-between items-center mt-2">
                      <span className={`px-2 py-1 text-xs rounded ${
                        issue.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        issue.status === 'resolved' ? 'bg-green-100 text-green-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {issue.status}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(issue.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </Link>
                ))
              )}
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Notifications</h2>
              <Link href="/notifications" className="text-primary-600 hover:text-primary-700">
                View All
              </Link>
            </div>
            <div className="space-y-4">
              {notifications.length === 0 ? (
                <p className="text-gray-500">No new notifications</p>
              ) : (
                notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 border rounded-lg ${!notification.is_read ? 'bg-blue-50' : ''}`}
                  >
                    <h3 className="font-semibold">{notification.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                    <span className="text-xs text-gray-500">
                      {new Date(notification.created_at).toLocaleDateString()}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

