import { LogIn, Sparkles, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

export const LoginPage = () => {
  const { signInWithLinkedIn } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setLoading(true);
      // call your LinkedIn OAuth login
      await signInWithLinkedIn();
      // don’t set loading false here, because user will be redirected
    } catch (error) {
      console.error('Login error:', error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      {/* subtle animated background grid */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsMjU1LDI1NSwwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-40"></div>

      <div className="relative max-w-md w-full">
        <div className="bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/20">
          <div className="flex justify-center mb-6">
            <div className="bg-gradient-to-br from-blue-500 to-cyan-500 p-4 rounded-2xl shadow-lg">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
          </div>

          <h1 className="text-3xl font-bold text-white text-center mb-2">
            LinkedIn Content Studio
          </h1>

          <p className="text-slate-300 text-center mb-8">
            Automate your LinkedIn content creation and posting with AI-powered workflows
          </p>

          {/* features list */}
          <div className="space-y-4 mb-8">
            <Feature
              color="blue"
              title="Automated Content Generation"
              desc="AI-powered posts and images"
            />
            <Feature
              color="cyan"
              title="Real-time Job Tracking"
              desc="Monitor every step of your workflow"
            />
            <Feature
              color="teal"
              title="LinkedIn Integration"
              desc="Direct publishing to your profile"
            />
          </div>

          {/* main login button */}
          <button
            onClick={handleLogin}
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Connecting...
              </>
            ) : (
              <>
                <LogIn className="w-5 h-5" />
                Sign in with OAuth 2.0
              </>
            )}
          </button>

          <p className="text-slate-400 text-xs text-center mt-6">
            By signing in, you agree to our secure OAuth 2.0 authentication process
          </p>
        </div>
      </div>
    </div>
  );
};

// small reusable feature component
const Feature = ({ color, title, desc }: { color: string; title: string; desc: string }) => (
  <div className="flex items-start gap-3">
    <div className={`bg-${color}-500/20 rounded-full p-1 mt-0.5`}>
      <div className={`w-2 h-2 bg-${color}-400 rounded-full`}></div>
    </div>
    <div>
      <p className="text-white font-medium">{title}</p>
      <p className="text-slate-400 text-sm">{desc}</p>
    </div>
  </div>
);
