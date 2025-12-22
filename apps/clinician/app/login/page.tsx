'use client';

import { useRouter } from 'next/navigation';
import { Card, Button, Typography, Space } from 'antd';
const { Title, Text } = Typography;

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = () => {
    // Placeholder login - just redirect to home
    router.push('/');
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh',
      background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)'
    }}>
      <Card 
        style={{ 
          width: 400, 
          textAlign: 'center',
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '16px'
        }}
        variant="borderless"
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ marginBottom: '20px' }}>
            <Title level={2} style={{ color: '#fff', margin: 0 }}>Starvit</Title>
            <Text style={{ color: 'rgba(255, 255, 255, 0.6)' }}>Clinician Dashboard</Text>
          </div>
          
          <Button 
            type="primary" 
            size="large" 
            block 
            onClick={handleLogin}
            style={{ 
              height: '48px',
              borderRadius: '8px',
              background: 'linear-gradient(90deg, #d4af37 0%, #f1c40f 100%)',
              border: 'none',
              fontWeight: 'bold'
            }}
          >
            Sign in with GCP
          </Button>

          <Text style={{ color: 'rgba(255, 255, 255, 0.4)', fontSize: '12px' }}>
            Clinician approval required for all actions. PHI boundary enforced.
          </Text>
        </Space>
      </Card>
    </div>
  );
}
